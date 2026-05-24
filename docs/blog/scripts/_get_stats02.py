import sys, os
sys.path.insert(0, r"C:\stock_analysis")
sys.stdout.reconfigure(encoding="utf-8")

# inline imports from 02_multifactor script
exec(open(r"C:\stock_analysis\scripts\blog\02_multifactor_make_images.py", encoding="utf-8").read().split("if __name__")[0])

df_raw = load_universe()
df = add_factor_scores(df_raw)
print(f"universe: {len(df)} 銘柄")

FACTORS_LIST = ["Value","Quality","Growth","Consensus","Sentiment","Momentum","Risk"]
n_all_60 = ((df[[f"score_{f}" for f in FACTORS_LIST]] >= 60).all(axis=1)).sum()
n_trap   = ((df["score_Value"] >= 70) & (df["score_Quality"] <= 30)).sum()
n_hot    = ((df["score_Momentum"] >= 90) & (df["score_Sentiment"] >= 90) & (df["score_Risk"] <= 20)).sum()
n_qv     = ((df["score_Value"] >= 70) & (df["score_Quality"] >= 70)).sum()
print(f"all-7-factors>=60: {n_all_60}")
print(f"value-trap: {n_trap}")
print(f"hot-zone: {n_hot}")
print(f"quality-value: {n_qv}")

n_consensus_mid = ((df["score_Consensus"] >= 49) & (df["score_Consensus"] <= 51)).sum()
print(f"Consensus~50 (missing proxy): {n_consensus_mid} / {len(df)} = {n_consensus_mid/len(df)*100:.0f}%")

from utils.universe_topix500 import topix_large100_codes
universe = topix_large100_codes()
pool = df[df["コード"].isin(universe)]
print(f"TOPIX large-100 pool: {len(pool)} 銘柄")
top20 = pool.nlargest(20, "score_総合")[["コード","銘柄名","score_総合"]+[f"score_{f}" for f in FACTORS_LIST]]
print(top20.to_string(index=False))

print("\n--- Quality-Value ゾーン上位8 ---")
qv = df[(df["score_Value"] >= 70) & (df["score_Quality"] >= 70)].nlargest(8, "score_総合")[["コード","銘柄名","score_Value","score_Quality","score_総合"]]
print(qv.to_string(index=False))

print("\n--- Value-Trap ゾーン上位7 ---")
trap_df = df[(df["score_Value"] >= 70) & (df["score_Quality"] <= 30)].nlargest(7, "score_Value")
trap_cols = ["コード","銘柄名","score_Value","score_Quality"]
extra = [c for c in ["PER実績","PBR予","配当利回り","ROE","ROA","営業利益率"] if c in trap_df.columns]
print(trap_df[trap_cols + extra].to_string(index=False))

print("\n--- Hot Zone (Mom>=90, Sen>=90, Risk<=20) ---")
hot = df[(df["score_Momentum"] >= 90) & (df["score_Sentiment"] >= 90) & (df["score_Risk"] <= 20)][["コード","銘柄名","市場","score_Momentum","score_Sentiment","score_Risk","score_総合"]]
print(hot.to_string(index=False))

print("\n--- 石油元売3社 ---")
for code in ["5020", "5019", "5021"]:
    row = df[df["コード"]==code]
    if not row.empty:
        r = row.iloc[0]
        print(f"{r['銘柄名']} 総合={r['score_総合']:.1f} V={r['score_Value']:.0f} Q={r['score_Quality']:.0f} Gr={r['score_Growth']:.0f} Co={r['score_Consensus']:.0f} Se={r['score_Sentiment']:.0f} Mo={r['score_Momentum']:.0f} Ri={r['score_Risk']:.0f}")
    else:
        print(f"code {code}: not found in universe")

print("\n--- 主要6社 ---")
for code in ["8306", "9433", "9984", "6758", "6861", "7203"]:
    row = df[df["コード"]==code]
    if not row.empty:
        r = row.iloc[0]
        print(f"{r['銘柄名']} 総合={r['score_総合']:.1f} Mo={r['score_Momentum']:.0f} Se={r['score_Sentiment']:.0f} Q={r['score_Quality']:.0f} V={r['score_Value']:.0f} Ri={r['score_Risk']:.0f} Gr={r['score_Growth']:.0f} Co={r['score_Consensus']:.0f}")
    else:
        print(f"code {code}: not found in universe")
