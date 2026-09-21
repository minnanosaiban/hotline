#!/usr/bin/env python
"""eneos-saiban の argument.md にある「認否のサイドノート」を、trial の書面（docs/trial/md/*.md.txt）へ取り込む。

argument.md（Jupyter Book）では、認否は本文の直前の {margin} ブロックに書いてある。
trial 側では、サイドノート作成ツールの「ウェブ用」書き出しと同じ形（段落の直後の <aside class="sn-note">）に直す。
  - merge … すでに trial にある書面（本文は検証済みなので触らない）へ、ノートだけを差し込む
  - new   … trial にまだ無い書面を argument.md の本文から作る（目次の復元・書式の変換つき）

一度きりの移行用（2026-09-21 に実行済み）。merge の書面にすでにサイドノートがあれば、二重に足さないよう止まる。
今後の書面は、サイドノートアプリの「ウェブ用」書き出しを貼る（README の「書面の追加・更新」）。

  python scripts/import_argument.py [出力先フォルダ]      （既定は docs/trial/md。別の場所へ出して確かめたいときに指定する）
"""
import html
import re
import sys
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path

SRC = Path(r'C:\minnanosaiban\eneos-saiban\argument.md')       # 元の主張書面と認否（Jupyter Book のソース）
ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / 'docs' / 'trial' / 'md'

# (argument.md の章番号, trial での id, merge | new)
JOBS = [
    ('02', 'toben', 'merge'), ('06', 'hikoku2', 'merge'), ('09', 'hikoku3', 'merge'),
    ('11', 'hikoku4', 'merge'), ('21', 'kouso', 'merge'),
    ('01', 'sojou', 'new'), ('05', 'dai1', 'new'), ('08', 'dai2', 'new'), ('10', 'dai3', 'new'),
    ('13', 'dai4', 'new'), ('14', 'kyushakumei', 'new'), ('15', 'soufu', 'new'),
]

FENCE = re.compile(r'^`````\{margin\}[ \t]*\n(.*?)^`````[ \t]*$\n?', re.S | re.M)
ENTRY = re.compile(r'<p class="margin-set[^"]*">')
LOG = []


def log(msg):
    LOG.append(msg)


# ---------------------------------------------------------------- 読み込み
def load_sections():
    text = SRC.read_text(encoding='utf-8')
    ms = list(re.finditer(r'(?m)^## (\d\d)　(.*)\n---\n', text))
    return {m.group(1): (m.group(2), text[m.end():(ms[i + 1].start() if i + 1 < len(ms) else len(text))])
            for i, m in enumerate(ms)}


def norm(s):
    """比較用: タグと空白を除いた本文"""
    return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', '', s)))


# ---------------------------------------------------------------- ノート
class NoteHtml(HTMLParser):
    """ノート1項目の HTML を整える。
    元の <p class="margin-set"><span class="margin-text"> の外枠を外し、閉じ忘れ・余分な閉じタグを直し、
    クラスを trial 側に合わせる（sphinx-design のバッジ → sn-badge、内部リンクのクラス除去）。"""

    def __init__(self, entry_id):
        super().__init__(convert_charrefs=False)
        self.out, self.stack, self.entry_id = [], [], entry_id
        self.missing_open_b = False

    def handle_starttag(self, tag, attrs):
        a, cls = dict(attrs), dict(attrs).get('class', '').split()
        if tag == 'span' and 'margin-text' in cls:
            self.stack.append((tag, False))        # 外枠。出力しない
            return
        if tag == 'br':
            self.out.append('<br>')
            return
        if tag == 'span' and 'sd-badge' in cls:
            self.out.append('<span class="sn-badge">')
        elif tag == 'span' and cls and set(cls) <= {'strong-rd', 'strong-rd-hover'}:
            self.out.append('<span class="%s">' % ' '.join(cls))
        elif tag == 'i' and cls:
            self.out.append('<i class="%s">' % ' '.join(cls))
        elif tag == 'a':
            href = (a.get('href') or '').replace('kansai.html#', '#')
            self.out.append('<a href="%s">' % href)
        elif tag in ('b', 'u') and not cls:
            self.out.append('<%s>' % tag)
        else:
            raise ValueError('想定外のタグ %s %s（%s）' % (tag, attrs, self.entry_id))
        self.stack.append((tag, True))

    def handle_endtag(self, tag):
        idx = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == tag), None)
        if idx is None:                            # 開きの無い閉じタグ（元の書き間違い）は捨てる
            if tag == 'b':
                self.missing_open_b = True
            log('  余分な </%s> を除いた（%s）' % (tag, self.entry_id))
            return
        while len(self.stack) > idx:
            t, emit = self.stack.pop()
            if emit:
                self.out.append('</%s>' % t)

    def handle_data(self, data):
        self.out.append(data)

    def handle_entityref(self, name):
        self.out.append('&%s;' % name)

    def handle_charref(self, name):
        self.out.append('&#%s;' % name)

    def result(self):
        self.close()
        while self.stack:
            t, emit = self.stack.pop()
            if emit:
                self.out.append('</%s>' % t)
        s = ''.join(self.out).strip()
        if self.missing_open_b:                    # ●「…」まで</b> のように、開きの <b> が抜けている（先頭から太字のつもり）
            s = '<b>' + s
        return re.sub(r'(?:<br>\s*)+$', '', s)     # 末尾の改行は、項目をつなぐ <br> とだぶるので除く


def build_aside(fence_body, tag):
    entries = ENTRY.split(fence_body)[1:]
    parts = []
    for n, e in enumerate(entries, 1):
        joined = ''
        for line in (l.strip() for l in e.strip().splitlines()):
            if joined and not joined.endswith('<br>'):
                joined += ' '
            joined += line
        p = NoteHtml('%s ノート%s' % (tag, n))
        p.feed(joined)
        parts.append(p.result())
    return '<aside class="sn-note">' + '<br>'.join(parts) + '</aside>'


# ---------------------------------------------------------------- 段落（merge 用）
P_OPEN = re.compile(r'<p\b[^>]*>')
P_END = re.compile(r'</p>|<p\b|<div\b|</div>|<table\b|<aside\b|\Z')


def paragraphs(text):
    """[(挿入位置, 正規化した本文)]。閉じてある <p> は </p> の直後、閉じ忘れは次のブロックの直前（本文末の空白の手前）"""
    out = []
    for m in P_OPEN.finditer(text):
        e = P_END.search(text, m.end())
        inner = text[m.end():e.start()]
        end = e.end() if e.group(0) == '</p>' else m.end() + len(inner.rstrip())
        out.append((end, norm(inner), m.start()))
    return out


def argument_notes(body):
    """[(ノートの HTML, 直後の段落の正規化本文, 直後の要素の種類)]"""
    notes = []
    for f in FENCE.finditer(body):
        rest = body[f.end():].lstrip()
        if rest.startswith('`````{margin}'):
            kind, key = 'fence', None
        else:
            m = P_OPEN.match(rest)
            if m:
                e = P_END.search(rest, m.end())
                kind, key = 'p', norm(rest[m.end():e.start()])
            elif rest.startswith('<div'):
                q = P_OPEN.search(rest)
                e = P_END.search(rest, q.end())
                kind, key = 'div', norm(rest[q.end():e.start()])
            else:
                raise ValueError('ノートの直後が想定外: %r' % rest[:60])
        notes.append([f.group(1), kind, key])
    # 連続するノートは、いちばん後ろの段落に付ける（同じ段落に、順番のまま並べる）
    for i in range(len(notes) - 1, -1, -1):
        if notes[i][1] == 'fence':
            notes[i][1], notes[i][2] = notes[i + 1][1], notes[i + 1][2]
    return notes


def similarity(a, b):
    """段落どうしの近さ。一致=1、片方がもう片方の書き出し（<br> の前後で段落を分けてある場合）=0.95、それ以外は文字列の類似度"""
    if a == b:
        return 1.0
    n = min(len(a), len(b))
    if n >= 12 and a[:n] == b[:n]:
        return 0.95
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def merge_notes(nn, tid, body):
    path = MD / ('%s.md.txt' % tid)
    text = path.read_text(encoding='utf-8')
    if '<aside class="sn-note">' in text:
        raise SystemExit('%s.md.txt には、すでにサイドノートが入っている（二重に足さないよう、ここで止める）' % tid)
    paras = paragraphs(text)
    inserts = {}                                   # 挿入位置 -> [aside]
    cursor = 0
    for n, (fence_body, kind, key) in enumerate(argument_notes(body), 1):
        best = None
        for j in range(cursor, len(paras)):
            ratio = similarity(paras[j][1], key)
            if best is None or ratio > best[0]:
                best = (ratio, j)
            if ratio == 1.0:
                break
        if best is None or best[0] < 0.85:
            raise ValueError('%s: ノート%d の直後の段落が見つからない: %s' % (tid, n, key[:40]))
        ratio, j = best
        cursor = j
        if ratio < 1.0:
            log('  %s ノート%d: 段落が完全には一致しない（類似度 %.3f）\n      argument: %s\n      %s: %s'
                % (tid, n, ratio, key[:50], tid, paras[j][1][:50]))
        aside = build_aside(fence_body, '%s ノート%d' % (tid, n))
        if kind == 'div':                          # 「← ＥＮＥＯＳの主張」など、囲み(div)の頭に付くノート
            start = paras[j][2]
            before = text[:start].rstrip()
            if not before.endswith('<div class="strong-rd-hover">'):
                log('  %s ノート%d: div の頭に付けるはずが、直前が div ではない → 段落の後ろに付けた' % (tid, n))
                inserts.setdefault(paras[j][0], []).append(aside)
            else:
                inserts.setdefault(len(before), []).append(aside)
        else:
            inserts.setdefault(paras[j][0], []).append(aside)
    for pos in sorted(inserts, reverse=True):
        text = text[:pos].rstrip() + '\n\n' + '\n\n'.join(inserts[pos]) + '\n\n' + text[pos:].lstrip()
    return text


# ---------------------------------------------------------------- 本文の変換（new 用）
TOKEN = re.compile(r'''
    (?P<note>@@NOTE(?P<n>\d+)@@)
  | (?P<table><table\b.*?</table>)
  | (?P<p><p\b[^>]*>.*?(?:</p>|(?=<p\b|<div\b|</div>|<table\b|@@NOTE|\Z)))
  | (?P<div><div\b[^>]*>)
  | (?P<enddiv></div>)
''', re.S | re.X)


def map_p_open(open_tag, first):
    """<p …> の class/style を、trial の書き方（doc / idt / hg-idt / padN / doc-gap-top / smaller）へ"""
    cls = re.search(r'class="([^"]*)"', open_tag)
    style = re.search(r'style="([^"]*)"', open_tag)
    classes = [c for c in (cls.group(1).split() if cls else [])]
    st = style.group(1) if style else ''
    center = 'text-align: center' in st
    if 'card-text' in classes:
        classes.remove('card-text')
    if not any(c in classes for c in ('doc', 'idt', 'hg-idt')):
        classes.insert(0 if not any(c.startswith('pad') for c in classes) else len(classes), 'doc')
    if 'margin-top: 1.6em' in st and not first:
        classes.append('doc-gap-top')
    if center:
        classes.append('center')
    if 'font-size: 0.85em' in st:
        classes.append('smaller')
    return '<p class="%s">' % ' '.join(classes)


def map_div_open(open_tag):
    cls = re.search(r'class="([^"]*)"', open_tag)
    classes = cls.group(1).split() if cls else []
    if 'card_01' in classes:
        return '<div class="card">'
    if 'base' in classes:
        pads = [c for c in classes if re.fullmatch(r'pad\d', c)]
        if pads:
            n = int(pads[0][3:]) - 1                # base の左余白ぶん、1つ小さくする（hotline 側の既存書面と同じ）
            return '<div class="pad%d">' % n if n > 0 else '<div>'
        return '<div>'
    if classes:
        return '<div class="%s">' % ' '.join(classes)
    return open_tag


def join_lines(inner):
    """段落の中の折り返し（元の Markdown の行末）をつなぐ。日本語どうしの間に空白を入れない"""
    def rep(m):
        a, b = m.group(1), m.group(2)
        return a + b if (ord(a) > 127 or a == '>' or ord(b) > 127 or b == '<') else a + ' ' + b
    return re.sub(r'(\S)[ \t]*\n[ \t]*(\S)', rep, inner.strip())


def card_entries(card):
    ents = []
    for m in re.finditer(r'<p class="card-text pad(\d)[^"]*"[^>]*>\s*<a [^>]*href="#([^"]+)">', card):
        ents.append((int(m.group(1)), m.group(2)))
    return ents


def heading_of(body, anchor):
    m = re.search(r'<a name="%s">\s*</a>\s*(?:</p>)?\s*<b>(.*?)</b>' % re.escape(anchor), body, re.S)
    if not m:
        raise ValueError('見出しが見つからない: %s' % anchor)
    return join_lines(m.group(1))


def build_new(nn, tid, body):
    m = re.match(r'\s*(?:<a name="[^"]*"></a>\s*)?<i class="fa-regular fa-file-pdf[^\n]*\n', body)
    if m:
        body = body[m.end():]
    card = None
    m = re.match(r'\s*<div class="base"[^>]*>\s*<div class="card_01">(.*?)</div>\s*</div>[ \t]*\n', body, re.S)
    if m:
        card, body = m.group(1), body[m.end():]

    asides = []
    def stash(f):
        asides.append(build_aside(f.group(1), '%s ノート%d' % (tid, len(asides) + 1)))
        return '\n@@NOTE%d@@\n' % (len(asides) - 1)
    body = FENCE.sub(stash, body)

    blocks, pending, pos, first = [], [], 0, True     # blocks: ('p', html, 本文) など
    for m in TOKEN.finditer(body):
        gap = body[pos:m.start()].strip()
        if gap:
            log('  %s: 想定外の本文（変換せずに残した）: %r' % (tid, gap[:60]))
            blocks.append(('raw', gap, ''))
        pos = m.end()
        if m.group('note'):
            pending.append(asides[int(m.group('n'))])
        elif m.group('table'):
            blocks.append(('table', m.group('table').strip(), ''))
            blocks.extend(('aside', a, '') for a in pending); pending = []
        elif m.group('p'):
            s = m.group('p')
            open_tag = P_OPEN.match(s).group(0)
            inner = re.sub(r'</p>\s*$', '', s[len(open_tag):])
            blocks.append(('p', '%s\n%s\n</p>' % (map_p_open(re.sub(r'<p\s+', '<p ', open_tag), first), join_lines(inner)),
                           norm(inner)))
            first = False
            blocks.extend(('aside', a, '') for a in pending); pending = []
        elif m.group('div'):
            blocks.append(('div', map_div_open(m.group('div')), ''))
            if pending:
                log('  %s: ノートの直後が div（囲みの頭）→ 直後の段落に付ける' % tid)
        elif m.group('enddiv'):
            blocks.append(('div', '</div>', ''))
    if body[pos:].strip():
        log('  %s: 末尾に想定外の本文: %r' % (tid, body[pos:].strip()[:60]))
    if pending:
        raise ValueError('%s: 後ろに段落の無いノートがある' % tid)

    # ノートが div の直後に来ていたものは、その中の最初の段落の後ろに回っていないので、ここでは扱わない（起きたら log に出る）
    # 目次（「目次」の次が「≪ 中略 ≫」なら、カードの目次から復元する）
    for i, b in enumerate(blocks[:-1]):
        if b[0] == 'p' and b[2] == '目次' and blocks[i + 1][0] == 'p' and blocks[i + 1][2] == '≪中略≫':
            if not card:
                log('  %s: 目次が「≪ 中略 ≫」だが、復元に使うカードが無い' % tid)
                break
            toc = []
            for k, anchor in card_entries(card):
                toc.append('<p class="pad%d hg-idt">\n%s\n</p>' % (k + 1, re.sub(r'</?b>', '', heading_of(body, anchor))))
            blocks[i + 1] = ('p', '\n\n'.join(toc), '')
            log('  %s: 目次を復元（%d項目）' % (tid, len(toc)))
            break
    return '\n\n'.join(b[1] for b in blocks) + '\n'


# ---------------------------------------------------------------- 検証
def strip_asides(text):
    return re.sub(r'\s*<aside class="sn-note">.*?</aside>\s*', ' ', text, flags=re.S)


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else MD
    out_dir.mkdir(parents=True, exist_ok=True)
    secs = load_sections()
    for nn, tid, kind in JOBS:
        title, body = secs[nn]
        before = (MD / ('%s.md.txt' % tid)).read_text(encoding='utf-8') if kind == 'merge' else ''
        text = merge_notes(nn, tid, body) if kind == 'merge' else build_new(nn, tid, body)
        n_fence = len(FENCE.findall(body))
        n_aside = text.count('<aside class="sn-note">')
        (out_dir / ('%s.md.txt' % tid)).write_text(text, encoding='utf-8', newline='\n')
        status = 'OK' if n_fence == n_aside else '!! 数が合わない'
        print('%s %-12s %-6s ノート %3d → aside %3d  %s' % (nn, tid, kind, n_fence, n_aside, status))
        if kind == 'merge':                        # ノートを除けば、元の本文と同じであること
            rest = strip_asides(text)
            if re.sub(r'\s+', '', rest) != re.sub(r'\s+', '', before):
                print('   !! ノートを除くと、元の本文と一致しない')
    if LOG:
        print('\n--- 記録 ---')
        print('\n'.join(LOG))


if __name__ == '__main__':
    main()
