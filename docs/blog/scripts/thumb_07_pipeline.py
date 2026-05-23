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
ax_l.text(0.07, 0.48, '金融庁データの', color=BLUE_L, fontsize=36, va='center', ha='left', fontweight='bold')
ax_l.text(0.07, 0.37, 'パイプライン解説', color=WHITE, fontsize=36, va='center', ha='left', fontweight='bold')

ax_r = fig.add_axes([0.46, 0.10, 0.50, 0.80], facecolor=BG)
ax_r.set_xlim(0, 100)
ax_r.set_ylim(0, 100)
ax_r.axis('off')

# ===== 左: EDINET / TDnet（2ソース） =====
for x, y, label, color, sub in [
    (18, 70, 'EDINET', BLUE_L, 'ZIP 8,907件'),
    (18, 38, 'TDnet',  GREEN,  '決算短信'),
]:
    ax_r.add_patch(patches.FancyBboxPatch((x-15, y-12), 30, 24,
                                          boxstyle='round,pad=1',
                                          facecolor=color, edgecolor='none', alpha=0.25))
    ax_r.text(x, y+3, label, color=WHITE, fontsize=24, ha='center', va='center', fontweight='bold')
    ax_r.text(x, y-6, sub,   color=SOFT,  fontsize=16, ha='center', va='center')

# ===== 中央: XBRLパース =====
ax_r.add_patch(patches.FancyBboxPatch((42, 42), 22, 24,
                                      boxstyle='round,pad=1',
                                      facecolor=BLUE_L, edgecolor='none', alpha=0.25))
ax_r.text(53, 57, 'XBRL', color=WHITE, fontsize=24, ha='center', va='center', fontweight='bold')
ax_r.text(53, 48, 'パース', color=SOFT, fontsize=20, ha='center', va='center')

# ===== 右: 構造化データ =====
ax_r.add_patch(patches.FancyBboxPatch((73, 42), 24, 24,
                                      boxstyle='round,pad=1',
                                      facecolor=GREEN, edgecolor='none', alpha=0.25))
ax_r.text(85, 57, '構造化', color=WHITE, fontsize=24, ha='center', va='center', fontweight='bold')
ax_r.text(85, 48, 'データ', color=SOFT, fontsize=20, ha='center', va='center')

# ===== 扇形矢印（EDINET/TDnet → パース） =====
ax_r.annotate('', xy=(42, 61), xytext=(33, 70),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=2, alpha=0.7))
ax_r.annotate('', xy=(42, 50), xytext=(33, 43),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=2, alpha=0.7))

# ===== 矢印（パース → 構造化） =====
ax_r.annotate('', xy=(73, 54), xytext=(64, 54),
              arrowprops=dict(arrowstyle='->', color=SOFT, lw=2, alpha=0.7))


OUT = os.path.join(os.path.dirname(__file__), '..', 'posts', 'img', '07_pipeline', '00_thumbnail.png')
OUT = os.path.normpath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
plt.close()
print(f'Saved -> {OUT}')
