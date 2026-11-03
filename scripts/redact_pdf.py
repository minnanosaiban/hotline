"""原告側の書面PDFを、公開用に仕上げる: 黒塗り（個人名・事件番号）→ 文字層（YomiToku）→ メタデータ → ファイル名。

  python scripts/redact_pdf.py <元PDFのフォルダ> [--out フォルダ] [--only 0101,0501,...] [--no-ocr]

流れ（1ファイルごと）
  1. 元のPDFの文字情報から、黒塗りする語の位置をページごとに調べる（字間の空白・改行をまたいでも見つかる）
       - 氏名: hikae/redact_terms.txt に書いた語（1行1語。この repo は公開なので、氏名はコードに書かない）
       - 事件番号: 「令和○年（ワ）第○○○号」の形の、年・事件の種類・番号の全部
  2. 各ページを 200dpi の画像にして、見つけた位置を黒く塗りつぶす。白黒のページは 1bit、色つきのページは色のまま
       （画像にするので、元の文字情報は残らない）
  3. 黒塗り後の画像を YomiToku（scan-ocr と同じ解析器）で OCR して、透明な文字層を付ける
       （黒塗り前の文字は、文字層のどこにも入らない）
  4. 検証: 文字層に氏名・事件番号が残っていないか。残っていれば、そのファイルは出力せず止める
  5. メタデータ: タイトルだけをファイル名（.pdf を除く）にそろえ、作成者・作成ソフト・日付などは空にする。XMP も消す
  6. ファイル名: scripts/add_pdf.py の file_stem で、検索されやすい名前にする

TABLE に、元のファイル名の頭4桁と、日付・書面名を書く。足すときはここだけ。
要 PyMuPDF・Pillow・numpy。OCR には scan-ocr の環境（yomitoku・torch）が要る。サイトのビルドには要らない。
"""
import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pdf_tools                      # noqa: E402
from add_pdf import file_stem         # noqa: E402

SIDE = "通報者側"
DPI = 200
THRESH = 160                          # 白黒のページを 1bit にするしきい値（pdf_tools.normalize_bilevel と同じ）
PAD = 4                               # 黒塗りの余白（画素）

# 元ファイルの頭4桁 → (日付, 書面名)。差し替え11本 + 新規8本
TABLE = {
    "0101": ("2024-02-19", "訴状"),
    "0102": ("2024-04-12", "訴状訂正申立書"),
    "0501": ("2024-05-17", "原告第１準備書面"),
    "0801": ("2024-07-19", "原告第２準備書面"),
    "1001": ("2024-08-09", "原告第３準備書面"),
    "1002": ("2024-08-09", "原告第１・第２準備書面訂正申立書"),
    "1301": ("2024-11-25", "原告第４準備書面"),
    "1302": ("2024-11-25", "原告第１・第２準備書面訂正申立書"),
    "1303": ("2024-12-23", "原告第４準備書面訂正申立書"),
    "1304": ("2024-12-23", "原告第４準備書面３頁及び４頁差替"),
    "1401": ("2024-11-25", "求釈明申立書"),
    "1501": ("2024-11-25", "文書送付嘱託申立書"),
    "1801": ("2025-01-30", "原告第５準備書面"),
    "1802": ("2025-03-18", "原告第５準備書面訂正申立書"),
    "2101": ("2025-06-06", "控訴理由書"),
    "2102": ("2025-07-14", "控訴理由書訂正申立書"),
    "2301": ("2025-07-14", "控訴理由補充書（１）"),
    "2302": ("2025-07-14", "文書送付嘱託申立書"),
    "2401": ("2025-07-14", "控訴理由補充書（２）"),
}

# 検索の語（NFKC 後の文字列に当てる。全角の数字は半角になっている）
TERMS_FILE = HERE.parent / "hikae" / "redact_terms.txt"      # Git に入れない（hikae/ は .gitignore）。
# 書き方: 「[黒塗り]」の下に黒塗りする語、「[検証]」の下に、黒塗りの取りこぼしを見つけるための語（氏名の一部など）を、1行1語で。


def load_terms():
    if not TERMS_FILE.exists():
        raise SystemExit(f"{TERMS_FILE} が無い。黒塗りする語を書いたファイルを作ってから動かす")
    sec, terms = None, {"黒塗り": [], "検証": []}
    for line in TERMS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line in ("[黒塗り]", "[検証]"):
            sec = line[1:-1]
        elif line and sec:
            terms[sec].append(re.escape(line))
    if not terms["黒塗り"]:
        raise SystemExit(f"{TERMS_FILE} に [黒塗り] の語が無い")
    return terms


_T = load_terms()
NAME_RE = re.compile("|".join(sorted(_T["黒塗り"], key=len, reverse=True)))
LEFT_RE = re.compile("|".join(_T["黒塗り"] + _T["検証"]))
CASENO_RE = re.compile(r"(?:令和\d+年)?(?:\([ワネハ]\))?第\d{4,5}号")
INVISIBLE = re.compile(r"[\s​-‏‪-‮⁠﻿]")


def norm(text):
    return unicodedata.normalize("NFKC", text or "")


def page_chars(page):
    """ページの文字を、読む順に (文字, bbox) で返す。空白・見えない制御文字は除く。"""
    out = []
    for b in page.get_text("rawdict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln["spans"]:
                for ch in sp["chars"]:
                    if INVISIBLE.fullmatch(ch["c"]):
                        continue
                    out.append((ch["c"], ch["bbox"]))
    return out


def find_boxes(page):
    """黒塗りする位置（PDFの座標 pt）を返す。同じ行にある文字は1つの長方形にまとめる。"""
    chars = page_chars(page)
    flat, owner = [], []              # NFKC 後の1文字ごとに、元の文字の番号を持つ
    for i, (c, _) in enumerate(chars):
        for n in norm(c):
            flat.append(n)
            owner.append(i)
    text = "".join(flat)
    hits = []
    for rx in (NAME_RE, CASENO_RE):
        for m in rx.finditer(text):
            hits.append((m.group(0), sorted(set(owner[m.start():m.end()]))))
    boxes = []
    for word, idxs in hits:
        rects = [fitz.Rect(chars[i][1]) for i in idxs]
        lines = []                    # 縦に重なるものを同じ行とみなす
        for r in sorted(rects, key=lambda r: (r.y0, r.x0)):
            for k, ln in enumerate(lines):
                if min(ln.y1, r.y1) - max(ln.y0, r.y0) > 0.5 * min(ln.height, r.height):
                    lines[k] = ln | r
                    break
            else:
                lines.append(fitz.Rect(r))
        boxes.append((word, lines))
    return boxes


def is_gray(img):
    small = img.resize((64, max(1, round(64 * img.height / img.width))))
    return all(abs(r - g) <= 30 and abs(g - b) <= 30 for r, g, b in small.getdata())


def redact_to_images(src, log=print):
    """src を画像にして黒塗りする。(page_size, PNG/JPEG のバイト列, 色つきか) のリストと、黒塗りした語の一覧を返す。"""
    doc = fitz.open(src)
    pages, report = [], []
    for page in doc:
        pix = page.get_pixmap(dpi=DPI, alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        draw = ImageDraw.Draw(im)
        s = DPI / 72
        for word, rects in find_boxes(page):
            report.append((page.number + 1, word))
            for r in rects:
                draw.rectangle([r.x0 * s - PAD, r.y0 * s - PAD, r.x1 * s + PAD, r.y1 * s + PAD], fill=(0, 0, 0))
        buf = io.BytesIO()
        if is_gray(im):
            im.convert("L").point(lambda v: 255 if v > THRESH else 0).convert("1").save(buf, format="PNG", optimize=True)
            color = False
        else:
            im.save(buf, format="JPEG", quality=88)
            color = True
        pages.append((page.rect.width, page.rect.height, buf.getvalue(), color))
    doc.close()
    return pages, report


def images_to_pdf(pages, dst):
    out = fitz.open()
    for w, h, data, _ in pages:
        p = out.new_page(width=w, height=h)
        p.insert_image(p.rect, stream=data)
    out.save(dst, garbage=3, deflate=True)
    out.close()


def leftovers(ocr_pages):
    """OCR した文字に、氏名・事件番号が残っていないか。残っている (ページ, 語) を返す。"""
    bad = []
    for i, pg in enumerate(ocr_pages, start=1):
        # 行ごとでなくページ全体をつなげて見る（行をまたいだ語も拾う）
        text = INVISIBLE.sub("", norm("".join(w.get("content") or "" for w in pg.get("words", []))))
        for rx in (LEFT_RE, CASENO_RE):
            bad += [(i, m.group(0)) for m in rx.finditer(text)]
    return bad


def finish_metadata(path, title):
    doc = fitz.open(path)
    doc.set_metadata({"title": title, "author": "", "subject": "", "keywords": "",
                      "creator": "", "producer": "", "creationDate": "", "modDate": "", "trapped": ""})
    doc.del_xml_metadata()
    doc.save(path + ".tmp", garbage=3, deflate=True)
    doc.close()
    Path(path + ".tmp").replace(path)


def process(src, key, out_dir, ocr=True, log=print):
    when, title = TABLE[key]
    stem = file_stem(SIDE, when, title)
    dst = Path(out_dir) / f"{stem}.pdf"
    log(f"[{key}] {title} → {dst.name}")
    pages, report = redact_to_images(src, log)
    log(f"  黒塗り {len(report)}か所: " + ", ".join(f"p{p}:{w}" for p, w in report))
    tmp = Path(out_dir) / f"_{key}_img.pdf"
    images_to_pdf(pages, tmp)
    try:
        if ocr:
            log("  OCR（YomiToku）…")
            ocr_data = pdf_tools.ocr_pages(tmp, log=lambda m: None)
            bad = leftovers(ocr_data)
            if bad:
                raise RuntimeError(f"黒塗り後の文字層に残っている: {bad}")
            pdf_tools.add_text_layer(tmp, ocr_data, dst)
        else:
            tmp.replace(dst)
    finally:
        if tmp.exists():
            tmp.unlink()
    finish_metadata(str(dst), stem)
    # 最終確認: 出力そのものの文字層
    with fitz.open(dst) as d:
        text = INVISIBLE.sub("", norm("".join(p.get_text() for p in d)))
        left = [m.group(0) for rx in (LEFT_RE, CASENO_RE) for m in rx.finditer(text)]
        if left:
            dst.unlink()
            raise RuntimeError(f"出力の文字層に残っている: {left}")
        log(f"  完了: {len(d)}ページ・{dst.stat().st_size / 1e6:.2f}MB・色つき{sum(p[3] for p in pages)}ページ")
    return dst


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src_dir")
    ap.add_argument("--out", default=str(HERE.parent / "hikae" / "差替PDF"))
    ap.add_argument("--only", default="", help="頭4桁をコンマ区切りで")
    ap.add_argument("--no-ocr", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    only = [k for k in a.only.split(",") if k] or list(TABLE)
    srcs = {f.name[:4]: f for f in Path(a.src_dir).glob("*.pdf")}
    for key in only:
        if key not in srcs:
            print(f"[{key}] 元のPDFが無い"); continue
        when, title = TABLE[key]
        if (out / f"{file_stem(SIDE, when, title)}.pdf").exists():
            print(f"[{key}] 出力済みなので飛ばす"); continue
        try:
            process(srcs[key], key, out, ocr=not a.no_ocr)
        except Exception as e:
            print(f"[{key}] 失敗: {e}")
    print("終了")
