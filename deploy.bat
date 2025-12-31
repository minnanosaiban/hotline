@echo off
setlocal

rem --- メモ（初回設定やコマンド確認用） ---
rem pip install -r requirements.txt
rem git clone https://github.com/minnanosaiban/hotline.git
rem git remote set-url origin https://github.com/minnanosaiban/hotline.git
rem mkdocs serve
rem --------------------------------------

echo === Deploy to GitHub Pages ===
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
rem gh-deployは site/ フォルダを自動で gh-pages ブランチに反映します
mkdocs gh-deploy --force
if %errorlevel% neq 0 (
    echo Deploy failed.
    pause
    exit /b
)

echo === Commit ^& Push to main ===
git add .
rem ビルド成果物(site/)をmainブランチのコミット対象から外す
git reset site/ >nul 2>&1
git commit -m "Update main source" || echo No changes to commit
git push origin main --force

echo === Done ===
pause