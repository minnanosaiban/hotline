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

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(-2, 2)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# Z-score分布
import numpy as np
z_vals = np.linspace(-3, 3, 100)
y_vals = 100 * np.exp(-z_vals**2 / 2) / np.sqrt(2 * np.pi)

ax_r.plot(z_vals, y_vals, color=BLUE_L, linewidth=2.5, alpha=0.8)
ax_r.fill_between(z_vals, 0, y_vals, color=BLUE_L, alpha=0.15)

# 警告ゾーン
ax_r.axvline(-2, color='#ff6b6b', linewidth=2, linestyle='--', alpha=0.6)
ax_r.axvline(2, color='#ff6b6b', linewidth=2, linestyle='--', alpha=0.6)

ax_r.text(-2, 75, '警告\nZ<-2', color='#ff6b6b', fontsize=13, ha='center', va='center', fontweight='bold')
ax_r.text(2, 75, '警告\nZ>+2', color='#ff6b6b', fontsize=13, ha='center', va='center', fontweight='bold')
ax_r.text(0, 35, '正常域', color=BLUE_L, fontsize=14, ha='center', va='center', fontweight='bold')

ax_r.text(0, 10, '139サンプル分析済', color=SOFT, fontsize=12, ha='center', va='center', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '09_zscore', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
