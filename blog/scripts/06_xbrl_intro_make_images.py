"""
blog/06_XBRLとは何か.md 用の画像生成スクリプト。

生成画像:
  01_oil_3companies_revenue_oi.png  — 石油元売 3 社の売上 / 営業利益 7 年推移
  02_oil_3companies_ni_roe.png      — 3 社の純利益 / ROE 7 年推移
  03_oil_3companies_cf.png          — 3 社の CF 3 種（営業/投資/財務）7 年推移
  04_data_depth_comparison.png      — 既存スクリーナー vs XBRL データ深度比較
  05_eneos_peakout.png              — ＥＮＥＯＳ 単独の 2022 ピークアウト構図

実行: python scripts/blog/06_xbrl_intro_make_images.py
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle


# ── デザイン設定 ────────────────────────────────────────────────────────────
mpl.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans JP"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["savefig.facecolor"] = "white"
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["savefig.dpi"] = 144

C_TEXT = "#202124"
C_TEXT_SUB = "#70757a"
C_GRID = "#eaeaea"

OUT_DIR = Path(r"C:/Users/mukai/OneDrive/デスクトップ/minnanosaiban/hotline/docs/blog/posts/img/06_xbrl")
OUT_DIR.mkdir(parents=True, exist_ok=True)

YUHO = Path(r"C:/stock_analysis/data/yuho")

OIL_3 = [
    ("E31632", "コスモエネＨＤ", "#27ae60"),
    ("E24050", "ＥＮＥＯＳ",      "#3498db"),
    ("E01084", "出光興産",       "#e67e22"),
]


def load_oil_series() -> pd.DataFrame:
    rows = []
    for ed, name, color in OIL_3:
        for f in sorted((YUHO / ed).glob("*.json")):
            with open(f, encoding="utf-8") as fp:
                d = json.load(fp)
            fy = d.get("metadata", {}).get("fiscal_year_end", "")
            fin = d.get("financials", {}) or {}
            rows.append({
                "name": name, "color": color,
                "fy": fy[:4],
                "net_sales": fin.get("net_sales"),
                "operating_income": fin.get("operating_income"),
                "net_income": fin.get("net_income"),
                "roe": fin.get("roe"),
                "eps": fin.get("eps"),
                "op_cf": fin.get("operating_cf"),
                "inv_cf": fin.get("investing_cf"),
                "fin_cf": fin.get("financing_cf"),
            })
    return pd.DataFrame(rows)


# ── 1) 売上 / 営業利益 7 年 ────────────────────────────────────────────────
def make_revenue_oi(df: pd.DataFrame) -> None:
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 5),
                                     gridspec_kw=dict(wspace=0.28))

    for name, color in [(n, c) for _, n, c in OIL_3]:
        sub = df[df["name"] == name].sort_values("fy")
        ax_l.plot(sub["fy"], sub["net_sales"] / 1e12,
                  marker="o", markersize=7, linewidth=2.2,
                  color=color, label=name)

    ax_l.set_xlabel("会計年度", fontsize=14, color=C_TEXT_SUB)
    ax_l.set_ylabel("売上高（兆円）", fontsize=15.4, color=C_TEXT)
    ax_l.set_title("売上高 7 年推移", fontsize=16.8, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")
    ax_l.legend(loc="best", fontsize=14, frameon=False)
    ax_l.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)

    # 営業利益: 2024-2025 のみ有効データ
    sub_op = df[df["operating_income"].notna()].copy()
    for name, color in [(n, c) for _, n, c in OIL_3]:
        s = sub_op[sub_op["name"] == name].sort_values("fy")
        if s.empty:
            continue
        ax_r.plot(s["fy"], s["operating_income"] / 1e11,
                  marker="s", markersize=8, linewidth=2.2,
                  color=color, label=name)

    ax_r.set_xlabel("会計年度", fontsize=14, color=C_TEXT_SUB)
    ax_r.set_ylabel("営業利益（千億円）", fontsize=15.4, color=C_TEXT)
    ax_r.set_title("営業利益 (パース対応分)", fontsize=16.8, fontweight="bold",
                   color=C_TEXT, pad=10, loc="left")
    ax_r.legend(loc="best", fontsize=14, frameon=False)
    ax_r.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)
    ax_r.text(0.02, 0.04, "※ 2019-2023 は本パーサが営業利益を抽出できなかった範囲",
              transform=ax_r.transAxes, fontsize=11.2, color=C_TEXT_SUB,
              ha="left", va="bottom", style="italic")

    fig.suptitle("石油元売 3 社  ―  有報 XBRL からの 7 年時系列",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "01_oil_3companies_revenue_oi.png")
    plt.close(fig)


# ── 2) 純利益 / ROE 7 年 ──────────────────────────────────────────────────
def make_ni_roe(df: pd.DataFrame) -> None:
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 5),
                                     gridspec_kw=dict(wspace=0.28))

    for _, name, color in OIL_3:
        sub = df[df["name"] == name].sort_values("fy")
        ax_l.plot(sub["fy"], sub["net_income"] / 1e11,
                  marker="o", markersize=7, linewidth=2.2,
                  color=color, label=name)

    ax_l.axhline(0, color="#999999", linewidth=0.8)
    ax_l.set_xlabel("会計年度", fontsize=14, color=C_TEXT_SUB)
    ax_l.set_ylabel("純利益（千億円）", fontsize=15.4, color=C_TEXT)
    ax_l.set_title("純利益 7 年推移  ―  2022 ピーク、2025 半減",
                   fontsize=16.8, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_l.legend(loc="best", fontsize=14, frameon=False)
    ax_l.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)

    # ピークの注釈（社別に位置を変えて重なり回避）
    annotate_offsets = {
        "ＥＮＥＯＳ":      (-0.7,  1.2, "right"),
        "出光興産":        (0.7,  -1.0, "left"),
        "コスモエネＨＤ":  (0.6,   0.6, "left"),
    }
    for _, name, color in OIL_3:
        sub = df[df["name"] == name].sort_values("fy")
        if sub.empty:
            continue
        peak_idx = sub["net_income"].idxmax()
        peak_row = sub.loc[peak_idx]
        x_pos = peak_row["fy"]
        y_pos = peak_row["net_income"] / 1e11
        ax_l.scatter(x_pos, y_pos, s=120, edgecolor=color, facecolor="white",
                     linewidth=2.5, zorder=5)
        dx, dy, ha = annotate_offsets.get(name, (0, 0.5, "center"))
        ax_l.annotate(
            f"{name} ピーク\n{peak_row['net_income']/1e11:.1f}千億",
            xy=(x_pos, y_pos), xytext=(dx, dy), textcoords="offset fontsize",
            fontsize=11.2, color=color, ha=ha, va="center", fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=color, lw=0.8, alpha=0.6),
        )

    # ROE
    for _, name, color in OIL_3:
        sub = df[df["name"] == name].sort_values("fy")
        roe_pct = sub["roe"] * 100
        ax_r.plot(sub["fy"], roe_pct,
                  marker="o", markersize=7, linewidth=2.2,
                  color=color, label=name)

    ax_r.axhline(0, color="#999999", linewidth=0.8)
    ax_r.axhline(10, color="#27ae60", linestyle=":", linewidth=0.7, alpha=0.6,
                 label="ROE 10% (優良ライン)")
    ax_r.set_xlabel("会計年度", fontsize=14, color=C_TEXT_SUB)
    ax_r.set_ylabel("ROE（%）", fontsize=15.4, color=C_TEXT)
    ax_r.set_title("ROE 7 年推移  ―  資本効率の長期トレンド",
                   fontsize=16.8, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_r.legend(loc="best", fontsize=12.6, frameon=False)
    ax_r.grid(color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)

    fig.suptitle("石油元売 3 社  ―  2022 利益ピークと直近のピークアウト構図",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "02_oil_3companies_ni_roe.png")
    plt.close(fig)


# ── 3) CF 3 種 7 年 ──────────────────────────────────────────────────────
def make_cf(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5),
                             gridspec_kw=dict(wspace=0.3))

    for ax, (_, name, color) in zip(axes, OIL_3):
        sub = df[df["name"] == name].sort_values("fy")
        x = sub["fy"].values
        op = sub["op_cf"].values / 1e11
        inv = sub["inv_cf"].values / 1e11
        fin = sub["fin_cf"].values / 1e11

        bw = 0.27
        idx = np.arange(len(x))
        ax.bar(idx - bw, op, width=bw, color="#27ae60", alpha=0.85,
               edgecolor="white", linewidth=0.8, label="営業CF")
        ax.bar(idx,      inv, width=bw, color="#e74c3c", alpha=0.85,
               edgecolor="white", linewidth=0.8, label="投資CF")
        ax.bar(idx + bw, fin, width=bw, color="#3498db", alpha=0.85,
               edgecolor="white", linewidth=0.8, label="財務CF")

        ax.axhline(0, color="#444444", linewidth=0.8)
        ax.set_xticks(idx)
        ax.set_xticklabels(x, fontsize=12.6)
        ax.set_ylabel("CF（千億円）" if ax is axes[0] else "",
                      fontsize=14, color=C_TEXT_SUB)
        ax.set_title(f"{name}", fontsize=16.1, fontweight="bold",
                     color=color, pad=10)
        ax.grid(axis="y", color=C_GRID, linewidth=0.5)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        if ax is axes[0]:
            ax.legend(loc="best", fontsize=12.6, frameon=False)

    fig.suptitle("キャッシュフロー 3 種の 7 年推移  ―  投資フェーズの可視化",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "03_oil_3companies_cf.png")
    plt.close(fig)


# ── 4) データ深度比較 ──────────────────────────────────────────────────────
def make_data_depth() -> None:
    """既存スクリーナー vs XBRL のデータ深度を視覚化（カバレッジテーブル風）"""
    categories = [
        ("ROE / PER / PBR", [1, 1, 1, 1]),
        ("EPS / 配当 / 売上", [1, 1, 1, 1]),
        ("業績予想修正率", [1, 0, 1, 1]),
        ("信用残・出来高", [1, 0, 0, 1]),
        ("セグメント別売上・利益", [0, 0.4, 0, 1]),
        ("地域別売上", [0, 0.4, 0, 1]),
        ("減価償却・設備投資", [0, 0.6, 0, 1]),
        ("運転資本（売掛・在庫）", [0, 0.6, 0, 1]),
        ("キャッシュフロー詳細", [0, 0.6, 0, 1]),
        ("注記・会計方針変更", [0, 0, 0, 1]),
        ("経営方針テキスト", [0, 0, 0, 1]),
        ("過去 7 年超の時系列", [0, 0.6, 0.6, 1]),
    ]
    sources = ["証券会社系\n（市販A）", "無料Web系\n（市販B）", "有料Web系\n（市販C）", "自前 XBRL\n→ JSON"]

    arr = np.array([row[1] for row in categories])
    labels = [row[0] for row in categories]

    fig, ax = plt.subplots(figsize=(11, 7))

    cmap = plt.get_cmap("RdYlGn")
    for i, lab in enumerate(labels):
        for j, src in enumerate(sources):
            v = arr[i, j]
            color = cmap(np.clip(v * 0.85 + 0.1, 0.05, 0.95))
            rect = Rectangle((j, len(labels) - i - 1), 1, 1,
                             facecolor=color, edgecolor="white", linewidth=1.5)
            ax.add_patch(rect)
            if v == 0:
                txt = "—"; tc = "#777777"
            elif v < 0.5:
                txt = "△"; tc = "#404040"
            elif v < 0.8:
                txt = "△+"; tc = "#404040"
            else:
                txt = "✓"; tc = "white"
            ax.text(j + 0.5, len(labels) - i - 0.5, txt,
                    fontsize=19.6, ha="center", va="center",
                    color=tc, fontweight="bold")

    ax.set_xlim(0, len(sources))
    ax.set_ylim(0, len(labels))
    ax.set_xticks(np.arange(len(sources)) + 0.5)
    ax.set_xticklabels(sources, fontsize=14.7, color=C_TEXT)
    ax.set_yticks(np.arange(len(labels)) + 0.5)
    ax.set_yticklabels(labels[::-1], fontsize=14, color=C_TEXT)
    ax.tick_params(length=0)
    ax.xaxis.tick_top()
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(False)

    ax.set_title("データ深度比較  ―  既存サービスと自前 XBRL の到達範囲",
                 fontsize=18.2, fontweight="bold", color=C_TEXT,
                 pad=42, loc="left")

    fig.text(0.5, -0.02,
             "✓ 完全提供  /  △+ 部分提供  /  △ 限定的  /  — 提供なし",
             fontsize=13.3, color=C_TEXT_SUB, ha="center")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "04_data_depth_comparison.png")
    plt.close(fig)


# ── 5) ＥＮＥＯＳ 単独の 2022 ピークアウト ──────────────────────────────────
def make_eneos_peakout(df: pd.DataFrame) -> None:
    sub = df[df["name"] == "ＥＮＥＯＳ"].sort_values("fy").reset_index(drop=True)

    fig, ax_ni = plt.subplots(figsize=(11.5, 5.5))
    ax_roe = ax_ni.twinx()

    x = sub["fy"]
    ni = sub["net_income"] / 1e11
    roe = sub["roe"] * 100

    # 純利益（バー）
    colors = ["#e74c3c" if v < 0 else "#3498db" for v in ni]
    bars = ax_ni.bar(x, ni, color=colors, alpha=0.7,
                     edgecolor="white", linewidth=1.0,
                     label="純利益（千億円、左軸）")
    for xi, v in zip(x, ni):
        ax_ni.text(xi, v + (0.2 if v >= 0 else -0.4), f"{v:.1f}",
                   ha="center", va="bottom" if v >= 0 else "top",
                   fontsize=13.3, fontweight="bold",
                   color="#3498db" if v >= 0 else "#e74c3c")

    # ROE（ライン）
    ax_roe.plot(x, roe, marker="o", markersize=8, linewidth=2.5,
                color="#9b59b6", label="ROE（%、右軸）")
    for xi, v in zip(x, roe):
        ax_roe.text(xi, v + 0.6, f"{v:.1f}%",
                    ha="center", va="bottom",
                    fontsize=12.6, color="#9b59b6", fontweight="bold")

    # ピーク注釈
    peak_idx = sub["net_income"].idxmax()
    peak_row = sub.iloc[peak_idx]
    ax_ni.annotate(
        f"2022 ピーク\n純利益 5,371 億円 / ROE 20.7%",
        xy=(peak_row["fy"], peak_row["net_income"] / 1e11),
        xytext=(2, 4.5), textcoords="data",
        fontsize=14, color="#E74C3C", fontweight="bold",
        ha="center",
        arrowprops=dict(arrowstyle="->", color="#E74C3C", lw=1.5),
    )

    ax_ni.axhline(0, color="#999999", linewidth=0.8)
    ax_ni.set_ylabel("純利益（千億円）", fontsize=15.4, color="#3498db")
    ax_roe.set_ylabel("ROE（%）", fontsize=15.4, color="#9b59b6")
    ax_ni.set_xlabel("会計年度", fontsize=14, color=C_TEXT_SUB)
    ax_ni.set_ylim(-3.5, 7.5)
    ax_roe.set_ylim(-12, 25)
    ax_ni.tick_params(axis="y", colors="#3498db")
    ax_roe.tick_params(axis="y", colors="#9b59b6")
    ax_ni.grid(axis="y", color=C_GRID, linewidth=0.5)
    for sp in ("top",):
        ax_ni.spines[sp].set_visible(False)
        ax_roe.spines[sp].set_visible(False)

    ax_ni.set_title("ＥＮＥＯＳ  ―  2022 ピークから 2025 へのピークアウト構図",
                    fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left")

    ax_ni.legend(loc="upper left", fontsize=14, frameon=False)
    ax_roe.legend(loc="upper right", fontsize=14, frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "05_eneos_peakout.png")
    plt.close(fig)


# ── main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_oil_series()
    print(f"[load] {len(df)} 行（{df['name'].nunique()} 社 × 7 期）")

    make_revenue_oi(df)
    print("[ok] 01_oil_3companies_revenue_oi.png")
    make_ni_roe(df)
    print("[ok] 02_oil_3companies_ni_roe.png")
    make_cf(df)
    print("[ok] 03_oil_3companies_cf.png")
    make_data_depth()
    print("[ok] 04_data_depth_comparison.png")
    make_eneos_peakout(df)
    print("[ok] 05_eneos_peakout.png")

    print("\n=== ＥＮＥＯＳ 7 年 純利益・ROE ===")
    sub = df[df["name"] == "ＥＮＥＯＳ"].sort_values("fy")
    for _, r in sub.iterrows():
        print(f"  {r['fy']}: 純利={r['net_income']/1e8:,.0f}億 / ROE={r['roe']*100:.1f}%")
