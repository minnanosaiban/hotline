"""
全 blog 画像生成スクリプトの _savefig_vpad を
PNG ピクセル行追加方式に一括置換する。
"""
from pathlib import Path
import re

SCRIPTS = Path(r"C:\stock_analysis\scripts\blog")

OLD = '''\
def _savefig_vpad(fig: plt.Figure, path: Path, bpad: float = 0.5) -> None:
    """下のみ余白 bpad インチを追加して保存する（上・左右は余白なし）。"""
    spacer = fig.text(0.5, -bpad / fig.get_figheight(), " ",
                      fontsize=1, alpha=0, va="bottom")
    fig.savefig(path, bbox_inches="tight", pad_inches=0)
    spacer.remove()'''

NEW = '''\
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
    plt.imsave(str(path), np.vstack([img, white]), dpi=fig.dpi)'''

changed = 0
for py in sorted(SCRIPTS.glob("[0-9][0-9]_*.py")):
    text = py.read_text(encoding="utf-8")
    if OLD in text:
        py.write_text(text.replace(OLD, NEW), encoding="utf-8")
        print(f"  patched {py.name}")
        changed += 1
    else:
        print(f"  skip    {py.name} (pattern not found)")

print(f"\n{changed} files patched.")
