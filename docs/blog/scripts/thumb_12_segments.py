"""
連載12 セグメント発進力 サムネイル生成
出力: docs/blog/posts/img/12_segments/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 12', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'セグメント', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '事業別成長で', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '転換期を検知', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# セグメント成長率
segments = [
    ('テストシステム', 50.9, '#ff6b6b'),
    ('宇宙・防衛', 28.3, '#4ecdc4'),
    ('ハンドラー', 12.5, '#45b7d1'),
    ('プローバー', 8.2, '#96ceb4'),
    ('部品', -5.3, '#dda15e'),
]

y_base = 75
for i, (name, growth, color) in enumerate(segments):
    y_pos = y_base - i * 14

    # バー（成長率表示）
    bar_width = growth / 2  # Scale down
    if bar_width > 0:
        ax_r.add_patch(patches.Rectangle((0, y_pos - 3), bar_width, 6, facecolor=color, edgecolor='none'))
    else:
        ax_r.add_patch(patches.Rectangle((bar_width, y_pos - 3), -bar_width, 6, facecolor=color, edgecolor='none'))

    # ラベル
    ax_r.text(-2, y_pos, name, color=WHITE, fontsize=12, ha='right', va='center', fontweight='bold')
    ax_r.text(bar_width + 2, y_pos, f'{growth:+.1f}%', color=color, fontsize=11, ha='left', va='center', fontweight='bold')

ax_r.axvline(0, color=SOFT, linewidth=1, linestyle='-', alpha=0.5)

ax_r.text(50, 15, '233銘柄 × 787セグメント', color=SOFT, fontsize=11, ha='center', va='center', style='italic')
ax_r.text(50, 5, 'アドバンテスト テストシステム 1兆円/+50%', color='#ff6b6b', fontsize=10, ha='center', va='center', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '12_segments', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
