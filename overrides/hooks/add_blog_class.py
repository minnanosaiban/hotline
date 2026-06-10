# -*- coding: utf-8 -*-
import re

def on_post_page(output, page, **kwargs):
    src = page.file.src_path.replace("\\", "/")
    if src.startswith("blog/posts/"):
        # 個別記事：共通の blog-post-page に加え、記事専用クラスも付与（一覧と区別するため）
        return re.sub(r"(<body\b)", r'\1 class="blog-post-page blog-article-page"', output, count=1)
    if src == "blog/index.md":
        return re.sub(r"(<body\b)", r'\1 class="blog-post-page"', output, count=1)
    if src.startswith("trial/") and src not in ("trial/index.md", "trial/eneos_claims.md"):
        return re.sub(r"(<body\b)", r'\1 class="trial-doc"', output, count=1)
    return output
