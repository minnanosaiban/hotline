"""
連載03 EPSリビジョン・モメンタム サムネイル生成
出力: docs/blog/posts/img/03_eps_revision/00_thumbnail.png
サイズ: 1280x670 px（Note 推奨 16:9）
実行: python docs/blog/scripts/thumb_03_eps_revision.py

設計方針:
  - 修正率 × 株価モメンタムの象限図（記事の散布図と同じ軸）
  - ★ = 右下「出遅れ買い候補」（上方修正済みだが市場が未追随）
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams

rcParams['font.family'] = 'Noto Sans JP'
rcParams['axes.unicode_minus'] = False

BG       = '#0d1b2a'
PANEL    = '#162236'
BLUE_L   = '#5fa8e5'
GREEN    = '#22c55e'
GREEN_BG = '#0e3a23'
MUTED_BG = '#1a2535'
MUTED_TX = '#a5b8cc'
WHITE    = '#f5f8fc'
SOFT     = '#b5c4d6'

DPI = 100
fig = plt.figure(figsize=(12.80, 6.70), dpi=DPI, facecolor=BG)

ax_l = fig.add_axes([0.0, 0.0, 0.44, 1.0], facecolor=BG)
ax_l.axis('off')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)

ax_l.add_patch(patches.Rectangle(
    (0.07, 0.875), 0.018, 0.055, facecolor=BLUE_L, linewidth=0
))
ax_l.text(0.110, 0.902, '連載 03', color=BLUE_L,
          fontsize=24, va='center', ha='left', fontweight='bold')

ax_l.text(0.07, 0.69, 'EPS', color=WHITE,
          fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.text(0.41, 0.69, 'リビジョン', color=WHITE,
          fontsize=36, va='center', ha='left', fontweight='bold')

ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))

ax_l.text(0.07, 0.48, '修正動向と', color=BLUE_L,
          fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, 'サプライズの統合', color=WHITE,
          fontsize=36, va='center', ha='left', fontweight='bold')


ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(-0.25, 2.05)
ax_r.set_ylim(-0.32, 2.25)
ax_r.axis('off')

zones = [
    (0, 1, 1, 1, MUTED_BG),   # 左上：逆行注意
    (1, 1, 1, 1, MUTED_BG),   # 右上：既反応済
    (0, 0, 1, 1, MUTED_BG),   # 左下：底入れ待ち
    (1, 0, 1, 1, GREEN_BG),   # 右下：★ 出遅れ買い候補
]
for (x, y, w, h, fc) in zones:
    ax_r.add_patch(patches.Rectangle(
        (x, y), w, h, facecolor=fc, edgecolor='none'
    ))

ax_r.add_patch(patches.Rectangle(
    (1, 0), 1, 1, fill=False, edgecolor=GREEN, linewidth=3
))

ax_r.plot([1, 1], [0, 2], color=SOFT, linewidth=0.8, alpha=0.3)
ax_r.plot([0, 2], [1, 1], color=SOFT, linewidth=0.8, alpha=0.3)

# ★ 右下: 出遅れ買い候補
ax_r.text(1.50, 0.72, '★', color=GREEN,
          fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text(1.50, 0.48, '出遅れ', color=GREEN,
          fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text(1.50, 0.24, '買い候補', color=WHITE,
          fontsize=24, ha='center', va='center', fontweight='bold')

other_zones = [
    (0.50, 1.55, '逆行注意',   MUTED_TX, 24),
    (1.50, 1.55, '既反応済',   MUTED_TX, 24),
    (0.50, 0.55, '底入れ待ち', MUTED_TX, 24),
]
for (x, y, txt, color, fs) in other_zones:
    ax_r.text(x, y, txt, color=color, fontsize=fs,
              ha='center', va='center')

ax_r.annotate('', xy=(2.05, -0.14), xytext=(-0.05, -0.14),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=1.4, alpha=0.7))
ax_r.text(0.50, -0.14, '下方', color=SOFT, fontsize=19,
          ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor='none'))
ax_r.text(1.50, -0.14, '上方', color=SOFT, fontsize=19,
          ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor='none'))
ax_r.text(1.00, -0.36, '業績修正率', color=SOFT, fontsize=24,
          ha='center', va='center', alpha=0.9, fontweight='bold')

ax_r.annotate('', xy=(-0.15, 2.05), xytext=(-0.15, -0.05),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=1.4, alpha=0.7))
ax_r.text(-0.15, 0.50, '低', color=SOFT, fontsize=19,
          ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor='none'))
ax_r.text(-0.15, 1.50, '高', color=SOFT, fontsize=19,
          ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor='none'))
ax_r.text(-0.15, 2.24, '株価モメンタム', color=SOFT, fontsize=24,
          ha='center', va='center', alpha=0.9, fontweight='bold')

OUT = os.path.join(
    os.path.dirname(__file__),
    '..', 'posts', 'img', '03_eps_revision', '00_thumbnail.png'
)
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
