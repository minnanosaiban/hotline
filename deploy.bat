@echo off
echo === MkDocs build ===
mkdocs build --clean
if %errorlevel% neq 0 exit /b

echo === MkDocs deploy to gh-pages ===
mkdocs gh-deploy --force
if %errorlevel% neq 0 exit /b

echo === Commit & Push to main ===
git add .
git commit -m "Update main source"
git push origin main

echo === Done ===
pause
