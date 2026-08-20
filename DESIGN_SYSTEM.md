# hotline デザインシステム — コンポーネント一覧

作成: 2026-08-17。`docs/css/01〜12`（9ファイル）と実ページ（Home / agm / trial / about / blog）を突き合わせて棚卸しした。
目的は2つ：①今後の手直しで一貫性を崩さないための正本、②「Markdownを知らなくてもMkDocs用mdが作れるアプリ」（sidenote-pdf応用）の部品パレット設計図。

サイト全体の方針（[[hotline-design-preferences]]と同じ）：
- 罫線より余白・背景色差・box-shadowで区切る
- 見出しは太字でなくサイズ／色バーで立てる（Homeのメインタイトルだけ太字の例外）
- 装飾は無彩色寄り、青とオレンジ（ENEOSブランド色）以外の色はほぼ使わない
- **縦余白の単一所有の原則**（2026-08-20導入）：セクション間の縦余白は「下の要素が margin-top で持つ」。margin-bottom・flexのgap・マージン相殺の組み合わせで余白を決めない（詳細は0.5章）

---

## 0. 基盤トークン

| 種類 | 定義場所 | 内容 |
|---|---|---|
| 色 | `01-color.css` | `--md-link-color`(青/メイン), `--md-warn-red`(警告赤), `--red-color-3`(サイドノート強調赤・ライト#dc3545/ダーク#f2545b), `--surface-gray`(灰背景), `--md-card-border`/`--md-card-border-soft`(枠線グレー), `--orange-color-1`(ENEOSブランド橙)。2026-08-20に未使用トークン23個を削除（値のメモは`hikae/color_memo.md`に退避）。定義するのは実際に使う色だけ |
| 文字サイズ | `03-typeset.css`冒頭コメント | h1 2.4rem／h2・`.larger` 1.6rem／`.large` 1.28rem／`.largest` 2.56rem／本文 16px／`.doc`系(裁判文書) 16px固定／h3・h4 18px／blog記事h1 1.6rem。太さは常に300〜400、強調はサイズで出す |
| 本文幅 | `03-typeset.css` `.width-40` | `max-width:32rem`（①の「40字幅」の実体。スマホは100%） |
| 余白 | 詳細は次章 | 基本スケールは1/2/4/6/8rem。詳細は「0.5 余白システム」参照 |

---

## 0.5 余白システム（スペーシング）

罫線を使わない分、このサイトは余白の一貫性そのものが「区切り」の役割を担っている。実際、値は行き当たりばったりでなく、rem単位の倍々スケール＋モバイルでの個別圧縮＋flexギャップの補正、という3層で作り込まれていた。

### 基本スケール（PC、本文カラム内）

| 値 | 位置づけ | 主な使用箇所 |
|---|---|---|
| 1rem | 段落内の細かい区切り | `.margin01` |
| 1.6rem | 見出し⇔本文（グレー枠内） | `.agm-section > p + p.margin02`（実余白は+10px）、accordionの`margin-top` |
| 2rem | 標準的な段落間 | `.margin02`、h1直後の既定 |
| 4rem | セクション内区切り（中） | `.margin04`、about `.about-work`間、trial `.q-num-gap`（株主質問N見出し） |
| 6rem | セクション間区切り（大） | `.gap-6`、`.issue-lead`、`.hero-band`の上下padding、`.agm-section`の前後margin、trial `--t-section-gap` |
| 8rem | ページ内最大の区切り | 本文`h2`の既定上マージン、footer上マージン |

数値はほぼ倍々（1→2→4→8）で、6remだけ4と8の中間に別途存在する（「セクションは分けたいがh2ほど離したくない」場面用）。**新しい余白を足すときはこの6段階のどれかに乗せる**のが基本で、独自の値（例：3.3rem）を新設しない。

### モバイル（≤767px）での圧縮：基準値は3rem

| PC | モバイル | 使用箇所 |
|---|---|---|
| 8rem（h2） | 3rem | 本文見出し（この8rem→3remが全体の基準、[[hotline-mobile-tuning]]に明記） |
| 6rem（`.gap-6`／`.agm-section`／`.issue-lead`／trial `--t-section-gap`） | **3rem に統一** | 各種セクション区切り（2026-08-17修正：issue-leadは3.5rem、trialは4remにズレていたのを3remへ統一） |
| 4rem（Home「3つの情報」／agm `.q-num-gap`／about `.about-work`＝いずれも番号つき項目の並び） | **圧縮なし（4remのまま）に統一** | 2026-08-17修正：aboutだけ3remに圧縮されていたのを、先に一致していたHome・agmの4remに合わせた |
| 2.5rem（trial `--t-item-gap`） | 2rem | trial項目間 |

「機械的に半分にする」のではなく**各コンポーネントで実測して過剰な空白を削っている**。6rem系はページによって3rem/3.5rem/4remにズレていたため3remへ統一、4rem系（番号つき項目の並び）はHome・agmが先に4remで一致していたためaboutをそちらに合わせた（詳細は「6. 整理の候補」参照）。

### コンポーネント内部のリズム（em単位）

judgement_2025のアコーディオン内（本文14px、サイト標準16pxと異なる）は、remでなくemで余白を取っている：`.q-card`/`.ex-card`は`1.4em`、`.f-head`は`4.0em 0 3.2em`、`.f-jumpnav`は`1.6em 0 3.4em`、`.tl-c`は`4.0em 0`。remだとアコーディオン内外でフォントサイズが違うため見た目の比率が崩れる＝**フォントサイズが変わる入れ子ではem、サイト全体の骨格はremという使い分け**になっている。

### 縦余白の単一所有の原則（2026-08-17〜20で「flexギャップの補正」問題を解消）

かつて`.agm-section`はflexの`gap:10px`とマージンが加算される構造で、「目標余白 − 直前のmargin-bottom − gap」というcalc補正が連鎖する、サイト内で最も壊れやすい箇所だった（旧`.agree-gap-agm`・旧`verdict-lead`補正）。2026-08-20に以下へ一本化し、補正ルール群・`.agree-gap-agm`クラス・モバイル専用の例外を全廃した：

- **縦余白は「下の要素」が margin-top だけで持つ。margin-bottom は使わない**（`.gap-6`の設計思想を全体に拡張）
- `.agm-section`は`gap:0`。枠内は`> p + p`の隣接ルールで基本リズム10pxを持ち、`p + p.margin02`＝`calc(1.6rem+10px)`、`p + p.margin04`／`p + p.verdict-lead`＝`calc(4rem+10px)`（実質98px、枠外`.agree-gap`と同値）。値は全て「見た目の実余白そのもの」で、引き算のcalc補正は存在しない
- リファクタ前後でPC・モバイル両方の全セクション間隔をブラウザ実測し、ピクセル単位で同一であることを確認済み

**枠内に新しい段落を足すときは`.margin02`／`.margin04`を付けるだけでよい**。直前・直後との組み合わせ確認は不要になった。

---

## 1. 見出し・強調

### `.bar-title`（行頭の青バー見出し）
罫線でなく色バーで見出し感を出す、確立された見出しパターン。
```html
<p class="larger width-40 margin02 agree-gap bar-title">
調査事項を曖昧にして回答
</p>
```
- 定義：`03-typeset.css`
- 使用：Home本文見出し（複数）、about `.about-work-title`、trial `.t-toc-head`（いずれも今回統合）

### `.sec-title` / `.issue-point`
`.sec-title`＝中央寄せの節見出し(2.4rem細字、Homeの大きな区切り)。タイポグラフィ（サイズ・太さ・中央寄せ）はこのクラスが単独で持つ——旧併記の`center`/`larger`/`margin02`は全て上書きされて死んでいたため2026-08-20にマークアップから削除（`<p class="sec-title">`だけでよい。上余白は文脈側：`.issue-lead`併用または`.gap-6 + p.sec-title`ルール）。`.issue-point`＝1.2rem太字の小見出し（Home冒頭の1/2/3）。

### 地の文の色つき強調 → `.text-warn` / `.text-main`（2026-08-17クラス化）
- `.text-warn`（赤・`--md-warn-red`）＝告発性の核心事実（ページの「背骨」）・警告ラベル。太字にしたい時は`<b>`で囲む（太さはタグ、色はクラスで分離）
- `.text-main`（青・`--md-link-color`）＝「裁判所の判断」ラベル、`.sec-title`の色つきバリエーション
- 定義：`03-typeset.css`
- 旧：`style="color: var(--md-warn-red/md-link-color);"`をHome 5箇所・agm 1箇所で都度手打ちしていたのをクラスに統合

### 太字黒（引用・説明中の重要語句）
`<b>…</b>`のまま。クラス化していない（サイト全体で`<b>`は「太さで強調」の標準手段のため、色を伴わないここは対象外）。

---

## 2. ボックス・カード

| 名前 | 見た目 | 罫線 | 定義 | 使用箇所 |
|---|---|---|---|---|
| `.agm-section` | 背景色(surface-gray)の枠 | なし（スマホはbox-shadowで側面を塗る） | `02-layout.css` | Homeの引用枠（Homeのみで使用。名前に反しagmページには無い） |
| `.card-blue`（旧`.card-bule`） | 背景色(surface-gray)+パディング | なし（2026-08-18に罫線→背景へ変更・命名も修正） | `05-card.css` | 音声解説カード等 |
| `.toc-card`/`.toc-grid` | 2列グリッドのリンクカード | なし（2026-08-18に罫線→背景へ変更、ホバーはbox-shadow） | `05-card.css` | trial indexの4枚、blog indexの読む順カード |
| `.about-work` | カードでなく番号+見出し+本文 | なし | `12-about.css` | aboutの制作物一覧（2026-08-10にカード形式を廃止した経緯あり） |
| `.q-card` / `.ex-card` | グレー地(実在の引用) / 白地+破線(架空の例文) | 例文のみ破線 | `11-trial.css` | judgement_2025アコーディオン内、「本物」と「説明用の例」を対で描き分ける |
| `.f-head` | 薄い青背景のカード（ラベル+タイトル+要約文） | なし | `11-trial.css` | judgement_2025の「理由１」「理由２」見出し |
| `.test-part` | ごく薄いグレー背景+box-shadow | なし（2026-08-18に罫線→背景+shadowへ変更） | `11-trial.css` | 「見分け方」等のまとめ枠（`.q-card`/`.f-head`と意味が違うため一段薄い背景で区別） |
| `.eneos-card` / `.qa-turn` | 会社公式引用=グレー地／実際の質問・検証=丸アイコン+本文 | なし | `11-trial.css` | agmの対照カード |

**罫線は全て解消済み**（2026-08-18）。サイト全体で「罫線より背景色・box-shadow」の方針が統一された。

### agm対照カードの実例
```html
<div class="eneos-card width-40">
<span class="qa-mark qa-mark--eneos">ENEOSが公表する株主質問</span>
…
</div>
<div class="qa-turn qa-turn--student width-40">
<span class="qa-mark qa-mark--student">🧑</span>…
</div>
<div class="qa-turn qa-turn--eval width-40">
<span class="qa-mark qa-mark--eval">検証</span>…
</div>
```

---

## 2.5 カルーセル

`.qa-carousel`（Swiper.js・CDN）：中央＋左右チラ見え＋自動送り（call4.jp参考）。agm/index.mdの質問パネル画像14枚専用（2026-08-20導入）。サイト全体のCSS/JSとは別系統で、`overrides/hooks/add_blog_class.py`が`agm/index.md`のときだけSwiper CDN・`docs/css/13-carousel.css`・`docs/js/qa-carousel.js`を注入する（他ページの読み込みには一切影響しない、という設計）。同じHTML構造（`.qa-carousel.swiper > .swiper-wrapper > .swiper-slide` + `.swiper-pagination`）を書けば`qa-carousel.js`のforEachが拾うので、別ページに増やす分には初期化コードの変更は不要（ただしSwiper CDN自体の注入は現状agm限定なので、他ページで使うならフックの条件分岐を広げる必要がある）。

## 3. アコーディオン

`.card-accordion`（`05-card.css`）：+/−開閉のグレーバー、`summary`をボタン風に。中の`blockquote`は明朝体(Noto Serif JP)で判決文引用と統一。judgement_2025で使用。

---

## 4. 裁判文書特有の型（②に対応）

### インデント・ぶら下げインデント
`03-typeset.css`で定義、明朝体(Noto Serif JP)・行間2.4・16px固定：
```html
<p class="idt">通常の字下げ（1em）</p>
<p class="hg-idt">ぶら下げインデント（1em）</p>
<p class="hg-idt2">ぶら下げインデント（2em、⑴⑵…の下の階層）</p>
<p class="hg-idt3">ぶら下げインデント（3em）</p>
```
`.pad1`〜`.pad9`は字下げなしの左パディングのみ版。

### 認定事実タイムライン `.tl-c`
縦線+ノードで時系列を表現。`.tl-out`の★マークで「判決に現れない出来事」を区別。`11-trial.css`、judgement_2025のみ。

---

## 5. まだ存在しないコンポーネント（③に対応）

**2カラム余白ノート（サイドノート）**：`eneos-saiban/argument.html`のような、本文の横に注釈が並ぶレイアウト。sidenote-pdfアプリのMD書き出し（Jupyter Book方式、段落の直後に`<aside class="margin">`を埋め込む形）は実装済みだが、これを受け止めるCSS（float配置・margin計算）がhotline側にまだ無い。裁判文書ページ（trial/judgement系）に載せるなら、`.doc`/`.idt`/`.hg-idt*`と共存できる設計にする必要がある。

---

## 6. 整理の候補（要判断）

1. ~~`.bar-title`とtrialの`.t-toc-head::before`の統合~~ → **2026-08-18対応済み**。`.t-toc-head`独自の`::before`を削除し、markup側で`.bar-title`クラスを併用する方式に統一（trial/index.md「2025年9月判決」・trial/eneos.md「NotebookLM 音声解説」の2箇所）。フォントサイズ換算が偶然一致していたため（`.larger`=1.6rem／`.t-toc-head`=2.0em、どちらも実質32px）、バーと文字の間隔調整なしにそのまま流用できた
2. ~~罫線が残る3箇所（`.card-bule`／`.toc-card`／`.test-part`）~~ → **2026-08-18対応済み**、全て背景色・box-shadow方式に変更
   - `.card-blue`（旧`.card-bule`）：`background: var(--surface-gray)`、角丸8px
   - `.toc-card`：`background: var(--surface-gray)`、ホバーは境界色でなくbox-shadowの浮き上がりで表現
   - `.test-part`：同じアコーディオン内の`.q-card`(surface-gray)・`.f-head`(薄い青)と意味が違う（「まとめ」の箱）ため、それらより一段薄い`--md-default-fg-color--lightest`＋box-shadowで区別
3. ~~「裁判所の判断」の青太字+アイコンラベルが未クラス化~~ → **2026-08-17対応済み**、`.text-main`をラベル・「こんなことも！？」（`.text-warn`）・地の文の赤字強調・Home box titleの色に統一適用
4. ~~`.card-bule`の名前（"bule"はblueの誤字）~~ → **2026-08-18対応済み**、`.card-blue`にリネーム（CSS 2ファイル・markdown 2ファイル）
5. ~~6rem系のスマホ圧縮バラつき（issue-lead 3.5rem／trial 4rem）~~ → **2026-08-17対応済み**、3remに統一
6. ~~4rem系（番号つき項目の並び）のスマホ圧縮バラつき（about `.about-work`だけ3remに圧縮）~~ → **2026-08-17対応済み**、Home「3つの情報」・agm `.q-num-gap`と同じ「圧縮なし(4remのまま)」に統一
7. ~~`.x-share`のインラインstyle`color:#FFFFFF`が全6ページで重複~~ → **2026-08-17調査の結果、削除**。`.x-share`自体が`color:var(--md-typeset-color) !important`を持っており、インラインの方が非`!important`のため実際には一度も反映されていなかった死んだ指定と判明（薄いグレーの背景に白文字では視認性的にもおかしい）。クラス化ではなく単純削除で解決
8. ~~`qa-mark--eneos`のインラインstyle`color:var(--md-typeset-color)`がagmで14回重複~~ → **2026-08-17対応済み**、クラス本体の色を`var(--orange-color-1)`（常に上書きされ一度も表示されていなかった）から実際の値に変更し、インラインを全削除
9. ~~whistleblower.md内`margin-top/bottom:1.6em`のインラインstyle（14箇所）と`!important`付け忘れによる不具合（7箇所）~~ → **2026-08-17対応済み**。`.doc-gap-top`/`.doc-gap-bottom`をクラス化し全置換（`.doc`/`.idt`/`.hg-idt*`と併用）。3段階フロー図内の2箇所（1704/1724行目）はすでに正しく動作しており、ユーザー指示により未クラス化のまま維持
10. ~~whistleblower.md内`.table-text`の`style="width:10em"`が日付列で9回重複~~ → **2026-08-17対応済み**、`.table-text-date`をクラス化
11. ~~`01-color.css`の未使用トークン23個（他訴訟の会社色等の名残・3世代の命名混在）~~ → **2026-08-20対応済み**、実使用トークンのみ残して削除。値のメモは`hikae/color_memo.md`へ退避。`--red-color-3`はスキーム別定義に移動しダーク変種（#f2545b）を追加（旧#dc3545はダーク背景でコントラスト約2.9:1と不足）
12. ~~`.agm-section`のflexギャップ補正連鎖（サイト内で最も壊れやすい箇所）~~ → **2026-08-20対応済み**、縦余白の単一所有の原則へ一本化（0.5章参照）。前後でブラウザ実測しピクセル一致を確認
13. ~~`.sec-title`併記の`center`/`larger`/`margin02`が全て上書きされ死んでいた~~ → **2026-08-20対応済み**、Home3箇所・agm1箇所のマークアップから削除（`.sec-title`単独で完結）。`verdict-lead`の`margin02`併記も同様に削除
14. ~~`strong { font-style: 700; }`（03-typeset.css）が無効値で一度も効いていなかった~~ → **2026-08-20対応済み**、削除（font-weightの誤記。太字はブラウザ既定で十分）
15. ~~ヘッダーのサイト名（`.md-header__title`）の左端がタブ行（Home等）と8pxズレていた~~ → **2026-08-20対応済み**、Material既定の`margin-left:1rem(20px)`を`12px`へ縮小し、画面幅≥76.234375em（ドロワーボタン非表示）で完全一致に。ドロワーボタンが出る幅では、ボタンの占有スペース分だけ残る（アイコンとの重なりを避けるため詳細度は保持。全ページ・ダークモードで実測確認済み）
16. `.x-share`（Xでシェアボタン）を無彩色チップからサイトの青（`--md-link-color`／地色に白文字、ホバーは`--md-link-hover-color`）へ変更（2026-08-20）。リンク・タブ下線と同じ「アクションの色」に統一する意図。オレンジ案（`--orange-color-1`）も試作したが、ＥＮＥＯＳロゴ文字だけに使う特別色のため見送り。音声プレーヤーの`accent-color`案は、Chromeのネイティブ音声コントロールは再生ボタン自体が着色されない（進捗バー・音量つまみのみ）ため効果が薄く見送り。`about-btn`のコメント（旧: .x-shareと同系の無彩色と説明）も実態に合わせて修正済み

---

## この一覧の使い道（sidenote-pdf応用アプリへの示唆）

前回の分岐（本文系ページのみ／特殊レイアウトページも含む）は、③（裁判文書へのサイドノート要望）から「特殊レイアウトページも含む」と判断。ただし上の棚卸しからすると、特殊レイアウトの中身は大きく2種類に分かれる：

- **文書系（`.doc`/`.idt`/`.hg-idt*`、`.tl-c`、将来の余白ノート）**：sidenote-pdfの編集モデル（段落単位の直接編集＋MD書き出し）と相性が良く、拡張の本命
- **サイト構成系（`.hero-band`、`.agm-section`、`.card-accordion`、対照カード群）**：ページのフレーム自体を組む部品で、WYSIWYG化するなら別枠の「ページテンプレート選択」に近い設計になる（1文書エディタというより1ページビルダー）

この2つを最初から同じUIで扱おうとすると設計が肥大化しそうなので、次に決めたいのは「まず文書系だけを対象にするか」です。
