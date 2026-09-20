# -*- coding: utf-8 -*-
"""
ENEOS TV「第16回定時株主総会」動画から、質問パネル14枚を静止画として抽出する。

agm/index.md にある .eneos-timestamp のタイムスタンプと同じ秒数を使い、
docs/agm/img/q01.png 〜 q14.png として書き出す（.qa-carousel が参照するファイル名と一致）。

事前準備（初回のみ）:
    pip install yt-dlp imageio-ffmpeg

実行:
    python scripts/extract_agm_panels.py

処理の流れ:
    1. 動画を一度だけダウンロード（音声なし・720p以下。パネルは静止画なので画質は十分）
    2. ffmpeg でタイムスタンプごとに1フレームだけ抜き出す（YouTubeのUIは写り込まない）
    3. ダウンロードした動画ファイルは残す（-y キャッシュ的に再実行を速くするため）。
       不要なら手動で削除して構わない。
"""
import os
import subprocess

import imageio_ffmpeg
import yt_dlp

VIDEO_URL = "https://www.youtube.com/watch?v=0kWavfBMS30"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(REPO_ROOT, "docs", "agm", "img")
VIDEO_FILE = os.path.join(SCRIPT_DIR, "_agm_video_cache.mp4")

# (質問番号, 秒数, 見出し／ログ表示用)
# 秒数は agm/index.md の .eneos-timestamp（&t=...s）と同じ
TIMESTAMPS = [
    (1, 2455, "コンプライアンス・安全について"),
    (2, 2580, "内部通報制度に関する、個別案件への対応について"),
    (3, 2672, "人材配置やスキルアップ等の人材活用について"),
    (4, 2816, "個別案件を踏まえ、内部通報制度をどのように運用しているか"),
    (5, 2962, "気候変動対策の方針について"),
    (6, 3124, "スポーツチーム（野球・バスケットボール）の保有方針について"),
    (7, 3229, "配当性向の維持を前提に、増配できないか"),
    (8, 3364, "潤滑油を用いた液浸冷却製品について"),
    (9, 3498, "グループ会社の組織・体制の再構築について"),
    (10, 3618, "カーボンニュートラル基本計画について"),
    (11, 3718, "Papua LNGプロジェクトにおける、人権ポリシー遵守状況について"),
    (12, 3870, "ENEOSウイングにおけるカルテル事案について"),
    (13, 4045, "中東情勢を受けた、原油調達への影響について"),
    (14, 4207, "株主総会のLIVE動画配信に関連する、株主への対応について"),
]


def download_video():
    if os.path.exists(VIDEO_FILE):
        print(f"[skip] 既に取得済み: {VIDEO_FILE}")
        return
    ydl_opts = {
        # 音声不要（フレーム抽出のみ）。720p以下で十分（パネルは静止画のテキストスライド）
        "format": "bestvideo[height<=720][ext=mp4]/bestvideo[height<=720]",
        "outtmpl": VIDEO_FILE,
    }
    print("[download] 動画を取得中…（数百MB程度かかる場合があります）")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([VIDEO_URL])


def extract_frames():
    os.makedirs(OUT_DIR, exist_ok=True)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    for num, sec, title in TIMESTAMPS:
        out_path = os.path.join(OUT_DIR, f"q{num:02d}.png")
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-ss", str(sec),
                "-i", VIDEO_FILE,
                "-frames:v", "1",
                "-q:v", "2",
                out_path,
            ],
            check=True,
            capture_output=True,
        )
        print(f"[ok] q{num:02d}.png ← {sec}s（{title}）")


if __name__ == "__main__":
    download_video()
    extract_frames()
    print(f"\n完了：{OUT_DIR} に14枚を書き出しました。")
