"""PDF を docs/pdf/ に入れる。検索されやすい名前とタイトルにそろえ、必要なら軽量化と文字層（OCR）も付ける。

  python scripts/add_pdf.py <元のPDF> <ENEOS側|通報者側|裁判所|関係法令等> <YYYY-MM-DD|甲17> <書面名> [--shrink] [--ocr] [--out フォルダ]

  例) python scripts/add_pdf.py 02_答弁書_ENEOS_公開.pdf ENEOS側 2024-04-15 答弁書 --ocr
  →   docs/pdf/ENEOS（エネオス）の内部通報制度をめぐる訴訟について――ENEOS側_2024年04月15日_答弁書.pdf
  例) python scripts/add_pdf.py 甲17_税務処理の確認経緯_ENEOS_公開.pdf 通報者側 甲17 税務処理の確認経緯
  →   docs/pdf/ENEOS（エネオス）の内部通報制度をめぐる訴訟について――通報者側_甲17_税務処理の確認経緯.pdf   （証拠は、日付の代わりに証拠番号）
  例) python scripts/add_pdf.py 公益通報ハンドブック_21頁.pdf 関係法令等 2017-09-01 公益通報ハンドブック２１頁
  →   docs/pdf/ENEOS（エネオス）の内部通報制度をめぐる訴訟について――関係法令等_2017年09月01日_公益通報ハンドブック２１頁.pdf
      （関係法令等は、裁判の当事者ではない参考資料。日付が分からない・重要でない場合も、YYYY-MM-DD の形で近い日付を入れる）

  --shrink  画像だけの白黒PDFを、A4・200dpi・1bit に作り直す（色つきのPDFは断る）。38MBの判決文が 1.4MB になる
  --ocr     文字情報の無いPDFに、透明な文字層を付ける（scan-ocr の OCR を使う。1ページ10〜25秒、CPUだけで動く）。
            文字が既にあるPDFでは何もしない
  --out     出力先（既定は docs/pdf）

ファイル名（.pdf を除く）は、PDF の「タイトル」（Info 辞書の Title）にも入れる。検索結果に出るタイトルは、このメタデータが使われる。
docs/trial2024/index.md の data-pdf には、最後に表示される「../pdf/<ファイル名>」を書く。
終わると、PDF 一覧ページ（docs/pdf/index.md）も作り直す（scripts/pdf_index.py。単独でも動かせる）。

要 PyMuPDF（このスクリプトだけで使う。サイトのビルドには要らない）:  pip install pymupdf
--shrink・--ocr は、scripts/pdf_tools.py（Pillow、scan-ocr の環境）を使う。
"""
import argparse
import re
import sys
import tempfile
from pathlib import Path

SITE = "ENEOS（エネオス）の内部通報制度をめぐる訴訟について"
SEP = "――"                                    # サイト名と区分の間（ダッシュ。U+2015 を2つ）。変えるのはここだけ
SIDES = ("ENEOS側", "通報者側", "裁判所", "関係法令等")
OUT = Path(__file__).resolve().parent.parent / "docs" / "pdf"


def file_stem(side, when, title):
    """ENEOS（エネオス）の内部通報制度をめぐる訴訟について――ENEOS側_2024年04月15日_答弁書
    when は日付（YYYY-MM-DD）か、証拠番号（甲17、甲8-16 など）。"""
    if side not in SIDES:
        raise ValueError(f"区分は {' / '.join(SIDES)} のどれか: {side!r}")
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", when)
    if m:
        label = f"{m.group(1)}年{m.group(2)}月{m.group(3)}日"
    elif re.fullmatch(r"[甲乙]\d+(?:-\d+)?", when):
        label = when
    else:
        raise ValueError(f"日付は YYYY-MM-DD、証拠は 甲17 のように: {when!r}")
    if re.search(r'[\\/:*?"<>|]', title):
        raise ValueError(f"書面名に使えない文字がある: {title!r}")
    return f"{SITE}{SEP}{side}_{label}_{title}"


def add_pdf(src, side, when, title, shrink=False, ocr=False, out=OUT, log=print):
    import fitz  # PyMuPDF

    stem = file_stem(side, when, title)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    dst = out / f"{stem}.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(src)
        if shrink or ocr:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import pdf_tools
        if shrink:
            log("白黒の A4・200dpi・1bit に作り直す…")
            nxt = Path(tmp) / "shrunk.pdf"
            pdf_tools.normalize_bilevel(work, nxt)
            log(f"  {work.stat().st_size / 1e6:.1f}MB → {nxt.stat().st_size / 1e6:.2f}MB")
            work = nxt
        if ocr:
            if pdf_tools.has_text(work):
                log("文字情報が既にあるので、OCR はしない")
            else:
                log("OCR して透明な文字層を付ける…")
                nxt = Path(tmp) / "ocr.pdf"
                pdf_tools.add_ocr_text_layer(work, nxt, log)
                work = nxt
        doc = fitz.open(work)
        meta = dict(doc.metadata or {})
        meta["title"] = stem
        doc.set_metadata(meta)
        # 全体を書き出し直す（古いタイトルの入った辞書を残さない）。画像などのデータは再圧縮しない。
        doc.save(dst, garbage=1, deflate=True)
        doc.close()
    return dst


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("side")
    ap.add_argument("when", help="YYYY-MM-DD または 甲17 のような証拠番号")
    ap.add_argument("title")
    ap.add_argument("--shrink", action="store_true")
    ap.add_argument("--ocr", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    try:
        dst = add_pdf(a.src, a.side, a.when, a.title, a.shrink, a.ocr, a.out)
    except ValueError as e:                 # 入力の誤り（区分・日付・色つきPDFなど）は、トレースバックを出さずに知らせる
        sys.exit(f"エラー: {e}")
    print(dst)
    print(f"data-pdf に書く値: ../pdf/{dst.name}")
    if Path(a.out).resolve() == OUT.resolve():        # 既定の出力先に入れたときだけ、一覧ページも作り直す
        import pdf_index
        pdf_index.write_index()
        print("PDF 一覧ページ（docs/pdf/index.md）を作り直した")
