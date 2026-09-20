<#
.SYNOPSIS
  Notify IndexNow (Bing / Yandex / Seznam / Naver ...) of all published URLs.

.DESCRIPTION
  Reads the freshly built sitemap (../site/sitemap.xml) and submits every <loc>
  to the IndexNow API in one bulk request. Run it AFTER `mkdocs gh-deploy`
  (the deploy regenerates site/sitemap.xml and pushes the live site).

  Key file must stay live at:
    https://minnanosaiban.github.io/hotline/<key>.txt
  (committed at docs/<key>.txt). Because the key sits under /hotline/, the
  keyLocation parameter is required and only /hotline/ URLs may be submitted.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\indexnow_ping.ps1
#>

$ErrorActionPreference = 'Stop'

# --- config -------------------------------------------------------------
$key         = 'e482d7edf83b50b925f361e389d57812'
$siteHost    = 'minnanosaiban.github.io'
$keyLocation = "https://$siteHost/hotline/$key.txt"
$endpoint    = 'https://api.indexnow.org/indexnow'   # fans out to all IndexNow engines
$exclude     = @('ai_studio_code', 'draft_scalping_prediction')  # drafts: don't submit
# ------------------------------------------------------------------------

$sitemap = Join-Path $PSScriptRoot '..\site\sitemap.xml'
if (-not (Test-Path $sitemap)) {
    throw "sitemap not found: $sitemap  (run `mkdocs gh-deploy` first so site/ is built)"
}

[xml]$xml = Get-Content -Raw -LiteralPath $sitemap
$urls = @($xml.GetElementsByTagName('loc') | ForEach-Object { $_.InnerText } |
    Where-Object { $u = $_; -not ($exclude | Where-Object { $u -like "*$_*" }) })

if ($urls.Count -eq 0) { throw 'no URLs found in sitemap' }

$body = @{
    host        = $siteHost
    key         = $key
    keyLocation = $keyLocation
    urlList     = $urls
} | ConvertTo-Json

try {
    $resp = Invoke-WebRequest -Uri $endpoint -Method Post `
        -ContentType 'application/json; charset=utf-8' -Body $body -UseBasicParsing
    Write-Host ("IndexNow OK: HTTP {0} {1}  ({2} URLs submitted)" -f `
        [int]$resp.StatusCode, $resp.StatusDescription, $urls.Count) -ForegroundColor Green
}
catch {
    $code = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { '?' }
    Write-Host ("IndexNow FAILED: HTTP {0} - {1}" -f $code, $_.Exception.Message) -ForegroundColor Red
    Write-Host "  200/202 = accepted. 403 = key file unreachable. 422 = URL/host or keyLocation mismatch."
    exit 1
}
