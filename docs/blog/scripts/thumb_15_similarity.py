"""
連載15 類似決算検索 サムネイル生成
出力: docs/blog/posts/img/15_similarity/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 15', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, '類似決算', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '10次元特徴で', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, 'ベンチマーク発見', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(-3, 3)
ax_r.set_ylim(-3, 3)
ax_r.axis('off')

# 散布図（ベクトル空間）
import numpy as np
np.random.seed(42)

# 丸紅と類似企業（商社クラスタ）
marubeni = [0.5, 0.3]
colors_point = [GREEN, GREEN, GREEN, GREEN, BLUE_L, BLUE_L, '#c55e22']
labels = ['丸紅', '三井物産', '三菱商事', '住友商事', '豊田通商', '日本郵政', '雪国まいたけ']
positions = [
    [0.5, 0.3],
    [0.7, 0.2],
    [0.4, 0.5],
    [0.8, 0.4],
    [1.8, 1.5],
    [2.5, 2.0],
    [-2.0, -2.0],
]

for pos, color, label in zip(positions, colors_point, labels):
    if label == '丸紅':
        ax_r.plot(pos[0], pos[1], 'o', color=GREEN, markersize=12, markeredgecolor='white', markeredgewidth=2)
    else:
        ax_r.plot(pos[0], pos[1], 'o', color=color, markersize=8, alpha=0.6)

    # ラベル
    offset = 0.25
    ax_r.text(pos[0] + offset, pos[1] + offset, label, color=color if label != '丸紅' else WHITE,
              fontsize=9, ha='left', va='bottom', fontweight='bold')

# 距離円
circle = patches.Circle((marubeni[0], marubeni[1]), 1.0, fill=False, edgecolor=GREEN, linewidth=2, linestyle='--', alpha=0.5)
ax_r.add_patch(circle)

ax_r.text(0, -2.5, '丸紅 2026/3期 類似Top-15 平均 +2.39% (勝率60%)', color=GREEN, fontsize=10, ha='center', va='top', fontweight='bold', style='italic')
ax_r.text(0, -2.8, 'vs 丸紅自身 -9.39% で個別ショック発見', color='#ff6b6b', fontsize=10, ha='center', va='top', fontweight='bold', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '15_similarity', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
