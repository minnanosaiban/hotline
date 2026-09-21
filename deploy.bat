@echo off
setlocal

rem ============================================================
rem  eneos-hotline deploy (GitHub Pages, built by GitHub Actions)
rem  Double-click after editing to publish the site.
rem
rem  Steps:
rem    1. Build check with Zensical. Stops here if the build fails.
rem    2. Commit and push to GitHub (master). Skipped when nothing is new;
rem       a failed push is retried up to 3 times.
rem    3. GitHub Actions builds and publishes the site (about 30 seconds).
rem       This script waits for it and reports success or failure.
rem    4. Notify IndexNow (Bing etc.). A failure here is not fatal.
rem
rem  First-time setup (run once in this folder):
rem    python -m venv .venv
rem    .venv\Scripts\pip install -r requirements.txt
rem
rem  Preview only: serve.bat     Build only: build.bat
rem  Site:    https://minnanosaiban.github.io/eneos-hotline/
rem  Actions: https://github.com/minnanosaiban/eneos-hotline/actions
rem ============================================================

set PYTHONUTF8=1

echo === Deploy eneos-hotline to GitHub Pages ===
cd /d "%~dp0"
echo Current: %CD%

echo === Check the environment ===
if not exist ".venv\Scripts\zensical.exe" (
    echo [ERROR] .venv\Scripts\zensical.exe was not found.
    echo         Run once in this folder:
    echo           python -m venv .venv
    echo           .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo === Build check ===
.venv\Scripts\zensical.exe build --clean
if %errorlevel% neq 0 (
    echo [ERROR] Build failed. Nothing was pushed.
    pause
    exit /b 1
)

echo === Commit ^& Push to GitHub, master ===
git add .
git commit -m "Update eneos-hotline" || echo No changes to commit

rem Push only when there is something new: commits that are not on origin/master yet.
set AHEAD=
for /f %%n in ('git rev-list --count origin/master..HEAD 2^>nul') do set AHEAD=%%n
if "%AHEAD%"=="0" (
    echo Nothing new to push.
    goto pushed
)

set TRIES=0
:do_push
set /a TRIES+=1
rem Errors such as Empty reply from server are often network or HTTP/2 hiccups. From the 2nd try, use HTTP/1.1.
if %TRIES% equ 1 git push -u origin master
if %TRIES% gtr 1 git -c http.version=HTTP/1.1 push -u origin master
if %errorlevel% equ 0 goto pushed
if %TRIES% lss 3 (
    echo [WARN] Push failed on try %TRIES% of 3. Trying again in 5 seconds.
    %SystemRoot%\System32	imeout.exe /t 5 /nobreak >nul
    goto do_push
)
echo [ERROR] Git push failed 3 times. Check the network, VPN, proxy and sign-in, then run this again.
echo         Your commit is saved on this PC and will be pushed next time.
pause
exit /b 1

:pushed

echo === Wait for GitHub Actions to publish the site ===
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\wait_deploy.ps1"
if %errorlevel% neq 0 (
    echo [ERROR] The deploy on GitHub Actions failed. Open the log:
    echo         https://github.com/minnanosaiban/eneos-hotline/actions
    pause
    exit /b 1
)

echo === Notify IndexNow ===
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\indexnow_ping.ps1"
if %errorlevel% neq 0 echo IndexNow ping failed - not fatal, continuing.

echo === Done ===
pause
