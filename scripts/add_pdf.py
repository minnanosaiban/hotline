"""PDF を docs/pdf/ にコピーして、検索されやすい名前とタイトル（メタデータ）にそろえる。

  python scripts/add_pdf.py <元のPDF> <ENEOS側|通報者側|裁判所> <YYYY-MM-DD> <書面名>

  例) python scripts/add_pdf.py 02_答弁書_ENEOS_公開.pdf ENEOS側 2024-04-15 答弁書
  →   docs/pdf/ENEOS（エネオス）の内部通報制度をめぐる訴訟についてーーENEOS側_2024年04月15日_答弁書.pdf

ファイル名（.pdf を除く）は、PDF の「タイトル」（Info 辞書の Title）にも入れる。検索結果に出るタイトルは、このメタデータが使われる。
docs/trial/index.md の data-pdf には、最後に表示される「../pdf/<ファイル名>」を書く。

要 PyMuPDF（このスクリプトだけで使う。サイトのビルドには要らない）:  pip install pymupdf
"""
import re
import sys
from pathlib import Path

SITE = "ENEOS（エネオス）の内部通報制度をめぐる訴訟について"
SEP = "ーー"                                   # サイト名と区分の間。ダッシュ「――」にしたいときはここだけ変える
SIDES = ("ENEOS側", "通報者側", "裁判所")
OUT = Path(__file__).resolve().parent.parent / "docs" / "pdf"


def file_stem(side, date, title):
    """ENEOS（エネオス）の内部通報制度をめぐる訴訟についてーーENEOS側_2024年04月15日_答弁書"""
    if side not in SIDES:
        raise ValueError(f"区分は {' / '.join(SIDES)} のどれか: {side!r}")
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", date)
    if not m:
        raise ValueError(f"日付は YYYY-MM-DD で: {date!r}")
    if re.search(r'[\\/:*?"<>|]', title):
        raise ValueError(f"書面名に使えない文字がある: {title!r}")
    y, mo, d = m.groups()
    return f"{SITE}{SEP}{side}_{y}年{mo}月{d}日_{title}"


def add_pdf(src, side, date, title):
    import fitz  # PyMuPDF

    stem = file_stem(side, date, title)
    dst = OUT / f"{stem}.pdf"
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(src)
    meta = dict(doc.metadata or {})
    meta["title"] = stem
    doc.set_metadata(meta)
    # 全体を書き出し直す（古いタイトルの入った辞書を残さない）。画像などのデータは再圧縮しない。
    doc.save(dst, garbage=1, deflate=False)
    doc.close()
    return dst


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    out = add_pdf(*sys.argv[1:])
    print(out)
    print(f"data-pdf に書く値: ../pdf/{out.name}")
