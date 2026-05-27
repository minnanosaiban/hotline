---
title: 株 × Python × AI
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

<p class="blog-main-title">株 × Python × AI</p>

<p>
Python と AI を使って、株価・決算短信・有報を分析してみました。
</p>

<p class="large" style="margin-top: 12rem !important; margin-bottom: 1rem !important;">おすすめの読み順</p>

<p class="margin02">ＥＮＥＯＳの "ピークアウト構図" という単一の物語。<b>「ＥＮＥＯＳの 2022 ピーク利益 5,371 億円が、なぜ、どこで、いつ剥落したのか」</b> を多角的に解剖していきます。</p>

</div>

<div class="toc-grid" style="margin-top: 0.8rem;">
<a href="posts/06_what_is_xbrl/" class="toc-card">
<span class="toc-card-num">読む順 1</span>
<span class="toc-card-title">連載06 XBRL とは何か</span>
<span class="toc-card-desc">ＥＮＥＯＳ純利 5,371→2,261 億の半減を見る</span>
</a>
<a href="posts/09_progress_zscore/" class="toc-card">
<span class="toc-card-num">読む順 2</span>
<span class="toc-card-title">連載09 進捗率 Z-score 早期警報</span>
<span class="toc-card-desc">3 ヶ月先の下方修正を Z-score で検出</span>
</a>
<a href="posts/10_accrual_analysis/" class="toc-card">
<span class="toc-card-num">読む順 3</span>
<span class="toc-card-title">連載10 アクルーアル分析</span>
<span class="toc-card-desc">2022 ピーク利益はキャッシュで裏付けられていなかった</span>
</a>
<a href="posts/02_multifactor_scoreboard/" class="toc-card">
<span class="toc-card-num">読む順 4</span>
<span class="toc-card-title">連載02 マルチファクタースコアボード</span>
<span class="toc-card-desc">業種代表 51 銘柄の中での ＥＮＥＯＳ の相対評価</span>
</a>
<a href="posts/13_car_event_study/" class="toc-card">
<span class="toc-card-num">読む順 5</span>
<span class="toc-card-title">連載13 CAR イベントスタディ</span>
<span class="toc-card-desc">CAR [-1,+20] = −13.89%、市場がピークアウトを織り込んだ瞬間</span>
</a>
</div>

<p class="toc-phase-label" style="margin-top: 4rem;">株価分析　全記事</p>

<p class="toc-phase-label">フェーズ1　無料データで作る業績スクリーニング</p>
<div class="toc-grid">
<a href="posts/01_garp_peg_roe/" class="toc-card">
<span class="toc-card-num">連載 01</span>
<span class="toc-card-title">PEG × ROE</span>
<span class="toc-card-desc">GARP の理論と実践</span>
</a>
<a href="posts/02_multifactor_scoreboard/" class="toc-card">
<span class="toc-card-num">連載 02</span>
<span class="toc-card-title">マルチファクタースコアボード</span>
<span class="toc-card-desc">7 軸で全方位優等生を探す</span>
</a>
<a href="posts/03_eps_revision_momentum/" class="toc-card">
<span class="toc-card-num">連載 03</span>
<span class="toc-card-title">EPS リビジョン・モメンタム</span>
<span class="toc-card-desc">出遅れ買い候補を発掘する</span>
</a>
<a href="posts/04_surprise_scoreboard/" class="toc-card">
<span class="toc-card-num">連載 04</span>
<span class="toc-card-title">連続サプライズ・スコアボード</span>
<span class="toc-card-desc">業績モメンタムが本物の銘柄</span>
</a>
<a href="posts/05_credit_supply_dashboard/" class="toc-card">
<span class="toc-card-num">連載 05</span>
<span class="toc-card-title">信用需給ダッシュボード</span>
<span class="toc-card-desc">踏み上げ候補を業績 × 需給で絞る</span>
</a>
</div>

<p class="toc-phase-label">フェーズ2　XBRL で決算データの中身に手を伸ばす</p>
<div class="toc-grid">
<a href="posts/06_what_is_xbrl/" class="toc-card">
<span class="toc-card-num">連載 06</span>
<span class="toc-card-title">XBRL とは何か</span>
<span class="toc-card-desc">ＥＮＥＯＳ純利益 5,371→2,261 億の半減</span>
</a>
<a href="posts/07_edinet_tdnet_parse/" class="toc-card">
<span class="toc-card-num">連載 07</span>
<span class="toc-card-title">EDINET / TDnet 取得とパース</span>
<span class="toc-card-desc">ZIP → JSON パイプラインの全工程</span>
</a>
<a href="posts/08_kessan_json_schema/" class="toc-card">
<span class="toc-card-num">連載 08</span>
<span class="toc-card-title">決算短信 JSON スキーマ設計</span>
<span class="toc-card-desc">263 マッピングルールの 5 原則</span>
</a>
</div>

<p class="toc-phase-label">フェーズ3　XBRL を投資シグナルに変換する</p>
<div class="toc-grid">
<a href="posts/09_progress_zscore/" class="toc-card">
<span class="toc-card-num">連載 09</span>
<span class="toc-card-title">進捗率 Z-score 早期警報</span>
<span class="toc-card-desc">下方修正を 1〜3 ヶ月先取りする</span>
</a>
<a href="posts/10_accrual_analysis/" class="toc-card">
<span class="toc-card-num">連載 10</span>
<span class="toc-card-title">アクルーアル分析</span>
<span class="toc-card-desc">利益の質を CF で見抜く</span>
</a>
<a href="posts/11_triangulation/" class="toc-card">
<span class="toc-card-num">連載 11</span>
<span class="toc-card-title">三角検証</span>
<span class="toc-card-desc">コンセンサス × ガイダンス × 実績</span>
</a>
<a href="posts/12_segment_analysis/" class="toc-card">
<span class="toc-card-num">連載 12</span>
<span class="toc-card-title">セグメント発進力スコア</span>
<span class="toc-card-desc">OPM ピークアウトを内訳分解</span>
</a>
<a href="posts/13_car_event_study/" class="toc-card">
<span class="toc-card-num">連載 13</span>
<span class="toc-card-title">CAR イベントスタディ</span>
<span class="toc-card-desc">8,049 イベントで PEAD を検証</span>
</a>
<a href="posts/14_llm_summary/" class="toc-card">
<span class="toc-card-num">連載 14</span>
<span class="toc-card-title">構造化 JSON × LLM 要約</span>
<span class="toc-card-desc">要約トーンと CAR の答え合わせ</span>
</a>
<a href="posts/15_similar_earnings_search/" class="toc-card">
<span class="toc-card-num">連載 15</span>
<span class="toc-card-title">類似決算検索</span>
<span class="toc-card-desc">個別ショックを類似群との乖離で発見</span>
</a>
<a href="posts/16_knn_prediction/" class="toc-card">
<span class="toc-card-num">連載 16</span>
<span class="toc-card-title">K-NN で値動き予測を試して失敗した話</span>
<span class="toc-card-desc">予測より発見のツールとして実用化（完結）</span>
</a>
</div>


