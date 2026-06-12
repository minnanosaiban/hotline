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

# まず、「株価」を取得する ― yfinance で取得、parquet 保存からチャートまで

![株価を取得する](img/01_get_stock_prices/00_thumbnail.png){width="1280"}

株価は yfinance から都度ロードして表示することもできますが、取得制限やパフォーマンスを考えると、**取得した株価データは parquet で保存しておくのがベストプラクティス**です（とくに 5 分足は約 60 日で消えるため、貯める価値が高い）。

本記事では、

- yfinanceから株価を取得する
- parquet 形式で保存する
- 5分足チャートを描画してみる

までを通します。

ここで作成する 5分足チャートの Python コードは GitHub に公開しています。それでは、フェーズ1「データ取得編」の出発点です。

<p class="fig-meta">データ出典: yfinance 日足・5分足 Close（`auto_adjust=True`）</p>

<div class="ref-quiet">
<a class="ref-card ref-card--quiet" href="https://github.com/ranaroussi/yfinance" target="_blank" rel="noopener">
<span class="ref-card-body">
<span class="ref-card-title">yfinance とは</span>
<span class="ref-card-desc">Yahoo!ファイナンスの株価データを取得する Python ライブラリ ― GitHub</span>
</span>
</a>
</div>




## なぜ、ローカルに株価を貯めるのか

yfinance で取れる株価は、足の種類で取得できる期間が大きく違います。

| 足       | 取得できる期間   | 主な用途         |
| ------- | --------- | ------------ |
| **日足**  | 10 年以上    | 長期トレンド・テクニカル |
| **5分足** | 約 60 日が上限 | 寄付・引け・場中の動き  |

- 5分足は「**今貯めないと将来取れない**」ので、定期取得して parquet に追記する価値が高い
- parquet は列指向・型保持・高圧縮。CSV より読み書きが速く、ファイルも小さい

> ⚠️ 貯めたデータは定期的に棚卸しを。上場廃止・超低流動性の銘柄が混ざると、騰落率や統計がゆがみます。また、株式分割・配当の調整として、`auto_adjust=True` を既定にします。


## yfinanceで株価を取得する

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


## 株価は parquet で保存する

取得した DataFrame は、そのまま parquet に書き出せます。

```python
df_5.to_parquet("data/prices/stocks/5min/5020.parquet")
```

5分足は **週次で追記** して貯めます（5分足は約 60 日分残るので、週 1 回の取得で十分です）。既存ファイルに連結し、重複行（同じ時刻）を落とすだけ。

```python
import pandas as pd

path = "data/prices/stocks/5min/5020.parquet"
new  = df_5                       # 新しく取得した5分足

old = pd.read_parquet(path)
merged = pd.concat([old, new])
merged = merged[~merged.index.duplicated(keep="last")].sort_index()
merged.to_parquet(path)
```

これを週末バッチで回せば、5分足が途切れず積み上がっていきます。保存・追記の全体像は Appendix の GitHub を参照してください。



## <i class="fa-brands fa-github"></i> Python コード

本記事のチャート画像・アプリ・データ取得・成形スクリプトは、すべて **GitHub に公開**しています。データは提供元の利用規約により再配布できませんが、データを各自取得すれば、本連載と同じものが再現できます（動かし方はリポジトリの README 参照）。


<div class="repo-link-wrap">
<a class="repo-link" href="https://github.com/minnanosaiban/blog/tree/main/01_chart_5min" target="_blank" rel="noopener">
<span class="repo-link-path">github.com/minnanosaiban/blog/01_chart_5min</span>
<i class="repo-link-arrow fa-solid fa-arrow-up-right-from-square"></i>
</a>
</div>

## 📌 自作アプリ紹介


<div class="keypoint" markdown="span">**― 寄付・引け・窓開けを一目で確認できる5分足チャート ―**</div>


<div class="repo-link-wrap">
<a class="repo-link" href="https://github.com/minnanosaiban/blog/tree/main/01_chart_5min" target="_blank" rel="noopener">
<span class="repo-link-path">github.com/minnanosaiban/blog/01_chart_5min</span>
<i class="repo-link-arrow fa-solid fa-arrow-up-right-from-square"></i>
</a>
</div>

Streamlit で作成したアプリです。チャート描画は Plotly、株価は yfinance で取得して parquet に保存しています。

- **株価チャートと騰落率テーブルの日付を揃えて**表示し、値動きと前日比を対応づけて読める
- **縦の境界線**でギャップアップ・ギャップダウンを視覚的に把握しやすく
- 銘柄コードを **カンマ・スペース・改行**で区切って **複数銘柄を入力**できる

<p class="fig-meta"><i class="fa-solid fa-expand"></i> クリックで拡大</p>

![5分足ローソク + 騰落率テーブル](https://github.com/minnanosaiban/blog/raw/main/01_chart_5min/app.png){width="1200"}

なお、**株価をあらかじめ貯めなくても、チャートは表示できます**。yfinance から直接取得して描く簡易版（`app_simple.py`）もおまけ で同梱しています。



---
