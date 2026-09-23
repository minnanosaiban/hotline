<#
.SYNOPSIS
  Wait for the GitHub Actions deploy of the commit that is checked out, and report the result.

.DESCRIPTION
  Called by deploy.bat right after `git push`. Finds the "Publish site" run for the current HEAD
  (it can take a few seconds to appear), then follows it until it finishes.

  A run normally takes about 30 seconds. GitHub Pages sometimes hangs in the last step
  ("Run actions/deploy-pages"), so a run that has not finished after -TimeoutSec (default 240)
  is treated as stuck: it is cancelled and re-run automatically, -Retries times (default 1).
  The site keeps serving the previous version the whole time.

  Exit code 0 = deployed, or nothing could be checked (GitHub CLI missing / not signed in /
                run not found / the run status could not be read).
  Exit code 1 = the run failed.
  Exit code 2 = the run was still not finished after the automatic re-run(s).
  Needs the GitHub CLI (gh), signed in as the owner of the repository.
#>
param(
    [int]$TimeoutSec = 240,   # give up on one attempt after this many seconds
    [int]$PollSec = 5,        # how often the run status is read
    [int]$Retries = 1         # how many times a stuck run is cancelled and re-run
)

$repo = 'minnanosaiban/hotline'
$actions = "https://github.com/$repo/actions"
$siteUrl = 'https://minnanosaiban.github.io/hotline/'

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "GitHub CLI (gh) was not found, so the deploy was not checked. See: $actions"
    exit 0
}

gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "GitHub CLI (gh) is not signed in (run: gh auth login), so the deploy was not checked. See: $actions"
    exit 0
}

$sha = (git rev-parse HEAD).Trim()
$id = $null
for ($i = 0; $i -lt 30 -and -not $id; $i++) {
    # Filter in PowerShell: Windows PowerShell 5.1 mangles double quotes passed to native commands (so no gh --jq here).
    $runs = gh run list --repo $repo --limit 10 --json databaseId,headSha 2>$null | ConvertFrom-Json
    $id = $runs | Where-Object { $_.headSha -eq $sha } | Select-Object -First 1 -ExpandProperty databaseId
    if (-not $id) { Start-Sleep -Seconds 3 }
}
if (-not $id) {
    Write-Host "No GitHub Actions run was found for $($sha.Substring(0, 7)), so the deploy was not checked. See: $actions"
    exit 0
}

# Read the run once. Returns $null when gh fails (network trouble etc.).
function Get-Run {
    $json = gh run view $id --repo $repo --json status,conclusion,attempt,startedAt,jobs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $json) { return $null }
    try { return ($json | ConvertFrom-Json -ErrorAction Stop) } catch { return $null }
}

# Follow one attempt of the run. Returns 'success', 'failed', 'timeout' or 'unknown'.
#  - Reads that still show an attempt older than $minAttempt (right after a re-run) are ignored.
#  - $fromRunStart: count the time from when GitHub started the run, not from when this script began
#    watching. That way a run that has already been stuck for a long time is dealt with at once.
function Wait-Attempt([int]$minAttempt, [bool]$fromRunStart) {
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $offset = 0.0
    $offsetDone = -not $fromRunStart
    $misses = 0
    $lastLabel = $null
    $lastBeat = 0.0
    while ($true) {
        $r = Get-Run
        if ($null -eq $r) {
            $misses++
            if ($misses -ge 6) { return 'unknown' }    # about 30 seconds of failed reads in a row
        }
        else {
            $misses = 0
            if ([int]$r.attempt -ge $minAttempt) {
                $script:attempt = [int]$r.attempt
                if (-not $offsetDone) {
                    $offsetDone = $true
                    try {
                        $started = ([DateTimeOffset]$r.startedAt).UtcDateTime
                        $offset = [Math]::Max(0.0, ([DateTime]::UtcNow - $started).TotalSeconds)
                    }
                    catch { $offset = 0.0 }
                }
                if ($r.status -eq 'completed') {
                    if ($r.conclusion -eq 'success') { return 'success' }
                    return 'failed'
                }
                $label = [string]$r.status
                foreach ($j in $r.jobs) {
                    foreach ($s in $j.steps) { if ($s.status -eq 'in_progress') { $label = [string]$s.name } }
                }
                $elapsed = $sw.Elapsed.TotalSeconds + $offset
                if ($label -ne $lastLabel -or ($elapsed - $lastBeat) -ge 30) {
                    Write-Host ('  [{0,3}s] {1}' -f [int]$elapsed, $label)
                    $lastLabel = $label
                    $lastBeat = $elapsed
                }
            }
        }
        if (($sw.Elapsed.TotalSeconds + $offset) -ge $TimeoutSec) { return 'timeout' }
        Start-Sleep -Seconds $PollSec
    }
}

# Cancel the stuck run and start it again.
# Returns 'restarted', 'success' (it finished fine just before it was cancelled) or 'failed' (could not restart).
function Restart-Run {
    gh run cancel $id --repo $repo *> $null
    $r = $null
    for ($i = 0; $i -lt 20; $i++) {              # a run cannot be re-run until it has stopped
        $r = Get-Run
        if ($r -and $r.status -eq 'completed') { break }
        Start-Sleep -Seconds $PollSec
    }
    if (-not $r -or $r.status -ne 'completed') { return 'failed' }
    if ($r.conclusion -eq 'success') { return 'success' }
    gh run rerun $id --repo $repo *> $null
    if ($LASTEXITCODE -ne 0) { return 'failed' }
    return 'restarted'
}

Write-Host "Following GitHub Actions run $id for commit $($sha.Substring(0, 7))"
$attempt = 1
$result = Wait-Attempt 1 $true
$restarts = 0
while ($result -eq 'timeout' -and $restarts -lt $Retries) {
    $restarts++
    Write-Host "[WARN] The run has not finished after $TimeoutSec seconds (it normally takes about 30). Cancelling it and running it again ($restarts of $Retries). The site keeps showing the previous version meanwhile."
    $next = $attempt + 1
    $how = Restart-Run
    if ($how -eq 'success') { $result = 'success'; break }
    if ($how -ne 'restarted') { break }           # could not restart: report it as stuck
    Write-Host "Running it again (attempt $next)"
    $result = Wait-Attempt $next $false
}

switch ($result) {
    'success' { Write-Host "Deployed: $siteUrl"; exit 0 }
    'failed'  { Write-Host "The run failed."; exit 1 }
    'unknown' { Write-Host "Could not read the run status (network?), so the deploy was not confirmed. See: $actions"; exit 0 }
    default   { Write-Host "The run was still not finished after $TimeoutSec seconds (automatic re-runs: $restarts of $Retries). GitHub Pages may be having trouble. The previous version stays online. See: $actions"; exit 2 }
}
