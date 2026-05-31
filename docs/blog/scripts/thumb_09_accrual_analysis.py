"""
連載10 アクルーアル分析 サムネイル生成
出力: docs/blog/posts/img/09_accrual_analysis/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 10', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'アクルーアル', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '利益の', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '現金化率を検証', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.12, 0.50, 0.78], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 120)
ax_r.axis('off')

# ベースライン
ax_r.plot([5, 95], [0, 0], color=SOFT, linewidth=1.2, alpha=0.4)

# 棒グラフ（色を落とす：alpha低め＋枠線で輪郭）
bars = [
    (18, 90,  '純利益',     BLUE_L, '100%'),
    (50, 35,  'CF',        GREEN,  ' 39%'),
    (82, 55,  'アクルーアル', SOFT,   ' 61%'),
]

for x, h, cat, color, pct in bars:
    ax_r.add_patch(patches.Rectangle(
        (x-13, 0), 26, h,
        facecolor=color, edgecolor=color,
        alpha=0.18, linewidth=2
    ))
    ax_r.add_patch(patches.Rectangle(
        (x-13, 0), 26, h,
        facecolor='none', edgecolor=color,
        alpha=0.7, linewidth=2
    ))
    ax_r.text(x, h + 5, pct, color=color, fontsize=24,
              ha='center', va='bottom', fontweight='bold')
    ax_r.text(x, -7, cat, color=WHITE, fontsize=20,
              ha='center', va='top', fontweight='bold')

# ENEOS の実数を下部に
ax_r.text(50, 15, 'ENEOS 2022  純利5,371億', color=SOFT, fontsize=20,
          ha='center', va='center')
ax_r.text(50, 4,  'CF 2,095億（39%）', color=GREEN, fontsize=20,
          ha='center', va='center', fontweight='bold')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '09_accrual_analysis', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
