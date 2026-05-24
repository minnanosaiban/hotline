# blog 画像生成スクリプト 設計基準

## 縮小率の統一

- **単体チャート**: `figsize` 幅 **13 インチ** / 144 DPI → 約 1872px（ブログ 800px カラムで約 43% 縮小）
- **グリッドチャート**: `cols × col_w` の可変幅を維持する（13 インチに固定しない）

## 余白（下のみ・上と左右は不要）

上部は Markdown の「クリックで拡大できます」テキストが余白を兼ねる。

```python
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["savefig.pad_inches"] = 0  # 左右・上余白なし

# 下のみ 0.5 インチ余白を追加するヘルパーで保存する
# ※ spacer 方式はコンテンツ下端位置によって余白が変わるため、
#   PNG にピクセル行を直接追加する方式を採用する。
def _savefig_vpad(fig: plt.Figure, path: Path, bpad: float = 0.5) -> None:
    """下のみ bpad インチの余白を追加して保存する（上・左右は余白なし）。"""
    import io
    import numpy as np
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches="tight", pad_inches=0, format="png")
    buf.seek(0)
    img = plt.imread(buf)                            # RGBA float32 (H, W, 4)
    pad_rows = max(1, round(bpad * fig.dpi))
    white = np.ones((pad_rows, img.shape[1], img.shape[2]), dtype=img.dtype)
    plt.imsave(str(path), np.vstack([img, white]), dpi=fig.dpi)
```

`fig.savefig(path)` の代わりに必ず `_savefig_vpad(fig, path)` を使う。

また、`subplots_adjust(bottom=X)` や `gridspec(bottom=X)` で独自の下余白を設けると
`_savefig_vpad` と二重に積み上がるため、これらの `bottom=` は **0 または省略** にする。

## フォントサイズ下限

| 用途 | 最小サイズ |
|---|---|
| 本文テキスト（軸ラベル・凡例・注釈） | **16** |
| 小ラベル（コード番号・補足・PEG/ROE 表示） | **16** |
| タイトル | **20** |
| サブタイトル（suptitle） | **21** |

## タイトルとグラフの間隔

```python
mpl.rcParams["axes.titlepad"] = 30  # タイトルとグラフ上端の余白（pt）
```

## タイトル重複の禁止

`fig.suptitle` を使う場合、`ax.set_title` は削除する（両方置くと重なる）。

## ズームヒント（Markdown 側）

各画像 `![]()` の**直前の行**に必ず配置する:

```markdown
<small style="color: var(--md-link-color);"><i class="fa-solid fa-expand"></i> クリックで拡大できます</small>

![alt](img/path.png){width="1200"}
```
