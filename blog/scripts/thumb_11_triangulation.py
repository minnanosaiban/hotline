"""
連載11 三角検証 サムネイル生成
出力: docs/blog/posts/img/11_triangulation/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 11', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, '三角検証', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '3ソース統合で', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '信頼度向上', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# 三角形（3ソース）
import math
cx, cy = 50, 60
radius = 25

# 頂点
p1 = (cx, cy + radius)  # 実績
p2 = (cx - radius * math.cos(math.pi/6), cy - radius * math.sin(math.pi/6))  # ガイダンス
p3 = (cx + radius * math.cos(math.pi/6), cy - radius * math.sin(math.pi/6))  # コンセンサス

# 三角形
triangle = patches.Polygon([p1, p2, p3], facecolor=BLUE_L, edgecolor=GREEN, linewidth=3, alpha=0.2)
ax_r.add_patch(triangle)

# ラベル
ax_r.text(p1[0], p1[1] + 5, '実績\n(EDINET)', color=GREEN, fontsize=12, ha='center', va='bottom', fontweight='bold')
ax_r.text(p2[0] - 8, p2[1], 'ガイダンス\n(決算短信)', color=BLUE_L, fontsize=11, ha='right', va='center', fontweight='bold')
ax_r.text(p3[0] + 8, p3[1], 'コンセンサス\n(アナリスト)', color='#22d4a8', fontsize=11, ha='left', va='center', fontweight='bold')

# 中央
ax_r.text(cx, cy, '検証点', color=WHITE, fontsize=13, ha='center', va='center', fontweight='bold')

ax_r.text(50, 20, '211銘柄で4象限分類', color=SOFT, fontsize=12, ha='center', va='center', style='italic')
ax_r.text(50, 10, '総合商社8社 クロス分析完了', color=SOFT, fontsize=11, ha='center', va='center', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '11_triangulation', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
