"""
blog/02_マルチファクタースコアボード.md 用の画像生成スクリプト。

生成画像:
  01_scoreboard_top20.png       — 総合スコア Top20 のヒートマップ表
  02_factor_distribution.png    — 7 ファクターのスコア分布ヒストグラム
  03_value_quality_scatter.png  — Value × Quality 散布図 + 主要銘柄ハイライト
  04_majors_radar.png           — 主要 6 社の 7 ファクターレーダー
  05_oil_refining_factors.png   — 石油元売 3 社の 7 ファクター比較レーダー + 横棒

実行: python scripts/blog/02_multifactor_make_images.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle

from config.paths import rakunav_file, PRICES_STOCKS_DAILY
from utils.price_metrics import compute_price_metrics
from utils.master_names import apply_master_names


# ── デザイン設定 ────────────────────────────────────────────────────────────
mpl.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans JP"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["savefig.facecolor"] = "white"
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["savefig.dpi"] = 144

FACTOR_COLORS = {
    "Value":     "#4C8BF5",
    "Quality":   "#50C878",
    "Growth":    "#F5A623",
    "Consensus": "#9B59B6",
    "Sentiment": "#E05C5C",
    "Momentum":  "#1ABC9C",
    "Risk":      "#8C8C8C",
}
FACTORS = list(FACTOR_COLORS)
C_TEXT     = "#202124"
C_TEXT_SUB = "#70757a"
C_GRID     = "#eaeaea"

OUT_DIR = Path(r"C:/Users/mukai/OneDrive/デスクトップ/minnanosaiban/hotline/docs/blog/posts/img/02_multifactor")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ── データ準備 ─────────────────────────────────────────────────────────────
RAKUNAV_SPECS = [
    (113, "EPS(一株あたり当期利益)", "EPS実績"),
    (215, "BPS(予)(一株あたり純資産)", "BPS予"),
    (141, "配当金(円)", "配当金"),
    (133, "EV/EBITDA倍率", "EV/EBITDA"),
    (118, "ROE(自己資本利益率)", "ROE"),
    (119, "ROA(総資産当期利益率)", "ROA"),
    (125, "売上高営業利益率", "営業利益率"),
    (130, "自己資本比率", "自己資本比率"),
    (122, "売上高変化率", "売上高変化率"),
    (129, "経常利益変化率", "経常利益変化率"),
    (219, "過去3年平均売上高成長率(予)", "過去3年平均売上高成長率(予)"),
    (220, "業績予想修正率(予)", "業績予想修正率(予)"),
    (221, "経常利益変化率(予)", "経常利益変化率(予)"),
]

FACTOR_DEFS = {
    "Value":     [("PER", False), ("PBR", False), ("EV/EBITDA", False), ("配当利回り", True)],
    "Quality":   [("ROE", True), ("ROA", True), ("営業利益率", True), ("自己資本比率", True)],
    "Growth":    [("売上高変化率", True), ("経常利益変化率", True)],
    "Consensus": [("業績予想修正率(予)", True), ("経常利益変化率(予)", True),
                  ("過去3年平均売上高成長率(予)", True)],
    "Sentiment": [("出来高増加率", True), ("売買代金増加率", True)],
    "Momentum":  [("値上り率", True), ("過去52週安値からの上昇率", True),
                  ("株価移動平均線からの乖離率①", True)],
    "Risk":      [("過去60日ボラティリティ", False), ("ベータ(対日経平均)", False)],
}


def _to_float(s):
    if pd.isna(s):
        return None
    s = str(s).strip()
    if s in ("", "-", "－", "---"):
        return None
    try:
        return float(s.replace(",", "").replace("+", ""))
    except ValueError:
        return None


def load_universe() -> pd.DataFrame:
    # rakunav 13 指標を統合
    merged = None
    for no, vc, oc in RAKUNAV_SPECS:
        p = rakunav_file(no)
        if p is None:
            raise FileNotFoundError(f"rakunav/{no}_*.csv が見つかりません")
        df = pd.read_csv(p, dtype=str, encoding="utf-8-sig")
        df["コード"] = df["コード"].astype(str).str.strip()
        cand = [c for c in df.columns if c == vc or c.startswith(vc)]
        df[oc] = df[cand[0]].map(_to_float)
        d = df[["コード", "銘柄名", "市場", oc]]
        merged = d if merged is None else merged.merge(d, on=["コード", "銘柄名", "市場"], how="outer")

    # 最新終値
    rows = []
    for p in PRICES_STOCKS_DAILY.glob("*.parquet"):
        try:
            s = pd.read_parquet(p, columns=["Close"])["Close"].dropna()
            if not s.empty:
                rows.append({"コード": p.stem, "Close_yf": float(s.iloc[-1])})
        except Exception:
            pass
    closes = pd.DataFrame(rows)
    merged = merged.merge(closes, on="コード", how="inner")

    # Value 自前計算
    merged["PER"]       = merged["Close_yf"] / merged["EPS実績"].where(merged["EPS実績"] > 0)
    merged["PBR"]       = merged["Close_yf"] / merged["BPS予"].where(merged["BPS予"] > 0)
    merged["配当利回り"] = merged["配当金"].where(merged["配当金"] > 0) / merged["Close_yf"] * 100

    # 価格・出来高指標
    pm = compute_price_metrics(merged["コード"].tolist())
    merged = merged.merge(pm, on="コード", how="left")

    # 銘柄名を price_targets の短縮表記に統一
    merged = apply_master_names(merged)
    return merged


def percentile_score(series: pd.Series, higher_better: bool) -> pd.Series:
    ranked = series.rank(pct=True, na_option="keep") * 100
    if not higher_better:
        ranked = 100 - ranked
    return ranked.fillna(50)


def add_factor_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for factor, metrics in FACTOR_DEFS.items():
        cols = []
        for col, higher in metrics:
            if col not in out.columns:
                continue
            series = out[col].where(out[col] > 0) if not higher else out[col]
            sc = f"_s_{col}"
            out[sc] = percentile_score(series, higher)
            cols.append(sc)
        out[f"score_{factor}"] = out[cols].mean(axis=1) if cols else 50.0
    out["score_総合"] = out[[f"score_{f}" for f in FACTORS]].mean(axis=1)
    return out


# 主要銘柄（連載01 と同じ 6 社で揃える）
MAJORS = [
    ("7203", "トヨタ"),
    ("9984", "ソフトバンクG"),
    ("6758", "ソニーG"),
    ("8306", "三菱UFJ"),
    ("6861", "キーエンス"),
    ("9433", "KDDI"),
]

# 連載01 と同じ石油元売 3 社（セクター内比較）
OIL_REFINERS = [
    ("5021", "コスモエネルギーHLDG", "#27ae60"),  # 緑: 最も Value 高
    ("5020", "ENEOS HLDG",          "#3498db"),  # 青
    ("5019", "出光興産",             "#e67e22"),  # オレンジ
]


# ── 1) Top20 スコアボード ──────────────────────────────────────────────────
def make_scoreboard_top20(df: pd.DataFrame) -> None:
    top = df.nlargest(20, "score_総合").reset_index(drop=True)
    top.index += 1
    cols = ["score_総合"] + [f"score_{f}" for f in FACTORS]
    labels = ["総合"] + FACTORS

    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(-0.5, 5.5 + len(cols) - 0.3)
    ax.set_ylim(len(top) + 1, -1)

    # ヘッダ
    ax.text(0.0, -0.5, "順位", fontsize=14, fontweight="bold", ha="center", va="center", color=C_TEXT)
    ax.text(1.0, -0.5, "コード", fontsize=14, fontweight="bold", ha="center", va="center", color=C_TEXT)
    ax.text(2.5, -0.5, "銘柄名", fontsize=14, fontweight="bold", ha="left",   va="center", color=C_TEXT)
    for i, lab in enumerate(labels):
        ax.text(5.5 + i, -0.5, lab, fontsize=14, fontweight="bold",
                ha="center", va="center", color=C_TEXT)

    cmap = plt.get_cmap("RdYlGn")
    for r, (_, row) in enumerate(top.iterrows()):
        ax.text(0.0, r + 0.5, f"{r+1}",   fontsize=14, ha="center", va="center", color=C_TEXT)
        ax.text(1.0, r + 0.5, row["コード"], fontsize=14, ha="center", va="center", color=C_TEXT)
        name = (row["銘柄名"] or "")[:14]
        ax.text(2.5, r + 0.5, name, fontsize=14, ha="left", va="center", color=C_TEXT)
        for i, col in enumerate(cols):
            v = row[col]
            color = cmap(np.clip(v / 100, 0.05, 0.95))
            rect = Rectangle((5.5 + i - 0.45, r + 0.05), 0.9, 0.9,
                             facecolor=color, edgecolor="white", linewidth=1.0)
            ax.add_patch(rect)
            txt_color = "white" if v < 35 or v > 70 else "#202124"
            ax.text(5.5 + i, r + 0.5, f"{v:.0f}",
                    fontsize=13.3, ha="center", va="center",
                    color=txt_color, fontweight="bold" if col == "score_総合" else "normal")

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ("top", "right", "left", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.set_title("総合スコア Top 20  ―  7 ファクター × ヒートマップ",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "01_scoreboard_top20.png")
    plt.close(fig)


# ── 2) ファクタースコア分布 ─────────────────────────────────────────────────
def make_factor_distribution(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(13.5, 6))
    axes = axes.flatten()
    for i, f in enumerate(FACTORS):
        ax = axes[i]
        s = df[f"score_{f}"].dropna()
        ax.hist(s, bins=20, range=(0, 100),
                color=FACTOR_COLORS[f], alpha=0.75, edgecolor="white", linewidth=0.5)
        med = float(s.median())
        ax.axvline(med, color="#202124", linestyle="--", linewidth=1.0, alpha=0.5)
        ax.text(med + 1.5, ax.get_ylim()[1] * 0.92, f"中央{med:.0f}",
                fontsize=12.6, color="#202124")
        ax.set_title(f, fontsize=15.4, fontweight="bold", color=C_TEXT)
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 50, 100])
        ax.tick_params(labelsize=8, colors=C_TEXT_SUB)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", color=C_GRID, linewidth=0.5)
    # 余ったセルを消す（マルチファクター → 8セル中 1つ余る）
    for ax in axes[len(FACTORS):]:
        ax.axis("off")

    fig.suptitle(f"7 ファクター スコア分布（対象 {len(df):,} 銘柄）",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "02_factor_distribution.png")
    plt.close(fig)


# ── 3) Value × Quality 散布図 ─────────────────────────────────────────────
def make_value_quality_scatter(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11.5, 8))

    # 4 象限の薄塗り
    ax.axhspan(70, 100, xmin=0.7, xmax=1.0, facecolor="#27ae60", alpha=0.08)  # 右上 ★Buffett
    ax.axhspan(70, 100, xmin=0.0, xmax=0.3, facecolor="#3498db", alpha=0.05)  # 左上 高品質グロース
    ax.axhspan(0,  30,  xmin=0.7, xmax=1.0, facecolor="#e74c3c", alpha=0.05)  # 右下 バリュー罠

    # 全銘柄背景
    base = df.dropna(subset=["score_Value", "score_Quality"])
    ax.scatter(base["score_Value"], base["score_Quality"],
               s=10, color="#bbbbbb", alpha=0.30, edgecolors="none", zorder=1)

    # 主要銘柄
    for code, _label_hint in MAJORS:
        row = df.loc[df["コード"] == code]
        if row.empty:
            continue
        r = row.iloc[0]
        label = r["銘柄名"]
        ax.scatter(r["score_Value"], r["score_Quality"],
                   s=180, color="#1ABC9C", edgecolor="white", linewidth=2.0, zorder=5)
        ax.annotate(label, xy=(r["score_Value"], r["score_Quality"]),
                    xytext=(10, 8), textcoords="offset points",
                    fontsize=14.7, fontweight="bold", color=C_TEXT,
                    bbox=dict(facecolor="white", alpha=0.88,
                              edgecolor="none", boxstyle="round,pad=0.25"))

    # 基準線
    ax.axhline(70, color="#27ae60", linestyle="--", alpha=0.5, linewidth=1.0)
    ax.axvline(70, color="#27ae60", linestyle="--", alpha=0.5, linewidth=1.0)
    ax.axhline(50, color="#cccccc", linestyle=":",  alpha=0.6, linewidth=0.8)
    ax.axvline(50, color="#cccccc", linestyle=":",  alpha=0.6, linewidth=0.8)

    # ゾーンラベル
    ax.text(85, 92, "★クオリティ・バリュー\n（バフェット流）",
            fontsize=14.7, fontweight="bold", color="#27ae60",
            ha="center", va="center")
    ax.text(15, 92, "高品質グロース\n（割高優良）", fontsize=14, color="#3498db",
            ha="center", va="center")
    ax.text(85, 12, "バリュー・トラップ警戒", fontsize=14, color="#e74c3c",
            ha="center", va="center")
    ax.text(15, 12, "低品質×割高\n（投資不適格）", fontsize=14, color="#888888",
            ha="center", va="center")

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Value スコア  ← 割高     割安 →", fontsize=15.4, color=C_TEXT)
    ax.set_ylabel("Quality スコア  ← 低品質    高品質 →", fontsize=15.4, color=C_TEXT)
    ax.set_title("Value × Quality 散布図  ―  4 ゾーンと主要銘柄の位置",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left")
    ax.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "03_value_quality_scatter.png")
    plt.close(fig)


# ── 4) 主要銘柄レーダー ─────────────────────────────────────────────────────
def make_majors_radar(df: pd.DataFrame) -> None:
    n_majors = len(MAJORS)
    n_cols = 3
    n_rows = (n_majors + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12.5, 4.0 * n_rows),
                             subplot_kw=dict(projection="polar"))
    axes = axes.flatten() if n_majors > 1 else [axes]

    angles = np.linspace(0, 2 * np.pi, len(FACTORS), endpoint=False).tolist()
    angles_closed = angles + [angles[0]]

    for i, (code, _label_hint) in enumerate(MAJORS):
        ax = axes[i]
        row = df.loc[df["コード"] == code]
        if row.empty:
            ax.axis("off")
            continue
        r = row.iloc[0]
        vals = [r[f"score_{f}"] for f in FACTORS]
        vals_closed = vals + [vals[0]]

        ax.fill(angles_closed, vals_closed, color="#1ABC9C", alpha=0.20)
        ax.plot(angles_closed, vals_closed, color="#1ABC9C", linewidth=2.0, marker="o", markersize=4)

        # 50 ライン
        ax.plot(angles_closed, [50] * len(angles_closed), color="#cccccc",
                linewidth=0.8, linestyle="--")

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75])
        ax.set_yticklabels(["25", "50", "75"], fontsize=9.8, color=C_TEXT_SUB)
        ax.set_xticks(angles)
        ax.set_xticklabels(FACTORS, fontsize=12.6, color=C_TEXT)

        total = r["score_総合"]
        label = r["銘柄名"]
        ax.set_title(f"{label}（総合 {total:.0f}）",
                     fontsize=15.4, fontweight="bold", color=C_TEXT, pad=14)

    for ax in axes[n_majors:]:
        ax.axis("off")

    fig.suptitle("主要 6 社の 7 ファクターレーダー",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=1.00)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "04_majors_radar.png")
    plt.close(fig)


# ── 5) 石油元売 3 社のセクター内比較 ────────────────────────────────────────
def make_oil_refining_compare(df: pd.DataFrame) -> None:
    """連載01 と同じ 3 社を 7 ファクター・レーダーと総合スコア比較バーで可視化。"""
    fig = plt.figure(figsize=(13, 5.6))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.05], wspace=0.32)

    angles = np.linspace(0, 2 * np.pi, len(FACTORS), endpoint=False).tolist()
    angles_closed = angles + [angles[0]]

    # 3 社のレーダー
    rows_for_table = []
    for i, (code, _label_hint, color) in enumerate(OIL_REFINERS):
        ax = fig.add_subplot(gs[0, i], projection="polar")
        row = df.loc[df["コード"] == code]
        if row.empty:
            ax.axis("off")
            continue
        r = row.iloc[0]
        label = r["銘柄名"]
        vals = [r[f"score_{f}"] for f in FACTORS]
        vals_closed = vals + [vals[0]]

        ax.fill(angles_closed, vals_closed, color=color, alpha=0.22)
        ax.plot(angles_closed, vals_closed, color=color, linewidth=2.0, marker="o", markersize=4)
        ax.plot(angles_closed, [50] * len(angles_closed), color="#cccccc",
                linewidth=0.8, linestyle="--")

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75])
        ax.set_yticklabels(["25", "50", "75"], fontsize=9.8, color=C_TEXT_SUB)
        ax.set_xticks(angles)
        ax.set_xticklabels(FACTORS, fontsize=11.9, color=C_TEXT)
        ax.set_title(f"{label}\n（総合 {r['score_総合']:.0f}）",
                     fontsize=14.7, fontweight="bold", color=C_TEXT, pad=12)

        rows_for_table.append({
            "label": label, "color": color,
            **{f: r[f"score_{f}"] for f in FACTORS},
            "total": r["score_総合"],
        })

    # 右端: 横棒比較（Value / Quality / Consensus / Momentum / Sentiment）
    ax_bar = fig.add_subplot(gs[0, 3])
    highlight = ["Value", "Quality", "Consensus", "Sentiment", "Momentum"]
    n_metrics = len(highlight)
    n_co = len(rows_for_table)
    bar_h = 0.24
    y_base = np.arange(n_metrics)
    for k, row in enumerate(rows_for_table):
        ys = y_base + (k - (n_co - 1) / 2) * bar_h
        vals = [row[m] for m in highlight]
        ax_bar.barh(ys, vals, height=bar_h, color=row["color"],
                    alpha=0.85, edgecolor="white", linewidth=0.8,
                    label=row["label"])
        for y, v in zip(ys, vals):
            ax_bar.text(v + 1.5, y, f"{v:.0f}", va="center",
                        fontsize=11.2, color=C_TEXT)

    ax_bar.axvline(50, color="#cccccc", linestyle=":", linewidth=0.8)
    ax_bar.set_yticks(y_base)
    ax_bar.set_yticklabels(highlight, fontsize=13.3, color=C_TEXT)
    ax_bar.invert_yaxis()
    ax_bar.set_xlim(0, 100)
    ax_bar.set_xticks([0, 25, 50, 75, 100])
    ax_bar.tick_params(labelsize=8, colors=C_TEXT_SUB)
    for sp in ("top", "right"):
        ax_bar.spines[sp].set_visible(False)
    ax_bar.set_title("主要ファクター比較", fontsize=14.7, fontweight="bold",
                     color=C_TEXT, pad=12, loc="left")
    ax_bar.legend(loc="lower right", fontsize=10.5, frameon=False)

    fig.suptitle("石油元売 3 社の 7 ファクター比較  ―  セクター内マルチファクター分析",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "05_oil_refining_factors.png", bbox_inches="tight")
    plt.close(fig)


# ── main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df_raw = load_universe()
    df = add_factor_scores(df_raw)
    print(f"[load] {len(df):,} 銘柄")
    print(f"[majors] " + ", ".join(
        f"{n}: 総合={df.loc[df['コード']==c, 'score_総合'].iloc[0]:.1f}"
        for c, n in MAJORS if (df['コード']==c).any()
    ))

    make_scoreboard_top20(df)
    print("[ok] 01_scoreboard_top20.png")
    make_factor_distribution(df)
    print("[ok] 02_factor_distribution.png")
    make_value_quality_scatter(df)
    print("[ok] 03_value_quality_scatter.png")
    make_majors_radar(df)
    print("[ok] 04_majors_radar.png")
    make_oil_refining_compare(df)
    print("[ok] 05_oil_refining_factors.png")

    # 連載02 用の分析用統計値も出力（記事執筆で参照）
    print("\n=== 分析用統計値 ===")
    n_all_60 = ((df[[f'score_{f}' for f in FACTORS]] >= 60).all(axis=1)).sum()
    n_trap   = ((df['score_Value'] >= 70) & (df['score_Quality'] <= 30)).sum()
    n_hot    = ((df['score_Momentum'] >= 90) & (df['score_Sentiment'] >= 90) & (df['score_Risk'] <= 20)).sum()
    n_qv     = ((df['score_Value'] >= 70) & (df['score_Quality'] >= 70)).sum()
    print(f"all-7-factors >= 60: {n_all_60} stocks")
    print(f"value-trap (Value>=70, Quality<=30): {n_trap} stocks")
    print(f"hot zone (Mom>=90, Sen>=90, Risk<=20): {n_hot} stocks")
    print(f"quality-value (V>=70 & Q>=70): {n_qv} stocks")

    # Top10 詳細
    print("\n=== 総合スコア Top10 ===")
    top10 = df.nlargest(10, "score_総合")[
        ["コード", "銘柄名", "市場", "score_総合"] + [f"score_{f}" for f in FACTORS]
    ]
    print(top10.to_string(index=False))
