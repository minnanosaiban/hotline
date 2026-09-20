# hotline-mkdocs

`https://minnanosaiban.github.io/hotline/`（MkDocs Material）から、「ＥＮＥＯＳの内部通報制度をめぐる訴訟について」だけを切り出す試作。
株価分析（blog）と運営者ページは別サイト（株価サイト側）へ分離する前提なので、ここには持ち込んでいない。元の `hotline` リポジトリには一切触れていない。

## 元の hotline との違い

- **株価分析（blog/）を除いた**。nav・フックのブログ分岐・`docs/blog/`・ブログ用CSS（`10-blog-reset.css` は廃止。判決ページの h2 と `.repo-link` だけ `11-trial.css` の先頭へ統合）がなくなった
- **運営者ページ（about/）も持たない**（株価サイト側へ）。フッターの「運営者について」のリンク先は `mkdocs.yml` の `extra.about_url` の1か所（今は仮に現行の URL）
- **NotebookLM の音声解説は載せない**（とりあえず。判決ページ末尾のセクションと、旧 eneos ページのカードを外した）
- **目次（Toc）を完全に出さない**。右のサイドバーだけでなく、スマホのメニュー内の目次も。Material の `partials/toc.html` を空にして実現している
  （右カラムは CSS でも `display: none`。ページに `hide: toc` を書き忘れても、空の枠が幅を取らない）。目次の自動退避 JS（`toc-toggle.js`）とその CSS は削除した
- **裁判文書は `trial/index.md` の1ページに集約**（書面ごとのアコーディオン）。本文は `docs/trial/md/<id>.md.txt` に置き、
  `:include:` でページに取り込む。生ファイルは静的に公開されるので、`.md` ボタン（コピー／ダウンロード）の元にもなる
- 旧 `trial/eneos/`・`trial/whistleblower/` は、一覧ページへ転送するだけのページ（`#アンカー`も引き継ぐ）にした
- フック `add_blog_class.py` は `add_body_class.py` に改名（中身は trial/・agm/ の body クラス付与と Swiper 注入だけ）
- `requirements.txt` は使っている3つだけ（mkdocs・mkdocs-material・mkdocs-glightbox）
- 音声ファイル（`docs/img/*.m4a`・`*.wav`、約100MB）・`deploy.bat`・空の `includes/sitemap.md` は持ち込んでいない

整理の前後で、Home・agm・書面一覧・見本帳の全要素（位置・サイズ・主要スタイル20項目）が一致することを、同じ条件のブラウザで比較して確認した
（判決ページは末尾の音声セクションが減っただけ）。

## 動かし方

```
pip install -r requirements.txt
python -m mkdocs serve        # http://localhost:8000/hotline/
python -m mkdocs build        # site/ に出力
```

## 書面の追加・更新

本文は**サイドノートアプリ**（sidenote-pdf-web、いずれ sidenote に統合）で作る。

1. アプリの「ウェブ用」書き出しをコピーして、`docs/trial/md/<id>.md.txt` に貼る（既にあるファイルなら上書き）
2. 書面を増やすときだけ、`docs/trial/index.md` の該当する側（原告側・被告側…）の `<div class="doc-rows">` に、次のブロックを1つ足す

```html
<details class="doc-acc" id="<id>" data-md="md/<id>.md.txt" data-pdf="<PDFのURL>" data-summary="<要約>" markdown>
<summary>書面名</summary>
<div class="doc-body" markdown>

:include: md/<id>.md.txt

</div>
</details>
```

`data-pdf`・`data-summary` は無ければ書かない（ボタンがグレーになる）。ボタン・開閉マーク・サイドノートの位置は `docs/js/doc-accordion.js` が付ける。

## 本文の書式（サイドノートアプリの書き出し）

| 形式 | 中身 | 扱い |
|---|---|---|
| ウェブ用 | 素のMarkdown＋`<aside class="sn-note">` | そのまま描画（CSSは `14-doc-accordion.css`）。**今後はこちら** |
| hotline用 | `:N X#id:` マーカー＋`<aside class="sidenote">` | `overrides/hooks/doc_indent.py` が展開。今の11書面はこの形式 |

今の11書面は、元の `eneos.md`・`whistleblower.md` を書面ごとに分割したもの（hotline 形式）。**全書面をウェブ用書き出しに替え終えたら、
`doc_indent.py`（実効88行）は不要**になる（`:include:` は、mkdocs.yml で有効な `pymdownx.snippets` の `--8<--` に置き換えられる）。

目次を出さない構成なので、貼った本文の見出しが目次に混ざる心配はない。

## 未対応・要判断

- **ホスティング・URL**: `site_url` と各ページの `url:`／`image:`（OGP）は、現行の `https://minnanosaiban.github.io/hotline/` のまま。どちらのサイトが `/hotline/` を引き継ぐかも未定
- **運営者ページのリンク先**: `mkdocs.yml` の `extra.about_url` は仮（現行の `/hotline/about/`）。株価サイト側の URL が決まったら差し替える
- 見本帳（`styleguide.md`）は、音声カードや `.repo-link` などの部品例を含んだまま（音声用のCSSは `05-card.css` に残っている）
- `mkdocs.yml` に、使っていない設定のコメントアウトが多く残っている（元のまま）
- `DESIGN_SYSTEM.md` は元のまま（ブログの記述を含む）
