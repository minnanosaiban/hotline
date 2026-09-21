"""PDF の軽量化と、透明な文字層（OCR）の追加。scripts/add_pdf.py から使う。

- normalize_bilevel: 画像だけの白黒PDFを A4・200dpi・1bit に作り直す（色つきなら断る）。
    元が 4591x6491 画素・カラーPNGのページ（1ページ約3MB）でも、1ページ 50〜100KB になる
- add_ocr_text_layer: 文字情報の無いPDFを OCR して、元の画像はそのままに、透明な文字を重ねる。
    OCR は scan-ocr（C:\\minnanosaiban\\scan-ocr、エンジンは YomiToku）の解析器を、そのまま使う
    （scan-ocr の「テキスト乗せPDF」は画像をJPEGで作り直すので、この用途では使わない）

要 PyMuPDF・Pillow。OCR には scan-ocr の環境（yomitoku・torch）が要る。サイトのビルドには要らない。
"""
import io
import json
import os
import sys
from pathlib import Path

A4_W = 595.276
PX_W = 1654            # A4 の 200dpi
THRESH = 160           # これより明るい画素は白
SCAN_OCR = Path(os.environ.get("SCAN_OCR_DIR", r"C:\minnanosaiban\scan-ocr"))


def has_text(path):
    import fitz
    with fitz.open(path) as doc:
        return any(page.get_text().strip() for page in doc)


def normalize_bilevel(src, dst):
    """画像だけの白黒PDFを、A4・200dpi・1bit のPDFに作り直す。"""
    import fitz
    from PIL import Image
    doc = fitz.open(src)
    out = fitz.open()
    for page in doc:
        imgs = page.get_images(full=True)
        if len(imgs) != 1:
            raise ValueError(f"{page.number + 1}ページ目: 画像が {len(imgs)} 個ある。画像1枚だけのページ以外は縮小できない")
        im = Image.open(io.BytesIO(doc.extract_image(imgs[0][0])["image"])).convert("RGB")
        small = im.resize((64, max(1, round(64 * im.height / im.width))))
        if any(abs(r - g) > 30 or abs(g - b) > 30 for r, g, b in small.getdata()):
            raise ValueError(f"{page.number + 1}ページ目: 色がついている。白黒ではないので 1bit にはしない")
        g = im.convert("L").resize((PX_W, round(im.height * PX_W / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        g.point(lambda v: 255 if v > THRESH else 0).convert("1").save(buf, format="PNG", optimize=True)
        p = out.new_page(width=A4_W, height=round(A4_W * g.height / g.width, 2))
        p.insert_image(p.rect, stream=buf.getvalue())
    out.save(dst, garbage=3, deflate=True)
    out.close()
    doc.close()


# ---------------------------------------------------------------- OCR と文字層
def ocr_pages(src, log=print):
    """scan-ocr の解析器で、各ページを 200dpi で OCR する。ページごとの結果（dict）のリストを返す。"""
    if str(SCAN_OCR) not in sys.path:
        sys.path.insert(0, str(SCAN_OCR))
    from ocr_pipeline import get_analyzer            # scan-ocr
    from yomitoku.data.functions import load_pdf
    analyzer = get_analyzer(lite=False, device="cpu")
    imgs = load_pdf(Path(src), dpi=200)
    pages = []
    for i, img in enumerate(imgs):
        result, _, _ = analyzer(img)
        pages.append({"px_w": int(img.shape[1]), "px_h": int(img.shape[0]), **result.model_dump()})
        log(f"  OCR {i + 1}/{len(imgs)}ページ")
    return pages


def _rect(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def _contained(outer, inner, threshold=0.7):
    ix1, iy1, ix2, iy2 = max(outer[0], inner[0]), max(outer[1], inner[1]), min(outer[2], inner[2]), min(outer[3], inner[3])
    if ix2 <= ix1 or iy2 <= iy1:
        return False
    return (ix2 - ix1) * (iy2 - iy1) / max(1, (inner[2] - inner[0]) * (inner[3] - inner[1])) >= threshold


def _reading_order(page):
    """OCR の行を、段落・表のセル・図の中の段落の順に並べる（どこにも属さない行は最後）。"""
    boxes = [(p.get("order") if p.get("order") is not None else 10 ** 6, "", p["box"], p.get("direction")) for p in page.get("paragraphs", [])]
    for t in page.get("tables", []):
        boxes += [(t["order"], f"{c['row']:04d}{c['col']:04d}", c["box"], "horizontal") for c in t.get("cells", [])]
    for f in page.get("figures", []):
        boxes += [(f["order"] if f.get("order") is not None else 10 ** 6, f"{k:04d}", p["box"], p.get("direction")) for k, p in enumerate(f.get("paragraphs", []))]
    boxes.sort(key=lambda b: (b[0], b[1]))
    words, used, out = page.get("words", []), set(), []
    for _, _, box, direction in boxes:
        inside = [(i, w) for i, w in enumerate(words) if i not in used and _contained(box, _rect(w["points"]))]
        inside.sort(key=(lambda iw: (-_rect(iw[1]["points"])[0], _rect(iw[1]["points"])[1])) if direction == "vertical"
                    else (lambda iw: (_rect(iw[1]["points"])[1], _rect(iw[1]["points"])[0])))
        used.update(i for i, _ in inside)
        out += [w for _, w in inside]
    rest = sorted(((i, w) for i, w in enumerate(words) if i not in used), key=lambda iw: (_rect(iw[1]["points"])[1], _rect(iw[1]["points"])[0]))
    return out + [w for _, w in rest]


def add_text_layer(src, pages, dst):
    """src の各ページに、OCR の文字を透明（render_mode=3）で重ねて dst に保存する。画像には触らない。"""
    import fitz
    import yomitoku
    font_file = Path(yomitoku.__file__).parent / "resource" / "MPLUS1p-Medium.ttf"
    font = fitz.Font(fontfile=str(font_file))
    doc = fitz.open(src)
    for page, data in zip(doc, pages):
        if page.rotation:
            page.remove_rotation()      # ページ回転（180°・270°）を、見た目を変えずに取り除く。回転したままだと、文字の向きと位置がずれる
        sx, sy = page.rect.width / data["px_w"], page.rect.height / data["px_h"]      # OCR の画素 → PDF の pt
        page.insert_font(fontname="mplus", fontfile=str(font_file))
        for w in _reading_order(data):
            text = (w.get("content") or "").strip()
            x1, y1, x2, y2 = _rect(w["points"])
            bw, bh = (x2 - x1) * sx, (y2 - y1) * sy
            if not text or bw <= 0 or bh <= 0:
                continue
            w1 = font.text_length(text, fontsize=1)
            fs = max(1.0, min(bw / w1 if w1 else bh, bh * 1.3))
            page.insert_text((x1 * sx, y1 * sy + bh * 0.82), text, fontname="mplus", fontsize=fs, render_mode=3)
    doc.subset_fonts()                                   # 使った文字の字形だけにする（フォント全体は入れない）
    doc.save(dst, garbage=3, deflate=True)
    doc.close()


def add_ocr_text_layer(src, dst, log=print):
    add_text_layer(src, ocr_pages(src, log), dst)
