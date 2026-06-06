---
title: 株 × Python × ML
description: ＥＮＥＯＳは、元社長のセクハラ不祥事を受け、宮田社長らがコンプライアンス徹底を表明しましたが、通報者に対する「法改正があった」との虚偽通知の疑いについて正面から向き合っていません。この問題について株主総会で問題提起をします。
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


</div>

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
<span class="toc-card-title">2-7 CARで「決算の効き」を測る</span>
<span class="toc-card-desc">主要5社の個別決算の効きをCARで検証</span>
</a>
</div>

## 株価分析　全記事

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
<span class="toc-card-desc">企業が金融庁に提出している決算 XBRL は使える</span>
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
<span class="toc-card-title">CARで「決算の効き」を測る</span>
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
<span class="toc-card-title">K-NN で値動き予測を試した話</span>
<span class="toc-card-desc">予測より発見のツールとして実用化</span>
</a>
<a href="posts/12_earnings_clustering/" class="toc-card">
<span class="toc-card-num">3-3</span>
<span class="toc-card-title">決算クラスタリング</span>
<span class="toc-card-desc">k-means で「決算の型」を3つ発見</span>
</a>
<a href="posts/13_random_forest/" class="toc-card">
<span class="toc-card-num">3-4</span>
<span class="toc-card-title">ランダムフォレスト</span>
<span class="toc-card-desc">予測は失敗、特徴量重要度の落とし穴を学ぶ</span>
</a>
<a href="posts/14_price_clustering/" class="toc-card">
<span class="toc-card-num">3-5</span>
<span class="toc-card-title">値動きクラスタリング</span>
<span class="toc-card-desc">業種コードなしに業界が再現された相関クラスタ</span>
</a>
<a href="posts/15_price_anomaly/" class="toc-card">
<span class="toc-card-num">3-6</span>
<span class="toc-card-title">突発材料の異常検知</span>
<span class="toc-card-desc">共動の崩れで「その銘柄だけ動いた日」を検出</span>
</a>
</div>
