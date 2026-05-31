import sys
sys.path.insert(0, r"C:\stock_analysis")
exec(open(r"C:\stock_analysis\scripts\blog\05_multifactor_scoreboard_make_images.py", encoding="utf-8").read().split("if __name__")[0])
df_raw = load_universe()
df = add_factor_scores(df_raw)
make_scoreboard_top20(df)
print("ok: 01_scoreboard_top20.png")
make_oil_refining_compare(df)
print("ok: 05_oil_refining_factors.png")
