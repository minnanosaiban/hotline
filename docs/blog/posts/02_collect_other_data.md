---
date: 2026-05-19
categories:
  - データ取得
tags:
  - TDnet
  - EDINET
  - XBRL
  - 決算短信
  - コンセンサス
---

# 株価以外も取得しよう ― EDINET・TDnet・証券会社のアプリを活用

![株価以外のデータを集める](img/02_collect_other_data/00_thumbnail.png){width="1280"}

株価だけ、チャートだけを見て株を買う。これだとギャンブルとそう変わりません。ギャンブルから一歩先へ。決算を分析することで銘柄の業績について多角的な分析が行えます。

本記事では決算に関するデータの取り方を一通り押さえ、連載01で紹介したチャートからもう一歩目的をもったチャート作成に進めていきます。

<!-- more -->



## 3 つのデータソース

| 取得元            | 情報                | 形式        |
| -------------- | ----------------- | --------- |
| **金融庁 EDINET** | 有価証券報告書（有報 XBRL ） | XBRL      |
| **東証 TDnet**   | 決算短信 XBRL ・決算発表日時 | HTML・XBRL |
| **証券会社のアプリ**   | 業績指標              | CSV       |

- 金融庁 EDINET と 東証 TDnet で取得するデータは、 **XBRL** というファイル形式です。XBRL の使い方は次回連載03 で扱います。本記事では **データの取り方** を解説します。

> ⚠️これらのデータは商用利用・データ転売が禁止です。個人の投資判断目的に限る。アクセス間隔を 1 秒以上空けるなどマナーを守って使用してください。

## 金融庁 EDINET

有報は、**PDF と XBRL**（タグ付きデータ）の二つの形式で入手することができます。この XBRL は EDINET 公式 API で 取得できます。

業績推移はヤフーファイナンスや株探などのサービスで確認できますが、期間は3～5年です。有報を遡って足せば **10 年超**の業績時系列も組めます。また、データを取得することで、銘柄の業績を比較した可視化が可能です。

```python
res = requests.get(f"https://disclosure.edinet-fsa.go.jp/api/v2/documents/{doc_id}",
    params={"type": 5, "Subscription-Key": API_KEY}) 
# type=5 で XBRL を取得
```




## 東証 TDnet 

**決算短信 XBRL や決算発表日時** は、有報 XBRL と違い、公式 API がないため、PDF の URL から ZIP の URL に変換し、そのURLでスクレイピングするという方法をとります。

```python
import re, requests
from bs4 import BeautifulSoup

url = f"https://www.release.tdnet.info/inbs/I_list_001_{target_date}.html"
soup = BeautifulSoup(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text, "html.parser")
# 決算短信のリンクと発表時刻を抽出し、date, time, code の3列で earnings.csv に保存
```


## 証券会社のアプリ

連載04〜07（PEG × ROE・マルチファクターなど）で「予想」「コンセンサス」として使う指標は、証券会社のアプリ から CSV でエクスポートできます。

- EPS / BPS / 配当 / ROE / ROA / EV/EBITDA / 業績予想修正率(予想) / 経常利益変化率(予想) など様々な指標がそろっています。
- 楽天証券・マネックス証券・SBI 証券・会社四季報などが同等の指標を提供しています。

> ⚠️本記事以降、「予想」と表記されているものは **アナリストのコンセンサス値** で、企業公式の業績予想とは異なります。



## <i class="fa-brands fa-github"></i> Python コード

本記事のチャート画像・アプリ・データ取得・成形スクリプトは、すべて **GitHub に公開**しています。データは提供元の利用規約により再配布できませんが、データを各自取得すれば、本連載と同じものが再現できます（動かし方はリポジトリの README 参照）。

> [<small><i class="fa-brands fa-github"></i> データ取得・成形 ― 金融庁 EDINET から有報 XBRL を取得して JSON に変換（連載03）</small>](https://github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_yuho.py)
> [<small>github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_yuho.py</small>](https://github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_yuho.py)
> [<small><i class="fa-brands fa-github"></i> データ取得・成形 ― 東証 TDnet から決算短信 XBRL を取得</small>](https://github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_kessan.py)
> [<small>github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_kessan.py</small>](https://github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_kessan.py)
> [<small><i class="fa-brands fa-github"></i> データ取得・成形 ― 東証 TDnet から決算発表日時を取得</small>](https://github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_tdnet.py)
> [<small>github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_tdnet.py</small>](https://github.com/minnanosaiban/blog/blob/main/03_xbrl_json/fetch_tdnet.py)
> [<small><i class="fa-brands fa-github"></i> Streamlit アプリ ― 複数銘柄を俯瞰するチャート</small>](https://github.com/minnanosaiban/blog/tree/main/02_1_chart_multi)
> [<small>github.com/minnanosaiban/blog/02_1_chart_multi</small>](https://github.com/minnanosaiban/blog/tree/main/02_1_chart_multi)
> [<small><i class="fa-brands fa-github"></i> Streamlit アプリ ― 決算発表直後の動きを確認するチャート</small>](https://github.com/minnanosaiban/blog/tree/main/02_2_chart_earnings_pattern)
> [<small>github.com/minnanosaiban/blog/02_2_chart_earnings_pattern</small>](https://github.com/minnanosaiban/blog/tree/main/02_2_chart_earnings_pattern)

#### 📈 Streamlit アプリ ― 複数銘柄を俯瞰するチャート

連載01 の株価だけでは「チャートを並べる」までですが、ここで取得した **業績指標（PER / PBR / 配当）** を重ねると、銘柄比較が一気に厚くなります。複数銘柄のファンダ指標とチャートを 4 列カードグリッドで **1 画面で俯瞰** する Streamlit アプリです。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![複数銘柄カードグリッド](https://github.com/minnanosaiban/blog/blob/main/02_1_chart_multi/app.png?raw=true){width="1200"}

#### 📈 Streamlit アプリ ― 決算発表直後の動きを確認するチャート

5分足 parquet と発表日時 `earnings.csv` で、決算発表後の値動きを 5 パターン（🟢上げ / 逆 V 字 / 無風 / V 字 / 🔴下げ）に自動分類する Streamlit アプリです。各銘柄の5分足チャートに、発表時刻の **縦点線**を入れていますので、決算発表直後の激しい株価の動きが確認できます。

<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![決算パターングリッド](https://github.com/minnanosaiban/blog/blob/main/02_2_chart_earnings_pattern/app.png?raw=true){width="1200"}

---

*データ出典: TDnet 適時開示（発表日時）/ 証券会社が無料で提供する銘柄情報シート CSV / EDINET API（金融庁）の有報 XBRL / TDnet の決算短信 XBRL*
