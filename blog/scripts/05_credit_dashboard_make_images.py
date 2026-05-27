"""
blog/05_信用需給ダッシュボード.md 用の画像生成スクリプト。

生成画像:
  01_credit_distribution.png  — 信用倍率と信用残レシオの分布（対数スケール）
  02_oil_refining_credit.png  — 石油元売 3 社の信用需給比較
  03_credit_changes.png       — 前週比(買) 急増/急減 Top10
  04_credit_vs_volume.png     — 信用倍率 × 出来高増加率 散布図（踏み上げスクリーナー）
  05_fund_vs_credit.png       — 業績 × 需給 4 象限マトリクス

実行: python scripts/blog/05_credit_dashboard_make_images.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, r"C:\stock_analysis")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from config.paths import rakunav_file
from utils.master_names import apply_master_names
from utils.price_metrics import compute_price_metrics


# ── デザイン設定 ────────────────────────────────────────────────────────────
mpl.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans JP"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["savefig.facecolor"] = "white"
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["savefig.dpi"] = 144
mpl.rcParams["savefig.pad_inches"] = 0        # left/right/top: no padding
mpl.rcParams["axes.titlepad"] = 30
mpl.rcParams["font.size"] = 16
mpl.rcParams["axes.titlesize"] = 20
mpl.rcParams["axes.labelsize"] = 16
mpl.rcParams["xtick.labelsize"] = 16
mpl.rcParams["ytick.labelsize"] = 16
mpl.rcParams["legend.fontsize"] = 16

C_UP   = "#5a9a72"
C_DOWN = "#c87878"
C_BUY  = "#4C8BF5"
C_SELL = "#8C8C8C"
C_HOT  = "#c87878"
C_OK   = "#5a9a72"
C_WARN = "#F39C12"
C_BG   = "#cccccc"
C_TEXT = "#202124"
C_TEXT_SUB = "#70757a"
C_GRID = "#eaeaea"

OUT_DIR = Path(r"C:/minnanosaiban/hotline/docs/blog/posts/img/05_credit")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _savefig_vpad(fig: plt.Figure, path: Path, bpad: float = 0.5) -> None:
    """下のみ bpad インチの余白を追加して保存する（上・左右は余白なし）。"""
    import io
    import numpy as np
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches="tight", pad_inches=0, format="png")
    buf.seek(0)
    img = plt.imread(buf)                            # RGBA float32 (H, W, 4)
    pad_rows = max(1, round(bpad * fig.dpi))
    white = np.ones((pad_rows, img.shape[1], img.shape[2]), dtype=img.dtype)
    plt.imsave(str(path), np.vstack([img, white]), dpi=fig.dpi)


# ── データ準備 ─────────────────────────────────────────────────────────────
RAKUNAV_SPECS = [
    (311, "信用残(買)",            "信用残(買)"),
    (312, "信用残(売)",            "信用残(売)"),
    (313, "前週比(買)",            "前週比(買)"),
    (314, "前週比(売)",            "前週比(売)"),
    (138, "信用残/売買高レシオ",   "信用残/売買高レシオ"),
    (220, "業績予想修正率(予)",    "業績予想修正率(予)"),
    (118, "ROE(自己資本利益率)",   "ROE"),
    (120, "時価総額(百万円)",      "時価総額"),
]


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
        merged = d if merged is None else merged.merge(
            d, on=["コード", "銘柄名", "市場"], how="outer"
        )

    merged["信用倍率"] = merged["信用残(買)"] / merged["信用残(売)"].where(merged["信用残(売)"] > 0)
    pm = compute_price_metrics(merged["コード"].tolist())
    merged = merged.merge(pm, on="コード", how="left")
    merged = apply_master_names(merged)
    return merged


OIL_REFINERS = [
    ("5021", "コスモエネＨＤ", "#888888"),
    ("5020", "ＥＮＥＯＳ",      "#444444"),
    ("5019", "出光興産",       "#aaaaaa"),
]


# ── 1) 信用倍率と信用残レシオの分布 ─────────────────────────────────────────
def make_credit_distribution(df: pd.DataFrame) -> None:
    f = df[df["時価総額"].fillna(0) >= 10_000]

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 5),
                                     gridspec_kw=dict(wspace=0.3))

    # 左: 信用倍率分布（対数）
    s_kr = f["信用倍率"].dropna()
    s_kr = s_kr[(s_kr > 0.01) & (s_kr < 1000)]
    log_kr = np.log10(s_kr)
    ax_l.hist(log_kr, bins=40, color=C_HOT, alpha=0.7,
              edgecolor="white", linewidth=0.5)
    med_log = float(log_kr.median())
    ax_l.axvline(med_log, color="#202124", linestyle="--", linewidth=1.0, alpha=0.7,
                 label=f"中央値 {10**med_log:.1f}倍")
    ax_l.axvline(0, color="#aaaaaa", linewidth=0.7, label="1.0倍（拮抗）")
    ax_l.axvline(np.log10(5), color=C_OK, linewidth=0.7,
                 linestyle=":", label="5倍（踏み上げ警戒）")
    ax_l.set_xticks([-1, 0, 1, 2, 3])
    ax_l.set_xticklabels(["0.1", "1", "10", "100", "1000"])
    ax_l.set_xlabel("信用倍率（倍、対数スケール）", fontsize=16, color=C_TEXT)
    ax_l.set_ylabel("銘柄数", fontsize=16, color=C_TEXT_SUB)
    ax_l.set_title(f"信用倍率の分布  ―  {len(s_kr):,} 銘柄",
                   fontsize=16, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_l.legend(loc="upper right", fontsize=16, frameon=False)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)
    ax_l.grid(axis="y", color=C_GRID, linewidth=0.5)

    # 右: 信用残/売買高レシオ分布
    s_ra = f["信用残/売買高レシオ"].dropna()
    s_ra = s_ra[(s_ra > 0) & (s_ra < 100)]
    ax_r.hist(s_ra, bins=40, color=C_WARN, alpha=0.7,
              edgecolor="white", linewidth=0.5)
    med = float(s_ra.median())
    ax_r.axvline(med, color="#202124", linestyle="--", linewidth=1.0, alpha=0.7,
                 label=f"中央値 {med:.1f}日")
    ax_r.axvline(10, color=C_DOWN, linewidth=0.7, linestyle=":",
                 label="10日（需給重）")
    ax_r.set_xlabel("信用残 / 売買高レシオ（日）", fontsize=16, color=C_TEXT)
    ax_r.set_ylabel("銘柄数", fontsize=16, color=C_TEXT_SUB)
    ax_r.set_title(f"信用残/売買高レシオの分布  ―  {len(s_ra):,} 銘柄",
                   fontsize=16, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_r.legend(loc="upper right", fontsize=16, frameon=False)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)
    ax_r.grid(axis="y", color=C_GRID, linewidth=0.5)

    fig.suptitle("信用需給の市場全体像（時価総額 100 億円以上）",
                 fontsize=16, fontweight="bold", color=C_TEXT, y=1.02)
    _savefig_vpad(fig, OUT_DIR / "01_credit_distribution.png")
    plt.close(fig)


# ── 2) 石油元売 3 社の信用需給 ──────────────────────────────────────────────
def make_oil_refining_credit(df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(13, 5.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.2, 1.0], wspace=0.34)

    # 本図ローカルの色設計
    #   パネルA(信用倍率)  : 3社識別だけで意味なし → 青系グラデーション
    #   パネルB(信用残買/売): 買vs売は意味あり → 落ち着いた青/グレー
    #   パネルC(前週比)    : +/- は意味あり → 落ち着いた緑/赤
    GRAD_BLUES = ["#8fb4d9", "#5a8fc4", "#2c5f9b"]  # 薄→濃 (コスモ/ＥＮＥＯＳ/出光)
    C_BUY_LOCAL  = "#5a8fc4"
    C_SELL_LOCAL = "#9aa0a6"
    C_UP_LOCAL   = "#5a9a72"
    C_DOWN_LOCAL = "#c87878"

    rows = []
    for (code, label, _color), grad in zip(OIL_REFINERS, GRAD_BLUES):
        r = df.loc[df["コード"] == code]
        if r.empty:
            continue
        r = r.iloc[0]
        rows.append({
            "コード": code, "銘柄名": label, "color": grad,
            "信用倍率": r["信用倍率"], "信用残(買)": r["信用残(買)"],
            "信用残(売)": r["信用残(売)"], "前週比(買)": r["前週比(買)"],
            "信用残/売買高レシオ": r["信用残/売買高レシオ"],
            "業績予想修正率(予)": r.get("業績予想修正率(予)"),
        })
    rdf = pd.DataFrame(rows)

    # パネル A: 信用倍率
    ax_a = fig.add_subplot(gs[0, 0])
    y = np.arange(len(rdf))
    bars = ax_a.barh(y, rdf["信用倍率"], color=rdf["color"], alpha=0.85,
                     edgecolor="white", linewidth=0.8)
    ax_a.axvline(1, color="#999999", linewidth=0.8, linestyle="--")
    ax_a.axvline(5, color=C_OK, linewidth=0.7, linestyle=":")
    for i, v in enumerate(rdf["信用倍率"]):
        ax_a.text(v + 0.3, i, f"{v:.2f}倍", va="center",
                  fontsize=16, fontweight="bold", color=C_TEXT)
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(rdf["銘柄名"], fontsize=16)
    ax_a.invert_yaxis()
    ax_a.set_xlim(0, max(rdf["信用倍率"]) * 1.25)
    ax_a.set_title("信用倍率（買 ÷ 売）", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")
    for sp in ("top", "right"):
        ax_a.spines[sp].set_visible(False)
    ax_a.grid(axis="x", color=C_GRID, linewidth=0.5)

    # パネル B: 信用残(買)/(売)
    ax_b = fig.add_subplot(gs[0, 1])
    h = 0.35
    ax_b.barh(y - h/2, rdf["信用残(買)"] / 1000, height=h,
              color=C_BUY_LOCAL, alpha=0.85, edgecolor="white", linewidth=0.8,
              label="信用残(買)（千株）")
    ax_b.barh(y + h/2, rdf["信用残(売)"] / 1000, height=h,
              color=C_SELL_LOCAL, alpha=0.85, edgecolor="white", linewidth=0.8,
              label="信用残(売)（千株）")
    for i, (b, s) in enumerate(zip(rdf["信用残(買)"], rdf["信用残(売)"])):
        ax_b.text(b / 1000 + 30, i - h/2, f"{b/1000:,.0f}",
                  va="center", fontsize=16, color=C_BUY_LOCAL)
        ax_b.text(s / 1000 + 30, i + h/2, f"{s/1000:,.0f}",
                  va="center", fontsize=16, color=C_SELL_LOCAL)
    ax_b.set_yticks(y)
    ax_b.set_yticklabels([""] * len(rdf))
    ax_b.invert_yaxis()
    ax_b.set_xlim(0, max(rdf["信用残(買)"]) / 1000 * 1.25)
    ax_b.set_title("信用残（千株）", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")
    ax_b.legend(loc="lower right", fontsize=16, frameon=False)
    for sp in ("top", "right"):
        ax_b.spines[sp].set_visible(False)
    ax_b.grid(axis="x", color=C_GRID, linewidth=0.5)

    # パネル C: 前週比(買)
    ax_c = fig.add_subplot(gs[0, 2])
    colors = [C_UP_LOCAL if v >= 0 else C_DOWN_LOCAL for v in rdf["前週比(買)"]]
    ax_c.barh(y, rdf["前週比(買)"] / 1000, color=colors, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    ax_c.axvline(0, color="#999999", linewidth=0.8)
    for i, v in enumerate(rdf["前週比(買)"]):
        ax_c.text(v / 1000 + (5 if v >= 0 else -5), i,
                  f"{v/1000:+.0f}千株",
                  va="center", ha="left" if v >= 0 else "right",
                  fontsize=16, fontweight="bold",
                  color=C_UP_LOCAL if v >= 0 else C_DOWN_LOCAL)
    ax_c.set_yticks(y)
    ax_c.set_yticklabels([""] * len(rdf))
    ax_c.invert_yaxis()
    ax_c.set_title("信用残(買) 前週比（千株）", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")
    for sp in ("top", "right"):
        ax_c.spines[sp].set_visible(False)
    ax_c.grid(axis="x", color=C_GRID, linewidth=0.5)
    xmax = max(abs(rdf["前週比(買)"].min()) / 1000, rdf["前週比(買)"].max() / 1000) * 1.5
    ax_c.set_xlim(-xmax, xmax)

    fig.suptitle("石油元売 3 社  ―  信用需給スナップショット",
                 fontsize=16, fontweight="bold", color=C_TEXT, y=1.02)
    _savefig_vpad(fig, OUT_DIR / "02_oil_refining_credit.png")
    plt.close(fig)


# ── 3) 前週比(買) 急増/急減 Top10 ─────────────────────────────────────────
def make_credit_changes(df: pd.DataFrame) -> None:
    f = df[df["時価総額"].fillna(0) >= 10_000].dropna(subset=["前週比(買)"])
    top_up = f.nlargest(10, "前週比(買)").iloc[::-1]
    top_dn = f.nsmallest(10, "前週比(買)").iloc[::-1]

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(14, 6),
                                     gridspec_kw=dict(wspace=0.45))

    # 急増
    y = np.arange(len(top_up))
    ax_l.barh(y, top_up["前週比(買)"] / 1_000_000, color=C_BUY, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, (_, r) in enumerate(top_up.iterrows()):
        v = r["前週比(買)"] / 1_000_000
        ax_l.text(v + 0.2, i, f"+{v:.2f}M株 (倍率{r['信用倍率']:.1f})",
                  va="center", fontsize=16, color=C_BUY, fontweight="bold")
    ax_l.set_yticks(y)
    ax_l.set_yticklabels([f"{r['コード']} {r['銘柄名']}"
                          for _, r in top_up.iterrows()], fontsize=16)
    ax_l.set_xlabel("前週比(買)（百万株）", fontsize=16, color=C_TEXT_SUB)
    ax_l.set_xlim(0, top_up["前週比(買)"].max() / 1_000_000 * 1.4)
    ax_l.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)
    ax_l.set_title("信用残(買) 前週比 急増 Top10", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")

    # 急減
    y = np.arange(len(top_dn))
    ax_r.barh(y, top_dn["前週比(買)"] / 1_000_000, color=C_DOWN, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, (_, r) in enumerate(top_dn.iterrows()):
        v = r["前週比(買)"] / 1_000_000
        ax_r.text(v - 0.2, i, f"{v:.2f}M株 (倍率{r['信用倍率']:.1f})",
                  va="center", ha="right",
                  fontsize=16, color=C_DOWN, fontweight="bold")
    ax_r.set_yticks(y)
    ax_r.set_yticklabels([f"{r['コード']} {r['銘柄名']}"
                          for _, r in top_dn.iterrows()], fontsize=16)
    ax_r.set_xlabel("前週比(買)（百万株）", fontsize=16, color=C_TEXT_SUB)
    ax_r.set_xlim(top_dn["前週比(買)"].min() / 1_000_000 * 1.4, 0)
    ax_r.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)
    ax_r.set_title("信用残(買) 前週比 急減 Top10", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")

    fig.suptitle("信用残(買) の週次変化  ―  時価総額 100 億円以上",
                 fontsize=16, fontweight="bold", color=C_TEXT, y=1.00)
    _savefig_vpad(fig, OUT_DIR / "03_credit_changes.png")
    plt.close(fig)


# ── 4) 信用倍率 × 出来高増加率 散布図 ────────────────────────────────────────
def make_credit_vs_volume(df: pd.DataFrame) -> None:
    f = df[df["時価総額"].fillna(0) >= 10_000].copy()
    f = f.dropna(subset=["信用倍率", "出来高増加率"])
    f = f[(f["信用倍率"] > 0) & (f["出来高増加率"] > 0)]
    f = f[(f["信用倍率"] < 200) & (f["出来高増加率"] < 10)]

    med_kr  = f["信用倍率"].median()
    med_vol = f["出来高増加率"].median()

    fig, ax = plt.subplots(figsize=(13, 7.5))

    # 右上ゾーン
    ax.axhspan(med_vol, 10, xmin=(med_kr - 0) / 200, xmax=1.0,
               facecolor=C_HOT, alpha=0.05)

    # 背景
    bg = f[~((f["信用倍率"] > med_kr) & (f["出来高増加率"] > med_vol))]
    ax.scatter(bg["信用倍率"], bg["出来高増加率"],
               s=14, color=C_BG, alpha=0.30, edgecolors="none", zorder=1)

    # 注目（右上）
    hot = f[(f["信用倍率"] > med_kr) & (f["出来高増加率"] > med_vol)]
    ax.scatter(hot["信用倍率"], hot["出来高増加率"],
               s=34, color=C_HOT, alpha=0.65, edgecolors="white", linewidth=0.4,
               zorder=4, label=f"踏み上げ候補 ({len(hot)})")

    # 石油元売
    for code, label, _ in OIL_REFINERS:
        r = df.loc[df["コード"] == code]
        if r.empty:
            continue
        r = r.iloc[0]
        x, y = r["信用倍率"], r["出来高増加率"]
        if pd.isna(x) or pd.isna(y):
            continue
        ax.scatter(x, y, s=200, color=C_TEXT, edgecolor="white",
                   linewidth=2.0, zorder=8, marker="*")
        ax.annotate(label, xy=(x, y), xytext=(10, 8),
                    textcoords="offset points",
                    fontsize=16, fontweight="bold", color=C_TEXT,
                    bbox=dict(facecolor="white", alpha=0.92,
                              edgecolor="#aaaaaa", boxstyle="round,pad=0.3"),
                    zorder=9)

    # 中央値ライン
    ax.axhline(med_vol, color="#777777", linestyle="--", linewidth=0.7)
    ax.axvline(med_kr, color="#777777", linestyle="--", linewidth=0.7)
    ax.axvline(5, color=C_OK, linestyle=":", linewidth=0.7, alpha=0.7)

    # ゾーンラベル
    ax.text(100, 5.5, "★踏み上げ候補★\n信用倍率高 × 出来高急増",
            fontsize=16, fontweight="bold", color=C_HOT,
            ha="center", va="center")
    ax.text(1, 5.5, "出来高急増\n空売り優位",
            fontsize=16, color=C_TEXT_SUB, ha="center", va="center")
    ax.text(100, 0.3, "信用倍率高\n出来高小（注目薄）",
            fontsize=16, color=C_TEXT_SUB, ha="center", va="center")

    ax.set_xlim(0, 200)
    ax.set_ylim(0, 7)
    ax.set_xlabel("信用倍率（倍）  ← 空売り優位    踏み上げリスク →",
                  fontsize=16, color=C_TEXT)
    ax.set_ylabel("出来高増加率（倍、yfinance 自前計算）  ← 閑散    急増 →",
                  fontsize=16, color=C_TEXT)
    ax.set_title(f"信用倍率 × 出来高増加率  ―  踏み上げスクリーナー（中央値: {med_kr:.1f}倍 / {med_vol:.2f}倍）",
                 fontsize=16, fontweight="bold", color=C_TEXT, pad=12, loc="left")
    ax.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper right", fontsize=16, frameon=True,
              facecolor="white", edgecolor="#dddddd")
    _savefig_vpad(fig, OUT_DIR / "04_credit_vs_volume.png")
    plt.close(fig)


# ── 5) 業績 × 需給 4 象限マトリクス ───────────────────────────────────────────
def make_fund_vs_credit(df: pd.DataFrame) -> None:
    from matplotlib.patches import Rectangle
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    from utils.universe_topix500 import load_topix500

    topix500_codes = set(load_topix500()["コード"].astype(str))
    f = df[df["コード"].astype(str).isin(topix500_codes)].copy()
    f = f.dropna(subset=["業績予想修正率(予)", "信用倍率"])
    f = f[f["信用倍率"] > 0]
    f = f[f["業績予想修正率(予)"].between(-30, 30) & f["信用倍率"].between(0.1, 100)]

    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_yscale("log")
    ax.set_xlim(-30, 30)
    ax.set_ylim(0.1, 100)

    # ── 4 象限を薄い背景色で塗り分け ────────────────────────────────
    # (x0, x1, y0, y1, facecolor, label, label_xy)
    ZONES = [
        (-30, -3, 5, 100,  "#c87878",  "踏み上げ罠",   (-15, 30)),
        (  3, 30, 5, 100,  "#5a9a72",  "踏み上げ候補",  ( 15, 30)),
        (-30, -3, 0.1, 1,  "#aaaaaa",  "空売り正解",   (-15, 0.3)),
        (  3, 30, 0.1, 1,  "#3498db",  "空売り優位",   ( 15, 0.3)),
    ]
    for x0, x1, y0, y1, color, label, (lx, ly) in ZONES:
        rect = Rectangle((x0, y0), x1 - x0, y1 - y0,
                         facecolor=color, alpha=0.10, edgecolor="none", zorder=0)
        ax.add_patch(rect)
        ax.text(lx, ly, label, ha="center", va="center",
                fontsize=15, color="#666666", alpha=0.9, zorder=1)

    # ── ゾーン分類して銘柄をプロット ─────────────────────────────────
    f["zone"] = "中立"
    f.loc[(f["業績予想修正率(予)"] >= 3) & (f["信用倍率"] > 5), "zone"] = "OK_hot"
    f.loc[(f["業績予想修正率(予)"] >= 3) & (f["信用倍率"] <= 1), "zone"] = "OK_short"
    f.loc[(f["業績予想修正率(予)"] <= -3) & (f["信用倍率"] > 5), "zone"] = "NG_trap"
    f.loc[(f["業績予想修正率(予)"] <= -3) & (f["信用倍率"] <= 1), "zone"] = "NG_correct"

    zone_styles = {
        "中立":       ("#999999", 0.25, 10),
        "OK_hot":     ("#5a9a72", 0.80, 38),
        "OK_short":   ("#3498db", 0.80, 38),
        "NG_trap":    ("#c87878", 0.80, 38),
        "NG_correct": ("#aaaaaa", 0.80, 38),
    }
    zone_label = {
        "中立":       "中立",
        "OK_hot":     f"業績OK × 踏み上げ候補 ({(f['zone']=='OK_hot').sum()})",
        "OK_short":   f"業績OK × 空売り優位 ({(f['zone']=='OK_short').sum()})",
        "NG_trap":    f"業績NG × 踏み上げ罠 ({(f['zone']=='NG_trap').sum()})",
        "NG_correct": f"業績NG × 空売り正解 ({(f['zone']=='NG_correct').sum()})",
    }
    for z in ["中立", "OK_short", "NG_correct", "OK_hot", "NG_trap"]:
        sub = f[f["zone"] == z]
        if sub.empty:
            continue
        color, alpha, size = zone_styles[z]
        ax.scatter(sub["業績予想修正率(予)"], sub["信用倍率"],
                   s=size, color=color, alpha=alpha,
                   edgecolors="white" if z != "中立" else "none",
                   linewidth=0.5 if z != "中立" else 0,
                   zorder=3 if z != "中立" else 2,
                   label=zone_label[z])

    # ── 石油元売ハイライト ─────────────────────────────────────────
    for code, label, _ in OIL_REFINERS:
        r = df.loc[df["コード"] == code]
        if r.empty:
            continue
        r = r.iloc[0]
        x, y = r["業績予想修正率(予)"], r["信用倍率"]
        if pd.isna(x) or pd.isna(y):
            continue
        ax.scatter(x, y, s=220, color=C_TEXT, edgecolor="white",
                   linewidth=2.0, zorder=10, marker="*")
        ax.annotate(label, xy=(x, y), xytext=(10, 8),
                    textcoords="offset points",
                    fontsize=16, fontweight="bold", color=C_TEXT,
                    bbox=dict(facecolor="white", alpha=0.92,
                              edgecolor="#aaaaaa", boxstyle="round,pad=0.3"),
                    zorder=11)

    # ── 軸目盛り（カスタム）─────────────────────────────────────────
    y_ticks = [0.1, 0.5, 1, 2, 5, 10, 20, 50, 100]
    ax.yaxis.set_major_locator(FixedLocator(y_ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}倍"))
    ax.yaxis.set_minor_locator(NullLocator())

    x_ticks = [-30, -20, -10, -3, 0, 3, 10, 20, 30]
    ax.xaxis.set_major_locator(FixedLocator(x_ticks))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):+d}%" if v != 0 else "0"))

    ax.set_xlabel("業績予想修正率(予)  ← 業績NG    業績OK →",
                  fontsize=16, color=C_TEXT)
    ax.set_ylabel("信用倍率（対数）  ← 空売り優位    踏み上げ →",
                  fontsize=16, color=C_TEXT)
    ax.set_title("業績 × 需給 4 象限マトリクス  ―  連載01〜04 の業績軸と連載05 の需給軸の合流",
                 fontsize=16, fontweight="bold", color=C_TEXT, pad=12, loc="left")
    ax.grid(color=C_GRID, linewidth=0.4, which="major", zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper left", fontsize=14, frameon=True,
              facecolor="white", edgecolor="#dddddd")
    _savefig_vpad(fig, OUT_DIR / "05_fund_vs_credit.png")
    plt.close(fig)


# ── main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_universe()
    print(f"[load] {len(df):,} 銘柄")

    make_credit_distribution(df)
    print("[ok] 01_credit_distribution.png")
    make_oil_refining_credit(df)
    print("[ok] 02_oil_refining_credit.png")
    make_credit_changes(df)
    print("[ok] 03_credit_changes.png")
    make_credit_vs_volume(df)
    print("[ok] 04_credit_vs_volume.png")
    make_fund_vs_credit(df)
    print("[ok] 05_fund_vs_credit.png")

    print("\n=== 統計 ===")
    f = df[df["時価総額"].fillna(0) >= 10_000].copy()
    print(f"フィルタ後 (時価総額>=100億): {len(f)}")

    s = f["信用倍率"].dropna()
    print(f"信用倍率: 中央値 {s.median():.2f}倍 / >5倍 {(s>5).sum()} / >10倍 {(s>10).sum()} / <=1倍 {(s<=1).sum()}")

    mat = f.dropna(subset=["業績予想修正率(予)", "信用倍率"])
    print(f"\n業績 × 需給 4 象限:")
    print(f"  業績OK × 踏み上げ候補: {((mat['業績予想修正率(予)']>=3) & (mat['信用倍率']>5)).sum()}")
    print(f"  業績OK × 空売り優位:   {((mat['業績予想修正率(予)']>=3) & (mat['信用倍率']<=1)).sum()}")
    print(f"  業績NG × 踏み上げ罠:   {((mat['業績予想修正率(予)']<=-3) & (mat['信用倍率']>5)).sum()}")
    print(f"  業績NG × 空売り正解:   {((mat['業績予想修正率(予)']<=-3) & (mat['信用倍率']<=1)).sum()}")
