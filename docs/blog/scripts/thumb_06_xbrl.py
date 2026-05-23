"""
連載06 XBRLとは何か サムネイル生成
出力: docs/blog/posts/img/06_xbrl/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 06', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'XBRL', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, 'タグ付き財務', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, 'データの標準フォーマット', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# XBRL 階層構造の簡略表現
levels = [
    (50, 85, '有報XBRL', 20, GREEN),
    (20, 70, '貸借対照表', 16, BLUE_L),
    (50, 70, '損益計算書', 16, BLUE_L),
    (80, 70, 'キャッシュフロー', 16, BLUE_L),
    (10, 50, '資産', 14, '#5fa8e5'),
    (25, 50, '負債', 14, '#5fa8e5'),
    (40, 50, '売上', 14, '#5fa8e5'),
    (60, 50, '利益', 14, '#5fa8e5'),
    (80, 50, '現金', 14, '#5fa8e5'),
]

for x, y, label, size, color in levels:
    ax_r.text(x, y, label, color=color, fontsize=size, ha='center', va='center', fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.4', facecolor=MUTED_BG, edgecolor=color, linewidth=1.5))

ax_r.text(50, 15, '＼機械可読性 ＋ 検証可能性／', color=WHITE, fontsize=14, ha='center', va='center', style='italic')
ax_r.text(50, 5, '企業 → 金融庁EDINET → 投資家', color=SOFT, fontsize=12, ha='center', va='center')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '06_xbrl', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
