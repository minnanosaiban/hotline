# 開発者向けメモ

このサイトを作る側の説明です。作業の経緯や細かい検証結果は [HISTORY.md](HISTORY.md) に残してあります。

- 公開先: https://minnanosaiban.github.io/hotline/ （GitHub Pages）
- ビルド: Zensical（主）、MkDocs 1.6.1（予備）。Python フックもプラグインも使わないので、どちらでも同じ見た目になります

## 目次

1. [ローカルで見る・公開する](#ローカルで見る公開する)
2. [ページの構成](#ページの構成)
3. [書面を追加・更新する](#書面を追加更新する)
4. [ＰＤＦを追加する](#ＰＤＦを追加する)
5. [検索エンジン向けの設定](#検索エンジン向けの設定)
6. [壊さないための決まりごと](#壊さないための決まりごと)
7. [ＵＲＬを変えるとき直す場所](#ＵＲＬを変えるとき直す場所)
8. [未対応・要判断](#未対応要判断)

## ローカルで見る・公開する

初回だけ、仮想環境を作って Zensical を入れます。

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

- **見る**: `serve.bat`（http://localhost:8000/ 。開くと `/hotline/` に移ります）
- **ビルドだけする**: `build.bat`（`site/` に出力）
- **公開する**: `deploy.bat`

必ずこのフォルダで動かしてください（本文の取り込み `--8<--` が、実行したフォルダ基準のため。`.bat` は `cd` してから動かしています）。

**`serve.bat` を動かしたまま `build.bat`・`deploy.bat` を実行しないでください。** どれも同じ `site/` を作り直すので、全ページが 404 になることがあります。その場合は `serve.bat` の画面を閉じて、開き直します。

### 公開の仕組み

`master` に push すると、GitHub Actions（`.github/workflows/pages.yml`）が Zensical でビルドして公開します（1〜2分）。進み具合は、リポジトリの Actions タブで見られます。設定は Settings > Pages > Source =「GitHub Actions」です。

`deploy.bat` は次の順に進みます。

1. ビルドを確認する（失敗したら push しない）
2. コミットして `git push` する（強制 push はしない。通信エラーなら 5 秒おきに最大 3 回まで再試行）
3. `scripts/wait_deploy.ps1` で公開の完了を待つ（GitHub CLI の `gh` が要る。4 分止まったら自動で 1 回やり直す。やり直しても終わらないときは Actions の URL を出して止まる。旧版は公開されたまま）
4. `scripts/indexnow_ping.ps1` で Bing などに更新を通知する（失敗しても止まらない）

### 予備: MkDocs でビルドする

```
pip install -r requirements-mkdocs.txt
python -m mkdocs serve
```

Material for MkDocs は更新終了で、MkDocs 2.0 とは互換がないため、`mkdocs<2` に固定しています。Zensical は 0.0.x です。上げるときは `requirements.txt` を書き換えて、「壊さないための決まりごと」に触れていないか、ビルド結果を見比べてください。

## ページの構成

- トップ: `docs/index.md`
- 株主総会質疑応答: `docs/agm/index.md`
- 訴訟資料公開: `docs/trial2025/`・`docs/trial2024/`・`docs/trial2021/` の各 `index.md`（提訴年ごと。タブのドロップダウンに並ぶ）
- 2026年提訴: `docs/.trial2026/index.md`（当面非公開。フォルダ名を `.` 始まりにして、サイトにコピーされないようにしてある）
- ＰＤＦ一覧: `docs/pdf/index.md`（`scripts/pdf_index.py` が作る。手では直さない）
- 見本帳: `docs/styleguide/index.md`（noindex）
- 書面の本文: `docs/<提訴年>/md/<id>.md.txt`（`.md` ボタンの元にもなる。公開される）
- 取り込み専用の部品: `docs/trial2024/.parts/*.md.txt`（公開されない。`--8<--` で取り込むだけ）
- 見た目: `docs/css/`、動き: `docs/js/`、テンプレートの差し替え: `overrides/`
- デザインの仕様: [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)

## 書面を追加・更新する

本文は**サイドノートアプリ**（`C:\minnanosaiban\sidenote`）で作ります。

1. アプリの「hotline用」ボタンで書き出して、`docs/<提訴年>/md/<id>.md.txt` に置く（既にあれば上書き）。拡張子を `.md.txt` にしているのは、独立したページにされないようにするためです
2. ＰＤＦがあるときは、下の手順で `docs/pdf/` に入れる
3. 書面を**増やすとき**だけ、提訴年のページの該当する欄（裁判所・被告（ＥＮＥＯＳ）側・原告（通報者）側）の `<div class="doc-rows" markdown>` に、次のブロックを足す

```html
<details class="doc-acc" id="<id>" data-md="md/<id>.md.txt" data-pdf="../pdf/<ファイル名>.pdf" data-summary="<要約>" markdown>
<summary>書面名</summary>
<div class="doc-body" markdown>

--8<-- "docs/trial2024/md/<id>.md.txt"

</div>
</details>
```

- `data-pdf`・`data-summary` は無ければ書かない（ボタンがグレーになります）
- ボタン・開閉マーク・サイドノートの位置は `docs/js/doc-accordion.js` が付けます
- 表示では「●」をアイコンに置き換えてあります。書き出しを貼った書面に「●」があれば、同じ置き換えが要ります（詳しくは HISTORY.md）
- 本文中のリンクに、矢印のアイコンは付けません
- 認否のサイドノートの取り込み経緯は HISTORY.md にあります

## ＰＤＦを追加する

```
python scripts/add_pdf.py <元のPDF> <ENEOS側|通報者側|裁判所> <YYYY-MM-DD|甲17> <書面名> [--shrink] [--ocr]
```

事前に `pip install pymupdf` が要ります。`--shrink`・`--ocr` は Pillow と scan-ocr の環境も要ります（サイトのビルドには要りません）。

- ファイル名とＰＤＦのタイトルは、検索されやすい同じ名前にそろえます（例: `ENEOS（エネオス）の内部通報制度をめぐる訴訟について――ENEOS側_2024年04月15日_答弁書.pdf`）。検索結果に出るタイトルは、このメタデータが使われます
- 証拠（甲号証）は、日付の代わりに証拠番号を入れます（`通報者側`）
- `--shrink` は画像だけの白黒ＰＤＦを A4・200dpi・1bit に縮めます。Googlebot が読むのは先頭 64MB までで、GitHub Pages の転送量にも目安（月 100GB）があるためです
- `--ocr` は文字情報のないＰＤＦに文字層を付けます（1 ページ約 20 秒）。ＯＣＲなので読み違いは残ります
- 追加すると、ＰＤＦ一覧ページも自動で作り直されます
- 最後に出る `../pdf/<ファイル名>` を、書面の `data-pdf` に書きます

## 検索エンジン向けの設定

狙う検索語は、「ENEOS／エネオス」×「通報」「通報 裁判」「通報 訴訟」です。

- `<title>`: 各ページ先頭の front matter `seo_title:` がそのまま使われます（`overrides/main.html`）。検索語を先頭に置きます。`title:` はヘッダーの表示や `og:title` 用で、別にしてあります
- 説明文: front matter の `description:`。ページごとに違う文にします
- 半角の「ENEOS」と「エネオス」を、`<title>`・説明文・フッターに併記しています
- 検索結果に出したくないページ: front matter に `robots: noindex, nofollow`。そのページはサイトマップにも載りません（`overrides/sitemap.xml`）
- `docs/robots.txt` は、サブパス（`/hotline/`）に置いても検索エンジンに読まれません。害はないので残してあります
- Googlebot が読むＨＴＭＬは先頭 2MB までです。`trial2024/index.html` は約 860KB（2026-09-24）なので、2MB に近づいたらページを分けます

公開後にやること:

1. **Google Search Console**: プロパティ `https://minnanosaiban.github.io/hotline/` を追加し、サイトマップ `sitemap.xml` を送って、各ページを「インデックス登録をリクエスト」する
2. **Bing Webmaster Tools**: サイトを追加する（`msvalidate.01` は `overrides/main.html` に入っています）
3. **IndexNow**: `deploy.bat` が通知します。単独では `powershell -ExecutionPolicy Bypass -File scripts\indexnow_ping.ps1`

## 壊さないための決まりごと

Zensical と MkDocs の両方で動かすための落とし穴です。

- **フック・プラグインを足さない。** Zensical は読みません。処理が要るなら、ソースへの焼き込みか、ページ内の JS/CSS で行います
- **`mkdocs.yml` に `watch:` を書かない。** `custom_dir` と併用すると、Zensical は何も出力しません（エラーも出ません）
- **raw ＨＴＭＬの相対パスは、ビルダーで解釈が違います。** 両方で同じ意味になるのは `フォルダ/index.md` 形式のページだけです。`docs/xxx.md` 直下で `../` を使うと壊れます。取り込み用ファイルの中のリンクは、**取り込み先のページから見た**書き方にします
- **`**強調**` が全角の句読点・括弧に隣接すると、Zensical では強調にならないことがあります。** そこは `<strong>…</strong>` と書きます
- 裁判文書系のページは、先頭に `<div class="trial-doc-marker" hidden></div>` を置きます。CSS がこれでページを見分けています
- サイドノートは、画面幅 1220px 以下では出しません
- アコーディオンの `summary` には `overflow: visible` が要ります（`.md` ボタンのメニューが切れないように）
- `overrides/` に新しいファイルを足したときは、`serve.bat` を再起動してください（足したファイルは検知されません）
- タブのドロップダウンは、独自の JS ではなく `<details>` で開閉します。独自のクリック処理は環境によって動かなかったためです（経緯は HISTORY.md）

## ＵＲＬを変えるとき直す場所

- `mkdocs.yml`: `site_url`、`extra.about_url`
- 各ページ先頭の `url:`・`image:` と、シェアボタンの URL（`docs/index.md`・`docs/agm/index.md`・`docs/trial*/index.md`・`docs/.trial2026/index.md`・`docs/about/index.md`）
- `scripts/pdf_index.py` の `BASE`（変えたら `python scripts/pdf_index.py`）
- `scripts/indexnow_ping.ps1` の `$keyLocation`
- `docs/robots.txt`、IndexNow のキー（`docs/e482d7edf83b50b925f361e389d57812.txt`）、Search Console の所有確認（`docs/googlee01c6dd3b7b5851f.html`）
- `docs/styleguide/index.md` の見本リンク

## 未対応・要判断

- 運営者ページ: フッターのリンク先は `tomo`（`https://minnanosaiban.github.io/tomo/`）です。このサイトの `about/`（noindex）を残すかは未定です
- 2026年提訴（`docs/.trial2026/`）の公開を再開するときは、フォルダ名を `trial2026/` に戻し、`mkdocs.yml` の nav と各ページの年別リンク（`trial-year-nav`）を元に戻します
- 旧サイトとの重複: 旧 `hotline` は `tomo` に名前が変わりました。Bing には、旧名のリポジトリのページが残っています
- `eneos-saiban` にまだ頼っているのは、`dai5` 本文中の ChatGPT ページへのリンクだけです
