#!/usr/bin/env python3
"""Build everything: the main pages (tools/build.py) and then the blog, sitemap and redirects (tools/build_blog.py).

    python3 tools/build_all.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
import build_blog  # noqa: E402
import blogcore  # noqa: E402

if __name__ == "__main__":
    build.main()
    try:
        build_blog.main()
    except blogcore.ContentError as e:
        print("BUILD ERROR:", e, file=sys.stderr)
        sys.exit(1)
