@echo off
rem Build the site into site\ with Zensical. Run from this folder: includes are relative to the working directory.
cd /d %~dp0
.venv\Scripts\zensical.exe build --clean
pause
