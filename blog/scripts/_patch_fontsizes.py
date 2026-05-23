"""
chart make_images スクリプト内の fontsize を 1.4 倍にする一括パッチ。
実行: python docs/blog/scripts/_patch_fontsizes.py
"""
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
SCALE = 1.4

targets = sorted(SCRIPTS_DIR.glob("[0-9][0-9]*_make_images.py"))

def scale_fontsize(m):
    val = float(m.group(1))
    new_val = round(val * SCALE, 1)
    # 整数になる場合は整数で返す
    if new_val == int(new_val):
        return f"fontsize={int(new_val)}"
    return f"fontsize={new_val}"

pattern = re.compile(r"fontsize=(\d+(?:\.\d+)?)")

for path in targets:
    original = path.read_text(encoding="utf-8")
    patched = pattern.sub(scale_fontsize, original)
    if patched != original:
        path.write_text(patched, encoding="utf-8")
        count = len(pattern.findall(original))
        print(f"  {path.name}: {count} 箇所を {SCALE}x に変換")
    else:
        print(f"  {path.name}: 変更なし")

print("\n完了")
