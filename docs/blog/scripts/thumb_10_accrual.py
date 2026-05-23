"""
連載10 アクルーアル分析 サムネイル生成
出力: docs/blog/posts/img/10_accrual/00_thumbnail.png
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
ax_l.text(0.110, 0.902, '連載 10', color=BLUE_L, fontsize=24, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.69, 'アクルーアル', color=WHITE, fontsize=72, va='center', ha='left', fontweight='bold')
ax_l.set_xlim(0, 1)
ax_l.set_ylim(0, 1)
ax_l.add_patch(patches.Rectangle((0.07, 0.578), 0.85, 0.004, facecolor=BLUE_L, linewidth=0, alpha=0.6))
ax_l.text(0.07, 0.48, '利益の', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, '現金化率を検証', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 120)
ax_r.axis('off')

# 利益 vs キャッシュフロー
categories = ['純利益', 'CF', 'アクルーアル']
y_base = [100, 39, 61]
colors_bar = [GREEN, BLUE_L, '#c55e22']

for i, (cat, val, color) in enumerate(zip(categories, y_base, colors_bar)):
    x_pos = 20 + i * 25
    # バー
    ax_r.add_patch(patches.Rectangle((x_pos-5, 0), 10, val, facecolor=color, edgecolor='none', alpha=0.7))
    # ラベル
    ax_r.text(x_pos, val + 3, f'{val}%', color=color, fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax_r.text(x_pos, -8, cat, color=WHITE, fontsize=12, ha='center', va='top', fontweight='bold')

ax_r.text(50, 60, 'ピーク利益の品質', color=SOFT, fontsize=13, ha='center', va='center', style='italic')
ax_r.text(50, 50, 'CF 39% (CF-based)', color=WHITE, fontsize=11, ha='center', va='center')

ax_r.text(50, 30, '91サンプル実装完了', color=SOFT, fontsize=12, ha='center', va='center')
ax_r.text(50, 20, 'ENEOS 2022: CF 2095億 / 純利 5371億', color='#c55e22', fontsize=10, ha='center', va='center', style='italic')

OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '10_accrual', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
