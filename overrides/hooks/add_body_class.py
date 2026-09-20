# -*- coding: utf-8 -*-
# 裁判文書系（trial/・agm/・見本帳）のページに body.trial-doc を付け、agm のカルーセル用に Swiper を注入する。
import re

# agm/index.md の質問パネル・カルーセル（.qa-carousel）専用。
# Swiper.js本体はCDN（jsdelivr）。他ページには一切注入しないため、サイト全体の読み込みには影響しない。
# 詳細は docs/css/13-carousel.css・docs/js/qa-carousel.js のコメント参照。
SWIPER_HEAD_TAGS = (
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">\n'
    '<link rel="stylesheet" href="../css/13-carousel.css">\n'
    "</head>"
)
SWIPER_BODY_TAGS = (
    '<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>\n'
    '<script src="../js/qa-carousel.js"></script>\n'
    "</body>"
)

def on_post_page(output, page, **kwargs):
    src = page.file.src_path.replace("\\", "/")
    # 裁判文書系（trial/ 配下すべて＝一覧の trial/index.md も含む）と agm/・見本帳は body.trial-doc
    if src.startswith("trial/") or src.startswith("agm/") or src == "styleguide.md":
        output = re.sub(r"(<body\b)", r'\1 class="trial-doc"', output, count=1)
    if src in ("agm/index.md", "styleguide.md"):
        output = re.sub(r"</head>", SWIPER_HEAD_TAGS, output, count=1)
        output = re.sub(r"</body>", SWIPER_BODY_TAGS, output, count=1)
    return output
