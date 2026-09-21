@echo off
setlocal

rem ============================================================
rem  eneos-hotline deploy (GitHub Pages, built by GitHub Actions)
rem  Double-click after editing to publish the site.
rem
rem  Steps:
rem    1. Build check with Zensical. Stops here if the build fails.
rem    2. Commit and push to GitHub (master).
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
git push -u origin master
if %errorlevel% neq 0 (
    echo [ERROR] Git push failed. Check the remote and the sign-in.
    pause
    exit /b 1
)

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
