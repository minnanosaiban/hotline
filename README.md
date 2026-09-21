# eneos-hotline

「ＥＮＥＯＳの内部通報制度をめぐる訴訟について」のサイト。公開先は **https://minnanosaiban.github.io/eneos-hotline/**（GitHub Pages）。

元は `https://minnanosaiban.github.io/hotline/`（MkDocs Material、`hotline` リポジトリ）にあったものから、株価分析（blog）と運営者ページを除いて切り出した。
元の `hotline` リポジトリには一切触れていない（旧サイトは今もそのまま公開されている）。

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
| **公開する** | **`deploy.bat`**（ビルド確認 → コミット・push → 公開の完了を確認、まで） |

`--8<--` での本文の取り込みは「コマンドを実行したフォルダ」基準なので、必ずこのフォルダで動かす（`.bat` は `cd` してから動かしている）。
間違えたときは、本文が黙って抜けるのではなく `Snippet at path … could not be found` で止まる（`check_paths: true`）。

## 公開（GitHub Pages）

**`master` に push すると、GitHub Actions（`.github/workflows/pages.yml`）が Zensical でビルドして公開する。** 普段は **`deploy.bat` をダブルクリック**すればよい（`git push` だけでも同じ）。
進み具合は、リポジトリの Actions タブで見られる（1〜2分）。公開後の確認は、上の URL を開く。

- **`deploy.bat` の流れ**: ① ビルド確認（失敗したら push しない）→ ② `git add .`・コミット・`git push -u origin master`（**強制 push はしない**。ほかのリポジトリの `deploy.bat` と違い、`gh-deploy` や `--force` は使わない）。送るものが無い（GitHub にまだ無いコミットが無い）ときは push せず、次へ進む。push が通信エラー（`Empty reply from server` など）で失敗したときは、5秒おきに最大3回まで再試行する（2回目からは HTTP/1.1）。3回とも失敗したら、コミットは手元に残したまま止まる
  → ③ `scripts/wait_deploy.ps1` が、GitHub Actions の実行（このコミットの分）を待って、成功か失敗かを表示する（GitHub CLI の `gh` が要る。無い・サインインしていないときは、待たずに Actions の URL を出すだけ）
  → ④ `scripts/indexnow_ping.ps1` で IndexNow に通知（失敗しても止まらない）。`.venv` が無い PC では、作り方を表示して止まる
- Actions は `requirements.txt` の固定版で入れるので、手元と同じ結果になる（公開された66ファイルを手元の `site/` と比べて、Windows の手元ビルドが HTML の改行を CRLF で出す点（公開側は LF）を除き、すべて一致することを確認した）
- 設定は Settings > Pages > Source = 「GitHub Actions」。ブランチ（gh-pages）は使わない
- 公開を止めたいときは、Settings > Pages でサイトを非公開にする（または Actions のワークフローを無効にする）

### 予備: MkDocs でビルドする

```
pip install -r requirements-mkdocs.txt
python -m mkdocs serve       # http://localhost:8000/eneos-hotline/
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
- **並びは「判決文の答え合わせ → 裁判所 → 被告（ＥＮＥＯＳ）側 → 原告（通報者）側」**（各欄の見出しは `<p class="t-toc-head bar-title doc-side">`）。
  **「判決文の答え合わせ」**（2026-09-21）は、実際の判決文と証拠をつき合わせた分析の欄で、6つの行に分けてある。どれも書面ではないので、PDF・`.md`・要約のボタンは付けない `data-plain` の行:
  「理由１　契約書の問題を指摘する通報は、そもそも無かった」（`bunseki-riyu-1`）、「理由２　「海外消費税を支払う合意」をしていたと推認できる」（`bunseki-riyu-2`。この2行は、高裁判決が棄却した2つの理由を判決文から抜粋したもの。もとは「高裁判決が棄却した２つの理由を判決文から抜粋」の1行で、理由ごとに分けた。理由１・理由２へのジャンプ用のミニ目次は、分けたので外した）、「判決文の認定事実に基づく事実のタイムライン」（`bunseki-timeline`）、「判決文の言い回しが、読み手に与える影響」（`bunseki-iimawashi`）、「関係法令・規程」（`bunseki-horei`）、「判決文の全文」（`bunseki-zenbun`。判決文の行へ案内する短い文）。本文は、公開しない取り込み用の `parts/bunseki-*.md`（`--8<--` で取り込む。もとは1つの `parts/bunseki.md` で、「判決の概要と分析（東京地裁・東京高裁）」の1行の中に入れ子のアコーディオンとして入っていたものを分けた。内容は変えていない）。
  その下の**「裁判所」**の欄に、東京地裁・東京高裁の**判決文の全文**（`tisai`・`kousai`）を、書面と同じ形（PDF・`.md`・要約）で置いた。判決文の該当箇所へのリンクは、同じページの中の飛び先（`#…`）になっている。
  各行の中の見た目（`.f-head`・引用・14px の文字など）は、`.accordion-body` の CSS で決まる。もとは入れ子の `.card-accordion` の中だけに効かせていたのを、行（`.doc-acc`）の中にも効くようにした（`05-card.css`）。判決文などの引用（`blockquote`。理由１・理由２の行）は、見出しを「高裁判決から引用」（判決文の該当箇所へのリンク）とし、文字は `small`（13px）にしてある（`14-doc-accordion.css`。サイト共通の `.md-content p` が 16px を指定しているので、枠だけでなく中の `p`・`li` にも指定した。引用でない地の文は 16px のまま。タイムラインの引用 `.tl-quote` と「関係法令・規程」の抜粋は、そのまま）
- **「判決の概要」は、アコーディオンの外、ページの上（一覧の先頭。「判決文の答え合わせ」の欄の前）に置いている**（2026-09-21。`docs/trial/index.md`）。一覧と同じ `toc-wrap doc-list` の中にあるので、見出し（`##`）も本文も、一覧と同じ列（32rem）にそろう。もとは「判決の概要と分析」の冒頭にあったが、上に出したので、そちらからは削除した（文はこの1か所だけ）。そこにあった導入「以下は、２つの理由の該当箇所を判決文から抜粋しました。」は、抜粋の行の見出しがあるので入れていない
- 旧 `trial/judgement_2025/`（判決の概要と分析のページ）は、「判決文の答え合わせ」の見出し（`id="bunseki"`。`14-doc-accordion.css` の `.doc-side[id]` で固定ヘッダーに隠れないようにしてある）へ飛ばす転送ページ（`redirect_to: trial/#bunseki`、`overrides/main.html`）にした。ナビの「判決書」は外した。判決文はここ（裁判文書ページ）にだけある
- 旧 `trial/eneos/`・`trial/whistleblower/` は持たない。旧サイト（`/hotline/`）の URL であって、新サイトには存在しなかったため
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
2. PDF があるときは、`python scripts/add_pdf.py …` で `docs/pdf/` に入れる（下の「PDF」。PDF 一覧ページも自動で作り直される）
3. 書面を増やすときだけ、`docs/trial/index.md` の該当する欄（裁判所・被告（ＥＮＥＯＳ）側・原告（通報者）側）の `<div class="doc-rows" markdown>` に、次のブロックを1つ足す

```html
<details class="doc-acc" id="<id>" data-md="md/<id>.md.txt" data-pdf="../pdf/<ファイル名>.pdf" data-summary="<要約>" markdown>
<summary>書面名</summary>
<div class="doc-body" markdown>

--8<-- "docs/trial/md/<id>.md.txt"

</div>
</details>
```

`data-pdf`・`data-summary` は無ければ書かない（ボタンがグレーになる）。ボタン・開閉マーク・サイドノートの位置は `docs/js/doc-accordion.js` が付ける。
目次を出さない構成なので、貼った本文の見出しが目次に混ざる心配はない。

今の書面のうち、被告側7行と原告側の4行（原告第５準備書面・控訴理由書・控訴理由補充書（１）（２））と判決文2行は、元の `eneos.md`・`whistleblower.md`・`judgement_2025.md` を分割したもの。旧形式（hotline 用書き出し）のマーカーは HTML に焼き込み済みなので、
そのままで表示できる（`.md` ボタンの「コピー／ダウンロード」では、旧形式は素の Markdown に変換して渡す）。今後の書面は「ウェブ用」のままでよい。
要約（`data-summary`）は、判決文2行にだけ入っている（主文は判決文から、理由は、「2024年2月提訴」の下の「判決の概要」の文から。手で書いた要約なので「AI要約」の表示は付かない）。

### 認否のサイドノート（`eneos-saiban` の `argument.md` から移した分）

`eneos-saiban/argument.md` の欄外メモ（`{margin}` ブロック。**原告の書面には被告の認否、被告の書面には原告の認否**）を、`scripts/import_argument.py` で取り込んだ（2026-09-21、一度きり。
すでにサイドノートのある書面には足さずに止まる）。同じ形（段落の直後の `<aside class="sn-note">`）なので、今後サイドノートアプリの「ウェブ用」書き出しを貼った書面と、同じ見た目・同じ動きになる。

- **ノートのある11書面**: 訴状、原告第１〜４準備書面、求釈明申立書、控訴理由書（＝原告側。被告の認否）、答弁書、被告準備書面（２）〜（４）（＝被告側。原告の認否）。ノートの数は、元の `{margin}` の数（261）と一致
- **原告側の7書面（訴状、原告第１〜４準備書面、求釈明申立書、文書送付嘱託申立書）は、この repo にまだ無かったので、`argument.md` の本文から起こした**（「原告第４準備書面以下」の外部リンクの行は、これに置き換えた）。
  書式は既存の書面に合わせて変換（インライン style → `doc-gap-top`・`smaller`、`base padN` の囲み → `pad(N-1)`、引用の枠 `card_01` → `card` など）。
  元で目次が「≪ 中略 ≫」になっていた書面（原告第１〜４準備書面）は、カードの目次と本文の見出しから目次を復元した。元の本文の末尾にあった単独の `##` を除き、文書送付嘱託申立書の重複アンカー `bunsyo_1`（2つ目）を `bunsyo_2` にした。これらの7書面の本文は、公開ビルドの `argument.html`（欄外のノートを除く）にそのまま含まれることを確かめた。PDF との突き合わせ（校正）はしない
- **すでにあった5書面（答弁書、被告準備書面（２）〜（４）、控訴理由書）の本文は、取り込みでは変えていない**（`argument.md` とは、1文字ほどの違い（「カ」と「力」、「令」と「今」など）が数か所あり、答弁書・被告準備書面の目次は「≪ 中略 ≫」になっていたので、本文は既存のものを正とし、ノートだけを差し込んだ）。ノートを除いた本文が、元と同じであることを確かめた（ビルド後の HTML でも、既存15書面の本文は取り込み前と同じ）。
  **控訴理由書だけは、取り込みのあとで `argument.html` に合わせて2か所を直した**（2026-09-21）: 「位置付けてる制度」→「位置付けている制度」、「一審判決の該当箇所」の枠の中の行頭にまぎれていた「> 」（ページに「>」が出ていた）を削除。直したあと、控訴理由書の本文は `argument.md` と完全に一致する
- ノートは、元は段落の**直前**に置かれていたので、対応する段落の**直後**へ回した（`doc-accordion.js` が、その段落の頭の位置へ寄せて、参照している行と揃える）。連続する複数のノートは、順番のまま同じ段落に付く。
  「← ＥＮＥＯＳの主張」の印は、元は囲み（div）の頭に付いていたが、その囲みの最初の段落に付けた
- 赤字の「争う」「否認」は `.strong-rd`、「← ＥＮＥＯＳの主張」のバッジは `.sn-badge`（`14-doc-accordion.css`）。ノートの中の「下記 ⑷」などのリンクは、このページの別の書面の位置（`#dai1_314` など）へ飛び、閉じている書面は開く
- **`.md` ボタン**: ノートは「> 」で始まる引用として、対応する段落の直後に出る
- **「●」は、表示ではアイコン `<i class="bi bi-dot"></i>` に置き換えてある**（2026-09-21。書面の本文の箇条書き66か所とノート181か所。ソースの `docs/trial/md/*.md.txt` の中で置き換えた）。`.md` ボタンでは元の「●」に戻して渡す（`doc-accordion.js` の `DOT_ICON_RE`）。ぶら下げの字下げ（`text-indent: -1em`）がアイコンの幅を打ち消して 0 にしてしまうので、`14-doc-accordion.css` に `.doc-body i.bi { text-indent: 0 }` を入れてある。ページの文字としては「●」でなくなるので、ページ内検索やコピーには出ない。**今後、サイドノートアプリの書き出しを貼った書面に「●」があれば、貼ったあとに同じ置き換えが要る**
- **幅 1220px 以下（スマホ・タブレット）では、ノートを出さない**（これまでのサイドノートと同じ方針で、スマホでは出さないことに決めた。`14-doc-accordion.css`）

## PDF（`docs/pdf/`）

書面・判決文・証拠の PDF は、この repo の `docs/pdf/` に置く（もとは `eneos-saiban` の `_static/` にあった。26本、合計 約20MB。`eneos-saiban` の元ファイルには手を付けていない）。
内訳は、裁判文書ページの20行分（書面18・判決文2）、判決ページが引用する証拠（甲号証）6本（甲17・19・20・21・25・26）。

- **ファイル名と PDF の「タイトル」（メタデータ）を、検索されやすい同じ名前にそろえる**:
  `ENEOS（エネオス）の内部通報制度をめぐる訴訟について――ENEOS側_2024年04月15日_答弁書.pdf`（区分は `ENEOS側`・`通報者側`・`裁判所`）。
  検索結果に出る PDF のタイトルは、このメタデータが使われる。区切りのダッシュ「――」（U+2015 を2つ）は `scripts/add_pdf.py` の `SEP` 1か所。日付は書面の冒頭にある日付（判決は言渡日）。
  **証拠（甲号証）は、日付の代わりに証拠番号**を入れる: `ENEOS（エネオス）の内部通報制度をめぐる訴訟について――通報者側_甲17_税務処理の確認経緯.pdf`（甲号証は原告＝通報者側の提出なので `通報者側`）
- **軽量化（判決文2本）**: 元は 38MB と 92MB だった。1ページが 1653×2337pt（A4 の約2.8倍）の大きさで、4591×6491 画素のカラーPNG（約3000万画素、約550dpi 相当）
  だったため。**A4・200dpi・1bit に作り直して、地裁 1.5MB・高裁 1.7MB** にした（もとが白黒のスキャンなので、文字・印影・黒塗りは鮮明なまま。紙の質感のノイズだけ消える）。
  理由は、Googlebot が読む PDF は**先頭 64MB まで**（92MB では後半が検索の対象から外れる）、GitHub Pages の転送量の目安が**月 100GB**（92MB だと約1,000回のダウンロードで到達）、閲覧者のダウンロード時間
- **文字層（OCR）**: 画像だけだった9本（判決文2本・答弁書・被告準備書面（１）〜（５）・控訴答弁書、計150ページ）に、scan-ocr（`C:\minnanosaiban\scan-ocr`、エンジンは YomiToku）で透明な文字層を付けた。
  画像は元のまま、その上に文字を重ねている（scan-ocr の「テキスト乗せPDF」は画像を JPEG で作り直して大きくなるので、認識結果だけを使った）。
  サイトの検証済み本文と比べた一致（5文字連続の再現率）は 92.8〜97.7%（判決文は 96.8%・97.7%）。MuPDF・PDFium（Chrome）・pypdf の3つで、同じ文字数が取り出せる。
  OCR なので読み違いは残る（例: 「ワ」→「八」）。文字層は検索とコピー用で、見た目には出ない。原告側の4本は、もともと文字情報があった
- **PDF 一覧ページ**（`docs/pdf/index.md`、URL は `/pdf/`。ヘッダーのタブには出さず、裁判文書ページの冒頭のリンクから行く）: PDF へのリンクが JavaScript を使わずに HTML に入るので、検索エンジンが PDF を見つけやすい。
  区分ごと（裁判所・被告（ＥＮＥＯＳ）側・原告（通報者）側・その証拠）に、書面名・日付・ページ数・大きさを並べ、本文の行がある書面には「本文」のリンクが付く。**`scripts/pdf_index.py` が `docs/pdf/` の中身から作る**（手では直さない）。`add_pdf.py` が PDF を足すたびに作り直す。nav に入れていないので、Zensical のサイトマップには載らない（MkDocs は載せる）。検索エンジンは、裁判文書ページ（サイトマップにある）のリンクからたどる
- **追加のしかた**: `python scripts/add_pdf.py <元のPDF> <ENEOS側|通報者側|裁判所> <YYYY-MM-DD|甲17> <書面名> [--shrink] [--ocr]`（`pip install pymupdf`。`--shrink`・`--ocr` は `scripts/pdf_tools.py` を使い、Pillow と scan-ocr の環境が要る。サイトのビルドには要らない）。
  `--shrink` は画像だけの白黒PDFを A4・200dpi・1bit に（色つきは断る）、`--ocr` は文字情報のないPDFに文字層を付ける（1ページ約20秒、CPUだけで動く）。最後に出る `../pdf/<ファイル名>` を `data-pdf` に書く
- 元の PDF にページ回転（180°・270°）が付いている場合は、文字層を重ねる前に、見た目を変えずに取り除く（回転したままだと、文字の向きと位置がずれる）
- PDF は Git ではバイナリ扱い（`.gitattributes` の `*.pdf binary`）
- 確認したこと: 13本とも、ページ数とタイトル（=ファイル名）が合っている。縮小していない11本は、元の PDF と描画が画素まで同じ。縮小した2本は、白黒化による差だけ（平均 5/255 以下）

## 検索エンジン向けの設定（「ENEOS 通報 裁判」などで見つかるように）

狙う検索語: 「ENEOS／エネオス」×「通報」「通報 裁判」「通報 訴訟」。

- **`<title>`**: 各ページ先頭の front matter `seo_title:` がそのまま `<title>` になる（`overrides/main.html`）。検索語を先頭に置く。
  `title:` の方はヘッダーの表示や `og:title` に使われるので、別にしてある。`seo_title` が無いページは「ページ名 - サイト名」
- **説明文**: front matter の `description:`（`<meta name="description">` と `og:description`）。ページごとに違う文にする
- 全角の「ＥＮＥＯＳ」は、検索エンジンが半角と同じに扱う。それでも `<title>`・説明文・フッターでは、半角の「ENEOS」と「エネオス」を併記している
- **フッターの1文**（`overrides/partials/copyright.html`）: 全ページの本文に「ENEOS（エネオス）」「通報」「裁判・訴訟」が入る
- **検索結果に出したくないページ**: front matter に `robots: noindex, nofollow`（見本帳に付けてある）
- **サイトマップ**: ビルドで `sitemap.xml` ができる（Zensical は nav にあるページだけ。MkDocs は全ページなので見本帳も入るが、noindex なので害はない）
- `docs/robots.txt` は、**サブパス（`/eneos-hotline/`）に置いても検索エンジンは読まない**（読まれるのはホスト直下だけ）。害はないので残してある。
  サイトマップは Search Console から送る
- **Googlebot が読む HTML は先頭 2MB まで**（公式ドキュメント）。裁判文書ページ（`trial/index.html`）は今 約470KB。書面を増やして 2MB に近づいたら、ページを分ける
- 効果が出るまでは、Search Console の登録と、サイトマップの送信が要る（下の「公開後にやること」）

## 公開後にやること

1. **Google Search Console**: 「URL プレフィックス」でプロパティ `https://minnanosaiban.github.io/eneos-hotline/` を追加して所有権を確認する。
   HTML ファイル方式の確認用ファイル（`googlee01c….html`）はこの repo にも入れてあるが、通らなければ Search Console が出す新しいファイルを `docs/` に置いて push する。
   その後、サイトマップ `sitemap.xml` を送り、各ページを「URL 検査 > インデックス登録をリクエスト」する
2. **Bing Webmaster Tools**: サイトを追加する（`msvalidate.01` の meta は `overrides/main.html` に入っている）。Search Console からのインポートも使える
3. **IndexNow**（Bing・Yandex などへの新規・更新の通知）: 公開後に `build.bat` でサイトマップを作り、`powershell -ExecutionPolicy Bypass -File scripts\indexnow_ping.ps1`
4. 旧サイト（`/hotline/`）に同じ本文が残っている間は、検索エンジンがどちらを正とみなすか割れる。旧サイトから新サイトへ `rel="canonical"`
   （または転送）を張れば確実（旧 `hotline` リポジトリの変更が要るので、この repo では行っていない）

## 設計ルール（Zensical と MkDocs の両方で動かすための落とし穴）

- **フック・プラグインを足さない**。Zensical は Python フックも MkDocs プラグインも読まない。処理が要るなら、ソースへの焼き込みか、ページ内の JS/CSS で
- **`mkdocs.yml` に `watch:` を書かない**。`custom_dir` と併用すると、Zensical は何も出力しない（エラーも出ない）
- **raw HTML の相対パス（`<a href>`・`<img src>`・`<script src>`・`<link href>`）は、ビルダーで解釈が違う**。Zensical はソースファイルの位置基準、MkDocs は書き換えず URL 基準。
  両方で同じ意味になるのは `フォルダ/index.md` 形式のページ（`agm/`・`trial/`・`styleguide/`）だけ。`docs/xxx.md` 直下のページで `../` を使うと壊れる。
  `index.md` でないページ（今は転送だけの `trial/judgement_2025.md`）では、Markdown リンクは `index.md#id` 形式、raw HTML には絶対パスを使う。取り込み用ファイル（`parts/`・`docs/trial/md/`）の中のリンクは、**取り込み先のページから見た**書き方にする（`trial/index.md` に取り込むなら、`#id` や `../pdf/…`）
  （`judgement_2025.md` を `judgement_2025/index.md` にすると、Material の `navigation.indexes` が節の見出しページ扱いにして、ナビからその行が消える）
- **`**強調**` が全角の句読点・括弧に隣接するとき、Zensical では強調にならない**ことがある（`pymdownx.betterem` の挙動差）。そういう箇所は `<strong>…</strong>` と書く
- 裁判文書系のページ（`trial/`・`agm/`・`styleguide/`・判決）は、先頭に `<div class="trial-doc-marker" hidden></div>` を置く。CSS が `body:has(.trial-doc-marker)` でページを見分けている
- サイドノートは画面幅 76.1875em 以下では出さない（本文列の外側の余白に置くため）
- 各グループ（`.doc-rows`）の最後の行の下の罫線は、`details.doc-acc` の `border: none` に詳細度で負けるので、`14-doc-accordion.css` で詳細度を上げて出している（これが無いと、最後の行が `details` のグループには閉じの罫線が出ない）
- アコーディオンの `summary` には `overflow: visible` が要る（`14-doc-accordion.css`）。テーマの `summary` は `overflow: hidden` で、`.md` ボタンのメニューが行の高さで切れてしまう

## 検証（Zensical 0.0.63 と MkDocs 1.6.1）

同じ条件（1280×800、同じ devicePixelRatio、同一オリジンの iframe）で、旧構成（フック・プラグイン有り）・MkDocs（フック無し）・Zensical の3つをビルドして、全要素の位置・サイズ・主要スタイル20項目を比べた。

- 旧構成 対 MkDocs（フック無し）: Home・agm・書面一覧・判決・見本帳の**記事本文が全要素一致**。ヘッダー・タブ・フッターも一致
- MkDocs 対 Zensical: 記事本文は全要素一致。差は次の3点だけ（いずれも実害なし）
  - サイドノートの幅が最大 7px 狭い（Zensical のクラシックテーマが `html { scrollbar-gutter: stable }` を付けるので、`100vw` からスクロールバー分が引かれる）
  - `<a href="">`（MkDocs は `href="."`）、`<link rel="next">` の追加、`search.json` の出力（検索窓は無いので使われない）
  - サイドバーの入れ子構造が違う（デスクトップでは非表示。スマホの引き出しの項目とリンク先は同じ）
- 機能（両ビルドで同じ結果）: 12書面すべての `.md.txt` が取得できる／`.md` のコピー・ダウンロード／要約ダイアログ／色の切り替え／
  引用リンク4本が該当書面を自動で開いて見出し直下（110px）に着地／agm のカルーセルと画像拡大／スマホ幅のメニュー／目次・検索が出ない／内部リンクの 404 なし
- 本文テキストは、現行サイトの該当セクションと文字数まで一致（Home 1824・agm 3813・書面一覧 96875・判決 39656・見本帳 1773）

## URL・ドメインを変えるとき直す場所

- `mkdocs.yml`: `site_url`、`extra.about_url`
- 各ページ先頭の `url:`・`image:`（OGP）と、シェアボタンの `https://twitter.com/share?url=…`: `docs/index.md`・`docs/agm/index.md`・`docs/trial/index.md`
- PDF 一覧ページの `url:`・シェアボタンの URL は `scripts/pdf_index.py` の `BASE` から作られる（変えたら `python scripts/pdf_index.py`）
- `scripts/indexnow_ping.ps1` の `$keyLocation`
- `docs/robots.txt`（`Sitemap:`）、`docs/e482d7edf83b50b925f361e389d57812.txt`（IndexNow のキー。`scripts/indexnow_ping.ps1` が使う）、`docs/googlee01c6dd3b7b5851f.html`（Search Console の所有確認）
- `docs/styleguide/index.md` の見本リンク

## その他のファイル

- `parts/bunseki-*.md`（6本）: 「判決文の答え合わせ」の各行の本文。公開されない（`docs/` の外）取り込み用。`.md` ボタンの元にする書面の本文は `docs/trial/md/` に置く
- `deploy.bat`・`scripts/wait_deploy.ps1`: 公開（上の「公開（GitHub Pages）」）。`serve.bat`・`build.bat`: 見る・ビルドする
- `scripts/add_pdf.py`・`scripts/pdf_tools.py`・`scripts/pdf_index.py`: PDF を `docs/pdf/` に、検索されやすい名前とタイトルで入れる。軽量化・OCR・一覧ページ（上の「PDF」）
- `scripts/extract_agm_panels.py`: agm のスライド画像の切り出し（元の hotline から）
- `DESIGN_SYSTEM.md`: 元の hotline のデザイン仕様。フック・ブログ・プラグインに関する記述は、この repo には当てはまらない

## 未対応・要判断

- **運営者ページのリンク先**: `extra.about_url` は仮（旧サイトの `https://minnanosaiban.github.io/hotline/about/`）。株価サイト側の URL が決まったら差し替える
- **旧サイトとの重複**: 旧 `/hotline/` に同じ本文が残っている（上の「公開後にやること」4）
- **`eneos-saiban` にまだ頼っているもの**: nav の「主張書面全文と認否」（`argument.html`。本文と認否のノートは裁判文書ページへ移したので、不要になったら `mkdocs.yml` の nav から外す）、`dai5` 本文中の ChatGPT ページへのリンク、「判決文の答え合わせ」の抜粋の行（`parts/bunseki-riyu.md`）の `argument.html#id21`（原告第１準備書面への参照）。PDF は移し終えた（原告側の7本と甲号証6本）。**甲8-16 の PDF は、`eneos-saiban` にも存在しない**（「判決文の答え合わせ」の抜粋の行とタイムラインの行の2か所のリンク `…/甲08-16_調査補助者とのメール2016-2017_ENEOS_公開.pdf#page=17` は、以前からリンク切れ）
  **甲8-16 の PDF は、`eneos-saiban` にも存在しない**（「判決文の答え合わせ」の2か所のリンク `…/甲08-16_調査補助者とのメール2016-2017_ENEOS_公開.pdf#page=17` は、以前からリンク切れ）。元のファイルがあれば `add_pdf.py` で移す
- 裁判文書ページの最後に「表示確認用（見本・削除可）」の行が出ている。公開ページなので、消してよければ `sample-web` の行と `docs/trial/md/sample-web.md.txt` を削除する
- 見本帳（`styleguide/index.md`）は、音声カードや `.repo-link` などの部品例を含んだまま（音声用のCSSは `05-card.css` に残っている）
- `mkdocs.yml` に、使っていない設定のコメントアウトが多く残っている（元のまま）
