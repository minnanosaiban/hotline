---
title: スタイルガイド（見本帳）
description: hotlineサイトの全コンポーネントを1ページに並べた内部向け見本帳です。
hide:
  - navigation
  - toc
---

<style>
/* この見本帳ページ専用の最小スタイル（サイト共通CSSには足さない） */
.sg-label {
  display: block;
  font-family: ui-monospace, "Consolas", monospace;
  font-size: 12px;
  color: var(--md-default-fg-color--light);
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
  padding-bottom: 0.3rem;
  margin: 4rem auto 1.2rem !important;
  max-width: 32rem;
  width: 100%;
}
.sg-swatches {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  max-width: 32rem;
  margin-left: auto;
  margin-right: auto;
}
.sg-swatch {
  width: 9.2rem;
  font-size: 11px;
  font-family: ui-monospace, "Consolas", monospace;
  color: var(--md-default-fg-color--light);
}
.sg-swatch i {
  display: block;
  height: 2.6rem;
  border-radius: 4px;
  border: 1px solid var(--md-default-fg-color--lightest);
  margin-bottom: 0.25rem;
}
</style>

<div class="center-container" markdown>

<div class="hero-band" markdown>
# スタイルガイド
<p>
本サイトの全コンポーネントを一覧する内部向けの見本帳です（ナビには載せていません）。正本は <code>DESIGN_SYSTEM.md</code>。ここでの見た目が崩れていたら、どこかの変更が回帰を起こしています。
</p>
</div>

<div markdown>

<p class="sg-label">0. 色トークン（01-color.css）</p>

<div class="sg-swatches">
<span class="sg-swatch"><i style="background: var(--md-link-color)"></i>--md-link-color<br>メイン青</span>
<span class="sg-swatch"><i style="background: var(--md-warn-red)"></i>--md-warn-red<br>警告赤</span>
<span class="sg-swatch"><i style="background: var(--red-color-3)"></i>--red-color-3<br>サイドノート赤</span>
<span class="sg-swatch"><i style="background: var(--md-accent-color)"></i>--md-accent-color<br>ENEOS橙</span>
<span class="sg-swatch"><i style="background: var(--surface-gray)"></i>--surface-gray<br>面グレー</span>
<span class="sg-swatch"><i style="background: var(--md-card-border)"></i>--md-card-border<br>枠線グレー</span>
</div>

<p class="sg-label">0.5 文字サイズスケール（03-typeset.css）</p>

<p class="width-40"><span class="largest">.largest 2.56rem</span></p>
<p class="width-40"><span class="larger">.larger 1.6rem（h2同等）</span></p>
<p class="width-40"><span class="large">.large 1.28rem</span></p>
<p class="width-40">本文 16px（.md-content p）── 太字は<b>タグで</b>、色は<span class="text-main">.text-main</span>と<span class="text-warn">.text-warn</span>で。</p>
<p class="width-40"><span class="smaller">.smaller 14px</span>　<span class="smallest">.smallest 12px</span></p>
<p class="width-40 doc">.doc 16px 明朝（裁判文書用、行間2.4）</p>

<p class="sg-label">1. 見出し（.sec-title／.issue-point／.bar-title）</p>

<p class="sec-title">
節見出し<br>.sec-title
</p>

<p class="width-40 issue-point">.issue-point ── 1.2rem太字の小見出し</p>

<p class="larger width-40 margin02 agree-gap bar-title">
行頭バー見出し（.bar-title + .larger）
</p>
<p class="width-40">
バー見出しの直後に来る本文段落。上余白は見出し側の .agree-gap（実質98px）が持つ。
</p>

<p class="sg-label">1.5 ボタン・リンク（.x-share／.repo-link）</p>

<p class="width-40">
<a href="https://minnanosaiban.github.io/hotline/" class="x-share"><i class="fa-brands fa-x-twitter"></i> でシェア</a>
</p>

<div class="repo-link-wrap">
<a class="repo-link" href="https://minnanosaiban.github.io/hotline/" target="_blank" rel="noopener">
<i class="repo-link-icon bi bi-filetype-pdf"></i>
<span class="repo-link-path">ＰＤＦの用意があります（.repo-link）</span>
<i class="repo-link-arrow fa-solid fa-arrow-up-right-from-square"></i>
</a>
</div>

<p class="sg-label">2. カード（.card-blue／.toc-card／対照カード）</p>

<div class="card-blue audio-wide">
<p  class="larger center margin01">
音声解説カード（.card-blue.audio-wide）</p>
<div class="audio-content center margin02">
  <audio controls preload="none">
    <source src="https://minnanosaiban.github.io/hotline/img/eneos_202508.m4a" type="audio/wav">
    お使いのブラウザは audio 要素をサポートしていません。
  </audio>
</div>
<p class="center smallest">
NotebookLM により生成（.smallest の注記行）
</p>
</div>

<div class="toc-grid">
<a href="https://minnanosaiban.github.io/hotline/trial/eneos/" class="toc-card">
<span class="toc-card-num">被告</span>
<span class="toc-card-title">リンクカード（.toc-card）</span>
<span class="toc-card-desc">2列グリッド（.toc-grid）で使用</span>
</a>
<a href="https://minnanosaiban.github.io/hotline/trial/whistleblower/" class="toc-card">
<span class="toc-card-num">原告</span>
<span class="toc-card-title">リンクカード（.toc-card）</span>
<span class="toc-card-desc">ホバーで box-shadow が浮く</span>
</a>
</div>

<p class="width-40 margin02">
対照カード（agm の質疑検証。.eneos-card ＝会社公表／.qa-turn ＝実際の質問・検証）：
</p>
<div class="eneos-card width-40">
<span class="qa-mark qa-mark--eneos">ENEOSが公表する株主質問</span>
<p><b>個別案件を踏まえ、コンプライアンスと安全についてどのように考えているか伺いたい。</b></p>
<a class="eneos-timestamp" href="https://www.youtube.com/watch?v=0kWavfBMS30&t=2455s" target="_blank" rel="noopener"><i class="fa-brands fa-youtube"></i> Youtube　ENEOS TV 40:55</a>
</div>
<div class="qa-turn qa-turn--student width-40">
<span class="qa-mark qa-mark--student">🧑</span>
<p class="qa-body">
<b>実際の株主質問の趣旨は？</b><br>
（.qa-turn--student の見本テキスト）
</p>
</div>
<div class="qa-turn qa-turn--eval width-40">
<span class="qa-mark qa-mark--eval">検証</span>
<p class="qa-body">
<b>正しく公開されている？</b><br>
（.qa-turn--eval の見本テキスト）
</p>
</div>

<p class="sg-label">2.1 グレー枠（.agm-section）── 余白の単一所有の原則で組む</p>

<div class="agm-section" markdown>

<p class="sec-title">
<span class="text-main">枠内の<br>節見出し</span>
</p>

<p class="width-40 verdict-lead">
節見出し直下のリード（.verdict-lead）。上余白は実質98px（枠外 .agree-gap と同値）。
</p>

<p class="width-40 margin04 bar-title">
<span class="larger">番号付き小見出し（.margin04）</span><br>
ただし書き行はこの位置
</p>
<p class="width-40 margin02">
枠内の本文段落（.margin02）。新しい段落は .margin02／.margin04 を付けるだけでよい（隣接補正は不要）。
</p>

</div>

<p class="sg-label">3. アコーディオン（.card-accordion）＋実文/例文カード</p>

<details class="card-accordion width-40" markdown>
<summary>開閉見本 ── 中に実文カードと例文カード</summary>
<div class="accordion-body" markdown>

<div class="q-card" markdown>
実文カード（.q-card）── グレー地。実在の引用に使う。
</div>

<div class="ex-card" markdown>
例文カード（.ex-card）── 白地＋破線。サイト作成の架空例文に使う。
</div>

</div>
</details>

<p class="sg-label">4. 裁判文書のインデント（.doc／.idt／.hg-idt 系）</p>

<div class="width-40" markdown>
<p class="doc">.doc ── 字下げなし。明朝・行間2.4。</p>
<p class="idt">.idt ── 通常の字下げ（1em）。段落本文に使う。この行が折り返しても2行目は左端に戻る。</p>
<p class="pad2 hg-idt">第１　.pad2 .hg-idt ── ぶら下げインデント。項目番号の後で折り返すと、2行目以降が本文開始位置に揃う見本です。</p>
<p class="pad3 hg-idt">１　ひとつ深い階層（.pad3 .hg-idt）</p>
<p class="pad5 hg-idt2">⑴　さらに深い階層（.hg-idt2 ＝ぶら下げ幅2em）で長い行を折り返したときの見本です。</p>
<p class="doc doc-gap-top">.doc-gap-top ── 段落の前に1.6emのゆとり（この段落）。</p>
</div>

<p class="sg-label">5. カルーセル（.qa-carousel）── 配置制約あり</p>

<p class="width-40 qa-carousel-lead">
本文ラッパーの外（center-container直下）に置くこと。見本は3枚。
</p>

</div>

<div class="qa-carousel swiper">
<div class="swiper-wrapper">
<div class="swiper-slide"><img class="qa-shot" src="../agm/img/q01.png" alt="カルーセル見本1" loading="lazy"></div>
<div class="swiper-slide"><img class="qa-shot" src="../agm/img/q02.png" alt="カルーセル見本2" loading="lazy"></div>
<div class="swiper-slide"><img class="qa-shot" src="../agm/img/q03.png" alt="カルーセル見本3" loading="lazy"></div>
</div>
<div class="swiper-pagination"></div>
</div>

<div markdown>

<p class="width-40 gap-6 smaller">
余白スケール：1 / 2 / 4 / 6 / 8rem（モバイルは6rem系→3rem、4rem系は圧縮なし）。新しい値は発明せず、縦余白は「下の要素が margin-top で持つ」。詳細は DESIGN_SYSTEM.md 0.5章。
</p>

</div>

</div>
