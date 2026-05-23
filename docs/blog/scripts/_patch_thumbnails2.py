"""
サムネイル第2パッチ
- キャッチコピー fontsize: 22 → 38
- キャッチコピー2行目 y: 0.33 → 0.28
- 英語名 y: 0.18 → 0.12
- XBRL (06) メインタイトル: 100pt → 80pt
"""
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

def patch_file(path: Path):
    text = path.read_text(encoding='utf-8')
    fname = path.name
    changed = False

    # 1) キャッチコピー fontsize=22 → 38
    #    ax_l.text 行のみが対象（ax_r には fontsize=22 は存在しない前提）
    new = re.sub(r'(ax_l\.text\([^)]*fontsize=)22([^)]*\))', r'\g<1>38\2', text)
    if new != text:
        text = new
        changed = True

    # 2) キャッチコピー2行目 y=0.33 → 0.28
    new = re.sub(r'(ax_l\.text\(0\.07,\s*)0\.33(,)', r'\g<1>0.28\2', text)
    if new != text:
        text = new
        changed = True

    # 3) 英語名 y=0.18 → 0.12
    new = re.sub(r'(ax_l\.text\(0\.07,\s*)0\.18(,)', r'\g<1>0.12\2', text)
    if new != text:
        text = new
        changed = True

    # 4) XBRL スクリプトのみ: メインタイトル 100pt → 80pt
    if fname == 'thumb_06_xbrl.py':
        new = re.sub(
            r"(ax_l\.text\(0\.07,\s*0\.69,\s*'XBRL'[^)]*fontsize=)100",
            r'\g<1>80',
            text
        )
        if new != text:
            text = new
            changed = True

    path.write_text(text, encoding='utf-8')
    status = 'patched' if changed else 'no change'
    print(f'  {status}: {fname}')


targets = sorted(SCRIPTS_DIR.glob('thumb_0[2-9]_*.py')) + \
          sorted(SCRIPTS_DIR.glob('thumb_1[0-6]_*.py'))

print(f'対象: {len(targets)} ファイル')
for p in targets:
    patch_file(p)
print('完了')
