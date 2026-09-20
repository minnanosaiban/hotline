# 文書インデントのクラス化 — 案A（preprocessor方式）設計メモ

作成: 2026-08-19。DESIGN_SYSTEM.mdの「4. 裁判文書特有の型」で挙げた`.doc`/`.idt`/`.hg-idt*`の煩雑さ対策として検討した案の一つ。attr_list案（`{: .class }`記法）は`nl2br`拡張との組み合わせで段落末尾に余計な`<br>`が入る不具合が起き、かつ行数もさほど減らなかったため見送り、次の一手として検討していた。

**2026-08-20 実装済み**：下記「後で詰める必要がある論点」を反映し、`hooks:`方式（このメモの「簡易版」）で`overrides/hooks/doc_indent.py`として実装した。実際の記法・詰めた論点は以下のとおり：

- マーカーは`:N X:`（N=0〜9のインデント段数、X=`d`(.doc)/`i`(.idt)/`h`・`h2`・`h3`(.hg-idt/.hg-idt2/.hg-idt3)）。N=0の場合はpadNクラスを付けない（実データの`.doc`単独・`.hg-idt`単独の慣習に合わせた）。
- アンカーは`:N X#anchor名:`で開始タグ直後に`<a name="anchor名"></a>`を自動挿入（386箇所中もっとも多い配置パターンに統一）。
- `center`／`smaller`／`doc-gap-top`／`doc-gap-bottom`はマーカー化せず、想定どおり生HTMLのまま（マーカーにマッチしない行は素通りするため共存可能）。
- 複数行への折り返しは、空行区切り＝1段落・ブロック内の単一改行はソフト改行として半角スペースに畳む方式（CommonMark準拠、sidenote-pdf-doc側のMarkdown取り込み・書き出しと規約を揃えた）。
- 併せて、trial/agm系ページの目次パネル（`.md-sidebar--secondary`）を同じフックで自動的に`hide: toc`にし、その余白にサイドノート（`<aside class="sidenote">`、生HTMLのまま）を出す設計にした。詳細は`docs/css/11-trial.css`のコメント参照。
- 書く側（sidenote-pdf-docの「hotline向け書き出し」）がこのマーカー＋サイドノートHTMLを自動生成するため、手打ちは例外の手直しのみで済む想定。

**2026-08-20 既存3ファイルの置き換えも完了**：`trial/eneos.md`・`whistleblower.md`・`judgement_2025.md`（386箇所のアンカー全て）を、変換スクリプト（`padN`＋`doc`/`idt`/`hg-idt(2/3)`の組み合わせだけを対象、`center`等の修飾付き段落やpadN+doc（無印）のようなマーカーで表現できない組み合わせは自動でスキップし生HTMLのまま残す）で新記法へ実際に置き換えた。検証は「レンダリング後のHTMLから`<p>`ごとの本文を順序付きで取り出し、変換前後で1対1比較する」方式（生の行diffは`</p>`の位置がほぼ全段落で変わるため大量の見かけ上の差分が出て使い物にならなかった）。3ファイルとも段落列が完全一致、アンカー数も252+112+22=386で一致することを確認済み。作業中に2つのバグを発見・修正した：①マーカー行同士が空行無しで隣接しているとdoc_indent.py側のブロック分割に失敗し後続行が展開されずリテラル表示される（変換スクリプト側で前後に空行を強制的に補う処理を追加）、②全角スペース（U+3000、「１．１　目的」等の見出し番号後によく使われる）を`\s+`の正規表現で畳むと半角スペースに変わってしまう（畳む対象を「改行を挟む半角空白/タブのみ」に限定して修正）。バックアップはリポジトリ外（スクラッチ領域）に保存、gitの元コミットも未変更のまま残っている。

## 「preprocessor」の位置づけ

Python-Markdown（mkdocsが内部で使っているMarkdownエンジン）の処理は大まかに5段階です。

1. **preprocessor** — Markdownをブロックに分割する前に、生のテキスト行をそのまま加工する段階
2. block parser — 空行区切りでブロック（段落・リスト等）に分割
3. inline processing — `**太字**`やリンクなどインライン記法を変換
4. treeprocessor — できあがったHTML木を後加工（attr_listはここで動いていたため、前回`nl2br`の`<br>`と衝突した）
5. postprocessor / serializer — 最終HTML文字列化

preprocessorは一番手前＝**まだMarkdownとして解釈される前のただの文字列**を相手にするので、「行頭のマーカーを見て、その行をまるごと`<p class="...">...</p>`という完成品のHTML行に置き換える」という単純な文字列置換で済む。置き換えた結果は最初から生のHTMLとして扱われるため、`nl2br`のような「Markdown段落の中身」に効く拡張がそもそも触れない。attr_list案での不具合は原理的に起きない、というのはこの段階の違いによる。

## 具体的な形（イメージ）

```python
import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

# 例: ":2h: 本文" → pad2 + hg-idt、":0d: 本文" → doc（0は無印略可にしてもよい）
MARKER_RE = re.compile(r'^:(\d)([dih]):\s?(.*)$')
STYLE_NAME = {'d': 'doc', 'i': 'idt', 'h': 'hg-idt'}

class DocIndentPreprocessor(Preprocessor):
    def run(self, lines):
        out = []
        for line in lines:
            m = MARKER_RE.match(line)
            if m:
                depth, style, text = m.groups()
                cls = STYLE_NAME[style] if depth == '0' else f'pad{depth} {STYLE_NAME[style]}'
                out.append(f'<p class="{cls}">{text}</p>')
            else:
                out.append(line)
        return out

class DocIndentExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(DocIndentPreprocessor(md), 'doc_indent', 25)
```

行内の`<b>`・`<a name="...">`・`<sup>`等はそのまま文字列として素通りするので、今までどおり生HTMLで書ける（`**太字**`に変える必要はない）。

## mkdocsへの組み込み方は2通り

- 上記のようにPython-Markdown拡張として書き、`mkdocs.yml`の`markdown_extensions:`にモジュールパスを追加する正攻法
- もしくは、mkdocs 1.4以降にある**`hooks:`機能**（`mkdocs.yml`に`hooks: [hooks/doc_indent.py]`と書き、そのファイルに`def on_page_markdown(markdown, page, config, files): return 加工後の文字列`を定義するだけ）を使う簡易版。拡張クラスの登録手続きが要らない分、今回のような「行を書き換えるだけ」の用途には軽くて向いている。実装するとしたらこちらを先に試す。

## 後で詰める必要がある論点

- マーカー記法そのもの（`:2h:`のような形が読みやすいか、他の候補があるか）
- `center`／`smaller`／`doc-gap-top`／`doc-gap-bottom`のような修飾クラスをどう表現するか（マーカーに文字を足す／別記号を用意する等）
- 1段落が原文で複数行に折り返されているケースの扱い（1行に結合して書く運用にするか、継続行を拾う処理を入れるか）
- テストはmkdocsを介さず`markdown.markdown()`に拡張だけ噛ませて出力を確認してから、実ファイルに適用する
