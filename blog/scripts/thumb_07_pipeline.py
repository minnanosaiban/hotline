"""
連載07 EDINET/TDnet取得とパース サムネイル生成
出力: docs/blog/posts/img/07_pipeline/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 07', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'EDINET/TDnet', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '金融庁の', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, 'データパイプライン解説', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# パイプラインフロー
stages = [
    (15, 75, '企業\n(有報)', BLUE_L),
    (40, 75, 'EDINET\n(ZIP)', GREEN),
    (65, 75, 'XBRL\nパース', BLUE_L),
    (15, 45, 'TDnet\n(決算短信)', BLUE_L),
    (40, 45, 'JSON\nスキーマ', GREEN),
    (65, 45, '投資家\n活用', BLUE_L),
]

for x, y, label, color in stages:
    ax_r.add_patch(patches.FancyBboxPatch((x-8, y-8), 16, 16,
                                          boxstyle='round,pad=0.5',
                                          facecolor=color, edgecolor='none', alpha=0.3))
    ax_r.text(x, y, label, color=WHITE, fontsize=12, ha='center', va='center', fontweight='bold')

# 矢印
for start_x, end_x in [(22, 33), (47, 58), (22, 33), (47, 58)]:
    ax_r.annotate('', xy=(end_x, 75), xytext=(start_x, 75),
                  arrowprops=dict(arrowstyle='->', color=SOFT, lw=2, alpha=0.6))
    ax_r.annotate('', xy=(end_x, 45), xytext=(start_x, 45),
                  arrowprops=dict(arrowstyle='->', color=SOFT, lw=2, alpha=0.6))

ax_r.text(50, 20, 'ZIP 8907件 → JSON 1368ファイル', color=SOFT, fontsize=12, ha='center', va='center', style='italic')
ax_r.text(50, 10, '有報 98 × 決算短信 263 マッピング', color=SOFT, fontsize=12, ha='center', va='center', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '07_pipeline', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
