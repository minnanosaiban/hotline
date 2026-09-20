@echo off
rem Preview at http://localhost:8000/ with Zensical. Run from this folder: includes are relative to the working directory.
cd /d %~dp0
.venv\Scripts\zensical.exe serve
pause
