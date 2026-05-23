"""
チャート make_images スクリプトのレイアウト修正パッチ。

変更内容:
  1. fig.suptitle(..., y=1.02) → y=0.99  (図内に収める)
  2. plt.tight_layout()        → plt.tight_layout(rect=[0, 0, 1, 0.95])  (suptitle 用余白)
  3. plt.savefig(OUT_DIR / ...) の直前に tight_layout がなければ挿入

実行: python docs/blog/scripts/_patch_layout.py
"""
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
targets = sorted(SCRIPTS_DIR.glob("[0-9][0-9]*_make_images.py"))

for path in targets:
    text = path.read_text(encoding="utf-8")
    original = text

    # 1. suptitle の y=1.02 → y=0.99（末尾がカンマ/括弧どちらでも対応）
    text = text.replace(', y=1.02)', ', y=0.99)')
    text = text.replace(' y=1.02)', ' y=0.99)')
    text = text.replace(', y=1.02,', ', y=0.99,')
    text = text.replace(' y=1.02,', ' y=0.99,')

    # 2. 既存 tight_layout() に rect を追加（rect= がまだないもの）
    text = re.sub(
        r'plt\.tight_layout\(\)',
        'plt.tight_layout(rect=[0, 0, 1, 0.95])',
        text,
    )

    # 3. plt.savefig(OUT_DIR / ... の直前に tight_layout がなければ挿入
    lines = text.split('\n')
    new_lines: list[str] = []
    for i, line in enumerate(lines):
        if re.search(r'plt\.savefig\(OUT_DIR\s*/', line):
            # 直前の非空行を確認
            prev = ''
            for prev_line in reversed(new_lines):
                if prev_line.strip():
                    prev = prev_line
                    break
            if 'tight_layout' not in prev:
                indent = re.match(r'(\s*)', line).group(1)
                new_lines.append(f'{indent}plt.tight_layout(rect=[0, 0, 1, 0.95])')
        new_lines.append(line)
    text = '\n'.join(new_lines)

    if text != original:
        path.write_text(text, encoding="utf-8")
        # 変更箇所をカウント
        n_y = len(re.findall(r'y=0\.99', text))
        n_tl = len(re.findall(r'tight_layout', text))
        print(f"  {path.name}: suptitle={n_y} / tight_layout={n_tl}")
    else:
        print(f"  {path.name}: 変更なし")

print("\n完了")
