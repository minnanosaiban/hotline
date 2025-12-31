@echo off
setlocal

rem git clone https://github.com/minnanosaiban/hotline.git
rem git remote set-url origin https://github.com/minnanosaiban/hotline.git
rem mkdocs build --clean
rem mkdocs serve
rem mkdocs gh-deploy --force
rem git add .
rem git reset site/
rem git commit -m "Update main branch (excluding site/)"
rem git push -f origin main


cd /d "%~dp0"

echo === Check Current Directory ===
echo Current: %CD%

echo === MkDocs build ===
mkdocs build --clean
if %errorlevel% neq 0 (
    echo Build failed.
    pause
    exit /b
)

echo === MkDocs deploy to gh-pages ===
mkdocs gh-deploy --force
if %errorlevel% neq 0 (
    echo Deploy failed.
    pause
    exit /b
)

echo === Commit ^& Push to main ===
git add .
git commit -m "Update main source" || echo No changes to commit
git push origin main

echo === Done ===
pause