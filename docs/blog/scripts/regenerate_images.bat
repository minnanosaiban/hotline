@echo off
set PYTHONPATH=C:\stock_analysis
set SCRIPTS=C:\stock_analysis\scripts\blog

echo ===== regenerate blog images =====
echo.

echo [01] 01_PEG_ROE_make_images.py
python "%SCRIPTS%\01_PEG_ROE_make_images.py"
if errorlevel 1 echo [ERROR] 01_PEG_ROE_make_images.py
echo.

echo [02] 02_multifactor_make_images.py
python "%SCRIPTS%\02_multifactor_make_images.py"
if errorlevel 1 echo [ERROR] 02_multifactor_make_images.py
echo.

echo [03] 03_revision_momentum_make_images.py
python "%SCRIPTS%\03_revision_momentum_make_images.py"
if errorlevel 1 echo [ERROR] 03_revision_momentum_make_images.py
echo.

echo [04] 04_surprise_score_make_images.py
python "%SCRIPTS%\04_surprise_score_make_images.py"
if errorlevel 1 echo [ERROR] 04_surprise_score_make_images.py
echo.

echo [05] 05_credit_dashboard_make_images.py
python "%SCRIPTS%\05_credit_dashboard_make_images.py"
if errorlevel 1 echo [ERROR] 05_credit_dashboard_make_images.py
echo.

echo [06] 06_xbrl_intro_make_images.py
python "%SCRIPTS%\06_xbrl_intro_make_images.py"
if errorlevel 1 echo [ERROR] 06_xbrl_intro_make_images.py
echo.

echo [07] 07_pipeline_make_images.py
python "%SCRIPTS%\07_pipeline_make_images.py"
if errorlevel 1 echo [ERROR] 07_pipeline_make_images.py
echo.

echo [08] 08_schema_make_images.py
python "%SCRIPTS%\08_schema_make_images.py"
if errorlevel 1 echo [ERROR] 08_schema_make_images.py
echo.

echo [09] 09_zscore_make_images.py
python "%SCRIPTS%\09_zscore_make_images.py"
if errorlevel 1 echo [ERROR] 09_zscore_make_images.py
echo.

echo [10] 10_accrual_make_images.py
python "%SCRIPTS%\10_accrual_make_images.py"
if errorlevel 1 echo [ERROR] 10_accrual_make_images.py
echo.

echo [11] 11_triangulation_make_images.py
python "%SCRIPTS%\11_triangulation_make_images.py"
if errorlevel 1 echo [ERROR] 11_triangulation_make_images.py
echo.

echo [12] 12_segments_make_images.py
python "%SCRIPTS%\12_segments_make_images.py"
if errorlevel 1 echo [ERROR] 12_segments_make_images.py
echo.

echo [13] 13_car_make_images.py
python "%SCRIPTS%\13_car_make_images.py"
if errorlevel 1 echo [ERROR] 13_car_make_images.py
echo.

echo ===== sync to docs =====
python "%SCRIPTS%\sync_to_docs.py"
echo.

echo ===== thumbnails =====
set THUMBS=C:\minnanosaiban\hotline\docs\blog\scripts

for %%n in (01_garp 02_multifactor 03_eps_revision 04_surprise 05_credit 06_xbrl 07_pipeline 08_schema 09_zscore 10_accrual 11_triangulation 12_segments 13_car 14_llm 15_similarity 16_prediction) do (
    echo [thumb_%%n]
    python "%THUMBS%\thumb_%%n.py"
    if errorlevel 1 echo [ERROR] thumb_%%n.py
)
echo.

echo ===== done =====
pause
