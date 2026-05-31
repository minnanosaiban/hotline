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
| `utils.price_refresh` | yfinance 日足から株価を最新化する共通ユーティリティ（連載04 で使用） |
| `utils.price_metrics` | yfinance 日足から Sentiment/Momentum/Risk 指標を計算する共通ユーティリティ（連載05 で使用） |
| `data/rakunav/*.csv` | 市販の銘柄情報サービスから 1 指標 1 ファイル形式で取得した CSV |
| `data/prices/stocks/daily/*.parquet` | yfinance で取得した個別銘柄の日足 OHLCV（parquet） |
| `data/prices/macro/daily/N225.parquet` | yfinance で取得した日経平均日足（β 計算で使用） |

自前で動かす場合は、これらに相当する関数・データを自分の環境で用意した上で、`import` 文や `OUT_DIR` などを書き換えてください。

## 命名規則

ファイル名は **記事スラッグに統一**しています（`<記事番号>_<スラッグ>_make_images.py` / `thumb_<記事番号>_<スラッグ>.py`）。画像フォルダ `posts/img/<記事番号>_<スラッグ>/` と 1 対 1 で対応します。

## 含まれるスクリプト

| ファイル | 対応記事 | 役割 |
|---|---|---|
| `02_collect_other_data_make_images.py` | [連載02](../posts/02_collect_other_data.md) | XBRL パイプライン全体像・ストレージ統計ほか計5枚 |
| `03_xbrl_to_json_make_images.py` | [連載03](../posts/03_xbrl_to_json.md) | 石油元売3社 7年 売上/自己資本比率・純利益/ROE・CF |
| `04_garp_peg_roe_make_images.py` | [連載04](../posts/04_garp_peg_roe.md) | GARP マップ・ランキングテーブル・株価チャート |
| `05_multifactor_scoreboard_make_images.py` | [連載05](../posts/05_multifactor_scoreboard.md) | スコアボード・ファクター分布・レーダー・3社比較 |
| `06_eps_revision_momentum_make_images.py` | [連載06](../posts/06_eps_revision_momentum.md) | リビジョン各種・モメンタム/バリュエーション散布図 |
| `07_surprise_scoreboard_make_images.py` | [連載07](../posts/07_surprise_scoreboard.md) | サプライズスコア Top20・修正率×経常変化率 4象限ほか |
| `08_progress_zscore_make_images.py` | [連載08](../posts/08_progress_zscore.md) | 進捗率分布・早期警報 Top15・四半期パターン |
| `09_accrual_analysis_make_images.py` | [連載09](../posts/09_accrual_analysis.md) | アクルーアル7年・純利益vs営業CF・散布図 |
| `10_triangulation_make_images.py` | [連載10](../posts/10_triangulation.md) | 三角検証概念図・4象限散布図・総合商社8社接続 |
| `11_segment_analysis_make_images.py` | [連載11](../posts/11_segment_analysis.md) | セグメントカバレッジ・加速/減速・主要4銘柄2年推移 |
| `12_car_event_study_make_images.py` | [連載12](../posts/12_car_event_study.md) | CAR 分布・ウィンドウ別サマリ・短期vs長期散布図 |
| `thumb_01_get_stock_prices.py` 〜 `thumb_15_knn_prediction.py` | 連載01–15 | 各記事のサムネイル `00_thumbnail.png` を生成 |

> `_archive/` には未公開記事用（信用需給）・旧連載の名残（スキーマ）・開発用の一回限りパッチを退避しています。
