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
  <a href="https://twitter.com/share?url=https://minnanosaiban.github.io/hotline/trial/ &text=株主総会意見 - ＥＮＥＯＳの内部通報制度をめぐる訴訟について"
     target="_blank" class="x-share" style="color: #FFFFFF;">
    <i class="fa-brands fa-x-twitter"></i> でシェア
  </a>
</p>

<p class="blog-main-title">株 × Python × ML</p>

<p>
Python と 機械学習を使って、株価・決算短信・有報を分析してみました。
</p>

<p class="large" style="margin-top: 12rem !important; margin-bottom: 1rem !important;">おすすめの読み順</p>

<p class="margin02">ＥＮＥＯＳの "ピークアウト構図" という単一の物語。<b>「ＥＮＥＯＳの 2022 ピーク利益 5,371 億円が、なぜ、どこで、いつ剥落したのか」</b> を多角的に解剖していきます。</p>

</div>

<div class="toc-grid" style="margin-top: 0.8rem;">
<a href="posts/03_xbrl_to_json/" class="toc-card">
<span class="toc-card-num">読む順 1</span>
<span class="toc-card-title">1-3 XBRL を JSON に変換して分析</span>
<span class="toc-card-desc">ＥＮＥＯＳ を時系列で見る</span>
</a>
<a href="posts/04_garp_peg_roe/" class="toc-card">
<span class="toc-card-num">読む順 2</span>
<span class="toc-card-title">2-1 GARP</span>
<span class="toc-card-desc">4 基準試算で「構造劣化かサイクル正常化か」を判定</span>
</a>
<a href="posts/06_accrual_analysis/" class="toc-card">
<span class="toc-card-num">読む順 3</span>
<span class="toc-card-title">2-3 アクルーアル分析</span>
<span class="toc-card-desc">ピーク利益はキャッシュで裏付けられていたか（利益の質）</span>
</a>
<a href="posts/08b_segment_core_stocks/" class="toc-card">
<span class="toc-card-num">読む順 4</span>
<span class="toc-card-title">2-6 コングロマリット・ディスカウント</span>
<span class="toc-card-desc">どのセグメントで剥落したか（OPM 内訳）</span>
</a>
<a href="posts/09b_narrative_car/" class="toc-card">
<span class="toc-card-num">読む順 5</span>
<span class="toc-card-title">2-8 ベンチマーク</span>
<span class="toc-card-desc">市場が織り込んだ瞬間</span>
</a>
</div>

<p class="toc-phase-label" style="margin-top: 4rem;">株価分析　全記事</p>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 無料データ取得</p>
<div class="toc-grid">
<a href="posts/01_get_stock_prices/" class="toc-card">
<span class="toc-card-num">1-1</span>
<span class="toc-card-title">株価を取得しよう</span>
<span class="toc-card-desc">yfinance → parquet → チャート</span>
</a>
<a href="posts/02_collect_other_data/" class="toc-card">
<span class="toc-card-num">1-2</span>
<span class="toc-card-title">株価以外も取得しよう</span>
<span class="toc-card-desc">EDINET・TDnet・証券会社のアプリを活用</span>
</a>
<a href="posts/03_xbrl_to_json/" class="toc-card">
<span class="toc-card-num">1-3</span>
<span class="toc-card-title">XBRL を JSON に変換して分析</span>
<span class="toc-card-desc">決算書そのものを分析に使う</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> データで銘柄分析</p>
<div class="toc-grid">
<a href="posts/04_garp_peg_roe/" class="toc-card">
<span class="toc-card-num">2-1</span>
<span class="toc-card-title">GARP</span>
<span class="toc-card-desc">PEG × ROE の理論と実践</span>
</a>
<a href="posts/05_multifactor_scoreboard/" class="toc-card">
<span class="toc-card-num">2-2</span>
<span class="toc-card-title">マルチファクタースコアボード</span>
<span class="toc-card-desc">7 軸で全方位優等生を探す</span>
</a>
<a href="posts/06_accrual_analysis/" class="toc-card">
<span class="toc-card-num">2-3</span>
<span class="toc-card-title">アクルーアル分析</span>
<span class="toc-card-desc">利益の質を CF で見抜く</span>
</a>
<a href="posts/07_triangulation/" class="toc-card">
<span class="toc-card-num">2-4</span>
<span class="toc-card-title">予想 × 業績</span>
<span class="toc-card-desc">コンセンサス × ガイダンス × 業績でズレを見抜く</span>
</a>
<a href="posts/08_segment_analysis/" class="toc-card">
<span class="toc-card-num">2-5</span>
<span class="toc-card-title">セグメント発進力スコア</span>
<span class="toc-card-desc">次の主力事業・隠れた高収益事業を発掘</span>
</a>
<a href="posts/08b_segment_core_stocks/" class="toc-card">
<span class="toc-card-num">2-6</span>
<span class="toc-card-title">コングロマリット・ディスカウント</span>
<span class="toc-card-desc">総合商社・ＥＮＥＯＳ をセグメントで読み解く</span>
</a>
<a href="posts/09_car_event_study/" class="toc-card">
<span class="toc-card-num">2-7</span>
<span class="toc-card-title">CAR イベントスタディ</span>
<span class="toc-card-desc">PEAD を検証</span>
</a>
<a href="posts/09b_narrative_car/" class="toc-card">
<span class="toc-card-num">2-8</span>
<span class="toc-card-title">二重CAR（ベンチマーク）</span>
<span class="toc-card-desc">業界の動きを除いた個別決算の効き</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 機械学習に挑戦</p>
<div class="toc-grid">
<a href="posts/10_similar_earnings_search/" class="toc-card">
<span class="toc-card-num">3-1</span>
<span class="toc-card-title">類似決算検索</span>
<span class="toc-card-desc">コサイン類似度で似た決算を発見</span>
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
</div>
