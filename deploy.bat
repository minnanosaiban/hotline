@echo off
setlocal

rem バッチファイルがある場所をカレントディレクトリにする（最も確実な方法）
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