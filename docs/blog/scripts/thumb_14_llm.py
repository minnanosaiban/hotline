"""
連載14 LLM要約 サムネイル生成
出力: docs/blog/posts/img/14_llm/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 14', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'LLM要約', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '決算情報を', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '1文で自動要約', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# パイプラインフロー
stages = [
    (15, 75, 'JSON', BLUE_L, 14),
    (30, 75, '→', WHITE, 14),
    (40, 75, 'プロンプト', BLUE_L, 14),
    (60, 75, '→', WHITE, 14),
    (70, 75, 'LLM', GREEN, 14),
    (85, 75, '→', WHITE, 14),
]

for x, y, label, color, size in stages:
    ax_r.text(x, y, label, color=color, fontsize=size, ha='center', va='center', fontweight='bold')

# 4要素
elements = [
    (25, 55, '数値特徴', BLUE_L),
    (50, 55, 'CAR値', GREEN),
    (75, 55, 'トーン', '#22d4a8'),
]

for x, y, label, color in elements:
    ax_r.add_patch(patches.FancyBboxPatch((x-8, y-4), 16, 8,
                                          boxstyle='round,pad=0.3',
                                          facecolor=MUTED_BG, edgecolor=color, linewidth=1.5))
    ax_r.text(x, y, label, color=color, fontsize=12, ha='center', va='center', fontweight='bold')

ax_r.text(50, 42, '出力: 1文要約', color=WHITE, fontsize=13, ha='center', va='center', fontweight='bold')

# 実績例
ax_r.text(50, 30, '丸紅: CAR +8.94% / トーン好気', color=GREEN, fontsize=11, ha='center', va='center', style='italic')
ax_r.text(50, 22, '双日: CAR +0.92% / トーン好気', color=BLUE_L, fontsize=11, ha='center', va='center', style='italic')
ax_r.text(50, 14, '一致率: 超過リターン方向と要約トーン', color=SOFT, fontsize=10, ha='center', va='center', style='italic')

ax_r.text(50, 5, 'Haiku 1銘柄 ¥0.4', color=SOFT, fontsize=9, ha='center', va='center', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '14_llm', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
