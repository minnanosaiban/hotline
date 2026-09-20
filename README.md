# eneos-hotline

`https://minnanosaiban.github.io/hotline/`（MkDocs Material）から、「ＥＮＥＯＳの内部通報制度をめぐる訴訟について」だけを切り出したサイト。
株価分析（blog）と運営者ページは別サイト（株価サイト側）へ分離する前提なので、ここには持ち込んでいない。元の `hotline` リポジトリには一切触れていない。

**ビルドは Zensical が主、MkDocs 1.6.1 は予備。** Python フックもプラグインも使わない作りなので、どちらでも同じ見た目になる（下の「検証」）。

## 動かし方

初回だけ、仮想環境を作って Zensical を入れる（バージョンは `requirements.txt` で固定）。

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

| 何をする | 方法 |
|---|---|
| ローカルで見る | `serve.bat`（`http://localhost:8000/`） |
| 公開用ファイルを作る | `build.bat`（`site/` に出力） |

`--8<--` での本文の取り込みは「コマンドを実行したフォルダ」基準なので、必ずこのフォルダで動かす（`.bat` は `cd` してから動かしている）。
間違えたときは、本文が黙って抜けるのではなく `Snippet at path … could not be found` で止まる（`check_paths: true`）。

### 予備: MkDocs でビルドする

```
pip install -r requirements-mkdocs.txt
python -m mkdocs serve       # http://localhost:8000/hotline/
python -m mkdocs build
```

- Material for MkDocs は **2026-11-05 で更新終了**（保守モード）。MkDocs 2.0 はプラグイン機構ごと作り直しで、この構成とは互換がない。`requirements-mkdocs.txt` は `mkdocs<2` に固定してある
- Zensical は 0.0.x（1.0 前）。**上げるときは `requirements.txt` を書き換えて、下の「設計ルール」の落とし穴に触れていないか、ビルド結果を見比べてから**

## 元の hotline との違い

- **株価分析（blog/）を除いた**。nav・ブログ用CSS（`10-blog-reset.css` は廃止。判決ページの h2 と `.repo-link` だけ `11-trial.css` の先頭へ統合）・`docs/blog/` がなくなった
- **運営者ページ（about/）も持たない**（株価サイト側へ）。フッターの「運営者について」のリンク先は `mkdocs.yml` の `extra.about_url` の1か所（今は仮に現行の URL）
- **NotebookLM の音声解説は載せない**（とりあえず。判決ページ末尾のセクションと、旧 eneos ページのカードを外した）。音声ファイル（`*.m4a`・`*.wav`、約100MB）も持ち込んでいない
- **目次（Toc）を完全に出さない**。右のサイドバーだけでなく、スマホのメニュー内の目次も。Material の `partials/toc.html` を空にして実現（右カラムは CSS でも `display: none`）
- **検索窓を出さない**（`plugins: []` と、`overrides/partials/header.html`）
- **裁判文書は `trial/index.md` の1ページに集約**（書面ごとのアコーディオン）。本文は `docs/trial/md/<id>.md.txt` に置いて `--8<--` で取り込む。生ファイルは静的に公開されるので、`.md` ボタン（コピー／ダウンロード）の元にもなる
- 旧 `trial/eneos/`・`trial/whistleblower/` は、一覧ページへ転送するだけのページ（`#アンカー`も引き継ぐ）にした
- **Python フック（`doc_indent.py`・`add_blog_class.py`）とプラグイン（`mkdocs-glightbox`）を無くした**。やっていたことは、ソースへの焼き込みと、ページ内のスクリプト・CSS に置き換えた
  - 独自マーカー `:N X#id:` → 本文ファイルに `<p class="padN …">` として焼き込み済み
  - `:include:` → `--8<-- "パス"`（標準の拡張 `pymdownx.snippets`）
  - `body.trial-doc` → CSS の `body:has(.trial-doc-marker)`（各ページ先頭の目印 `<div class="trial-doc-marker" hidden></div>`）
  - agm・見本帳への Swiper 注入 → そのページの md に `<link>`・`<script>` を直接書いた
  - 画像クリックで拡大 → `docs/vendor/glightbox/`（同梱）と `docs/js/lightbox.js`
- `deploy.bat`・空の `includes/sitemap.md` は持ち込んでいない

## 書面の追加・更新

本文は**サイドノートアプリ**（sidenote-pdf-web、いずれ sidenote に統合）で作る。

1. アプリの「ウェブ用」書き出し（素の Markdown＋`<aside class="sn-note">`）をコピーして、`docs/trial/md/<id>.md.txt` に貼る（既にあるファイルなら上書き）
   - 拡張子を `.md.txt` にしているのは、ビルダーが独立したページにしてしまわないようにするため
2. 書面を増やすときだけ、`docs/trial/index.md` の該当する側（原告側・被告側…）の `<div class="doc-rows" markdown>` に、次のブロックを1つ足す

```html
<details class="doc-acc" id="<id>" data-md="md/<id>.md.txt" data-pdf="<PDFのURL>" data-summary="<要約>" markdown>
<summary>書面名</summary>
<div class="doc-body" markdown>

--8<-- "docs/trial/md/<id>.md.txt"

</div>
</details>
```

`data-pdf`・`data-summary` は無ければ書かない（ボタンがグレーになる）。ボタン・開閉マーク・サイドノートの位置は `docs/js/doc-accordion.js` が付ける。
目次を出さない構成なので、貼った本文の見出しが目次に混ざる心配はない。

今の11書面は、元の `eneos.md`・`whistleblower.md` を書面ごとに分割したもの。旧形式（hotline 用書き出し）のマーカーは HTML に焼き込み済みなので、
そのままで表示できる（`.md` ボタンの「コピー／ダウンロード」では、旧形式は素の Markdown に変換して渡す）。今後の書面は「ウェブ用」のままでよい。

## 設計ルール（Zensical と MkDocs の両方で動かすための落とし穴）

- **フック・プラグインを足さない**。Zensical は Python フックも MkDocs プラグインも読まない。処理が要るなら、ソースへの焼き込みか、ページ内の JS/CSS で
- **`mkdocs.yml` に `watch:` を書かない**。`custom_dir` と併用すると、Zensical は何も出力しない（エラーも出ない）
- **raw HTML の相対パス（`<a href>`・`<img src>`・`<script src>`・`<link href>`）は、ビルダーで解釈が違う**。Zensical はソースファイルの位置基準、MkDocs は書き換えず URL 基準。
  両方で同じ意味になるのは `フォルダ/index.md` 形式のページ（`agm/`・`trial/`・`styleguide/`）だけ。`docs/xxx.md` 直下のページで `../` を使うと壊れる。
  `trial/judgement_2025.md` のように `index.md` でないページでは、Markdown リンクは `index.md#id` 形式、raw HTML には絶対パスを使う
  （判決ページを `judgement_2025/index.md` にすると、Material の `navigation.indexes` が節の見出しページ扱いにして、ナビから「判決書」の行が消える）
- **`**強調**` が全角の句読点・括弧に隣接するとき、Zensical では強調にならない**ことがある（`pymdownx.betterem` の挙動差）。そういう箇所は `<strong>…</strong>` と書く
- 裁判文書系のページ（`trial/`・`agm/`・`styleguide/`・判決）は、先頭に `<div class="trial-doc-marker" hidden></div>` を置く。CSS が `body:has(.trial-doc-marker)` でページを見分けている
- サイドノートは画面幅 76.1875em 以下では出さない（本文列の外側の余白に置くため）

## 検証（Zensical 0.0.63 と MkDocs 1.6.1）

同じ条件（1280×800、同じ devicePixelRatio、同一オリジンの iframe）で、旧構成（フック・プラグイン有り）・MkDocs（フック無し）・Zensical の3つをビルドして、全要素の位置・サイズ・主要スタイル20項目を比べた。

- 旧構成 対 MkDocs（フック無し）: Home・agm・書面一覧・判決・見本帳の**記事本文が全要素一致**。ヘッダー・タブ・フッターも一致
- MkDocs 対 Zensical: 記事本文は全要素一致。差は次の3点だけ（いずれも実害なし）
  - サイドノートの幅が最大 7px 狭い（Zensical のクラシックテーマが `html { scrollbar-gutter: stable }` を付けるので、`100vw` からスクロールバー分が引かれる）
  - `<a href="">`（MkDocs は `href="."`）、`<link rel="next">` の追加、`search.json` の出力（検索窓は無いので使われない）
  - サイドバーの入れ子構造が違う（デスクトップでは非表示。スマホの引き出しの項目とリンク先は同じ）
- 機能（両ビルドで同じ結果）: 12書面すべての `.md.txt` が取得できる／`.md` のコピー・ダウンロード／要約ダイアログ／色の切り替え／転送ページが `#アンカー` を保つ／
  引用リンク4本が該当書面を自動で開いて見出し直下（110px）に着地／agm のカルーセルと画像拡大／スマホ幅のメニュー／目次・検索が出ない／内部リンクの 404 なし
- 本文テキストは、現行サイトの該当セクションと文字数まで一致（Home 1824・agm 3813・書面一覧 96875・判決 39656・見本帳 1773）

## URL・ドメインを変えるとき直す場所

- `mkdocs.yml`: `site_url`、`extra.about_url`
- 各ページ先頭の `url:`・`image:`（OGP）と、シェアボタンの `https://twitter.com/share?url=…`: `docs/index.md`・`docs/agm/index.md`・`docs/trial/index.md`・`docs/trial/judgement_2025.md`
- `docs/trial/judgement_2025.md` の年表の1リンク `/hotline/trial/#hikoku2_214`（raw HTML なので絶対パス）
- `docs/robots.txt`（`Sitemap:`）、`docs/e482d7edf83b50b925f361e389d57812.txt`（IndexNow のキー。`scripts/indexnow_ping.ps1` が使う）、`docs/googlee01c6dd3b7b5851f.html`（Search Console の所有確認）
- `docs/styleguide/index.md` の見本リンク

## その他のファイル

- `scripts/extract_agm_panels.py`: agm のスライド画像の切り出し（元の hotline から）
- `DESIGN_SYSTEM.md`: 元の hotline のデザイン仕様。フック・ブログ・プラグインに関する記述は、この repo には当てはまらない

## 未対応・要判断

- **ホスティング・URL**: `site_url` と各ページの `url:`／`image:`（OGP）は、現行の `https://minnanosaiban.github.io/hotline/` のまま。どちらのサイトが `/hotline/` を引き継ぐかも未定
- **運営者ページのリンク先**: `extra.about_url` は仮（現行の `/hotline/about/`）。株価サイト側の URL が決まったら差し替える
- 見本帳（`styleguide/index.md`）は、音声カードや `.repo-link` などの部品例を含んだまま（音声用のCSSは `05-card.css` に残っている）
- `mkdocs.yml` に、使っていない設定のコメントアウトが多く残っている（元のまま）
- 旧 `trial/eneos/`・`trial/whistleblower/` の転送ページは、サイトマップにも載る（検索エンジンには転送として扱われるはず。気になるなら外す）
