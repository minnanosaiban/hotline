"""docs/pdf/ にある PDF から、PDF 一覧ページ（docs/pdf/index.md）を作る。

  python scripts/pdf_index.py

ファイル名（scripts/add_pdf.py の付け方）から、区分・日付（または証拠番号）・書面名を読み取り、
ページ数とファイルの大きさを調べて、静的なリンクの一覧にする。PDF へのリンクが、JavaScript を使わずに HTML にそのまま入るので、
検索エンジンが PDF を見つけやすい。裁判文書ページ（提訴年ごとの trial/・trial2021/・trial2025/）に本文の行があるものには、「本文」のリンクも付く。
add_pdf.py は、PDF を足すたびに、これを自動で動かす。要 PyMuPDF。
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "docs" / "pdf"
TRIAL_PAGES = [  # (URLのパス, index.md) 「裁判文書公開」の各提訴年ページ。2026-09-22、複数年に分割したときに追加
    ("../trial/", ROOT / "docs" / "trial" / "index.md"),
    ("../trial2021/", ROOT / "docs" / "trial2021" / "index.md"),
    ("../trial2025/", ROOT / "docs" / "trial2025" / "index.md"),
]
BASE = "https://minnanosaiban.github.io/eneos-hotline/"

NAME = re.compile(r"^(?P<site>.+?)――(?P<side>ENEOS側|通報者側|裁判所)_(?P<label>\d{4}年\d{2}月\d{2}日|[甲乙]\d+(?:-\d+)?)_(?P<title>.+)$")
GROUPS = [   # 見出し、区分、証拠か
    ("裁判所", "裁判所", False),
    ("被告（ＥＮＥＯＳ）側", "ENEOS側", False),
    ("原告（通報者）側", "通報者側", False),
    ("原告（通報者）側の証拠（甲号証）", "通報者側", True),
]


def _size(n):
    return f"{n / 1e6:.1f}MB" if n >= 1e6 else f"{max(1, round(n / 1e3))}KB"


def _exhibit_key(label):
    m = re.match(r"[甲乙](\d+)(?:-(\d+))?", label)
    return (label[0], int(m.group(1)), int(m.group(2) or 0))


def _text_rows():
    """裁判文書ページ（提訴年ごとに複数）の本文の行: PDF のファイル名 → (ページのURL, 行の id)"""
    rows = {}
    for url, path in TRIAL_PAGES:
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        for id_, name in re.findall(r'id="([a-z0-9-]+)" data-md="[^"]*" data-pdf="\.\./pdf/([^"]+)"', t):
            rows[name] = (url, id_)
    return rows


def collect():
    import fitz
    items = []
    for p in sorted(PDF_DIR.glob("*.pdf")):
        m = NAME.match(p.stem)
        if not m:
            print(f"（名前の形が違うので一覧から外した: {p.name}）")
            continue
        with fitz.open(p) as doc:
            pages = doc.page_count
        items.append({**m.groupdict(), "file": p.name, "pages": pages, "bytes": p.stat().st_size, "exhibit": m["label"][0] in "甲乙"})
    return items


def build(items):
    text_rows = _text_rows()
    total = sum(i["bytes"] for i in items)
    out = [f"""---
title: PDF一覧
description: ENEOS（エネオス）の通報をめぐる裁判・訴訟の裁判文書の PDF の一覧です。判決文、準備書面、答弁書、控訴理由書、証拠（甲号証）の PDF を、区分・日付・書面名が分かるファイル名で並べています。
seo_title: ENEOS（エネオス）の通報をめぐる裁判・訴訟｜裁判文書のPDF一覧
url: {BASE}pdf/
image: {BASE}img/card1.png
twitter_card: summary
hide:
  - navigation
  - toc
---

<!-- このページは scripts/pdf_index.py が docs/pdf/ の中身から作る。手で直さず、python scripts/pdf_index.py で作り直す。 -->

<div class="trial-doc-marker" hidden></div>

<div class="trial-page center-container" markdown>

<div class="hero-band" markdown>
# PDF一覧
<p>
ＥＮＥＯＳ（エネオス）の内部通報制度をめぐる訴訟の、裁判文書の PDF です。本文（テキスト）は、<a href="../trial/">裁判文書公開</a>のページで読めます。
</p>
</div>

<p class="base00 hero-share">
  <a href="https://twitter.com/share?url={BASE}pdf/ &text=PDF一覧 - ＥＮＥＯＳの内部通報制度をめぐる訴訟について"
     target="_blank" class="x-share">
    <i class="fa-brands fa-x-twitter"></i> でシェア
  </a>
</p>

<div class="toc-wrap doc-list" markdown>

<p class="doc-lead">全{len(items)}件・合計 {_size(total)}。PDF には文字情報が入っていて、検索やコピーができます。</p>
"""]
    for heading, side, exhibit in GROUPS:
        rows = [i for i in items if i["side"] == side and i["exhibit"] == exhibit]
        if not rows:
            continue
        rows.sort(key=(lambda i: _exhibit_key(i["label"])) if exhibit else (lambda i: i["label"]))
        out.append(f'<p class="t-toc-head bar-title doc-side">{heading}</p>\n\n<div class="doc-rows" markdown>\n')
        for i in rows:
            title = html.escape(i["title"])
            name = html.escape(i["file"], quote=True)
            head = f'{html.escape(i["label"])}　{title}' if exhibit else title
            date = "" if exhibit else f'<span class="doc-date">{html.escape(i["label"])}</span>'
            link = ""
            if i["file"] in text_rows:
                trial_url, row_id = text_rows[i["file"]]
                link = f'<a class="dbtn" href="{trial_url}#{row_id}">本文</a>'
            out.append(
                f'<div class="pdf-row"><a class="pdf-main" href="{name}" target="_blank" rel="noopener">'
                f'<i class="bi bi-file-earmark-pdf" aria-hidden="true"></i> <span class="doc-title">{head}</span></a>'
                f'{date}<span class="doc-note">{i["pages"]}ページ・{_size(i["bytes"])}</span>{link}</div>')
        out.append("\n</div>\n")
    out.append("</div>\n\n</div>\n")
    return "\n".join(out)


def write_index():
    items = collect()
    (PDF_DIR / "index.md").write_text(build(items), encoding="utf-8", newline="\n")
    return len(items)


if __name__ == "__main__":
    print(f"{write_index()} 件の PDF で、{PDF_DIR / 'index.md'} を作った")
