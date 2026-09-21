<#
.SYNOPSIS
  Wait for the GitHub Actions deploy of the commit that is checked out, and report the result.

.DESCRIPTION
  Called by deploy.bat right after `git push`. Finds the "Publish site" run for the current HEAD
  (it can take a few seconds to appear), then follows it until it finishes.
  Exit code 0 = deployed, or nothing could be checked (GitHub CLI missing / not signed in / run not found).
  Exit code 1 = the run failed. Needs the GitHub CLI (gh), signed in as the owner of the repository.
#>
$repo = 'minnanosaiban/eneos-hotline'
$actions = "https://github.com/$repo/actions"

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

Write-Host "Following GitHub Actions run $id for commit $($sha.Substring(0, 7))"
gh run watch $id --repo $repo --exit-status --interval 5 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "The run failed."
    exit 1
}
Write-Host "Deployed: https://minnanosaiban.github.io/eneos-hotline/"
exit 0
