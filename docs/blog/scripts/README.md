# 参考コード（動作保証なし）

このディレクトリのスクリプトは **記事に掲載した分析の参考コード** です。執筆者のローカル環境（独立した分析リポジトリ）の各種モジュール・データに依存しているため、**そのまま実行しても動作しません**。

## 用途

- 記事本文中のコード抜粋の **全体像** を確認したい読者向け
- 自前の環境で類似の分析を組む際の **設計の叩き台** として参照

## 動かすために必要なもの（参考）

各スクリプトは概ね次に依存しています。

| 依存 | 説明 |
|---|---|
| `config.paths` | データディレクトリ・指標 CSV のパス管理モジュール |
| `utils.price_refresh` | yfinance 日足から株価を最新化する共通ユーティリティ（01 で使用） |
| `utils.price_metrics` | yfinance 日足から Sentiment/Momentum/Risk 指標を計算する共通ユーティリティ（02 で使用） |
| `data/rakunav/*.csv` | 市販の銘柄情報サービスから 1 指標 1 ファイル形式で取得した CSV |
| `data/prices/stocks/daily/*.parquet` | yfinance で取得した個別銘柄の日足 OHLCV（parquet） |
| `data/prices/macro/daily/N225.parquet` | yfinance で取得した日経平均日足（β 計算で使用） |

自前で動かす場合は、これらに相当する関数・データを自分の環境で用意した上で、`import` 文や `OUT_DIR` などを書き換えてください。

## 含まれるスクリプト

| ファイル | 対応記事 | 役割 |
|---|---|---|
| `01_PEG_ROE_make_images.py` | [連載04 PEG × ROE 銘柄分析](../posts/04_garp_peg_roe.md) | GARP マップ・ランキングテーブル・株価チャート計5枚の画像生成 |
| `02_multifactor_make_images.py` | [連載05 マルチファクタースコアボード](../posts/05_multifactor_scoreboard.md) | スコアボード・ファクター分布・Value×Quality 散布図・主要銘柄レーダー・石油元売3社比較計5枚の画像生成 |
| `03_revision_momentum_make_images.py` | [連載06 EPSリビジョン・モメンタム](../posts/06_eps_revision_momentum.md) | 市場別リビジョン・石油元売3社リビジョン・強度ランキング・リビジョン×モメンタム/バリュエーション散布図 計5枚の画像生成 |
| `04_surprise_score_make_images.py` | [連載07 連続サプライズ・スコアボード](../posts/07_surprise_scoreboard.md) | サプライズスコア Top20・石油元売3社サプライズ・修正率×経常変化率 4象限散布図・単一vs合成シグナル重なり・3シグナル分布 計5枚の画像生成 |
| `05_credit_dashboard_make_images.py` | 信用需給ダッシュボード（記事は未公開） | 信用倍率分布・石油元売3社信用需給・前週比急増/急減 Top10・信用倍率×出来高散布図・業績×需給 4象限マトリクス 計5枚の画像生成 |
| `06_xbrl_intro_make_images.py` | [連載03 XBRL を JSON に変換して分析](../posts/03_xbrl_to_json.md) | 石油元売3社 7年売上/営業利益・純利益/ROE・CF 3 種・データ深度比較・ENEOS ピークアウト 計5枚の画像生成 |
| `07_pipeline_make_images.py` | [連載03 XBRL を JSON に変換して分析](../posts/03_xbrl_to_json.md) | パイプライン全体像・ストレージ統計・決算短信分布・マッピング辞書構成・ENEOS 7 期取得カタログ 計5枚の画像生成 |
| `08_schema_make_images.py` | [連載03 XBRL を JSON に変換して分析](../posts/03_xbrl_to_json.md) | セクション別ルール分布・会計基準×カテゴリ ヒートマップ・net_sales 1対N 構造・実データカバレッジ・5 原則 計5枚の画像生成 |
| `09_zscore_make_images.py` | [連載08 進捗率 Z-score 早期警報](../posts/08_progress_zscore.md) | 進捗率分布・早期警報 Top15・業績超過 Top15・売上×営利散布図・四半期パターン 計5枚の画像生成 |
| `10_accrual_make_images.py` | [連載09 アクルーアル分析](../posts/09_accrual_analysis.md) | 石油元売3社アクルーアル7年・純利益vs営業CF対比・13社ランキング・純利益×CF散布図・ENEOS 2022 利益の質 計5枚の画像生成 |
| `11_triangulation_make_images.py` | [連載10 三角検証](../posts/10_triangulation.md) | 三角検証概念図・4象限散布図 211 銘柄・上方修正期待 Top10・達成困難 Top10・総合商社8社の連載09×10 接続 計5枚の画像生成 |
| `12_segments_make_images.py` | [連載11 セグメント発進力](../posts/11_segment_analysis.md) | セグメントカバレッジ・ソニーG6セグメント構成・加速/減速 Top10・高利益率 Top15・主要4銘柄2年推移 計5枚の画像生成 |
