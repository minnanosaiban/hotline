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

🔹**PEG ― 成長率に対する割安度**

PER を成長率で割って「成長性に見合った株価か」を測ります。PER 30 倍でも年率 60% 成長なら PEG = 0.5 で超割安、PER 10 倍でも減益予想なら PEG = ∞ で罠。

`PEG（予） = PER（予） ÷ EPS成長率(%)`

| 目安 | 判定 |
| --- | --- |
| ≤ 0.5 | 超割安 |
| ≈ 1.0 | 適正 |
| ≥ 2.0 | 割高 |

🔹**ROE ― 自己資本の利益効率**

`ROE = 当期純利益 ÷ 自己資本 × 100`

| 目安 | 判定 |
| --- | --- |
| ≥ 15% | 超優良（堀の可能性） |
| ≥ 10% | 優良 |
| ≤ 5% | 構造的低収益（罠警戒） |

🔹**GARP ― 低 PEG × 高 ROE**

**割安（低 PEG）かつ高品質（高 ROE）** の銘柄を選ぶ戦略です。PEG 単独だと借入で売上を膨らませた低 ROE 企業も拾ってしまうため、ROE 併用で品質を担保します。

| 戦略 | 失敗パターン |
| --- | --- |
| グロース投資 | 成長鈍化で PER が再評価され株価急落 |
| バリュー投資 | 構造的低収益のバリュートラップ |

GARP はこの中間で **「成長性を確認しつつ妥当な価格で買う」** スタンスです。



## プロットで確認

GARP は、PEG（横軸）× ROE（縦軸）でプロットすることにより、 「割安 × 高 ROE の理想ゾーン」が一目で分かります。

母集団は **TOPIX 500（JPX 規模区分 Core30 + Large70 + Mid400 = 496 銘柄）**。3 層構造でプロットします：

- **背景のグレーの小ドット** ― TOPIX 500 全銘柄（PEG ≤ 3.0 / ROE 範囲内のみ表示）
- **水色の中ドット** ― **TOPIX 大型 100 銘柄**（Core30 + Large70）
- **ラベル付きの大ドット** ― 日経 225 主要 15 社

緑が **GARP 理想ゾーン**（PEG ≤ 1.0 かつ ROE ≥ 10%）です。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>
<small style="color: var(--md-link-color);">2026.05.22作成</small>

![GARP マップ 主要銘柄](img/01_PEG_ROE/01_garp_map.png){width="1200"}

- **理想ゾーンに入っている主要銘柄は三井住友だけ** ― **割安 × 高 ROE の両立は、大型株では稀**であることが一目で分かる
- 大型株（水色）は ROE 帯にばらつきがあるが、PEG ≤ 1.0 の領域には少ない ―「妥当な価格」を厳格に求めると候補が限られる
- 中小型株（背景グレー）には PEG が極端に低い銘柄が散在 ―「割安だが流動性・知名度が低い」候補は中小型に多い

> 💡 GARP マップは個別銘柄の買い時判定ではなく、**多数銘柄の初期スクリーニング**のフィルタとして使うのが現実的。大型株中心なら PEG 上限を 1.3 まで緩める、中小型まで広げるなら PEG ≤ 1.0 を厳守 ― この二択を意識すると条件設定がぶれない。



## 石油元売 3 社比較

ここで、石油元売 3 社の銘柄比較を見てみましょう。市況・精製マージン・在庫評価など共通の事業構造を持ちながら、GARP マップ上の位置はまったく異なります。

- **コスモエネＨＤ**: PEG 0.12 / ROE 12.4% → ★GARP 理想ゾーン
- **出光興産**: PEG 0.46 / ROE 9.4% → 惜しい位置（ROE があと一歩）
- **ＥＮＥＯＳ**: PEG 0.22 / ROE 8.0% → バリュー候補だが低収益

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>
<small style="color: var(--md-link-color);">2026.05.22作成</small>

![石油元売3社 GARP](img/01_PEG_ROE/03_oil_refining.png){width="1200"}

数字だけ見ればコスモが圧倒的に魅力的ですが、**直近 6 ヶ月**の株価動向で印象が逆転します。

**GARP 理想ゾーンのコスモは −5.2% で唯一の下落**、ROE が劣る ＥＮＥＯＳ は +29.7%、出光は +17.6% と上昇しています。一見矛盾するこの結果は、いくつかの解釈ができます。

1. **市況連動セクター特有の罠**: 石油元売の業績は原油価格・精製マージンに大きく左右される。コスモの予想 EPS 成長率 +47.66% はコンセンサスが楽観的すぎる可能性があり、**次回下方修正で PEG が一気に跳ね上がる**
2. **市場は既に予想を織り込み済み**: ＥＮＥＯＳ / 出光は GARP 的にはイマイチでも、市場は **次の業績改善期待** を先取りして買われている。GARP が「過去の予想ベース」の評価であるのに対し、株価は「次の予想変化」を読みに行っている
3. **流動性プレミアム**: ＥＮＥＯＳ は時価総額が大きく機関投資家の資金が入りやすい。コスモは相対的に小型で見落とされやすい

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>
<small style="color: var(--md-link-color);">2026.05.22作成</small>

![石油元売3社 チャート](img/01_PEG_ROE/05_oil_charts.png){width="1200"}

<div class="margin01">
<div class="card-bule">
<p class="small"><b>➡️ PEG・ROE が捉えきれない構造要因</b></p>
<p class="small pad2">石油元売は売上の約 8 割が石油製品。<b>原油価格（在庫影響）・市況・金利環境が会計利益を強く揺さぶります</b>。</p>
<p class="small pad2">ＥＮＥＯＳ は 2025 年 3 月 28 日に 2025/3 期営業利益を 2024 年 11 月公表比 ▲3,950 億円下方修正しました。主因は <b>のれん減損 ▲1,600 億円</b>（2017 年 JX HD・東燃ゼネラル石油の経営統合に伴うのれんを、金利上昇等を受けて減損）と <b>在庫影響 ▲1,500 億円</b>。同時期に <b>JX金属 IPO</b>（57.6% 売却）も進行し、当期利益を +1,300 億円押し上げました。</p>
<p class="small pad2">ＥＮＥＯＳ自身は <b>「実質営業利益（在庫影響除き・非継続含む）4,400 億円水準を維持」「一過性要因も除いた本業利益 4,250 億円（ROE 7.9%）」</b> と説明しています（<a href="https://www.hd.eneos.co.jp/news/release_information/upload/20250328_03_01_0960492.pdf" target="_blank">出典: 2025/3/28 業績予想修正</a>）。</p>
<p class="small pad2">PEG・ROE は <b>会計利益ベース</b> の指標。石油元売はこうした一時／構造要因まで読まないと実態を見誤ります。</p>
</div>
</div>

<div class="margin01">
<div class="card-bule">
<p class="small"><b>➡️ 執筆者試算: 4 つの修正率基準</b></p>
<p class="small pad2">ＥＮＥＯＳ の「修正率」は基準次第で大きく変わります。下記の証券会社が無料で提供している値 ▲3.74%（連載03 で扱うコンセンサス予想経常利益の最新スナップショット）と、2025/3/28 公式 PDF（2024/11 公表比）から計算した 4 基準を並べると：</p>
<table class="table-set" style="font-size: 0.85em; margin: 0.5em 0;">
<thead><tr><th>基準</th><th>修正率</th><th>解釈</th></tr></thead>
<tbody>
<tr><td>コンセンサス予想経常利益</td><td><b>▲3.74%</b></td><td>コンセンサス基準（連載03）</td></tr>
<tr><td>営業利益（公表）</td><td><b>▲94%</b></td><td>のれん減損・在庫影響含む</td></tr>
<tr><td>当期利益（純利益）</td><td><b>▲2.27%</b></td><td>JX金属 IPO 益で相殺</td></tr>
<tr><td>実質営業利益（在庫除き・非継続含む）</td><td><b>+4.76%</b></td><td>ENEOS 本業主張</td></tr>
<tr><td>一過性除き本業利益</td><td><b>+1.19%</b></td><td>ROE 7.9%</td></tr>
</tbody>
</table>
<p class="small pad2"><b>同じ「修正」でも ▲94% から +4.76% まで分散</b>。連載03 のリビジョン値・連載04 のサプライズ・連載05 の需給判断を読むときは、この <b>4 基準のどれを採用するか</b> が投資判断の分かれ目になります。なお、コンセンサス値 ▲3.74% は本稿執筆時点のスナップショット、他 4 行は 2024/11 公表 → 2025/3 修正時点の差分であり、参照期間が完全には一致しない点には注意が必要です。</p>
</div>
</div>

つまり **「GARP マップで光る銘柄」と「直近で上がる銘柄」は必ずしも一致しません**。GARP は中長期スタンスであり、短期株価とは別次元の話です。



## Streamlit アプリ紹介

本記事と同じ GARP マップを **Streamlit + Plotly** で操作可能にしたアプリを公開しています。コードを差し替えるだけで自分の保有銘柄を散布図にプロットしたり、PEG / ROE の閾値を動かして "理想ゾーン" を再定義したりできます。

> 📝 **アプリ公開予定**: GitHub リポジトリ（準備中）。`app_chart.py` と同じく Streamlit ベースで、`requirements.txt` だけ揃えればローカルで動きます。

```python
# Plotly 版 GARP マップ（最小実装の抜粋）
import plotly.express as px

def garp_scatter(df, peg_th=1.0, roe_th=10.0):
    fig = px.scatter(df, x="PEG", y="ROE",
                     hover_data=["コード", "銘柄名", "PER", "成長率%"],
                     color_discrete_sequence=["#7eaee0"])
    # GARP 理想ゾーン
    fig.add_shape(type="rect", x0=0, x1=peg_th, y0=roe_th, y1=60,
                  fillcolor="#27ae60", opacity=0.08, line_width=0)
    fig.add_vline(x=peg_th, line_dash="dash", line_color="#e74c3c")
    fig.add_hline(y=roe_th, line_dash="dash", line_color="#27ae60")
    fig.update_layout(xaxis_title="PEG（予） ← 割安  割高 →",
                      yaxis_title="ROE（%） ← 低収益  高収益 →")
    return fig
```

データ取得は連載中の `compute_peg()` を流用、株価は `yfinance` で最新化。手元の保有銘柄 CSV を読み込めば、自分専用の GARP マップが描けます。



## まとめ

- **GARP = 低 PEG × 高 ROE** で、バリュートラップを避けつつ高品質な割安成長株を選ぶ戦略
- **散布図が GARP の標準的な可視化**。PEG × ROE の 2 軸でファンダの位置と市場全体の分布を同時に見られる
- 主要 15 社のうち **GARP 理想ゾーン入りは三井住友のみ** ― 大型株での両立は稀
- 石油元売 3 社では **コスモ（GARP 理想）が −5%、ＥＮＥＯＳ が +30%** と GARP と株価が逆転 ― PEG / ROE は会計利益ベースで、原油市況・一時要因（のれん減損等）の影響が大きい
- ＥＮＥＯＳ の業績予想修正率は **基準次第で ▲94% から +4.76% まで分散**（編集部試算）。"中身" を見ないと判断を誤る

次回は **マルチファクター・スコアボード** を実装します。GARP の考え方を、Value / Quality / Growth / Sentiment / Momentum / Risk の 7 ファクターに拡張します。



## Appendix ― Python コード

画像生成の全コードは [`01_PEG_ROE_make_images.py`](../scripts/01_PEG_ROE_make_images.py) を参照。執筆者ローカルのモジュール・データに依存するため、そのままでは動きません。

```python
import pandas as pd

def compute_peg(price: float, eps_actual: float, eps_forecast: float) -> dict:
    """株価・前期EPS・予想EPSから PER/成長率/PEG を計算する。

    前期EPS ≤ 0（赤字脱却中）または成長率 ≤ 0（減益予想）の銘柄は
    PEG=NaN として GARP 対象から除外する。
    """
    if eps_forecast is None or eps_forecast <= 0:
        return {"PER": None, "成長率%": None, "PEG": None}
    per = price / eps_forecast
    if eps_actual is None or eps_actual <= 0:
        return {"PER": per, "成長率%": None, "PEG": None}
    growth_pct = (eps_forecast - eps_actual) / abs(eps_actual) * 100
    if growth_pct <= 0:
        return {"PER": per, "成長率%": growth_pct, "PEG": None}
    return {"PER": per, "成長率%": growth_pct, "PEG": per / growth_pct}
```

```python
import matplotlib.pyplot as plt

def plot_garp_map(df, majors, peg_th=1.0, roe_th=10.0):
    fig, ax = plt.subplots(figsize=(13, 8))
    bg = df.dropna(subset=["PEG", "ROE"])
    bg = bg[(bg["PEG"] > 0) & (bg["PEG"] <= 3.0)]
    ax.scatter(bg["PEG"], bg["ROE"],
               s=18, color="#cccccc", alpha=0.35, edgecolors="none")
    ax.axhspan(roe_th, 60, xmin=0, xmax=peg_th/3.0,
               facecolor="#27ae60", alpha=0.07)
    ax.axvline(peg_th, color="#e74c3c", linestyle="--", alpha=0.6)
    ax.axhline(roe_th, color="#27ae60", linestyle="--", alpha=0.6)
    for code, name in majors:
        row = df.loc[df["コード"] == code].iloc[0]
        peg, roe = row["PEG"], row["ROE"]
        color = _quadrant_color(peg, roe, peg_th, roe_th)
        ax.scatter(peg, roe, s=200, color=color,
                   edgecolor="white", linewidth=2.0, zorder=5)
        ax.annotate(name, xy=(peg, roe), xytext=(10, 8),
                    textcoords="offset points",
                    fontsize=10.5, fontweight="bold",
                    bbox=dict(facecolor="white", alpha=0.85,
                              edgecolor="none", boxstyle="round,pad=0.25"))
    ax.set_xlabel("PEG（予）  ← 割安   割高 →")
    ax.set_ylabel("ROE（%）  ← 低収益   高収益 →")
    return fig
```

---

*データ出典: 証券会社が無料で提供する ROE / 前期 EPS / 予想 EPS + yfinance 日足 Close*
