"""
サムネイルスクリプト一括パッチ
- サブタイトル行を削除（またはメインタイトルに統合）
- レイアウト位置を調整
"""
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

# --- メインタイトルを統合する対象 ---
# (ファイル名パターン, 新タイトルテキスト, 新フォントサイズ)
MERGE_RULES = {
    'thumb_03_eps_revision.py':   ('EPSリビジョン', 72),
    'thumb_07_pipeline.py':       ('EDINET/TDnet', 65),
    'thumb_08_schema.py':         ('JSONスキーマ', 78),
    'thumb_13_car.py':            ('CARイベント', 80),
    'thumb_14_llm.py':            ('LLM要約', 85),
    'thumb_16_prediction.py':     ('K-NN予測', 85),
}

def patch_file(path: Path):
    text = path.read_text(encoding='utf-8')
    fname = path.name

    # 1) メインタイトル統合（対象ファイルのみ）
    if fname in MERGE_RULES:
        new_text, new_size = MERGE_RULES[fname]
        # メインタイトル行のテキストとフォントサイズを置換
        text = re.sub(
            r"(ax_l\.text\(0\.07,\s*0\.6[0-9],\s*')[^']+(',\s*color=WHITE,\s*\n?\s*fontsize=)\d+",
            lambda m: m.group(1) + new_text + m.group(2) + str(new_size),
            text
        )
        # インライン形式も対応
        text = re.sub(
            r"(ax_l\.text\(0\.07,\s*0\.6[0-9],\s*')[^']+(',\s*color=WHITE,\s*fontsize=)\d+",
            lambda m: m.group(1) + new_text + m.group(2) + str(new_size),
            text
        )

    # 2) サブタイトル行を削除
    #    y が 0.44〜0.52 の範囲にある ax_l.text 行（コメント行も含む）
    # コメント行 "# サブタイトル" を削除
    text = re.sub(r'\n\s*# サブタイトル\n', '\n', text)
    # ax_l.text の行（y=0.44〜0.52）を削除（複数行形式・1行形式）
    # 複数行形式: ax_l.text(0.07, 0.4x または 0.5x, ... \n          fontsize=...)
    text = re.sub(
        r"ax_l\.text\(0\.07,\s*0\.[45][0-9],\s*'[^']*',\s*color=WHITE,\n\s*fontsize=\d+,[^\n]*\)\n",
        '',
        text
    )
    # 1行形式
    text = re.sub(
        r"ax_l\.text\(0\.07,\s*0\.[45][0-9],\s*'[^']*',\s*color=WHITE,\s*fontsize=\d+,[^\n]*\)\n",
        '',
        text
    )

    # 3) セパレータ位置を移動: [0.36, 0.36] → [0.53, 0.53]
    text = text.replace('[0.36, 0.36]', '[0.53, 0.53]')

    # 4) キャッチコピー・英語名の y 位置を移動
    # 0.275 → 0.43（キャッチコピー1行目）
    text = re.sub(r'(ax_l\.text\(0\.07,\s*)0\.275(,)', r'\g<1>0.43\2', text)
    # 0.195 → 0.33（キャッチコピー2行目）
    text = re.sub(r'(ax_l\.text\(0\.07,\s*)0\.195(,)', r'\g<1>0.33\2', text)
    # 0.085 → 0.18（英語フルネーム）
    text = re.sub(r'(ax_l\.text\(0\.07,\s*)0\.085(,)', r'\g<1>0.18\2', text)

    path.write_text(text, encoding='utf-8')
    print(f'  patched: {fname}')


targets = sorted(SCRIPTS_DIR.glob('thumb_0[2-9]_*.py')) + \
          sorted(SCRIPTS_DIR.glob('thumb_1[0-6]_*.py'))

print(f'対象: {len(targets)} ファイル')
for p in targets:
    patch_file(p)
print('完了')
