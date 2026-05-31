---
date: 2026-05-20
categories:
  - 銘柄分析
tags:
  - GARP
  - PEG
  - ROE
  - ピーター・リンチ
---

# PEG × ROE で「成長と割安の両立銘柄」を発掘する ― GARP の理論と実践

![GARP とは何か](img/01_PEG_ROE/00_thumbnail.png){width="1280"}

「PER が低いから割安」 ― この判断には、**成長率を見ていない**という落とし穴があります。

ピーター・リンチが伝説的ファンドを年率 29% で運用した **GARP（Growth At a Reasonable Price）** 戦略は、PEG と ROE の組み合わせで「成長性と割安度を両立した銘柄」を見つけ出します。

<!-- more -->



## GARP の概要

**GARP（Growth At a Reasonable Price）** は、**割安（低 PEG）かつ高品質（高 ROE）** の銘柄を選ぶ戦略です。グロース投資が陥る「成長鈍化での PER 再評価による株価急落」、バリュー投資が陥る「構造的低収益のバリュートラップ」 ― この 2 つの失敗の **中間** に位置し、**「成長性を確認しつつ妥当な価格で買う」** スタンスです。

🔹 **PEG（予想） = PER（予想） ÷ EPS成長率(%)** ― 成長率に対する割安度

PER 30 倍でも年率 60% 成長なら PEG = 0.5 で超割安、PER 10 倍でも減益予想なら PEG = ∞ で罠。

| 目安 | 判定 |
| --- | --- |
| ≤ 0.5 | 超割安 |
| ≈ 1.0 | 適正 |
| ≥ 2.0 | 割高 |

🔹 **ROE = 当期純利益 ÷ 自己資本 × 100** ― 自己資本の利益効率

| 目安 | 判定 |
| --- | --- |
| ≥ 15% | 超優良(堀の可能性) |
| ≥ 10% | 優良 |
| ≤ 5% | 構造的低収益（罠警戒） |

><small>※ 本記事の「予想」表記は、**証券会社が無料配信するアナリストコンセンサス値**。企業公式の業績予想とは異なります。</small>



## プロットで確認

GARP は、PEG（横軸）× ROE（縦軸）でプロットすると、「割安 × 高 ROE の理想ゾーン」が一目で分かります。**緑が GARP 理想ゾーン**（PEG ≤ 1.0 かつ ROE ≥ 10%）です。

- **理想ゾーンに入っている主要銘柄は三井住友だけ** ― **割安 × 高 ROE の両立は、大型株では稀**であることが一目で分かる
- 大型株（水色）は ROE 帯にばらつきがあるが、PEG ≤ 1.0 の領域には少ない ―「妥当な価格」を厳格に求めると候補が限られる
- 中小型株（背景グレー）には PEG が極端に低い銘柄が散在 ―「割安だが流動性・知名度が低い」候補は中小型に多い

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>
<small style="color: var(--md-link-color);">2026.05.22作成</small>

![GARP マップ 主要銘柄](img/01_PEG_ROE/01_garp_map.png){width="1200"}





## 石油元売 3 社比較

#### GARP では理想ゾーンのコスモ

ここで、石油元売 3 社の銘柄比較を見てみましょう。市況・精製マージン・在庫評価など共通の事業構造を持ちながら、GARP マップ上の位置はまったく異なります。

- **コスモエネＨＤ**: PEG 0.12 / ROE 12.4% → 🌟GARP 理想ゾーン
- **出光興産**: PEG 0.46 / ROE 9.4% → 惜しい位置（ROE があと一歩）
- **ＥＮＥＯＳ**: PEG 0.22 / ROE 8.0% → バリュー候補だが低収益

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>
<small style="color: var(--md-link-color);">2026.05.22作成</small>

![石油元売3社 GARP](img/01_PEG_ROE/03_oil_refining.png){width="1200"}

#### なぜ株価は逆行するのか

数字だけ見ればコスモが圧倒的に魅力的ですが、**直近 6 ヶ月**の株価動向で印象が逆転します。

**GARP 理想ゾーンのコスモは −5.2% で唯一の下落**、ROE が劣る ＥＮＥＯＳ は +29.7%、出光は +17.6% と上昇しています。一見矛盾するこの結果は、いくつかの解釈ができます。

1. **市況連動セクター特有の罠**: 石油元売の業績は原油価格・精製マージンに大きく左右される。コスモの予想 EPS 成長率 +47.66% はコンセンサスが楽観的すぎる可能性があり、**次回下方修正で PEG が一気に跳ね上がる懸念**
2. **次の業績改善期待を先取り**: ＥＮＥＯＳ / 出光は GARP 的にはイマイチでも、市場が先回りして買いに動いている可能性。GARP が「過去の予想ベース」を見るのに対し、株価は「次の予想変化」を読みに行く
3. **流動性プレミアム**: ＥＮＥＯＳ は時価総額が大きく機関投資家の資金が入りやすい一方、コスモは相対的に小型で見落とされやすい

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>
<small style="color: var(--md-link-color);">2026.05.22作成</small>

![石油元売3社 チャート](img/01_PEG_ROE/05_oil_charts.png){width="1200"}

 > 💡 「GARP マップで光る銘柄」と「直近で上がる銘柄」は必ずしも一致せず。GARP は中長期スタンスであり、短期株価とは別次元の話。


## まとめ

- **GARP = 低 PEG × 高 ROE** で、バリュートラップを避けつつ高品質な割安成長株を選ぶ戦略
- **散布図が GARP の標準的な可視化**。PEG × ROE の 2 軸でファンダの位置と市場全体の分布を同時に見られる
- 主要 15 社のうち **GARP 理想ゾーン入りは三井住友のみ** ― 大型株での両立は稀
- 石油元売 3 社では **コスモ（GARP 理想）が −5%、ＥＮＥＯＳ が +30%** と GARP と株価が逆転 ― PEG / ROE は会計利益ベースで、原油市況・一時要因（のれん減損等）の影響が大きい

次回は **マルチファクター・スコアボード** を実装します。GARP の考え方を、Value / Quality / Growth / Sentiment / Momentum / Risk の 7 ファクターに拡張します。


## Appendix ― Python コード <i class="fa-brands fa-github"></i>

本記事のアプリ・チャート画像生成スクリプトは、すべて **GitHub に公開**しています。データは提供元の利用規約により再配布できませんが、**yfinance** や **無料コンセンサスデータ** を組み合わせれば、ご自身の銘柄リストで同じ構図のアプリや PNG が生成できます。

> <i class="fa-brands fa-github"></i> **リポジトリ** [`github.com/minnanosaiban/blog/01_PEG_ROE`](https://github.com/minnanosaiban/blog/tree/main/01_PEG_ROE)

#### Streamlit アプリ ― 「自分専用の銘柄分析ツール」を体験

「自社銘柄が GARP 上どこにいるか、毎週月曜にブラウザで確認したい」 ― Excel と Web アプリ開発の **ちょうど中間** に位置するのが **Streamlit + Plotly**。ホバー・ズーム・パンが揃ったインタラクティブなダッシュボードを体験できます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![GARP スクリーナー アプリ画面](https://github.com/minnanosaiban/blog/blob/main/04_PEG_ROE/app.png?raw=true){width="1200"}

> 🔗 [`github.com/minnanosaiban/blog/01_PEG_ROE`](https://github.com/minnanosaiban/blog/tree/main/01_PEG_ROE) 



#### チャート画像 ― ダブルクリック一発で PNG を作成

本記事の図はすべて **Matplotlib** で生成しています。**デスクトップショートカットからダブルクリック一発で最新データの高解像度 PNG / PDF を再生成**。Windows タスクスケジューラ / cron に登録すれば、毎週・毎月の定点観測を手を動かさず回せます。

> 🔗 [`github.com/minnanosaiban/blog/01_PEG_ROE/01_PEG_ROE_make_images.py`](https://github.com/minnanosaiban/blog/blob/main/01_PEG_ROE/01_PEG_ROE_make_images.py)


---

*データ出典: 証券会社が無料で提供する ROE / 前期 EPS / 予想 EPS + yfinance 日足 Close*
