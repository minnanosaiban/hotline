"""
連載08 決算短信JSONスキーマ設計 サムネイル生成
出力: docs/blog/posts/img/08_schema/00_thumbnail.png
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams

rcParams['font.family'] = 'Noto Sans JP'
rcParams['axes.unicode_minus'] = False

BG = '#0d1b2a'
BLUE_L = '#5fa8e5'
GREEN = '#22c55e'
MUTED_BG = '#1a2535'
WHITE = '#f5f8fc'
SOFT = '#b5c4d6'

DPI = 100
fig = plt.figure(figsize=(12.80, 6.70), dpi=DPI, facecolor=BG)

ax_l = fig.add_axes([0.0, 0.0, 0.44, 1.0], facecolor=BG)
ax_l.axis('off')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)

ax_l.add_patch(patches.Rectangle((0.07, 0.875), 0.018, 0.055, facecolor=BLUE_L, linewidth=0))
ax_l.text(0.110, 0.902, '連載 08', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'JSON', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.text(0.50, 0.69, 'スキーマ', color=SOFT, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '決算データの', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '構造化設計5原則', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# 5つの原則
principles = [
    (84, '1. 単一責任',  GREEN),
    (71, '2. 拡張性',    BLUE_L),
    (58, '3. 検証可能性','#22d4a8'),
    (45, '4. 遡及性',    '#d4a822'),
    (32, '5. 再利用性',  '#a822d4'),
]

for y, label, color in principles:
    ax_r.add_patch(patches.FancyBboxPatch((6, y-6), 88, 12,
                                          boxstyle='round,pad=0.5',
                                          facecolor=MUTED_BG, edgecolor=color, linewidth=2))
    ax_r.text(50, y, label, color=color, fontsize=24, ha='center', va='center', fontweight='bold')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '08_schema', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
