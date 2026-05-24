---
date: 2026-05-20
categories:
  - 銘柄分析
tags:
  - マルチファクター
  - クオンツ
  - GARP
  - バリュー
  - Quality
---

# マルチファクターで銘柄を採点する ― スコアボードで「全方位優等生」を発見する

![マルチファクタースコアボード](img/02_multifactor/00_thumbnail.png){width="1280"}

「PER が低いから買い」「ROE が高いから買い」 ― 単一指標スクリーニングには、落とし穴があります。

連載01 の [PEG × ROE 銘柄分析](01_garp_peg_roe.md) の 2 軸を、本記事では **Value / Quality / Growth / Consensus / Sentiment / Momentum / Risk** の 7 ファクターに拡張。

TOPIX 500 銘柄（495 銘柄）でパーセンタイル化してスコアを算出し、**TOPIX 大型 100 銘柄に絞ったスコア序列** を Top 20 として可視化します。「GARP 圏外なのに +35% 上昇」「GARP 理想なのに −2% 下落」という逆転現象を、7 ファクターで定量的に再検証します。

<!-- more -->



## マルチファクターモデルの概要


学術研究の Fama-French 3 / 5 ファクター、Carhart 4 ファクター、Q-factor モデルなど、機関投資家が使う代表的なクオンツモデルは「複数ファクターを並列スコア化して合成する」という共通構造を持ちます。

本ダッシュボードは 7 ファクターを採用します。

| ファクター | 観点 | 主要指標 |
|---|---|---|
| **Value** | 割安度 | PER / PBR / EV/EBITDA / 配当利回り |
| **Quality** | 収益性・財務健全性 | ROE / ROA / 営業利益率 / 自己資本比率 |
| **Growth** | 過去の成長実績 | 売上高変化率 / 経常利益変化率 |
| **Consensus** | 将来予想の改善度 | 業績予想修正率 / 経常利益変化率(予) / 3年売上成長率(予) |
| **Sentiment** | 需給の熱量 | 出来高増加率 / 売買代金増加率 |
| **Momentum** | 株価のトレンド | 値上り率 / 52週安値からの上昇率 / MA乖離率 |
| **Risk** | リスク要素（低いほど良い） | 60日ボラティリティ / β（対日経平均） |

7 ファクターをスコア化したうえで、**すべてのファクターが平均以上** の銘柄は単一指標スクリーニングの落とし穴をすべて回避できる「オールラウンダー」です。長期保有候補としてポートフォリオのコアに据える価値があります。逆に **ある一つだけ突出して低い** 銘柄は、その低スコア要因を理由に敬遠する判断材料になります。これがマルチファクター採点の本質的な利点です。



## 分析で分かったこと

### 総合スコア Top 20 ― TOPIX 大型 100 銘柄（Core30 + Large70）内の序列

トップは **ＳＯＭＰＯＨＤ（総合 70.0）** で、Growth 91 / Consensus 80 / Sentiment 99 と需給・業績の両輪が揃った形。続いてインフラ系 **ＪＰＸ（67.0）**、ディフェンシブ代表の **ＪＴ（66.0）** が 3 位に入りました。医療機器の **テルモ（63.4）** と製薬の **大塚ＨＤ（62.8）** が続き、**ソフトバンクＧ（62.8）** が Momentum 99 の需給の強さで 6 位に食い込んでいます。

- **ディフェンシブ（高配当・低ボラ）が上位**: ＪＴ・ＮＴＴは Risk 84/98 と「リスクの低さ」が総合スコアを押し上げる。守りの強い銘柄は単体ファクターで突出しなくても全方位平均で勝つ
- **需給の強さで突出**: ソフトバンクＧは Momentum 99 / Sentiment 92 / Growth 83 だが Risk **0** と、攻めに偏った最高ボラ構成
- **業種 1 位でも下位は普通にある**: ＥＮＥＯＳ（石油元売 1 位）は TOPIX 大型 100 内でも Top 20 圏外（総合 45.3）。業種大手とマルチファクター評価は別物
- **連載 narrative の石油元売 3 社**: コスモエネＨＤは TOPIX Mid400 のため大型 100 外。Value 92 のファンダ強さが Sentiment 22 の需給弱さで相殺された姿（後述の 3 社比較で深掘り）

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![スコアボード Top20](img/02_multifactor/01_scoreboard_top20.png){width="1200"}

### 石油元売 3 社のセクター内比較 ― 連載01 の再検証

ここで本記事の核心、石油元売 3 社をマルチファクター視点で再評価します。連載01 では同じ 3 社を PEG × ROE 平面で比較し、**「GARP 理想ゾーンのコスモが −2% で唯一の下落、ROE が劣る ＥＮＥＯＳ が +35.8% で大きく上昇」** という GARP マップ位置と株価動向の逆転現象を観察しました。7 ファクターで見直すと、この逆転がより精緻に説明できます。

- **コスモエネＨＤ**: ファンダ面では圧倒的（Value 92 / Consensus 68）だが、**Sentiment 22 / Momentum 35 で需給は冷えたまま**。投資家がコンセンサスの強気予想を信用していないか、流動性プレミアム不足で資金が回らない状態
- **ＥＮＥＯＳ**: Value 70 / Quality 32 と地味だが、**Growth 54 / Sentiment 57 / Momentum 51 で「動いている」**。経常利益変化率 +408% という実績がモメンタムを支える
- **出光興産**: 中庸型。突出した強みも弱みもなく、3 社の中間に位置する

連載01 で「コスモは GARP 理想ゾーンなのに下落」した謎は、**ファンダ（Value 92 + Consensus 68）と需給（Sentiment 22 + Momentum 35）のスコアが乖離している** ことで定量的に説明できます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![石油元売3社 ファクター比較](img/02_multifactor/05_oil_refining_factors.png){width="1200"}

| 銘柄 | 総合 | Value | Quality | Growth | Consensus | Sentiment | Momentum | Risk |
|---|---|---|---|---|---|---|---|---|
| **コスモエネＨＤ** | **47.9** | **92** | 41 | 19 | **68** | **22** | 35 | 59 |
| ＥＮＥＯＳ | 45.3 | 70 | 32 | 54 | 22 | 57 | 51 | 32 |
| 出光興産 | 41.4 | 76 | 30 | 22 | 25 | 45 | 39 | 54 |


<div class="margin01">
<div class="card-bule">
<p class="small"><b>📝 ＥＮＥＯＳ Growth 54 と Consensus 22 の断層</b></p>
<p class="small pad2">ＥＮＥＯＳ の Growth 54 を支える経常利益変化率 +408% は、原油急騰局面を含む <b>過去実績</b>。一方 Consensus 22 は、構造要因（のれん減損・在庫影響）による下方修正という <b>先行き</b> を映しています ― マルチファクター採点は時系列の異なるシグナルを 1 枚で扱うため、Growth と Consensus が逆方向を指す現象が起きます。</p>
<p class="small pad2">下方修正の中身、ENEOS 公式の「実質営業利益 4,400 億円維持」スタンス、<b>4 つの修正率基準（▲94% から +4.76% まで分散）</b> の試算は <a href="01_garp_peg_roe.md">連載01</a> 参照。</p>
</div>
</div>

```
連載01（2 ファクター）: コスモは Value × Growth 両立 → 買い候補に見える
連載02（7 ファクター）: コスモは Value ◎ だが Sentiment✗ Momentum ✗
                       → 「ファンダ良いが市場が振り向いていない」
                       → 待つか、需給転換のサインを別に見る必要あり
```

これがマルチファクター採点の本質的な価値です。**ファンダだけ、需給だけでは見えない「乖離」が一目で分かる**。次回連載03 で扱う EPS リビジョン・モメンタムは、まさにこの「ファンダと需給の乖離が縮まる瞬間」を時系列で捉えます。

### 主要 6 社の 7 ファクターレーダー

レーダーチャートの **歪み** を見ると、銘柄の個性が一目で分かります。キーエンスは Quality 一点突出の「典型的な高品質・割高銘柄」、ソフトバンクＧ は Risk 軸だけ極端に凹んだ「高リターン高リスク型」というように、性格の違いを視覚化できます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![主要6社レーダー](img/02_multifactor/04_majors_radar.png){width="1200"}

| 銘柄 | 総合 | 形状の特徴 |
|---|---|---|
| **ソフトバンクＧ** | 62.8 | Momentum 99 / Sentiment 92 / Growth 83 と需給・業績が最強。Risk **0** ＝ ほぼ最高ボラティリティが唯一の弱点 |
| **三菱ＵＦＪ** | 56.0 | Momentum 73 / Sentiment 81 が強く、最近の銀行株上昇を反映。一方 Quality 32（銀行は ROE が構造的に低い） |
| **キーエンス** | 55.7 | Quality **92**（高 ROE で別格）だが Value 6（PER が市場下位 6%） |
| **ＫＤＤＩ** | 52.3 | バランス型。Risk 69（低ボラ）で長期保有向き |
| **トヨタ** | 41.7 | 全ファクターが 34〜70 で突出した強みなし。Sentiment 12 / Momentum 42 から直近モメンタム弱め |
| **ソニーＧ** | 37.8 | Sentiment 23 / Momentum 42 と需給・モメンタムが低迷。Quality 55 / Growth 18 と内需型の地合い |



### Value × Quality 散布図 ― クオリティ・バリュー銘柄の発見

ファクター間散布図で **Value × Quality** をプロットすると、ウォーレン・バフェットが好むとされる「クオリティ・バリュー」銘柄を視覚的に発掘できます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![Value × Quality 散布図](img/02_multifactor/03_value_quality_scatter.png){width="1200"}

右上の緑ゾーン（Value ≥ 70 かつ Quality ≥ 70）は **高品質 × 割安** で、「素晴らしい企業を妥当な価格で買う」というバフェット流の長期投資ゾーンに対応します。今回の TOPIX 500（495 銘柄）のうち、このゾーンに入ったのは **7 銘柄**。総合スコア順の上位は以下のとおりです。

| 銘柄 | Value | Quality | 総合 |
|---|---|---|---|
| ニフコ（7988） | 74 | 78 | 55.0 |
| 日本新薬（4516） | 82 | 74 | 53.6 |
| ＳＡＮＫＹＯ（6417） | 88 | 93 | 50.4 |
| 全国保証（7164） | 71 | 73 | 49.8 |
| アマノ（6436） | 74 | 80 | 48.4 |
| 三和ＨＤ（5929） | 71 | 79 | 43.9 |
| ＴＯＹＯＴＩＲＥ（5105） | 89 | 80 | 43.1 |

主要 6 社のうち散布図右上ゾーンに入った銘柄はゼロでした。**大型株は「知名度プレミアム」で常に Value スコアが下がる傾向** があり、TOPIX 500 内でも中型株（Mid400）が中心となる結果です。

### バリュー・トラップの早期検出

逆に右下（Value 高 × Quality 低、Quality ≤ 30）は **構造的低収益のため永遠に割安評価される** バリュー・トラップ警戒ゾーンです。TOPIX 500 中 **20 銘柄** が該当し、PER の安さに目を奪われて買うと痛い目を見るリスクがあります。

| 銘柄 | Value | Quality | 配当利回り | ROE |
|---|---|---|---|---|
| アルフレッサＨＤ | 87 | 20 | 3.1% | 8.4% |
| かんぽ | 87 | 19 | 2.7% | 4.6% |
| 東北電 | 87 | 24 | 4.0% | 8.1% |
| マツダ | 84 | 17 | 5.2% | 1.9% |
| カネカ | 84 | 28 | 3.0% | 6.4% |
| ＳＢＩ新生 | 83 | 29 | — | 10.4% |
| ＳＵＢＡＲＵ | 83 | 28 | 4.7% | 3.3% |

配当利回りの高さに飛びつくと、ROE 一桁台の構造的低収益体質に資金が固定される可能性があります。**「Value 単独」ではなく必ず Quality を併用する** ― これがマルチファクター採点の効果です。

### 過熱銘柄の検出

`Momentum ≥ 90` かつ `Sentiment ≥ 90` かつ `Risk ≤ 20`（高ボラ）の三条件を満たした銘柄は **6 銘柄** ありました。

| 銘柄 | 市場 | Momentum | Sentiment | Risk | 総合 |
|---|---|---|---|---|---|
| ＦＵＪＩ（6134） | 東P | 96 | 92 | 11 | 68.2 |
| 富士電機（6504） | 東P | 96 | 91 | 7 | 60.5 |
| 太陽誘電（6976） | 東P | 99 | 99 | 3 | 53.8 |
| 村田製（6981） | 東P | 98 | 97 | 6 | 52.3 |
| ソフトバンクＧ（9984） | 東P | 99 | 92 | 0 | 62.8 |
| ホトニクス（6965） | 東P | 94 | 95 | 7 | 44.0 |

これらは **「天井圏で過熱した」パターン** に近く、新規エントリーよりも保有銘柄の **利益確定検討** に使うのが定石です。TOPIX 500 では東証プライムの電子部品・電機系大型株が集中しています。Risk スコアが極端に低い（=ボラティリティが市場上位 5%）ことが共通しています。

### ファクタースコア分布から市場の温度感を読む

各ファクターのヒストグラムを並べると、**市場全体の地合い** が読み取れます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![ファクター分布](img/02_multifactor/02_factor_distribution.png){width="1200"}

各ファクターの分布形状を比較すると、**Consensus は 30〜70 の中央付近に集中しており、0〜20 の低スコア帯がほとんど空**です。これはアナリストの予想修正が大きく動く銘柄は限られており、多くは中立圏にとどまっていることを反映しています。**Sentiment** は対照的にほぼ一様分布で、0 から 90 まで各スコア帯に満遍なく銘柄が分散しています。

**Momentum** がやや左寄り（中央 47）なのは「直近の市場が中央値より少し弱い」状態を、**Risk** が右寄り（中央 51）なのは「高ボラ銘柄が相対的に少ない」ことを示しています。

### 「全方位優等生」を探したが…

冒頭で「全方位優等生」を目標に掲げましたが、**今回の集計で 7 ファクターすべてが 60 以上の銘柄は 0 銘柄** でした。

これは閾値が厳しすぎることを意味します。実用的には：

- **5 ファクター以上 ≥ 60**: 数十銘柄が該当
- **Value & Quality & Risk ≥ 60**: 数十銘柄 ― 「割安 × 高品質 × 低リスク」の保守的優良株
- **Growth & Consensus & Momentum ≥ 70**: 「成長加速」の積極派候補

このように **どの組み合わせで絞り込むかが投資スタイルを表現する** ことになります。マルチファクターの真価は、合成スコアの絶対値ではなく **「どの組み合わせが今市場で機能しているか」を観察できる** 点にあります。



## スコアの計算方法

ここまでスコアの順位で銘柄を比較してきましたが、そのスコアは具体的にどう算出しているのか。本記事では 7 ファクターを統合スコアに合成するため、すべての指標を **パーセンタイルランクで 0〜100 に正規化** してから単純平均します。

```
[単一指標のスコア化]
  ・高いほど良い指標（ROE 等）: score = rank_pct(value) × 100
  ・低いほど良い指標（PER 等）: score = 100 − rank_pct(value) × 100
  ・データ欠損は score = 50（中立）で補完
  ・バリュエーション系は正の値のみ採点対象（赤字銘柄の PER は除外）

[ファクタースコア = 構成指標のスコアの単純平均]
  例: Quality = mean(score(ROE), score(ROA), score(営業利益率), score(自己資本比率))

[総合スコア = 7 ファクタースコアの単純平均]
```

「PER 10 倍は割安か？」という問いは市場環境に依存しますが、パーセンタイル化すれば **「今のユニバース内で何位か」** で評価できるため、市場環境に左右されない相対評価になります。総合スコアの解釈は次のとおりです。

| 総合スコア | 解釈 |
|---|---|
| 70 以上 | 7 ファクター平均で上位 30% — 注目候補 |
| 60〜70 | 上位 30〜50% — バランスの良い銘柄 |
| 50〜60 | 中庸 |
| 40 以下 | 改善の兆しがあるか、別観点で再評価が必要 |

なお Value 指標のうち **PER / PBR / 配当利回りは yfinance の最新終値で自前計算** しています（連載01 と共通。EV/EBITDA は構成要素が多く実用的でないため証券会社が提供しているデータの値をそのまま使用）。

```
PER（実）   = Close_yf ÷ EPS実績
PBR（予）   = Close_yf ÷ BPS予
配当利回り  = 配当金 ÷ Close_yf × 100
```

正規化を集団内（フィルター後のユニバース）で行うため、**スコア 100 は「相対順位トップ」を意味し、絶対値の魅力を保証するものではない** 点に注意が必要です。


## まとめ

- 単一指標スクリーニングの落とし穴（バリュー・トラップ / 成長停止 / 過熱）を **7 ファクター統合採点** で自動回避できる
- パーセンタイル化により **異なるスケールの指標を統一比較** でき、市場環境に左右されない相対評価になる
- スコア計算は **TOPIX 500（495 銘柄）でパーセンタイル化**、表示する Top 20 は **TOPIX 大型 100 銘柄（Core30 + Large70）に絞る** ことで「大型株の中での序列」として読める形に
- TOPIX 大型 100 内 Top 20 では **ディフェンシブ（ＪＴ・セコム）と需給・業績強銘柄（ＳＯＭＰＯＨＤ・ソフトバンクＧ）** が混在。業種最大手（ＥＮＥＯＳ など）でも総合スコアは Top 20 外になることがある
- ファクター間散布図で **クオリティ・バリュー 7 銘柄 / バリュー罠 20 銘柄 / 過熱 6 銘柄** を一発抽出できる
- 石油元売 3 社の例では、コスモ（Value 92 / Consensus 68）と Sentiment 22 / Momentum 35 の **乖離** が、連載01 で観察した「ファンダ良いのに株価下落」を定量説明
- ＥＮＥＯＳ の Growth 54 / Consensus 22 の断層は、**過去実績（原油急騰局面含む）と先行き（構造要因による下方修正）の方向感のズレ** を映す。詳細と 4 基準試算は連載01 参照
- **「全 7 ファクター ≥ 60」は 0 銘柄** — 完璧な銘柄は存在せず、自分が重視するファクターの組み合わせを決めることが投資スタイルの表現になる

次回は **EPS リビジョン・モメンタム** を実装します。本ダッシュボードの Consensus / Momentum ファクターを時系列で深掘りし、アナリスト予想の修正動向と株価のズレから「出遅れ買い候補」を発掘します。

## Python コードの紹介

本分析の中核となるコードを抜粋して紹介します。画像生成の全コードは [`02_multifactor_make_images.py`](../scripts/02_multifactor_make_images.py) を参照してください（執筆者ローカルのモジュール・データに依存しているため、そのままでは動きません。動作要件は [scripts/README](../scripts/README.md) を参照）。

### パーセンタイルスコア化

```python
import pandas as pd

def percentile_score(series: pd.Series, higher_better: bool) -> pd.Series:
    """有効値のみでパーセンタイルランク（0〜100）を計算。NaN は 50 で補完。"""
    ranked = series.rank(pct=True, na_option="keep") * 100
    if not higher_better:
        ranked = 100 - ranked
    return ranked.fillna(50)


def add_factor_scores(df: pd.DataFrame, factor_defs: dict) -> pd.DataFrame:
    """7 ファクターのスコアと総合スコアを DataFrame に追加。"""
    out = df.copy()
    for factor, metrics in factor_defs.items():
        cols = []
        for col, higher in metrics:
            if col not in out.columns:
                continue
            # バリュエーション系は正の値のみランキング対象（赤字銘柄除外）
            series = out[col].where(out[col] > 0) if not higher else out[col]
            sc = f"_s_{col}"
            out[sc] = percentile_score(series, higher)
            cols.append(sc)
        out[f"score_{factor}"] = out[cols].mean(axis=1) if cols else 50.0
    factor_cols = [f"score_{f}" for f in factor_defs]
    out["score_総合"] = out[factor_cols].mean(axis=1)
    return out
```

### 価格指標の自前計算（Sentiment / Momentum / Risk）

yfinance 日足 parquet から 7 つの市場指標を計算します。

```python
import numpy as np
import pandas as pd

def compute_price_metrics(close: pd.Series, volume: pd.Series,
                          n225_logret: pd.Series) -> dict:
    out = {}
    last = float(close.iloc[-1])

    # Momentum
    out["値上り率"] = (last / float(close.iloc[-2]) - 1) * 100
    out["過去52週安値からの上昇率"] = (last / float(close.iloc[-252:].min()) - 1) * 100
    out["株価移動平均線からの乖離率①"] = (last / float(close.iloc[-25:].mean()) - 1) * 100

    # Sentiment（当日 vs 直近 20 営業日平均）
    out["出来高増加率"]   = float(volume.iloc[-1]) / float(volume.iloc[-21:-1].mean())
    turnover = close * volume
    out["売買代金増加率"] = float(turnover.iloc[-1]) / float(turnover.iloc[-21:-1].mean())

    # Risk
    log_ret = np.log(close / close.shift(1)).dropna()
    out["過去60日ボラティリティ"] = float(log_ret.iloc[-60:].std() * np.sqrt(252) * 100)

    joined = pd.concat([log_ret.iloc[-252:], n225_logret], axis=1, join="inner").dropna()
    var_m = float(joined.iloc[:, 1].var())
    out["ベータ(対日経平均)"] = float(joined.iloc[:, 0].cov(joined.iloc[:, 1]) / var_m)
    return out
```

### レーダーチャート描画

```python
import numpy as np
import matplotlib.pyplot as plt

FACTORS = ["Value", "Quality", "Growth", "Consensus",
           "Sentiment", "Momentum", "Risk"]

def plot_radar(ax, scores: dict[str, float], title: str):
    angles = np.linspace(0, 2 * np.pi, len(FACTORS), endpoint=False).tolist()
    angles_closed = angles + [angles[0]]
    vals = [scores[f] for f in FACTORS]
    vals_closed = vals + [vals[0]]

    ax.fill(angles_closed, vals_closed, color="#1ABC9C", alpha=0.20)
    ax.plot(angles_closed, vals_closed, color="#1ABC9C", linewidth=2.0,
            marker="o", markersize=4)
    # 50 ライン
    ax.plot(angles_closed, [50] * len(angles_closed),
            color="#cccccc", linewidth=0.8, linestyle="--")

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 100)
    ax.set_xticks(angles)
    ax.set_xticklabels(FACTORS, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=14)
```

### スコアボードのヒートマップ表

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_scoreboard(ax, top_df, cols, labels):
    cmap = plt.get_cmap("RdYlGn")
    for r, (_, row) in enumerate(top_df.iterrows()):
        for i, col in enumerate(cols):
            v = row[col]
            color = cmap(np.clip(v / 100, 0.05, 0.95))
            rect = Rectangle((5.5 + i - 0.45, r + 0.05), 0.9, 0.9,
                             facecolor=color, edgecolor="white", linewidth=1.0)
            ax.add_patch(rect)
            # 背景の明暗に応じて文字色を反転
            txt_color = "white" if v < 35 or v > 70 else "#202124"
            ax.text(5.5 + i, r + 0.5, f"{v:.0f}",
                    ha="center", va="center", fontsize=9.5,
                    color=txt_color)
```


---

*データ出典: 証券会社が無料で提供する 13 指標（EPS / BPS / 配当金 / EV/EBITDA / ROE / ROA / 営業利益率 / 自己資本比率 / 売上高変化率 / 経常利益変化率 / 業績予想修正率(予) / 経常利益変化率(予) / 過去3年平均売上高成長率(予)） + yfinance 日足 Close / Volume*
