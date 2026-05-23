"""
連載13 CARイベントスタディ サムネイル生成
出力: docs/blog/posts/img/13_car/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 13', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'CARイベント', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, 'イベント直後の', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '超過リターンを検出', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(-25, 25)
ax_r.set_ylim(-20, 20)
ax_r.axis('off')

# CARチャート（t=0でイベント発生）
import numpy as np
t = np.linspace(-20, 20, 100)
# ENEOS ピークアウト CAR: [-1,+20]=-13.89%
car_curve = -13.89 * (1 - np.exp(-0.1 * np.abs(t)))
for i in range(len(t)-1):
    if t[i] >= -1 and t[i+1] <= 20:
        ax_r.plot(t[i:i+2], car_curve[i:i+2], color='#ff6b6b', linewidth=3, alpha=0.8)

ax_r.axvline(0, color=SOFT, linewidth=1.5, linestyle='--', alpha=0.6)
ax_r.axhline(0, color=SOFT, linewidth=1, alpha=0.3)

# イベント期間
ax_r.fill_between([-1, 20], -20, 20, color=GREEN, alpha=0.05)
ax_r.text(9.5, -15, 'Event Window\n[-1, +20]', color=GREEN, fontsize=11, ha='center', va='center', fontweight='bold')

# マーカー
ax_r.plot(0, 0, 'o', color=BLUE_L, markersize=8)
ax_r.text(0, 2, 'イベント\nt=0', color=BLUE_L, fontsize=10, ha='center', va='bottom', fontweight='bold')

ax_r.text(0, -20, 'ENEOS 2025/3期通期: CAR = -13.89% (r=+0.694)', color='#ff6b6b', fontsize=9, ha='center', va='top', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '13_car', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
