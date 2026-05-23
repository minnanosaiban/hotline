"""
blog/08_決算短信JSONスキーマ設計.md 用の画像生成スクリプト。

生成画像:
  01_section_distribution.png       — セクション別ルール数（performance 圧倒の構図）
  02_standard_category_heatmap.png  — 会計基準 × カテゴリ のヒートマップ
  03_net_sales_multi_tags.png       — net_sales 系 json_path × xbrl_tag の 1:N 構造
  04_field_coverage.png             — 実データのフィールドカバレッジ
  05_schema_principles.png          — スキーマ設計 5 原則のサマリカード

実行: python scripts/blog/08_schema_make_images.py
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
from matplotlib.patches import FancyBboxPatch, Rectangle


# ── デザイン設定 ────────────────────────────────────────────────────────────
mpl.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans JP"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["savefig.facecolor"] = "white"
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["savefig.dpi"] = 144

C_PERF = "#3498db"
C_BS   = "#27ae60"
C_DIV  = "#9b59b6"
C_META = "#7f8c8d"
C_TEXT = "#202124"
C_TEXT_SUB = "#70757a"
C_GRID = "#eaeaea"

OUT_DIR = Path(r"C:/Users/mukai/OneDrive/デスクトップ/minnanosaiban/hotline/docs/blog/posts/img/08_schema")
OUT_DIR.mkdir(parents=True, exist_ok=True)

STOCK = Path(r"C:/stock_analysis")


# ── 1) セクション別ルール分布 ─────────────────────────────────────────────────
def make_section_distribution() -> None:
    km = pd.read_csv(STOCK / "collectors/kessan_mapping.csv")
    km["section"] = km["json_path"].str.split(".").str[0]
    counts = km["section"].value_counts()

    # カテゴリラベル日本語化
    label_map = {
        "performance": "performance\n（業績）",
        "dividend": "dividend\n（配当）",
        "balance_sheet": "balance_sheet\n（貸借）",
        "notes": "notes\n（注記）",
        "accounting_changes": "accounting_changes\n（会計方針変更）",
        "metadata": "metadata\n（メタ）",
        "shares": "shares\n（株式）",
        "consolidation_changes": "consolidation_changes\n（連結範囲変更）",
        "corrections": "corrections\n（訂正）",
        "audit": "audit\n（監査）",
    }
    labels = [label_map.get(s, s) for s in counts.index]

    fig, ax = plt.subplots(figsize=(13, 6))
    colors = [C_PERF if "performance" in s else
              C_BS if "balance" in s else
              C_DIV if "dividend" in s else
              C_META for s in counts.index]

    y = np.arange(len(counts))
    ax.barh(y, counts.values, color=colors, alpha=0.85,
            edgecolor="white", linewidth=0.8)
    for i, v in enumerate(counts.values):
        ax.text(v + 2, i, f"{v}（{v/len(km)*100:.0f}%）",
                va="center", fontsize=14, fontweight="bold", color=C_TEXT)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=14)
    ax.invert_yaxis()
    ax.set_xlabel("ルール数", fontsize=14.7, color=C_TEXT_SUB)
    ax.set_xlim(0, max(counts.values) * 1.18)
    ax.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    ax.set_title(f"kessan_mapping.csv  ―  セクション別ルール分布（全 {len(km)} ルール）",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left")

    # 注釈
    fig.text(0.95, -0.02,
             "performance が 70% を占める = 業績データへの集中投資が設計の意図",
             fontsize=13.3, color=C_TEXT_SUB, ha="right", style="italic")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "01_section_distribution.png")
    plt.close(fig)


# ── 2) 会計基準 × カテゴリ ヒートマップ ───────────────────────────────────────
def make_standard_category_heatmap() -> None:
    km = pd.read_csv(STOCK / "collectors/kessan_mapping.csv")
    cross = pd.crosstab(km["category"], km["accounting_standard"])
    # 列順: IFRS / JP / any
    cols = [c for c in ["IFRS", "JP", "any"] if c in cross.columns]
    cross = cross[cols]
    # 行順を合計の降順で
    cross = cross.loc[cross.sum(axis=1).sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(10, 6))
    arr = cross.values
    cmap = plt.get_cmap("Blues")
    vmax = arr.max()

    im = ax.imshow(arr, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            v = arr[i, j]
            tc = "white" if v > vmax * 0.5 else "#202124"
            label = str(int(v)) if v > 0 else "—"
            ax.text(j, i, label, ha="center", va="center",
                    fontsize=16.8, fontweight="bold", color=tc)

    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, fontsize=15.4, fontweight="bold")
    ax.set_yticks(range(len(cross.index)))
    ax.set_yticklabels(cross.index, fontsize=14.7)
    ax.tick_params(length=0)
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(False)

    ax.set_title("会計基準 × カテゴリ クロス  ―  対応の網羅性",
                 fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left")

    # サイドの合計
    for i, total in enumerate(cross.sum(axis=1).values):
        ax.text(len(cols) - 0.2, i, f"計 {total}", fontsize=14,
                ha="left", va="center", color=C_TEXT_SUB,
                fontweight="bold", clip_on=False)

    cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.10)
    cbar.set_label("ルール数", fontsize=12.6, color=C_TEXT_SUB)
    cbar.ax.tick_params(labelsize=8, colors=C_TEXT_SUB)

    fig.text(0.05, -0.02,
             "IFRS が performance で 104 / balance_sheet で 8 と充実 = IFRS 採用大企業に対応",
             fontsize=13.3, color=C_TEXT_SUB, ha="left", style="italic")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "02_standard_category_heatmap.png")
    plt.close(fig)


# ── 3) net_sales 系の 1 json_path : N xbrl_tag 構造 ──────────────────────────
def make_net_sales_multi_tags() -> None:
    km = pd.read_csv(STOCK / "collectors/kessan_mapping.csv")
    # net_sales 系の json_path に紐づく xbrl_tag 群
    target = km[km["json_path"].str.contains("net_sales", na=False)]
    grouped = target.groupby("json_path").agg(
        n_tags=("xbrl_tag", "count"),
        standards=("accounting_standard", lambda s: ",".join(sorted(set(s)))),
    ).sort_values("n_tags", ascending=False)

    fig, ax = plt.subplots(figsize=(13, 6))
    y = np.arange(len(grouped))

    bars = ax.barh(y, grouped["n_tags"], color="#3498db", alpha=0.85,
                   edgecolor="white", linewidth=0.8)
    for i, (_, row) in enumerate(grouped.iterrows()):
        ax.text(row["n_tags"] + 0.15, i, f"{row['n_tags']}タグ [{row['standards']}]",
                va="center", fontsize=14, fontweight="bold", color=C_TEXT)

    ax.set_yticks(y)
    ax.set_yticklabels(grouped.index, fontsize=13.3, family="monospace")
    ax.invert_yaxis()
    ax.set_xlabel("紐づく XBRL タグ数", fontsize=14.7, color=C_TEXT_SUB)
    ax.set_xlim(0, grouped["n_tags"].max() * 1.45)
    ax.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    total = grouped["n_tags"].sum()
    ax.set_title(
        f"net_sales 系  ―  1 つの JSON パスに複数 XBRL タグ（全 {total} ルール）",
        fontsize=18.2, fontweight="bold", color=C_TEXT, pad=14, loc="left",
    )

    fig.text(0.05, -0.02,
             "1 つの net_sales フィールドの裏に、会計基準 × 文脈で異なる XBRL タグが多数存在",
             fontsize=13.3, color=C_TEXT_SUB, ha="left", style="italic")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "03_net_sales_multi_tags.png")
    plt.close(fig)


# ── 4) 実データのフィールドカバレッジ ────────────────────────────────────────
def make_field_coverage() -> None:
    stmts = STOCK / "data/statements"
    files = list(stmts.glob("*_FY.json"))[:500]

    field_counts: dict[str, int] = {}
    for f in files:
        with open(f, encoding="utf-8") as fp:
            d = json.load(fp)

        def walk(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if v is None:
                        continue
                    walk(v, f"{path}.{k}" if path else k)
            elif isinstance(obj, list):
                pass
            else:
                field_counts[path] = field_counts.get(path, 0) + 1

        walk(d)

    cov = pd.DataFrame({
        "field": list(field_counts.keys()),
        "count": list(field_counts.values()),
    })
    cov["coverage"] = cov["count"] / len(files) * 100
    # _source 系を除外
    cov = cov[~cov["field"].str.startswith("_source")]
    cov = cov.sort_values("coverage", ascending=False)

    # Top 15 + Bottom 5（ただし segments の細かいキーは除く）
    top = cov[~cov["field"].str.startswith("segments.aggregates")].head(15)
    # 低カバレッジ代表
    low_targets = ["performance.forecast.lower.net_sales",
                   "performance.forecast.upper.net_sales",
                   "accounting_changes.estimates_changed",
                   "consolidation_changes.scope_change",
                   "corrections.original_filing_date",
                   "notes.material_subsequent_events",
                   "dividend.current.q4_dps",
                   "balance_sheet.current.equity_ratio",
                   "shares.outstanding_with_treasury"]
    low_subset = cov[cov["field"].isin(low_targets)].sort_values("coverage")

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(14, 6),
                                     gridspec_kw=dict(wspace=0.55))

    # Top 高カバレッジ
    y = np.arange(len(top))
    colors = ["#27AE60" if c >= 90 else "#3498DB" if c >= 70 else "#F39C12"
              for c in top["coverage"]]
    ax_l.barh(y, top["coverage"], color=colors, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, (_, r) in enumerate(top.iterrows()):
        ax_l.text(r["coverage"] + 1, i, f"{r['coverage']:.1f}%",
                  va="center", fontsize=13.3, fontweight="bold", color=C_TEXT)
    ax_l.set_yticks(y)
    ax_l.set_yticklabels(top["field"], fontsize=11.9, family="monospace")
    ax_l.invert_yaxis()
    ax_l.set_xlabel("カバレッジ（%）", fontsize=14, color=C_TEXT_SUB)
    ax_l.set_xlim(0, 110)
    ax_l.set_title(f"高カバレッジ Top 15  ―  全銘柄で安定取得可能",
                   fontsize=16.1, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_l.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)

    # 代表的な低カバレッジ
    y = np.arange(len(low_subset))
    ax_r.barh(y, low_subset["coverage"], color="#cccccc", alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, (_, r) in enumerate(low_subset.iterrows()):
        ax_r.text(r["coverage"] + 1, i, f"{r['coverage']:.1f}%",
                  va="center", fontsize=13.3, fontweight="bold", color=C_TEXT)
    ax_r.set_yticks(y)
    ax_r.set_yticklabels(low_subset["field"], fontsize=11.9, family="monospace")
    ax_r.invert_yaxis()
    ax_r.set_xlabel("カバレッジ（%）", fontsize=14, color=C_TEXT_SUB)
    ax_r.set_xlim(0, max(low_subset["coverage"].max() * 1.4, 5))
    ax_r.set_title("低カバレッジ代表例  ―  該当時のみ存在するフィールド",
                   fontsize=16.1, fontweight="bold", color=C_TEXT, pad=10, loc="left")
    ax_r.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)

    fig.suptitle(f"実データでのフィールドカバレッジ  ―  決算短信 FY 500 ファイルでの集計",
                 fontsize=18.9, fontweight="bold", color=C_TEXT, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "04_field_coverage.png")
    plt.close(fig)


# ── 5) スキーマ設計 5 原則 ─────────────────────────────────────────────────
def make_schema_principles() -> None:
    principles = [
        ("①", "意味的なセクション分け",
         "技術分類（instant/duration）でなく\n会計上意味のある単位で切る",
         "balance_sheet / performance / cash_flow"),
        ("②", "時間軸の対称性",
         "current / prior / forecast を\n同じフィールド構造で持つ",
         "performance.{current,prior,forecast}.net_sales"),
        ("③", "会計基準の透過性",
         "使う側のコードは基準を意識しない\nマッピング辞書で完全吸収",
         "1 json_path : N xbrl_tag (IFRS+JP+業種別)"),
        ("④", "優先順位による複数候補対応",
         "同じ json_path に複数タグが対応する場合\npriority で最優先タグを明示",
         "net_sales: NetSales > OperatingRevenues"),
        ("⑤", "データ駆動・コード変更不要",
         "スキーマ拡張は CSV 編集だけで完結\nパーサーコードは触らない",
         "CSV に 1 行追加 → 再パース実行"),
    ]

    fig, ax = plt.subplots(figsize=(13.5, 7.5))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, len(principles) + 1.2)
    ax.axis("off")

    colors_box = ["#3498db", "#27ae60", "#9b59b6", "#e67e22", "#1abc9c"]

    for i, ((num, title, desc, example), color) in enumerate(zip(principles, colors_box)):
        y_top = len(principles) - i + 0.1
        # 番号バッジ
        ax.add_patch(FancyBboxPatch((0.2, y_top - 0.85), 1.0, 0.85,
                                    boxstyle="round,pad=0.05",
                                    facecolor=color, edgecolor="none"))
        ax.text(0.7, y_top - 0.42, num, fontsize=30.8, fontweight="bold",
                color="white", ha="center", va="center")

        # タイトル
        ax.text(1.6, y_top - 0.20, title, fontsize=17.5,
                fontweight="bold", color=color, va="center")
        # 説明
        ax.text(1.6, y_top - 0.65, desc, fontsize=13.3,
                color=C_TEXT, va="center")
        # 実装例
        ax.add_patch(Rectangle((6.6, y_top - 0.85), 6.7, 0.85,
                               facecolor="#f5f5f5", edgecolor="#dddddd",
                               linewidth=0.5))
        ax.text(6.9, y_top - 0.42, "例: " + example,
                fontsize=14, color=C_TEXT, va="center")

    ax.set_title("XBRL → JSON スキーマ設計  ―  5 原則",
                 fontsize=19.6, fontweight="bold", color=C_TEXT,
                 pad=14, loc="left")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_DIR / "05_schema_principles.png")
    plt.close(fig)


# ── main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    make_section_distribution()
    print("[ok] 01_section_distribution.png")
    make_standard_category_heatmap()
    print("[ok] 02_standard_category_heatmap.png")
    make_net_sales_multi_tags()
    print("[ok] 03_net_sales_multi_tags.png")
    make_field_coverage()
    print("[ok] 04_field_coverage.png")
    make_schema_principles()
    print("[ok] 05_schema_principles.png")
