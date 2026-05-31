@echo off
set PYTHONPATH=C:\stock_analysis
set SCRIPTS=C:\stock_analysis\scripts\blog
set THUMBS=C:\minnanosaiban\hotline\docs\blog\scripts

echo ===== regenerate blog images (make_images) =====
echo.

for %%f in (
  02_collect_other_data_make_images
  03_xbrl_to_json_make_images
  04_garp_peg_roe_make_images
  05_multifactor_scoreboard_make_images
  06_eps_revision_momentum_make_images
  07_surprise_scoreboard_make_images
  08_progress_zscore_make_images
  09_accrual_analysis_make_images
  10_triangulation_make_images
  11_segment_analysis_make_images
  12_car_event_study_make_images
) do (
  echo [make] %%f.py
  python "%SCRIPTS%\%%f.py"
  if errorlevel 1 echo [ERROR] %%f.py
  echo.
)

echo ===== sync to docs (stock -> docs/blog/scripts) =====
python "%SCRIPTS%\sync_to_docs.py"
echo.

echo ===== thumbnails (run from docs; relative output path) =====
for %%n in (
  01_get_stock_prices
  02_collect_other_data
  03_xbrl_to_json
  04_garp_peg_roe
  05_multifactor_scoreboard
  06_eps_revision_momentum
  07_surprise_scoreboard
  08_progress_zscore
  09_accrual_analysis
  10_triangulation
  11_segment_analysis
  12_car_event_study
  13_llm_summary
  14_similar_earnings_search
  15_knn_prediction
) do (
  echo [thumb_%%n]
  python "%THUMBS%\thumb_%%n.py"
  if errorlevel 1 echo [ERROR] thumb_%%n.py
)
echo.

echo ===== done =====
pause
