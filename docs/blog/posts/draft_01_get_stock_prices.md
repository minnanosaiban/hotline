<!--
========================================================================
【再構成ドラフト】新・連載01（フェーズ1 データ取得編）
  旧05_streamlit_charts.md の「株価取得 + app1/app2」部分を再編
  最終ファイル名（番号振り直し後）: 01_get_stock_prices.md
  画像の最終置き場: img/01_prices/（暫定で img/05_charts/ を参照）
========================================================================
-->
---
date: 2026-05-18
categories:
  - データ取得
tags:
  - yfinance
  - parquet
  - Streamlit
  - Plotly
  - 株価
---

# まずは株価を取得しよう ― yfinance から parquet 保存、そしてチャートへ

![株価を取得する](img/05_charts/chat2.png){width="1280"}

銘柄分析は、**データを手元に持つこと**から始まります。株価は **yfinance** を使えば誰でも無料で取得できます。ただ、分析のたびに API を叩くのは遅く、特に **5分足は約60日より前が取れません** ― 今日取らなければ二度と手に入らないのです。だから取得した株価は **parquet 形式で保存して貯めていきます**。

本記事では、株価の取り方・parquet での保存・貯めたデータを使った 2 つのチャートアプリまでを通します。フェーズ1「データ取得編」の出発点です。

<!-- more -->



## 概要 ― なぜ parquet に貯めるのか

yfinance（Yahoo! Finance ラッパー）で取れる株価は、足の種類で取得できる期間が大きく違います。

| 足 | 取得できる期間 | 主な用途 |
| --- | --- | --- |
| 日足 | 10 年以上 | 長期トレンド・テクニカル |
| 5分足 | **約 60 日が上限** | 寄付・引け・場中の動き |

- 5分足は「**今貯めないと将来取れない**」ので、定期取得して parquet に追記する価値が高い
- parquet は列指向・型保持・高圧縮。CSV より読み書きが速く、ファイルも小さい
- 株式分割をさかのぼって調整する `auto_adjust=True` を **既定** にします（分割の前後で株価が不連続にならない）

> 💡 貯めたデータは定期的に棚卸しを。上場廃止・超低流動性の銘柄が混ざると、騰落率や統計がゆがみます。



## 株価の取り方 ― yfinance

東証銘柄は `{コード}.T` で指定します（ＥＮＥＯＳ ＝ `5020.T`）。

```python
import yfinance as yf

# 日足（長期）
df_d = yf.download("5020.T", period="2y", interval="1d", auto_adjust=True)

# 5分足（直近のみ・約60日が上限）
df_5 = yf.download("5020.T", period="60d", interval="5m", auto_adjust=True)
```

最新値だけ欲しいときは `fast_info` が高速です。

```python
yf.Ticker("5020.T").fast_info.get("lastPrice")
```



## parquet で保存・追記する

取得した DataFrame は、そのまま parquet に書き出せます。

```python
df_5.to_parquet("data/prices/stocks/5min/5020.parquet")
```

5分足は **日々追記** して貯めます。既存ファイルに連結し、重複行（同じ時刻）を落とすだけ。

```python
import pandas as pd

old = pd.read_parquet(path)
merged = pd.concat([old, new])
merged = merged[~merged.index.duplicated(keep="last")].sort_index()
merged.to_parquet(path)
```

これを週末バッチで回せば、5分足が途切れず積み上がっていきます。保存・追記の全体像は Appendix の GitHub を参照してください。



## チャート1 ― 5分足ローソク + 日足ライン

貯めた 5分足を複数銘柄まとめてローソク足で並べ、右上に日足ラインを小さく添えるアプリです。寄付・引け・**窓開け**を視覚で確認できます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![5分足ローソク + 日足ライン](img/05_charts/chat1.png){width="1200"}

- **縦の境界線**（朝寄り＝濃い、午後寄り＝薄い）でギャップアップ・ギャップダウンを可視化
- 銘柄コードはカンマ・改行で区切って **複数銘柄入力**
- 当日終値は `fast_info.lastPrice` で上書きし、5分足末尾と公式引け値のズレを補正



## チャート2 ― 複数銘柄カードグリッド

各銘柄をカード化して 4 列に並べ、ファンダ指標（PER / PBR / 配当）とテクニカル（RSI）、90 日チャートを **1 画面で俯瞰** するアプリです。連載05「マルチファクター・スコアボード」のチャート版にあたります。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![複数銘柄カードグリッド](img/05_charts/chat2.png){width="1200"}

- 各カード: **銘柄名 / 価格 / 90 日騰落率 / エリア塗りチャート / RSI・PER・PBR・配当**
- 線と塗りの色は **90 日騰落率** で統一（上昇＝緑、下落＝赤）
- PER / PBR / 配当は証券会社が無料で提供する指標 CSV から、RSI は yfinance 日足から自前計算（Wilder RSI(14)）

石油元売 3 社（ＥＮＥＯＳ 5020 / 出光興産 5019 / コスモエネＨＤ 5021）を並べると、同じ市況セクターでも値動きの差が一目で分かります。



## まとめ

- 株価は **yfinance** で無料取得。日足は長期、**5分足は約 60 日が上限**なので貯める価値が高い
- 保存は **parquet**（速い・小さい・型保持）。5分足は重複を落として **日々追記**
- `auto_adjust=True` で株式分割をさかのぼって調整するのが既定
- 貯めたデータだけで、**5分足ローソク**と**複数銘柄カードグリッド**の 2 チャートが作れる

次回は **株価以外のデータ**（決算発表日時・無料の業績指標・XBRL）の取り方に進みます。



## Appendix ― Python コード <i class="fa-brands fa-github"></i>

本記事のチャート 2 アプリと取得・保存スクリプトは、すべて **GitHub に公開**しています。株価は提供元の利用規約により再配布できませんが、**yfinance** さえあれば、ご自身の銘柄リストで同じ画面を再現できます。

> <i class="fa-brands fa-github"></i> **リポジトリ** [`github.com/minnanosaiban/blog/05_charts`](https://github.com/minnanosaiban/blog/tree/main/05_charts)

#### Chart 1 ― 5分足ローソク + 日足ライン（app1.py）

`yfinance` だけで動く、最も依存の少ないアプリ。複数銘柄入力・縦境界線でのギャップ表示・当日値補正まで Altair で実装。

> 🔗 [`github.com/minnanosaiban/blog/05_charts/app1.py`](https://github.com/minnanosaiban/blog/blob/main/05_charts/app1.py)

#### Chart 2 ― 複数銘柄カードグリッド（app2.py）

無料の指標 CSV を読み、4 列カードグリッドで指標＋チャートを並列表示。エリア塗りは Plotly、RSI は Wilder 方式（EWMA）。

> 🔗 [`github.com/minnanosaiban/blog/05_charts/app2.py`](https://github.com/minnanosaiban/blog/blob/main/05_charts/app2.py)

---

*データ出典: yfinance 日足・5分足 Close（`auto_adjust=True`）/ 証券会社が無料で提供する銘柄情報シート CSV*
