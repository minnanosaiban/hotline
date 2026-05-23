"""
連載09 Z-score早期警報 サムネイル生成
出力: docs/blog/posts/img/09_zscore/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 09', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'Z-score', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '進捗率の', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '異常を統計検出', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.08, 0.50, 0.84], facecolor=BG)
ax_r.set_xlim(-4.5, 4.5)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# Z-score正規分布曲線（ピーク=62）
import numpy as np
z_vals = np.linspace(-4.5, 4.5, 400)
y_vals = 62 * np.exp(-z_vals**2 / 2)

mask_low    = z_vals <= -2
mask_normal = (z_vals >= -2) & (z_vals <= 2)
mask_high   = z_vals >= 2

ax_r.fill_between(z_vals, 0, y_vals, where=mask_low,    color='#ff6b6b', alpha=0.40)
ax_r.fill_between(z_vals, 0, y_vals, where=mask_normal, color=BLUE_L,    alpha=0.18)
ax_r.fill_between(z_vals, 0, y_vals, where=mask_high,   color=GREEN,     alpha=0.40)
ax_r.plot(z_vals, y_vals, color=BLUE_L, linewidth=2.5, alpha=0.9)

# ±2 の境界線
ax_r.plot([-2, -2], [0, 62 * np.exp(-2)], color='#ff6b6b', linewidth=2, linestyle='--', alpha=0.85)
ax_r.plot([ 2,  2], [0, 62 * np.exp(-2)], color=GREEN,     linewidth=2, linestyle='--', alpha=0.85)

# ゾーンラベル
ax_r.text(-3.3, 80, '警告',  color='#ff6b6b', fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text(-3.3, 68, 'Z < −2', color='#ff6b6b', fontsize=20, ha='center', va='center')
ax_r.text( 0,   80, '正常域', color=BLUE_L,    fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text( 3.3, 80, '好調',  color=GREEN,     fontsize=32, ha='center', va='center', fontweight='bold')
ax_r.text( 3.3, 68, 'Z > +2', color=GREEN,     fontsize=20, ha='center', va='center')

# 代表例ドット
ax_r.scatter([-4.5], [4], color='#ff6b6b', s=120, zorder=5, clip_on=False)
ax_r.text(-3.5, 14, 'E・J HD  Z=−5.56', color='#ff6b6b', fontsize=20, ha='center', va='center', fontweight='bold')
ax_r.scatter([4.71], [4], color=GREEN, s=120, zorder=5)
ax_r.text(3.4, 14, '京葉瓦斯  Z=+4.71', color=GREEN, fontsize=20, ha='center', va='center', fontweight='bold')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '09_zscore', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
