# -*- coding: utf-8 -*-
"""
裁判文書ページ（trial/・agm/）向けの2つの機能をon_page_markdownで行うフック。

1. 項番マーカー（:N X[#anchor名]:）の展開
   :N X: 本文  → <p class="padN {クラス}">本文</p>
   N = 0〜9のインデント段数（実データはpad1〜pad6が中心）。
   X = d(.doc, Nは無視) / i(.idt) / h・h2・h3(.hg-idt/.hg-idt2/.hg-idt3)。
   N=0の場合はpadNクラスを付けない（実データの慣習：.doc単独 / .hg-idt単独）。
   :N X#anchor名: の形にすると、開始タグ直後に<a name="anchor名"></a>を自動挿入する
   （386箇所の既存アンカーで最も多い「開始タグ直後・独立した行」の配置に合わせている）。
   マッチしない行・ブロックはそのまま素通りするので、既存の生HTML（center/smaller/
   doc-gap-top等の稀な修飾を含む）と共存できる。詳細はDOC_INDENT_PREPROCESSOR_PLAN.md参照。

   ブロックは空行区切り＝1段落として扱う（CommonMark同様、ブロック内の単一改行はソフト改行として
   半角スペースに畳む）。この規約はsidenote-pdf-doc側のMarkdown取り込み・書き出しと揃えてある。

2. 目次パネルの自動非表示
   trial/agm系ページは、Material標準の目次パネル（右カラム）の代わりにサイドノートを
   同じ場所（.md-sidebar--secondary）に出す設計のため、front matterへhide:tocを手で書かなくても
   自動で効くようにする（新しいtrialページを追加しても手打ち不要にするため）。
"""
import re

# h2/h3をhより先に置き、"h2"の2文字目がhにマッチして"2"だけ残る、といった誤マッチを防ぐ。
MARKER_RE = re.compile(
    r'^[ \t]*:(?P<n>[0-9])(?P<kind>h2|h3|h|i|d)(?:#(?P<anchor>[A-Za-z0-9_\-]+))?:[ \t]*'
)

TRIAL_PATH_PREFIXES = ("trial/", "agm/")
TRIAL_PATH_EXCLUDE = ("trial/index.md", "agm/index.md")


def _class_for(n, kind):
    pad = f"pad{n}" if n > 0 else None
    if kind == "d":
        return "doc"
    if kind == "i":
        return f"{pad} idt" if pad else "doc idt"
    hg = {"h": "hg-idt", "h2": "hg-idt2", "h3": "hg-idt3"}[kind]
    return f"{pad} {hg}" if pad else hg


def _expand_block(block):
    m = MARKER_RE.match(block)
    if not m:
        return block   # マーカーでなければ触らない（生HTML・通常のMarkdownと共存させる）
    n = int(m.group("n"))
    kind = m.group("kind")
    anchor = m.group("anchor")
    # マーカーの後ろ（複数行にまたがっていてもよい）を1つの段落テキストとして扱う。
    text = block[m.end():].replace("\n", " ").strip()
    cls = _class_for(n, kind)
    anchor_html = f'<a name="{anchor}"></a>\n' if anchor else ""
    return f'<p class="{cls}">\n{anchor_html}{text}\n</p>'


def _is_trial_page(src):
    return src.startswith(TRIAL_PATH_PREFIXES) and src not in TRIAL_PATH_EXCLUDE


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_path.replace("\\", "/")
    if not _is_trial_page(src):
        return markdown

    hide = page.meta.setdefault("hide", [])
    if "toc" not in hide:
        hide.append("toc")

    blocks = re.split(r"\n{2,}", markdown.strip())
    return "\n\n".join(_expand_block(b) for b in blocks)
