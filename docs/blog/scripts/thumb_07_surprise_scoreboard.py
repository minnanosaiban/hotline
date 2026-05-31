"""
連載04 連続サプライズ・スコアボード サムネイル生成
出力: docs/blog/posts/img/07_surprise_scoreboard/00_thumbnail.png
サイズ: 1280x670 px（Note 推奨 16:9）
実行: python docs/blog/scripts/thumb_04_surprise.py
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

# ===== 左エリア =====
ax_l = fig.add_axes([0.0, 0.0, 0.44, 1.0], facecolor=BG)
ax_l.axis('off')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)

ax_l.add_patch(patches.Rectangle((0.07, 0.875), 0.018, 0.055, facecolor=BLUE_L, linewidth=0))
ax_l.text(0.110, 0.902, '連載 04', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')

# タイトル: 「連続」小 + 「サプライズ」大、ベースライン揃え
ax_l.text(0.07, 0.69, '連続', color=WHITE,
          fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.text(0.44, 0.69, 'サプライズ', color=SOFT,
          fontsize=36, va='center', ha='left', fontweight='bold')

ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))

ax_l.text(0.07, 0.48, '複数シグナルで', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '本物の強気を検出', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

# ===== 右エリア（4象限）=====
ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(-0.25, 2.05)
ax_r.set_ylim(-0.32, 2.25)
ax_r.axis('off')

zones = [
    (0, 1, 1, 1, MUTED_BG),   # 左上：回復期待
    (1, 1, 1, 1, GREEN_BG),   # 右上：★ 上方修正 × 来期成長
    (0, 0, 1, 1, MUTED_BG),   # 左下：回避ゾーン
    (1, 0, 1, 1, MUTED_BG),   # 右下：ピークアウト警戒
]
for (x, y, w, h, fc) in zones:
    ax_r.add_patch(patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor='none'))

ax_r.add_patch(patches.Rectangle((1, 1), 1, 1, fill=False, edgecolor=GREEN, linewidth=3))

ax_r.plot([1, 1], [0, 2], color=SOFT, linewidth=0.8, alpha=0.3)
ax_r.plot([0, 2], [1, 1], color=SOFT, linewidth=0.8, alpha=0.3)

# ★ 右上: 上方修正 × 来期成長（本命）
ax_r.text(1.50, 1.72, '★', color=GREEN, fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text(1.50, 1.48, '上方修正×', color=GREEN, fontsize=28, ha='center', va='center', fontweight='bold')
ax_r.text(1.50, 1.24, '来期成長', color=WHITE, fontsize=24, ha='center', va='center', fontweight='bold')

# 他象限
other_zones = [
    (0.50, 1.55, '回復期待',         MUTED_TX, 24),
    (0.50, 0.55, '回避ゾーン',       MUTED_TX, 24),
    (1.50, 0.55, 'ピークアウト警戒', MUTED_TX, 22),
]
for (x, y, txt, color, fs) in other_zones:
    ax_r.text(x, y, txt, color=color, fontsize=fs, ha='center', va='center')

# 軸ラベル（X: 業績予想修正率）
ax_r.annotate('', xy=(2.05, -0.14), xytext=(-0.05, -0.14),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=1.4, alpha=0.7))
ax_r.text(0.50, -0.14, '低', color=SOFT, fontsize=19, ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor='none'))
ax_r.text(1.50, -0.14, '高', color=SOFT, fontsize=19, ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor='none'))
ax_r.text(1.00, -0.36, '業績予想修正率', color=SOFT, fontsize=24, ha='center', va='center', alpha=0.9, fontweight='bold')

# 軸ラベル（Y: 直近株価モメンタム）
ax_r.annotate('', xy=(-0.15, 2.05), xytext=(-0.15, -0.05),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=1.4, alpha=0.7))
ax_r.text(-0.15, 0.50, '低', color=SOFT, fontsize=19, ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor='none'))
ax_r.text(-0.15, 1.50, '高', color=SOFT, fontsize=19, ha='center', va='center', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor='none'))
ax_r.text(-0.15, 2.24, '経常利益変化率(予)', color=SOFT, fontsize=22, ha='center', va='center', alpha=0.9, fontweight='bold')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '07_surprise_scoreboard', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
