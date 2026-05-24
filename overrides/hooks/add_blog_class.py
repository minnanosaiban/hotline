# -*- coding: utf-8 -*-
import re

def on_post_page(output, page, **kwargs):
    src = page.file.src_path.replace("\\", "/")
    if src.startswith("blog/posts/") or src == "blog/index.md":
        return re.sub(r"(<body\b)", r'\1 class="blog-post-page"', output, count=1)
    return output
