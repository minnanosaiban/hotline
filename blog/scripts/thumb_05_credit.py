"""
連載05 信用需給ダッシュボード サムネイル生成
出力: docs/blog/posts/img/05_credit/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 05', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, '信用需給', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '信用倍率と出来高で', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '仕掛けを検出', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(-0.25, 2.05)
ax_r.set_ylim(-0.32, 2.25)
ax_r.axis('off')

zones = [
    (0, 1, 1, 1, '#1a4d2e'),
    (1, 1, 1, 1, MUTED_BG),
    (0, 0, 1, 1, MUTED_BG),
    (1, 0, 1, 1, '#4d1a1a'),
]
for (x, y, w, h, fc) in zones:
    ax_r.add_patch(patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor='none'))

ax_r.add_patch(patches.Rectangle((0, 1), 1, 1, fill=False, edgecolor=GREEN, linewidth=3))
ax_r.plot([1, 1], [0, 2], color=SOFT, linewidth=0.8, alpha=0.3)
ax_r.plot([0, 2], [1, 1], color=SOFT, linewidth=0.8, alpha=0.3)

ax_r.text(0.50, 1.72, '✓', color=GREEN, fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text(0.50, 1.48, '整理中', color=GREEN, fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text(0.50, 1.24, '需給好転', color=WHITE, fontsize=24, ha='center', va='center', fontweight='bold')

other_zones = [
    (1.50, 1.55, '踏み上げ罠', '#a5b8cc', 24),
    (0.50, 0.55, '弱気ムード', '#a5b8cc', 24),
]
for (x, y, txt, color, fs) in other_zones:
    ax_r.text(x, y, txt, color=color, fontsize=fs, ha='center', va='center')

ax_r.annotate('', xy=(2.05, -0.14), xytext=(-0.05, -0.14),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=1.4, alpha=0.7))
ax_r.text(1.00, -0.36, '信用倍率', color=SOFT, fontsize=24, ha='center', va='center', alpha=0.9, fontweight='bold')

ax_r.annotate('', xy=(-0.15, 2.05), xytext=(-0.15, -0.05),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=1.4, alpha=0.7))
ax_r.text(-0.15, 2.24, '出来高', color=SOFT, fontsize=24, ha='center', va='center', alpha=0.9, fontweight='bold')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '05_credit', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
