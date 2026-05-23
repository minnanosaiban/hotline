@echo off
set PYTHONPATH=C:\stock_analysis
cd /d "C:\Users\mukai\OneDrive\デスクトップ\minnanosaiban\hotline"

echo ===== サムネイル 再生成 =====
echo.

for %%f in (docs\blog\scripts\thumb_01_garp.py
            docs\blog\scripts\thumb_02_multifactor.py
            docs\blog\scripts\thumb_03_eps_revision.py
            docs\blog\scripts\thumb_04_surprise.py
            docs\blog\scripts\thumb_05_credit.py
            docs\blog\scripts\thumb_06_xbrl.py
            docs\blog\scripts\thumb_07_pipeline.py
            docs\blog\scripts\thumb_08_schema.py
            docs\blog\scripts\thumb_09_zscore.py
            docs\blog\scripts\thumb_10_accrual.py
            docs\blog\scripts\thumb_11_triangulation.py
            docs\blog\scripts\thumb_12_segments.py
            docs\blog\scripts\thumb_13_car.py
            docs\blog\scripts\thumb_14_llm.py
            docs\blog\scripts\thumb_15_similarity.py
            docs\blog\scripts\thumb_16_prediction.py) do (
    echo --- %%~nf ---
    python %%f
    if errorlevel 1 (
        echo [エラー] %%~nf が失敗しました
    )
    echo.
)

echo ===== 完了 =====
pause
