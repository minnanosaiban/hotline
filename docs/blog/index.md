---
title: 株 × Python × ML - ENEOSの内部通報制度をめぐる訴訟について - ENEOS裁判 （エネオス）-
description: ENEOS（エネオス）の内部通報制度をめぐる訴訟について、裁判文書をもとに当事者双方の主張を公開しています。調査事項のすり替え・通報者への誤認誘導・不正送金となり得る解決策など、具体的な問題を記録しています。株主総会や記者会見で問題提起しています。
# date: 2023-03-06
# categories:
  # - NTTデータにおけるセクハラに関する紛争
  # - 労働委員会
# tags:
  # - NTTデータ
  # - パーソルテンプスタッフ
  # - セクハラ
  # - 雇止め
# links:
  # - [東京労働委員会命令書](https://www.metro.tokyo.lg.jp/information/press/2024/03/2024030701)
  # - [命令書別紙](https://www.metro.tokyo.lg.jp/documents/d/tosei/01_01b_02)
# url: https://minnanosaiban.github.io/hotline/trial/
# image: https://minnanosaiban.github.io/hotline/img/card1.png
twitter_card: summary
hide:
    - date
    # - navigation
    # - toc
# icon: material/home
---

<style>.md-typeset h1 { display: none !important; }</style>

<p>
  <a href="https://twitter.com/share?url=https://minnanosaiban.github.io/hotline/trial/ &text=裁判文書公開 - ＥＮＥＯＳの内部通報制度をめぐる訴訟について"
     target="_blank" class="x-share" style="color: #FFFFFF;">
    <i class="fa-brands fa-x-twitter"></i> でシェア
  </a>
</p>

<p class="blog-main-title">株 × Python × ML</p>

<p>
Python と 機械学習を使って、株価・決算短信・有報を分析してみました。
</p>

## おすすめの読み順

<div class="toc-grid" style="margin-top: 0.8rem;">
<a href="posts/03_xbrl_to_json/" class="toc-card">
<span class="toc-card-num">読む順 1</span>
<span class="toc-card-title">1-3 決算 XBRL を JSON に変換</span>
<span class="toc-card-desc">決算そのものを分析、元売3社業績比較</span>
</a>
<a href="posts/04_garp_peg_roe/" class="toc-card">
<span class="toc-card-num">読む順 2</span>
<span class="toc-card-title">2-1 4象限で GARP を見る</span>
<span class="toc-card-desc">「成長と割安の両立銘柄」を発掘</span>
</a>
<a href="posts/06_accrual_analysis/" class="toc-card">
<span class="toc-card-num">読む順 3</span>
<span class="toc-card-title">2-3 アクルーアル分析</span>
<span class="toc-card-desc">ＥＮＥＯＳ「ピークの裏付けは？」、キャッシュ実態</span>
</a>
<a href="posts/08b_segment_core_stocks/" class="toc-card">
<span class="toc-card-num">読む順 4</span>
<span class="toc-card-title">2-6 コングロマリット・ディスカウント</span>
<span class="toc-card-desc">総合商社・ＥＮＥＯＳ をセグメントで読み解く</span>
</a>
<a href="posts/09b_narrative_car/" class="toc-card">
<span class="toc-card-num">読む順 5</span>
<span class="toc-card-title">2-7 CARで見る「決算の効き」</span>
<span class="toc-card-desc">主要5社の個別決算の効きをCARで検証</span>
</a>
</div>

## 株価分析　目次

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 無料データを取得編</p>
<div class="toc-grid">
<a href="posts/01_get_stock_prices/" class="toc-card">
<span class="toc-card-num">1-1</span>
<span class="toc-card-title">まず、「株価」を取得する</span>
<span class="toc-card-desc">parquet 保存からチャートまで、自作アプリも</span>
</a>
<a href="posts/02_collect_other_data/" class="toc-card">
<span class="toc-card-num">1-2</span>
<span class="toc-card-title">EDINET・TDnet 等を活用</span>
<span class="toc-card-desc">企業が開示している決算 XBRL は使える</span>
</a>
<a href="posts/03_xbrl_to_json/" class="toc-card">
<span class="toc-card-num">1-3</span>
<span class="toc-card-title"> 決算 XBRL を JSON に変換</span>
<span class="toc-card-desc">決算そのものを分析、元売3社業績比較</span>
</a>
</div>
<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 決算データで分析編</p>
<div class="toc-grid">
<a href="posts/04_garp_peg_roe/" class="toc-card">
<span class="toc-card-num">2-1</span>
<span class="toc-card-title">4象限で GARP を見る</span>
<span class="toc-card-desc">「成長と割安の両立銘柄」を発掘</span>
</a>
<a href="posts/05_multifactor_scoreboard/" class="toc-card">
<span class="toc-card-num">2-2</span>
<span class="toc-card-title">マルチファクタースコア</span>
<span class="toc-card-desc">7 軸で全方位優等生を探す</span>
</a>
<a href="posts/06_accrual_analysis/" class="toc-card">
<span class="toc-card-num">2-3</span>
<span class="toc-card-title">アクルーアル分析</span>
<span class="toc-card-desc">ＥＮＥＯＳ「ピークの裏付けは？」、キャッシュ実態</span>
</a>
<a href="posts/07_triangulation/" class="toc-card">
<span class="toc-card-num">2-4</span>
<span class="toc-card-title">コンセンサス予想を検証</span>
<span class="toc-card-desc"> 「予想のズレ」で将来の業績修正の向きを先回り</span>
</a>
<a href="posts/08_segment_analysis/" class="toc-card">
<span class="toc-card-num">2-5</span>
<span class="toc-card-title">セグメント分析</span>
<span class="toc-card-desc">発進力スコアリングで隠れた高収益事業を発掘</span>
</a>
<a href="posts/08b_segment_core_stocks/" class="toc-card">
<span class="toc-card-num">2-6</span>
<span class="toc-card-title">コングロマリット・ディスカウント</span>
<span class="toc-card-desc">総合商社・ＥＮＥＯＳをセグメントで読み解く</span>
</a>
<a href="posts/09b_narrative_car/" class="toc-card">
<span class="toc-card-num">2-7</span>
<span class="toc-card-title">CARで見る「決算の効き」</span>
<span class="toc-card-desc">元売・商社 主要5社の市場反応を検証</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 機械学習チャレンジ編</p>
<div class="toc-grid">
<a href="posts/10_similar_earnings_search/" class="toc-card">
<span class="toc-card-num">3-1</span>
<span class="toc-card-title">コサイン類似度</span>
<span class="toc-card-desc">数値特徴量で「類似決算」を発見</span>
</a>
<a href="posts/11_knn_prediction/" class="toc-card">
<span class="toc-card-num">3-2</span>
<span class="toc-card-title">K-NN 分類</span>
<span class="toc-card-desc">似た決算群から外れた個別ショックを抽出</span>
</a>
<a href="posts/12_earnings_clustering/" class="toc-card">
<span class="toc-card-num">3-3</span>
<span class="toc-card-title">K-means クラスタリング</span>
<span class="toc-card-desc">教師なし学習が分けた「決算の型」</span>
</a>
<a href="posts/13_random_forest/" class="toc-card">
<span class="toc-card-num">3-4</span>
<span class="toc-card-title">ランダムフォレスト</span>
<span class="toc-card-desc">予測は失敗、特徴量重要度の落とし穴を学ぶ</span>
</a>
<a href="posts/14_price_clustering/" class="toc-card">
<span class="toc-card-num">3-5</span>
<span class="toc-card-title">階層型クラスタリング</span>
<span class="toc-card-desc">値動きの相関で再現する業界地図</span>
</a>
<a href="posts/15_price_anomaly/" class="toc-card">
<span class="toc-card-num">3-6</span>
<span class="toc-card-title">PCA 異常検知</span>
<span class="toc-card-desc">値動きの「共動の崩れ」で突発材料を検出</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 番外編</p>
<div class="toc-grid">
<a href="posts/16_intraday_stats/" class="toc-card">
<span class="toc-card-num">EX-1</span>
<span class="toc-card-title">超短期のエッジ検証</span>
<span class="toc-card-desc">5分足×コスト控除後、残ったのは場中開示だけ</span>
</a>
<a href="posts/17_intraday_ml/" class="toc-card">
<span class="toc-card-num">EX-2</span>
<span class="toc-card-title">LightGBM で次の5分</span>
<span class="toc-card-desc">並べ替えはできる、でもコストに勝てない</span>
</a>
</div>

<div class="md-footer-note" style="margin-top: 3rem;">
  <div class="md-footer-note__section">
    <p class="md-footer-note__heading">データの取り扱いについて</p>
    <ul>
      <li>本アプリは個人利用および学習を目的としたツールであり、投資勧誘を目的としたものではありません。</li>
      <li>yfinance ライブラリを使用しています。利用にあたっては、Yahoo! 規約を遵守してください。</li>
      <li>短時間での大量取得はサーバーに負担がかかります。API のレート制限を守り、過度なリクエストは避けてください。</li>
    </ul>
  </div>
  <div class="md-footer-note__section">
    <p class="md-footer-note__heading">⚠️ 免責事項</p>
    <ul>
      <li><strong>データの正確性</strong>: 取得データは正確性や即時性を保証しません。</li>
      <li><strong>損害への責任</strong>: 本ツールの利用により生じたいかなる損害についても、制作者は一切の責任を負いません。</li>
    </ul>
  </div>
</div>
