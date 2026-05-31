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
ax_l.text(0.07, 0.69, 'EDINET', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.text(0.66, 0.69, '/TDnet', color=SOFT, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '有報・決算短信を', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, 'XBRLで取得する', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.06, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# ===== XBRLを利用 タイトル =====
ax_r.text(50, 92, 'XBRLを利用', color=BLUE_L, fontsize=36,
          ha='center', va='center', fontweight='bold', style='italic')

# ===== 左ボックス: 有報PDF（非構造） =====
ax_r.add_patch(patches.FancyBboxPatch(
    (4, 32), 33, 47,
    boxstyle='round,pad=1.5',
    facecolor=MUTED_BG, edgecolor=SOFT, linewidth=2
))

# 内側タイトル
ax_r.text(20.5, 72, '有報PDF', color=WHITE, fontsize=24,
          ha='center', va='center', fontweight='bold')

# 非構造テキストを表すグレーの帯
line_widths = [22, 19, 24, 17, 23, 20]
for i, w in enumerate(line_widths):
    y = 62 - i * 4.5
    ax_r.add_patch(patches.Rectangle(
        (10, y), w, 1.6,
        facecolor=SOFT, alpha=0.45, edgecolor='none'
    ))

# ボックス下ラベル
ax_r.text(20.5, 24, '非構造', color=SOFT, fontsize=24,
          ha='center', va='center', fontweight='bold')

# ===== vs =====
ax_r.text(50, 55, 'vs', color=BLUE_L, fontsize=28,
          ha='center', va='center', fontweight='bold', style='italic')

# ===== 右ボックス: XBRL（構造化） =====
ax_r.add_patch(patches.FancyBboxPatch(
    (63, 32), 33, 47,
    boxstyle='round,pad=1.5',
    facecolor=MUTED_BG, edgecolor=GREEN, linewidth=2.5
))

# 内側タイトル
ax_r.text(79.5, 72, 'XBRL', color=GREEN, fontsize=24,
          ha='center', va='center', fontweight='bold')

# タグ:値ペア（XBRL の構造を象徴）
tags = [
    (64, 'NetSales',  '150,000億'),
    (56, 'NetIncome',   '2,261億'),
    (48, 'Assets',    '85,000億'),
    (40, 'Cash',       '9,400億'),
]
for y, tag, val in tags:
    ax_r.text(66, y, f'{tag}:', color=BLUE_L, fontsize=13,
              ha='left', va='center', fontweight='bold')
    ax_r.text(94, y, val, color=WHITE, fontsize=13,
              ha='right', va='center', fontweight='bold')

# ボックス下ラベル
ax_r.text(79.5, 24, '機械可読', color=GREEN, fontsize=24,
          ha='center', va='center', fontweight='bold')
ax_r.text(79.5, 15, '横断比較が容易に', color=GREEN, fontsize=20,
          ha='center', va='center', fontweight='bold')


OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '07_pipeline', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
