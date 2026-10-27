#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, Seznam, Naver and others; Google does not use it) about new or changed URLs.

    python3 tools/indexnow.py https://truesquareremodel.com/blog/<slug>/ [more urls]
    python3 tools/indexnow.py --dry-run <urls>     print the payload, send nothing

The key comes from content/config.yaml (indexnow_key) and the key file lives at public/<key>.txt, which is public
by design. Before pinging, each URL is polled with GET until it answers 200 (every 15 s, up to 5 minutes), because
Cloudflare Pages deploys main a minute or two after the push and IndexNow should not see a 404.
Exit code is 0 only when IndexNow answers 200 or 202.
"""
import argparse
import json
import sys
import time
from urllib.parse import urlparse

import requests
import yaml
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/indexnow"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--dry-run", action="store_true", help="print the payload and exit without sending")
    ap.add_argument("--no-wait", action="store_true", help="skip polling the URLs for HTTP 200")
    args = ap.parse_args()
    with open(os.path.join(ROOT, "content", "config.yaml"), encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    key = str(cfg.get("indexnow_key", "")).strip()
    if not key:
        print("ERROR: indexnow_key is missing in content/config.yaml", file=sys.stderr)
        sys.exit(1)
    host = urlparse(args.urls[0]).hostname
    payload = {"host": host, "key": key, "keyLocation": f"https://{host}/{key}.txt", "urlList": args.urls}
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return
    if not args.no_wait:
        deadline = time.time() + 300
        pending = list(args.urls)
        while pending and time.time() < deadline:
            still = []
            for u in pending:
                try:
                    code = requests.get(u, timeout=20).status_code
                except requests.RequestException:
                    code = None
                if code != 200:
                    still.append(u)
            pending = still
            if pending:
                print(f"waiting for {len(pending)} url(s) to go live ...")
                time.sleep(15)
        if pending:
            print("WARNING: not live after 5 minutes, pinging anyway:", ", ".join(pending))
    r = requests.post(ENDPOINT, json=payload, headers={"Content-Type": "application/json; charset=utf-8"}, timeout=30)
    print("IndexNow:", r.status_code, r.text[:200])
    sys.exit(0 if r.status_code in (200, 202) else 1)


if __name__ == "__main__":
    main()
