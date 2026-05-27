"""
blog/07_EDINET_TDnet取得とパース.md 用の画像生成スクリプト。

生成画像:
  01_pipeline_diagram.png   — EDINET/TDnet → ZIP → JSON パイプライン全体像
  02_storage_stats.png      — 各ディレクトリの ZIP/JSON 件数とサイズ
  03_kessan_distribution.png — 決算短信 JSON の決算期末月 + 種別 分布
  04_mapping_dict.png       — マッピング辞書 yuho/kessan のカテゴリ別構成
  05_eneos_catalog.png      — ENEOS 7 期分の有報取得カタログ実例

実行: python scripts/blog/07_pipeline_make_images.py
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

sys.path.insert(0, r"C:\stock_analysis")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle


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

C_EDI  = "#444444"
C_TDN  = "#666666"
C_ZIP  = "#888888"
C_JSON = "#aaaaaa"
C_TEXT = "#202124"
C_TEXT_SUB = "#70757a"
C_GRID = "#eaeaea"

OUT_DIR = Path(r"C:/minnanosaiban/hotline/docs/blog/posts/img/07_pipeline")
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


STOCK = Path(r"C:/stock_analysis")


# ── 1) パイプライン全体像 ─────────────────────────────────────────────────────
def make_pipeline_diagram() -> None:
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x, y, w, h, label, color, fc="white"):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                              linewidth=1.5, edgecolor=color, facecolor=fc)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=16, fontweight="bold", color=color)

    def arrow(x1, y1, x2, y2, label=None, color="#666666"):
        a = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle="->", mutation_scale=18,
                            color=color, linewidth=1.5)
        ax.add_patch(a)
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.18, label,
                    fontsize=16, ha="center", va="bottom",
                    color=color, style="italic")

    # EDINET 経路（上段）
    box(0.3,  5.0, 2.4, 0.95, "EDINET API\n(金融庁)", C_EDI)
    box(3.5,  5.0, 2.4, 0.95, "ZIP\ndata/yuho_zip/", C_ZIP)
    box(6.7,  5.0, 2.4, 0.95, "XBRL → JSON\nparse_yuho_xbrl", C_TEXT)
    box(9.9,  5.0, 2.7, 0.95, "JSON\ndata/yuho/", C_JSON)

    arrow(2.7, 5.48, 3.5, 5.48, "①書類取得")
    arrow(5.9, 5.48, 6.7, 5.48, "②解凍")
    arrow(9.1, 5.48, 9.9, 5.48, "③マッピング")

    # マッピング辞書（上段下に注記）
    box(7.0, 3.5, 5.5, 0.7, "yuho_mapping.csv  (98 ルール、IFRS/JP/業種別タクソノミ)",
        "#666666", fc="#f5f5f5")
    arrow(8.0, 4.2, 8.0, 5.0, color="#999999")

    # TDnet 経路（下段）
    box(0.3,  1.5, 2.4, 0.95, "TDnet\n(スクレイピング)", C_TDN)
    box(3.5,  1.5, 2.4, 0.95, "ZIP\ndata/statements_zip/", C_ZIP)
    box(6.7,  1.5, 2.4, 0.95, "XBRL → JSON\nxbrl_to_json", C_TEXT)
    box(9.9,  1.5, 2.7, 0.95, "JSON\ndata/statements/", C_JSON)

    arrow(2.7, 1.98, 3.5, 1.98, "①PDF→ZIP変換")
    arrow(5.9, 1.98, 6.7, 1.98, "②解凍")
    arrow(9.1, 1.98, 9.9, 1.98, "③マッピング")

    box(7.0, 0.05, 5.5, 0.7, "kessan_mapping.csv  (263 ルール、IFRS/JP × performance/BS/CF 等)",
        "#666666", fc="#f5f5f5")
    arrow(8.0, 0.75, 8.0, 1.5, color="#999999")

    # 凡例的なタイトル
    ax.text(0.3, 6.4, "EDINET 経路（有価証券報告書／四半期報告書）",
            fontsize=16, fontweight="bold", color=C_EDI)
    ax.text(0.3, 2.9, "TDnet 経路（決算短信／適時開示）",
            fontsize=16, fontweight="bold", color=C_TDN)

    ax.set_title(
        "自前 XBRL パイプラインの全体像  ―  2 経路 × 3 ステップ × マッピング辞書",
        fontsize=20, fontweight="bold", color=C_TEXT, pad=24, loc="left",
    )

    _savefig_vpad(fig, OUT_DIR / "01_pipeline_diagram.png")
    plt.close(fig)


# ── 2) ストレージ統計 ──────────────────────────────────────────────────────
def make_storage_stats() -> None:
    info = []
    for sub, label in [
        ("data/yuho_zip",          "有報 ZIP"),
        ("data/yuho",              "有報 JSON"),
        ("data/yuho_text",         "有報テキスト JSON"),
        ("data/statements_zip",    "決算短信 ZIP"),
        ("data/statements",        "決算短信 JSON"),
        ("data/statements_md",     "決算短信 MD"),
    ]:
        d = STOCK / sub
        if d.exists():
            files = [f for f in d.rglob("*") if f.is_file()]
            size = sum(f.stat().st_size for f in files) / 1024 / 1024
            info.append({"label": label, "count": len(files), "size_mb": size})

    df = pd.DataFrame(info)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 5),
                                     gridspec_kw=dict(wspace=0.35))

    colors = [C_ZIP if "ZIP" in s else C_JSON for s in df["label"]]
    y = np.arange(len(df))

    # 件数
    ax_l.barh(y, df["count"], color=colors, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, v in enumerate(df["count"]):
        ax_l.text(v + max(df["count"]) * 0.01, i, f"{v:,}",
                  va="center", fontsize=16, fontweight="bold", color=C_TEXT)
    ax_l.set_yticks(y)
    ax_l.set_yticklabels(df["label"], fontsize=16)
    ax_l.invert_yaxis()
    ax_l.set_xlabel("ファイル数", fontsize=16, color=C_TEXT_SUB)
    ax_l.set_xlim(0, max(df["count"]) * 1.15)
    ax_l.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)
    ax_l.set_title("ファイル数", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=24, loc="left")

    # サイズ
    ax_r.barh(y, df["size_mb"], color=colors, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, v in enumerate(df["size_mb"]):
        ax_r.text(v + max(df["size_mb"]) * 0.01, i, f"{v:,.0f} MB",
                  va="center", fontsize=16, fontweight="bold", color=C_TEXT)
    ax_r.set_yticks(y)
    ax_r.set_yticklabels(df["label"], fontsize=16)
    ax_r.invert_yaxis()
    ax_r.set_xlabel("サイズ（MB）", fontsize=16, color=C_TEXT_SUB)
    ax_r.set_xlim(0, max(df["size_mb"]) * 1.18)
    ax_r.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)
    ax_r.set_title("ストレージサイズ", fontsize=16, fontweight="bold",
                   color=C_TEXT, pad=24, loc="left")

    fig.suptitle("自前 XBRL パイプラインのストレージ状況",
                 fontsize=20, fontweight="bold", color=C_TEXT, y=1.02)
    _savefig_vpad(fig, OUT_DIR / "02_storage_stats.png")
    plt.close(fig)


# ── 3) 決算短信 JSON の決算期末月 + 種別 分布 ──────────────────────────────
def make_kessan_distribution() -> None:
    stmts = STOCK / "data/statements"
    rows = []
    for f in stmts.glob("*.json"):
        parts = f.stem.split("_")
        code = parts[0]
        fy_end = parts[1] if len(parts) > 1 else ""
        kind = "_".join(parts[2:]) if len(parts) > 2 else ""
        fy_month = fy_end[5:7] if len(fy_end) >= 7 else ""
        rows.append({"code": code, "fy_end": fy_end, "kind": kind, "fy_month": fy_month})
    df = pd.DataFrame(rows)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 5.5),
                                     gridspec_kw=dict(wspace=0.32))
    fig.subplots_adjust(top=0.75)

    # 決算期末月分布
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    counts = [(df["fy_month"] == m).sum() for m in months]

    colors_m = ["#5a9a72" if c > 300 else "#F39C12" if c > 100 else "#cccccc" for c in counts]
    bars = ax_l.bar(months, counts, color=colors_m, alpha=0.85,
                    edgecolor="white", linewidth=0.8)
    for b, c in zip(bars, counts):
        if c > 0:
            ax_l.text(b.get_x() + b.get_width() / 2, b.get_height() + 8,
                      str(c), ha="center", va="bottom", fontsize=16,
                      color=C_TEXT, fontweight="bold")
    ax_l.set_xlabel("決算期末月", fontsize=16, color=C_TEXT)
    ax_l.set_ylabel("ファイル数", fontsize=16, color=C_TEXT_SUB)
    ax_l.set_title(f"決算期末月の分布（全 {len(df):,} ファイル）",
                   fontsize=16, fontweight="bold", color=C_TEXT, pad=24, loc="left")
    ax_l.grid(axis="y", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)

    # 種別分布
    kind_order = ["FY", "forecast_FY", "Q1", "forecast_Q1", "Q2", "forecast_Q2",
                  "Q3", "forecast_Q3"]
    kind_counts = [(df["kind"] == k).sum() for k in kind_order]
    colors_k = [C_EDI if "forecast" not in k else C_TDN for k in kind_order]

    y = np.arange(len(kind_order))
    ax_r.barh(y, kind_counts, color=colors_k, alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, c in enumerate(kind_counts):
        ax_r.text(c + 8, i, str(c), va="center", fontsize=16,
                  fontweight="bold", color=C_TEXT)
    ax_r.set_yticks(y)
    ax_r.set_yticklabels(kind_order, fontsize=16)
    ax_r.invert_yaxis()
    ax_r.set_xlabel("ファイル数", fontsize=16, color=C_TEXT_SUB)
    ax_r.set_xlim(0, max(kind_counts) * 1.15)
    ax_r.set_title("書類種別の分布",
                   fontsize=16, fontweight="bold", color=C_TEXT, pad=24, loc="left")
    ax_r.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)

    fig.suptitle("決算短信 JSON  ―  カバレッジの内訳",
                 fontsize=20, fontweight="bold", color=C_TEXT, y=0.98)
    _savefig_vpad(fig, OUT_DIR / "03_kessan_distribution.png")
    plt.close(fig)


# ── 4) マッピング辞書 yuho / kessan のカテゴリ別構成 ─────────────────────────
def make_mapping_dict() -> None:
    mp = pd.read_csv(STOCK / "collectors/yuho_mapping.csv")
    km = pd.read_csv(STOCK / "collectors/kessan_mapping.csv")

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 6.5),
                                     gridspec_kw=dict(wspace=0.5))
    fig.subplots_adjust(top=0.82)

    # yuho_mapping
    cat_y = mp["category"].value_counts().head(10).iloc[::-1]
    y = np.arange(len(cat_y))
    ax_l.barh(y, cat_y.values, color="#3498db", alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, v in enumerate(cat_y.values):
        ax_l.text(v + 0.3, i, str(v), va="center", fontsize=16,
                  fontweight="bold", color=C_TEXT)
    ax_l.set_yticks(y)
    ax_l.set_yticklabels(cat_y.index, fontsize=16)
    ax_l.set_xlabel("ルール数", fontsize=16, color=C_TEXT_SUB)
    ax_l.set_xlim(0, max(cat_y.values) * 1.18)
    ax_l.set_title(f"yuho_mapping.csv（全 {len(mp)} ルール）",
                   fontsize=15, fontweight="bold", color=C_TEXT, pad=24, loc="center")
    ax_l.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_l.spines[sp].set_visible(False)

    # kessan_mapping（category）
    cat_k = km["category"].value_counts().iloc[::-1]
    y = np.arange(len(cat_k))
    ax_r.barh(y, cat_k.values, color="#888888", alpha=0.85,
              edgecolor="white", linewidth=0.8)
    for i, v in enumerate(cat_k.values):
        ax_r.text(v + 1.5, i, str(v), va="center", fontsize=16,
                  fontweight="bold", color=C_TEXT)
    ax_r.set_yticks(y)
    ax_r.set_yticklabels(cat_k.index, fontsize=16)
    ax_r.set_xlabel("ルール数", fontsize=16, color=C_TEXT_SUB)
    ax_r.set_xlim(0, max(cat_k.values) * 1.15)
    ax_r.set_title(f"kessan_mapping.csv（全 {len(km)} ルール）",
                   fontsize=15, fontweight="bold", color=C_TEXT, pad=24, loc="center")
    ax_r.grid(axis="x", color=C_GRID, linewidth=0.5)
    for sp in ("top", "right"):
        ax_r.spines[sp].set_visible(False)

    # accounting_standard 注記
    std_k = km["accounting_standard"].value_counts()
    note = "  +  ".join(f"{k}: {v}" for k, v in std_k.items())
    fig.text(0.55, -0.02, f"会計基準別: {note}",
             fontsize=16, color=C_TEXT_SUB, ha="left", style="italic")

    fig.suptitle("マッピング辞書の構成  ―  XBRL 要素 ID → JSON キーの対応",
                 fontsize=20, fontweight="bold", color=C_TEXT, y=0.98)
    _savefig_vpad(fig, OUT_DIR / "04_mapping_dict.png")
    plt.close(fig)


# ── 5) ENEOS 7 期取得カタログ ─────────────────────────────────────────────
def make_eneos_catalog() -> None:
    ed_dir = STOCK / "data/yuho/E24050"
    rows = []
    for f in sorted(ed_dir.glob("*.json")):
        with open(f, encoding="utf-8") as fp:
            d = json.load(fp)
        meta = d.get("metadata", {})
        fin = d.get("financials", {}) or {}
        rows.append({
            "fy_end": meta.get("fiscal_year_end"),
            "doc_id": meta.get("doc_id"),
            "filing": meta.get("filing_date"),
            "std": meta.get("accounting_standard"),
            "consol": "連結" if meta.get("is_consolidated") else "単独",
            "net_sales": fin.get("net_sales"),
            "ni": fin.get("net_income"),
        })
    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(13.5, 5.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(len(df) + 1, -1)
    ax.axis("off")

    # ヘッダ
    headers = [("会計年度", 0.5, "center"), ("doc_id", 2.0, "center"),
               ("提出日", 3.6, "center"), ("基準", 5.0, "center"),
               ("連/単", 5.9, "center"), ("売上高", 7.5, "right"),
               ("純利益", 9.5, "right"), ("ファイル", 11.5, "left")]
    for lab, x, ha in headers:
        ax.text(x, -0.5, lab, fontsize=16, fontweight="bold",
                ha=ha, va="center", color=C_TEXT)

    for r, row in enumerate(rows):
        ax.text(0.5, r + 0.5, row["fy_end"], fontsize=16,
                ha="center", va="center", color=C_TEXT, fontweight="bold")
        ax.text(2.0, r + 0.5, row["doc_id"], fontsize=16,
                ha="center", va="center", color="#666666", family="monospace")
        ax.text(3.6, r + 0.5, row["filing"], fontsize=16,
                ha="center", va="center", color=C_TEXT_SUB)
        ax.text(5.0, r + 0.5, row["std"], fontsize=16,
                ha="center", va="center", color="#3498db", fontweight="bold")
        ax.text(5.9, r + 0.5, row["consol"], fontsize=16,
                ha="center", va="center", color=C_TEXT_SUB)
        ns = row["net_sales"]
        ni = row["ni"]
        ns_t = f"{ns/1e12:.2f}兆" if ns else "—"
        ni_t = f"{ni/1e11:+.1f}千億" if ni else "—"
        ni_c = "#5a9a72" if ni and ni > 0 else "#c87878"
        ax.text(7.5, r + 0.5, ns_t, fontsize=16,
                ha="right", va="center", color=C_TEXT)
        ax.text(9.5, r + 0.5, ni_t, fontsize=16, fontweight="bold",
                ha="right", va="center", color=ni_c)
        ax.text(11.5, r + 0.5, f"E24050_{row['fy_end']}.json",
                fontsize=16, ha="left", va="center", color=C_TEXT_SUB,
                family="monospace")

    # 注釈
    ax.text(0.5, len(df) + 0.7,
            "doc_id S100W1E2 = 2025-06-24 提出の最新有報（SummaryOfBusinessResults に 5 期分の要約データを内包）",
            fontsize=16, color=C_TEXT_SUB, style="italic", va="top")

    ax.set_title("ＥＮＥＯＳ（E24050）  ―  有報 7 期分の取得カタログ実例",
                 fontsize=20, fontweight="bold", color=C_TEXT, pad=24, loc="left")
    _savefig_vpad(fig, OUT_DIR / "05_eneos_catalog.png")
    plt.close(fig)


# ── main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    make_pipeline_diagram()
    print("[ok] 01_pipeline_diagram.png")
    make_storage_stats()
    print("[ok] 02_storage_stats.png")
    make_kessan_distribution()
    print("[ok] 03_kessan_distribution.png")
    make_mapping_dict()
    print("[ok] 04_mapping_dict.png")
    make_eneos_catalog()
    print("[ok] 05_eneos_catalog.png")
