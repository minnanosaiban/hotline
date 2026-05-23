"""
blog/03_EPSリビジョンモメンタム.md 用の画像生成スクリプト。

生成画像:
  01_market_revision.png       — 市場別 上方/下方修正銘柄数 + 修正比率
  02_oil_refining_revision.png — 石油元売 3 社のリビジョン × モメンタム
  03_revision_strength.png     — 大幅上方/下方修正 Top10 横棒
  04_revision_vs_momentum.png  — 4 象限散布図（出遅れ買い + 逆行注意）
  05_revision_vs_valuation.png — 4 象限散布図（修正済み割安）

実行: python scripts/blog/03_revision_momentum_make_images.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

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

C_UP    = "#27ae60"  # 緑: 上方修正
C_DOWN  = "#e74c3c"  # 赤: 下方修正
C_WARN  = "#f39c12"  # オレンジ: 逆行注意
C_VAL   = "#2ECC71"  # 明緑: 修正済み割安
C_BG    = "#cccccc"
C_TEXT  = "#202124"
C_TEXT_SUB = "#70757a"
C_GRID  = "#eaeaea"

OUT_DIR = Path(r"C:/Users/mukai/OneDrive/デスクトップ/minnanosaiban/hotline/docs/blog/posts/img/03_revision")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ── データ準備 ─────────────────────────────────────────────────────────────
RAKUNAV_SPECS = [
    (220, "業績予想修正率(予)",         "業績予想修正率(予)"),
    (213, "EPS(予)(一株あたり当期利益)", "EPS予"),
    (118, "ROE(自己資本利益率)",         "ROE"),
    (120, "時価総額(百万円)",            "時価総額"),
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
    merged["PER予"] = merged["Close_yf"] / merged["EPS予"].where(merged["EPS予"] > 0)

    pm = compute_price_metrics(merged["コード"].tolist())
    merged = merged.merge(pm, on="コード", how="left")
    merged = apply_master_names(merged)
    return merged


OIL_REFINERS = [
    ("5021", "コスモエネＨＤ", "#27ae60"),
    ("5020", "ＥＮＥＯＳ",      "#3498db"),
    ("5019", "出光興産",       "#e67e22"),
]


# ── 1) 市場別リビジョン地合い ───────────────────────────────────────────────
def make_market_revision(df: pd.DataFrame) -> None:
    target_markets = ["東P", "東S", "東G"]
    stats = []
    for mk in target_markets:
        s = df[df["市場"] == mk]["業績予想修正率(予)"].dropna()
        s = s[s != 0]
        u = (s > 0).sum()
        d = (s < 0).sum()
        stats.append({"市場": mk, "上方修正": u, "下方修正": d,
                      "比率": u / d if d > 0 else np.nan})
    sdf = pd.DataFrame(stats)

    # 全体
    s_all = df["業績予想修正率(予)"].dropna()
    s_all = s_all[s_all != 0]
    total_u = (s_all > 0).sum()
    total_d = (s_all < 0).sum()
    total_ratio = total_u / total_d

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(12.5, 4.6),
                                     gridspec_kw=dict(width_ratios=[1.4, 1]))

    # 左: 市場別グルーピング棒
    x = np.arange(len(sdf))
    w = 0.36
    ax_l.bar(x - w/2, sdf["上方修正"], width=w, color=C_UP, label="上方修正")
    ax_l.bar(x + w/2, sdf["下方修正"], width=w, color=C_DOWN, label="下方修正")
    for i, row in sdf.iterrows():
        ax_l.text(i - w/2, row["上方修正"] + 4, f"{int(row['上方修正'])}",
                  ha="center", va="bottom", fontsize=12.6, color=C_UP, fontweight="bold")
        ax_l.text(i + w/2, row["下方修正"] + 4, f"{int(row['下方修正'])}",
                  ha="center", va="bottom", fontsize=12.6, color=C_DOWN, fontweight="bold")
    ax_l.set_xticks(x)
    ax_l.set_xticklabels(sdf["市場"], fontsize=15.4, color=C_TEXT)
    ax_l.set_title("市場別 上方/下方修正 銘柄数",
                   fontsize=16.8, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_l.legend(loc="upper right", fontsize=12.6, frameon=False)
    ax_l.grid(axis="y", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)
    ax_l.set_ylim(0, max(sdf["上方修正"].max(), sdf["下方修正"].max()) * 1.18)

    # 右: 修正比率テーブル風 + 全体
    ax_r.axis("off")
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 1)
    ax_r.text(0.0, 0.95, "修正比率（上方 ÷ 下方）", fontsize=16.8,
              fontweight="bold", color=C_TEXT, va="top")

    rows = [("全市場", total_u, total_d, total_ratio)] + [
        (r["市場"], int(r["上方修正"]), int(r["下方修正"]), r["比率"])
        for _, r in sdf.iterrows()
    ]
    y0 = 0.78
    for i, (mk, u, d, ratio) in enumerate(rows):
        y = y0 - i * 0.16
        color = C_UP if ratio >= 1.5 else (C_DOWN if ratio < 0.8 else "#888888")
        label = "強気" if ratio >= 1.5 else "中立" if ratio >= 0.8 else "弱気"
        ax_r.text(0.0, y, mk, fontsize=15.4, fontweight="bold", color=C_TEXT)
        ax_r.text(0.32, y, f"{u}/{d}", fontsize=14, color=C_TEXT_SUB)
        ax_r.text(0.62, y, f"{ratio:.2f}", fontsize=19.6, fontweight="bold", color=color)
        ax_r.text(0.84, y, label, fontsize=14, color=color)

    ax_r.text(0.0, 0.02,
              "判定: ≥1.5 強気 / 0.8〜1.5 中立 / <0.8 弱気",
              fontsize=11.9, color=C_TEXT_SUB, va="bottom")

    fig.suptitle(f"市場全体のリビジョン地合い  ―  対象 {len(df):,} 銘柄",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "01_market_revision.png")
    plt.close(fig)


# ── 2) 石油元売 3 社のリビジョン ───────────────────────────────────────────
def make_oil_refining_revision(df: pd.DataFrame) -> None:
    """3 社の修正率と値上り率を横並びで比較。連載01/02 からの流れを意識。"""
    fig, ax = plt.subplots(figsize=(11.5, 5.5))

    labels = []
    rev_vals = []
    rise_vals = []
    colors = []
    per_vals = []
    for code, label, color in OIL_REFINERS:
        r = df.loc[df["コード"] == code]
        if r.empty:
            continue
        r = r.iloc[0]
        labels.append(label)
        rev_vals.append(r["業績予想修正率(予)"])
        rise_vals.append(r["値上り率"])
        colors.append(color)
        per_vals.append(r["PER予"])

    n = len(labels)
    y = np.arange(n)
    h = 0.36

    ax.barh(y - h/2, rev_vals, height=h,
            color=[C_DOWN if v < 0 else C_UP for v in rev_vals],
            alpha=0.85, edgecolor="white", linewidth=0.8, label="業績予想修正率(予)")
    ax.barh(y + h/2, rise_vals, height=h,
            color="#5b8def", alpha=0.7, edgecolor="white", linewidth=0.8,
            label="値上り率（日次%）")

    for i, (rv, rs) in enumerate(zip(rev_vals, rise_vals)):
        ax.text(rv + (0.15 if rv >= 0 else -0.15), i - h/2,
                f"{rv:+.2f}%", va="center",
                ha="left" if rv >= 0 else "right",
                fontsize=14, fontweight="bold",
                color=C_DOWN if rv < 0 else C_UP)
        ax.text(rs + (0.15 if rs >= 0 else -0.15), i + h/2,
                f"{rs:+.2f}%", va="center",
                ha="left" if rs >= 0 else "right",
                fontsize=14, color="#3358aa")

    ax.axvline(0, color="#999999", linewidth=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([
        f"{lab}\n(PER予 {p:.1f})" for lab, p in zip(labels, per_vals)
    ], fontsize=15.4, color=C_TEXT)
    ax.invert_yaxis()
    ax.set_xlim(-5.5, 5.5)
    ax.set_xlabel("%（左:下方修正/下落, 右:上方修正/上昇）",
                  fontsize=14, color=C_TEXT_SUB)
    ax.legend(loc="lower right", fontsize=13.3, frameon=False)
    ax.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("石油元売 3 社  ―  業績予想修正率 vs 値上り率",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "02_oil_refining_revision.png")
    plt.close(fig)


# ── 3) リビジョン強度ランキング ────────────────────────────────────────────
def make_revision_strength(df: pd.DataFrame) -> None:
    """大幅上方/下方修正 Top10 を横棒で並べる。極端な異常値（-90%等）も注釈"""
    f = df.copy()
    # 流動性フィルタ
    f = f[f["時価総額"].fillna(0) >= 10_000]

    top_up = f[f["業績予想修正率(予)"] > 0].nlargest(10, "業績予想修正率(予)").iloc[::-1]
    top_dn = f[f["業績予想修正率(予)"] < 0].nsmallest(10, "業績予想修正率(予)").iloc[::-1]

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 6),
                                     gridspec_kw=dict(wspace=0.45))

    # 上方
    y = np.arange(len(top_up))
    ax_l.barh(y, top_up["業績予想修正率(予)"], color=C_UP, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, (_, r) in enumerate(top_up.iterrows()):
        ax_l.text(r["業績予想修正率(予)"] + 0.4, i,
                  f"+{r['業績予想修正率(予)']:.1f}%",
                  va="center", fontsize=11.9, color=C_UP, fontweight="bold")
    ax_l.set_yticks(y)
    ax_l.set_yticklabels([f"{r['コード']} {r['銘柄名']}"
                          for _, r in top_up.iterrows()],
                         fontsize=12.6, color=C_TEXT)
    ax_l.set_xlabel("業績予想修正率(予)（%）", fontsize=13.3, color=C_TEXT_SUB)
    ax_l.set_xlim(0, top_up["業績予想修正率(予)"].max() * 1.15)
    ax_l.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)
    ax_l.set_title("大幅上方修正 Top10", fontsize=16.8, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")

    # 下方
    y = np.arange(len(top_dn))
    ax_r.barh(y, top_dn["業績予想修正率(予)"], color=C_DOWN, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, (_, r) in enumerate(top_dn.iterrows()):
        ax_r.text(r["業績予想修正率(予)"] - 0.4, i,
                  f"{r['業績予想修正率(予)']:.1f}%",
                  va="center", ha="right",
                  fontsize=11.9, color=C_DOWN, fontweight="bold")
    ax_r.set_yticks(y)
    ax_r.set_yticklabels([f"{r['コード']} {r['銘柄名']}"
                          for _, r in top_dn.iterrows()],
                         fontsize=12.6, color=C_TEXT)
    ax_r.set_xlabel("業績予想修正率(予)（%）", fontsize=13.3, color=C_TEXT_SUB)
    ax_r.set_xlim(top_dn["業績予想修正率(予)"].min() * 1.15, 0)
    ax_r.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)
    ax_r.set_title("大幅下方修正 Top10", fontsize=16.8, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")

    fig.suptitle("リビジョン強度ランキング  ―  時価総額 100 億円以上",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=1.00)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "03_revision_strength.png")
    plt.close(fig)


# ── 4) リビジョン × モメンタム 散布図 ────────────────────────────────────────
def make_revision_vs_momentum(df: pd.DataFrame) -> None:
    f = df.copy()
    f = f[f["時価総額"].fillna(0) >= 10_000]
    f = f[f["ROE"].fillna(-99) >= 5]
    f = f.dropna(subset=["業績予想修正率(予)", "値上り率"])
    f = f[f["業績予想修正率(予)"].between(-30, 30) & f["値上り率"].between(-15, 15)]

    fig, ax = plt.subplots(figsize=(12, 7.5))

    # ゾーン背景
    ax.axhspan(-15, 2, xmin=(3 - (-30)) / 60, xmax=1.0,
               facecolor=C_DOWN, alpha=0.04)  # 出遅れ買い候補（右下）
    ax.axhspan(2, 15, xmin=0.0, xmax=(-3 - (-30)) / 60,
               facecolor=C_WARN, alpha=0.05)  # 逆行注意（左上）

    # 背景銘柄
    bg = f[~((f["業績予想修正率(予)"] >= 3) & (f["値上り率"] <= 2))]
    bg = bg[~((bg["業績予想修正率(予)"] <= -3) & (bg["値上り率"] >= 2))]
    ax.scatter(bg["業績予想修正率(予)"], bg["値上り率"],
               s=14, color=C_BG, alpha=0.30, edgecolors="none", zorder=1)

    # 出遅れ買い候補
    lag = f[(f["業績予想修正率(予)"] >= 3) & (f["値上り率"] <= 2)]
    ax.scatter(lag["業績予想修正率(予)"], lag["値上り率"],
               s=44, color=C_DOWN, alpha=0.75, edgecolors="white", linewidth=0.6,
               zorder=4, label=f"出遅れ買い候補 ({len(lag)})")

    # 逆行注意
    warn = f[(f["業績予想修正率(予)"] <= -3) & (f["値上り率"] >= 2)]
    ax.scatter(warn["業績予想修正率(予)"], warn["値上り率"],
               s=44, color=C_WARN, alpha=0.85, edgecolors="white", linewidth=0.6,
               zorder=4, label=f"逆行注意 ({len(warn)})")

    # 石油元売 3 社ハイライト
    for code, label, _ in OIL_REFINERS:
        r = df.loc[df["コード"] == code]
        if r.empty:
            continue
        r = r.iloc[0]
        x, y = r["業績予想修正率(予)"], r["値上り率"]
        ax.scatter(x, y, s=180, color="#1F4E8C", edgecolor="white",
                   linewidth=2.0, zorder=8, marker="*")
        ax.annotate(label, xy=(x, y), xytext=(10, 8),
                    textcoords="offset points",
                    fontsize=14.7, fontweight="bold", color="#1F4E8C",
                    bbox=dict(facecolor="white", alpha=0.92,
                              edgecolor="#1F4E8C", boxstyle="round,pad=0.3"),
                    zorder=9)

    # 基準線
    ax.axhline(0, color="#777777", linewidth=0.8)
    ax.axvline(0, color="#777777", linewidth=0.8)
    ax.axhline(2, color=C_DOWN, linestyle="--", linewidth=0.7, alpha=0.5)
    ax.axvline(3, color=C_DOWN, linestyle="--", linewidth=0.7, alpha=0.5)
    ax.axvline(-3, color=C_WARN, linestyle="--", linewidth=0.7, alpha=0.5)
    ax.axhline(-15, color="#cccccc", linewidth=0.4)

    # ゾーンラベル
    ax.text(20, -10, "★出遅れ買い候補★\n上方修正 × 株価未反応",
            fontsize=14.7, fontweight="bold", color=C_DOWN, ha="center", va="center")
    ax.text(-20, 10, "逆行注意\n下方修正 × 株価上昇",
            fontsize=14.7, color=C_WARN, ha="center", va="center")
    ax.text(20, 10, "既反応 / 利食い検討", fontsize=12.6, color=C_TEXT_SUB,
            ha="center", va="center")
    ax.text(-20, -10, "底入れ待ち\n下方修正 × 株価下落", fontsize=12.6,
            color=C_TEXT_SUB, ha="center", va="center")

    ax.set_xlim(-30, 30)
    ax.set_ylim(-15, 15)
    ax.set_xlabel("業績予想修正率(予)（%）  ← 下方修正    上方修正 →",
                  fontsize=19.6, color=C_TEXT)
    ax.set_ylabel("値上り率（%）  ← 株価下落    株価上昇 →",
                  fontsize=19.6, color=C_TEXT)
    ax.set_title("リビジョン × 株価モメンタム  ―  4 象限の戦略マップ",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=12, loc="left")
    ax.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="lower right", fontsize=14, frameon=True,
              facecolor="white", edgecolor="#dddddd")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "04_revision_vs_momentum.png")
    plt.close(fig)


# ── 5) リビジョン × バリュエーション 散布図 ──────────────────────────────────
def make_revision_vs_valuation(df: pd.DataFrame) -> None:
    f = df.copy()
    f = f[f["時価総額"].fillna(0) >= 10_000]
    f = f[f["ROE"].fillna(-99) >= 5]
    f = f.dropna(subset=["業績予想修正率(予)", "PER予"])
    f = f[f["業績予想修正率(予)"].between(-30, 30) & f["PER予"].between(0, 40)]

    fig, ax = plt.subplots(figsize=(12, 7.5))

    # ゾーン背景
    ax.axhspan(0, 15, xmin=(3 - (-30)) / 60, xmax=1.0,
               facecolor=C_VAL, alpha=0.07)  # 修正済み割安

    # 背景銘柄
    cand = f[(f["業績予想修正率(予)"] >= 3) & (f["PER予"] <= 15)]
    bg = f.drop(cand.index, errors="ignore")
    ax.scatter(bg["業績予想修正率(予)"], bg["PER予"],
               s=14, color=C_BG, alpha=0.30, edgecolors="none", zorder=1)

    # 修正済み割安候補
    ax.scatter(cand["業績予想修正率(予)"], cand["PER予"],
               s=46, color=C_VAL, alpha=0.85, edgecolors="white", linewidth=0.6,
               zorder=4, label=f"修正済み割安候補 ({len(cand)})")

    # 石油元売 3 社ハイライト
    for code, label, _ in OIL_REFINERS:
        r = df.loc[df["コード"] == code]
        if r.empty:
            continue
        r = r.iloc[0]
        if pd.isna(r["PER予"]):
            continue
        x, y = r["業績予想修正率(予)"], r["PER予"]
        ax.scatter(x, y, s=180, color="#1F4E8C", edgecolor="white",
                   linewidth=2.0, zorder=8, marker="*")
        ax.annotate(label, xy=(x, y), xytext=(10, -10),
                    textcoords="offset points",
                    fontsize=14.7, fontweight="bold", color="#1F4E8C",
                    bbox=dict(facecolor="white", alpha=0.92,
                              edgecolor="#1F4E8C", boxstyle="round,pad=0.3"),
                    zorder=9)

    # 基準線
    ax.axvline(3, color=C_VAL, linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axhline(15, color=C_VAL, linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axvline(0, color="#999999", linewidth=0.8)

    ax.text(20, 7, "★修正済み割安★\n上方修正 × 低PER",
            fontsize=15.4, fontweight="bold", color=C_VAL, ha="center", va="center")
    ax.text(-20, 25, "下方修正 × 割高", fontsize=12.6, color=C_TEXT_SUB,
            ha="center", va="center")
    ax.text(20, 25, "上方修正だが割高グロース", fontsize=12.6, color=C_TEXT_SUB,
            ha="center", va="center")

    ax.set_xlim(-30, 30)
    ax.set_ylim(0, 40)
    ax.set_xlabel("業績予想修正率(予)（%）  ← 下方修正    上方修正 →",
                  fontsize=19.6, color=C_TEXT)
    ax.set_ylabel("PER（予）  ← 割安    割高 →", fontsize=19.6, color=C_TEXT)
    ax.set_title("リビジョン × バリュエーション  ―  修正済み割安銘柄の発掘",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=12, loc="left")
    ax.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper right", fontsize=14, frameon=True,
              facecolor="white", edgecolor="#dddddd")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "05_revision_vs_valuation.png")
    plt.close(fig)


# ── main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_universe()
    print(f"[load] {len(df):,} 銘柄")

    make_market_revision(df)
    print("[ok] 01_market_revision.png")
    make_oil_refining_revision(df)
    print("[ok] 02_oil_refining_revision.png")
    make_revision_strength(df)
    print("[ok] 03_revision_strength.png")
    make_revision_vs_momentum(df)
    print("[ok] 04_revision_vs_momentum.png")
    make_revision_vs_valuation(df)
    print("[ok] 05_revision_vs_valuation.png")

    # 統計値
    s = df["業績予想修正率(予)"].dropna()
    s = s[s != 0]
    print(f"\n=== 統計 ===")
    print(f"上方修正: {(s>0).sum()} 銘柄")
    print(f"下方修正: {(s<0).sum()} 銘柄")
    print(f"修正比率: {(s>0).sum() / (s<0).sum():.2f}")

    f = df[(df["時価総額"].fillna(0) >= 10_000) & (df["ROE"].fillna(-99) >= 5)]
    lag = f[(f["業績予想修正率(予)"] >= 3) & (f["値上り率"] <= 2)]
    warn = f[(f["業績予想修正率(予)"] <= -3) & (f["値上り率"] >= 2)]
    val = f[(f["業績予想修正率(予)"] >= 3) & (f["PER予"].between(0, 15))]
    print(f"\nフィルタ後: {len(f)} 銘柄")
    print(f"出遅れ買い候補（修正>=3 & 値上り<=2）: {len(lag)}")
    print(f"逆行注意（修正<=-3 & 値上り>=2）: {len(warn)}")
    print(f"修正済み割安（修正>=3 & PER<=15）: {len(val)}")
