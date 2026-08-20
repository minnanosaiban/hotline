# -*- coding: utf-8 -*-
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
    if src.startswith("blog/posts/"):
        # 個別記事：共通の blog-post-page に加え、記事専用クラスも付与（一覧と区別するため）
        output = re.sub(r"(<body\b)", r'\1 class="blog-post-page blog-article-page"', output, count=1)
    elif src == "blog/glossary.md":
        # 用語集：記事と同じ読み物スタイルを当てる
        output = re.sub(r"(<body\b)", r'\1 class="blog-post-page blog-article-page"', output, count=1)
    elif src == "blog/index.md":
        output = re.sub(r"(<body\b)", r'\1 class="blog-post-page"', output, count=1)
    elif src.startswith("trial/") and src != "trial/index.md":
        output = re.sub(r"(<body\b)", r'\1 class="trial-doc"', output, count=1)
    elif src.startswith("agm/"):
        output = re.sub(r"(<body\b)", r'\1 class="trial-doc"', output, count=1)
    if src == "agm/index.md":
        output = re.sub(r"</head>", SWIPER_HEAD_TAGS, output, count=1)
        output = re.sub(r"</body>", SWIPER_BODY_TAGS, output, count=1)
    return output
