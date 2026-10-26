#!/usr/bin/env python3
"""Print the absolute URLs of blog posts whose generated HTML changed between two git revisions.

    python3 tools/changed_posts.py <before-sha> <after-sha>
"""
import subprocess
import sys

SITE = "https://truesquareremodel.com"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    before, after = sys.argv[1], sys.argv[2]
    out = subprocess.run(["git", "diff", "--name-only", before, after, "--", "public/blog"],
                         capture_output=True, text=True, check=True).stdout.split()
    urls = []
    for path in out:
        parts = path.split("/")
        if len(parts) == 4 and parts[3] == "index.html" and parts[2] != "page":
            urls.append(f"{SITE}/blog/{parts[2]}/")
        elif path == "public/blog/index.html":
            urls.append(f"{SITE}/blog/")
    for u in dict.fromkeys(urls):
        print(u)


if __name__ == "__main__":
    main()
