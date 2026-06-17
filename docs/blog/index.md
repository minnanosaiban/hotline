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
Python と機械学習で、株価・決算短信・有価証券報告書を読み解きます。無料で手に入るデータとコードだけで、データ取得から企業価値分析・機械学習まで再現できます。
</p>

## おすすめの読み順

<div class="toc-grid" style="margin-top: 0.8rem;">
<a href="posts/02-08_enterprise_value/" class="toc-card">
<span class="toc-card-num">読む順 1</span>
<span class="toc-card-title">2-8 EVで見る「会社の値段」</span>
<span class="toc-card-desc">時価総額に借金を足し、13社を簡易DCFで検証</span>
</a>
<a href="posts/02-03_accrual_analysis/" class="toc-card">
<span class="toc-card-num">読む順 2</span>
<span class="toc-card-title">2-3 アクルーアル分析</span>
<span class="toc-card-desc">ＥＮＥＯＳの最高益に「現金の裏付け」はあるか</span>
</a>
<a href="posts/02-06_segment_core_stocks/" class="toc-card">
<span class="toc-card-num">読む順 3</span>
<span class="toc-card-title">2-6 コングロマリット・ディスカウント</span>
<span class="toc-card-desc">総合商社・ＥＮＥＯＳ をセグメントで読み解く</span>
</a>
<a href="posts/02-07_narrative_car/" class="toc-card">
<span class="toc-card-num">読む順 4</span>
<span class="toc-card-title">2-7 CARで見る「決算の効き」</span>
<span class="toc-card-desc">主要5社の個別決算の効きをCARで検証</span>
</a>
<a href="posts/01-03_xbrl_to_json/" class="toc-card">
<span class="toc-card-num">読む順 5</span>
<span class="toc-card-title">1-3 決算 XBRL を JSON に変換</span>
<span class="toc-card-desc">自分で再現するなら ― データの作り方から</span>
</a>
</div>

## 連載目次

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 無料データを取得編</p>
<div class="toc-grid">
<a href="posts/01-01_get_stock_prices/" class="toc-card">
<span class="toc-card-num">1-1</span>
<span class="toc-card-title">まず、「株価」を取得する</span>
<span class="toc-card-desc">yfinance から parquet 保存、自作アプリまで</span>
</a>
<a href="posts/01-02_collect_other_data/" class="toc-card">
<span class="toc-card-num">1-2</span>
<span class="toc-card-title">決算データを無料で集める</span>
<span class="toc-card-desc">EDINET・TDnet の公式 XBRL を活用</span>
</a>
<a href="posts/01-03_xbrl_to_json/" class="toc-card">
<span class="toc-card-num">1-3</span>
<span class="toc-card-title">決算 XBRL を JSON に変換</span>
<span class="toc-card-desc">「決算そのもの」を分析、元売3社を比較</span>
</a>
<a href="posts/EX-03_kessan_note_app/" class="toc-card">
<span class="toc-card-num">番外編</span>
<span class="toc-card-title">決算Noteで記事下書き</span>
<span class="toc-card-desc">JSONから記事プロンプトを自動生成するアプリ</span>
</a>
</div>
<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 決算データで分析編</p>
<div class="toc-grid">
<a href="posts/02-01_garp_peg_roe/" class="toc-card">
<span class="toc-card-num">2-1</span>
<span class="toc-card-title">4象限で GARP を見る</span>
<span class="toc-card-desc">「成長と割安の両立」銘柄を探す</span>
</a>
<a href="posts/02-02_multifactor_scoreboard/" class="toc-card">
<span class="toc-card-num">2-2</span>
<span class="toc-card-title">マルチファクタースコア</span>
<span class="toc-card-desc">7軸で「全方位の優等生」を探す</span>
</a>
<a href="posts/02-03_accrual_analysis/" class="toc-card">
<span class="toc-card-num">2-3</span>
<span class="toc-card-title">アクルーアル分析</span>
<span class="toc-card-desc">ＥＮＥＯＳの最高益に「現金の裏付け」はあるか</span>
</a>
<a href="posts/02-04_triangulation/" class="toc-card">
<span class="toc-card-num">2-4</span>
<span class="toc-card-title">コンセンサス予想を検証</span>
<span class="toc-card-desc">会社予想とのズレから「修正の向き」を読む</span>
</a>
<a href="posts/02-05_segment_analysis/" class="toc-card">
<span class="toc-card-num">2-5</span>
<span class="toc-card-title">セグメント分析</span>
<span class="toc-card-desc">連結に埋もれた「強い事業」を発進力スコアで探す</span>
</a>
<a href="posts/02-06_segment_core_stocks/" class="toc-card">
<span class="toc-card-num">2-6</span>
<span class="toc-card-title">コングロマリット・ディスカウント</span>
<span class="toc-card-desc">総合商社・ＥＮＥＯＳをセグメントで読み解く</span>
</a>
<a href="posts/02-07_narrative_car/" class="toc-card">
<span class="toc-card-num">2-7</span>
<span class="toc-card-title">CARで見る「決算の効き」</span>
<span class="toc-card-desc">元売・商社 主要5社の市場反応を検証</span>
</a>
<a href="posts/02-08_enterprise_value/" class="toc-card">
<span class="toc-card-num">2-8</span>
<span class="toc-card-title">EVで見る「会社の値段」</span>
<span class="toc-card-desc">時価総額に借金を足し、13社を簡易DCFで検証</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 機械学習チャレンジ編</p>
<div class="toc-grid">
<a href="posts/03-01_similar_earnings_search/" class="toc-card">
<span class="toc-card-num">3-1</span>
<span class="toc-card-title">コサイン類似度</span>
<span class="toc-card-desc">「似ている決算」を数値で検索する</span>
</a>
<a href="posts/03-02_knn_prediction/" class="toc-card">
<span class="toc-card-num">3-2</span>
<span class="toc-card-title">K-NN 分類</span>
<span class="toc-card-desc">似た決算群から外れた「個別ショック」を検出</span>
</a>
<a href="posts/03-03_earnings_clustering/" class="toc-card">
<span class="toc-card-num">3-3</span>
<span class="toc-card-title">K-means クラスタリング</span>
<span class="toc-card-desc">教師なし学習が分けた「決算の型」</span>
</a>
<a href="posts/03-04_random_forest/" class="toc-card">
<span class="toc-card-num">3-4</span>
<span class="toc-card-title">ランダムフォレスト</span>
<span class="toc-card-desc">予測は失敗、「特徴量重要度」の落とし穴を学ぶ</span>
</a>
<a href="posts/03-05_price_clustering/" class="toc-card">
<span class="toc-card-num">3-5</span>
<span class="toc-card-title">階層型クラスタリング</span>
<span class="toc-card-desc">値動きの相関で再現する業界地図</span>
</a>
<a href="posts/03-06_price_anomaly/" class="toc-card">
<span class="toc-card-num">3-6</span>
<span class="toc-card-title">PCA 異常検知</span>
<span class="toc-card-desc">値動きの「共動の崩れ」で突発材料を検出</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 番外編</p>
<div class="toc-grid">
<a href="posts/EX-01_intraday_stats/" class="toc-card">
<span class="toc-card-num">EX-1</span>
<span class="toc-card-title">超短期のエッジを統計で探す</span>
<span class="toc-card-desc">5分足×コスト控除後、残ったのは場中開示だけ</span>
</a>
<a href="posts/EX-02_intraday_ml/" class="toc-card">
<span class="toc-card-num">EX-2</span>
<span class="toc-card-title">LightGBM で「次の5分」を当てられるか</span>
<span class="toc-card-desc">並べ替えはできる、でもコストに勝てない</span>
</a>
</div>

<p class="toc-phase-label"><i class="fa-solid fa-layer-group"></i> 用語集</p>
<div class="toc-grid">
<a href="glossary/" class="toc-card">
<span class="toc-card-num">用語集</span>
<span class="toc-card-title">50音順用語集</span>
<span class="toc-card-desc">財務・会計・機械学習・データの用語集</span>
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
