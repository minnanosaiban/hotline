@echo off
set PYTHONPATH=C:\stock_analysis
cd /d "C:\Users\mukai\OneDrive\デスクトップ\minnanosaiban\hotline"

echo ===== チャート画像 再生成 =====
echo.

for %%f in (docs\blog\scripts\01_PEG_ROE_make_images.py
            docs\blog\scripts\02_multifactor_make_images.py
            docs\blog\scripts\03_revision_momentum_make_images.py
            docs\blog\scripts\04_surprise_score_make_images.py
            docs\blog\scripts\05_credit_dashboard_make_images.py
            docs\blog\scripts\06_xbrl_intro_make_images.py
            docs\blog\scripts\07_pipeline_make_images.py
            docs\blog\scripts\08_schema_make_images.py
            docs\blog\scripts\09_zscore_make_images.py
            docs\blog\scripts\10_accrual_make_images.py
            docs\blog\scripts\11_triangulation_make_images.py
            docs\blog\scripts\12_segments_make_images.py) do (
    echo --- %%~nf ---
    python %%f
    if errorlevel 1 (
        echo [エラー] %%~nf が失敗しました
    )
    echo.
)

echo ===== 完了 =====
pause
