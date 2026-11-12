#!/usr/bin/env python3
"""Check in Google Search Console whether the recent blog posts are indexed (URL Inspection API, read only).

    python3 tools/gsc_index_check.py              check posts from the last 30 days, print a table
    python3 tools/gsc_index_check.py --dry-run    list the URLs that would be checked, call nothing

Needs the secret GSC_SERVICE_ACCOUNT_JSON (the service account key) and, optionally, GSC_SITE (default
"sc-domain:truesquareremodel.com"; use the URL-prefix form "https://truesquareremodel.com/" if that is how the
property was added). The service account's e-mail must be added as a user of the property in Search Console.
Without the secret the script prints a notice and exits 0. A post older than 3 days that is not indexed makes
the script write the list to the file given by --report and exit 3, so the workflow can open an issue.
Google offers no API to REQUEST indexing of a normal page; this only reads the status.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"


def recent_posts(days):
    xml = open(os.path.join(ROOT, "public", "sitemap.xml"), encoding="utf-8").read()
    today = dt.date.today()
    out = []
    for loc, last in re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", xml):
        if not re.search(r"/blog/[^/]+/$", loc):
            continue
        age = (today - dt.date.fromisoformat(last)).days
        if age <= days:
            out.append((loc, last, age))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--grace", type=int, default=3, help="days before a non-indexed post is reported")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default="", help="write the list of problems to this file")
    a = ap.parse_args()

    posts = recent_posts(a.days)
    if a.dry_run or not posts:
        for p in posts:
            print(p[0], p[1])
        print(f"{len(posts)} post(s) in the last {a.days} days")
        return 0
    key = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
    if not key:
        print("GSC_SERVICE_ACCOUNT_JSON is not set: nothing checked (set it once, see the PR that added this script).")
        return 0

    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    creds = service_account.Credentials.from_service_account_info(json.loads(key), scopes=[SCOPE])
    session = AuthorizedSession(creds)
    site = os.environ.get("GSC_SITE", "").strip() or "sc-domain:truesquareremodel.com"

    problems = []
    for url, last, age in posts:
        r = session.post(ENDPOINT, json={"inspectionUrl": url, "siteUrl": site, "languageCode": "en-US"}, timeout=60)
        if r.status_code != 200:
            print(f"{url}  API error {r.status_code}: {r.text[:200]}")
            problems.append(f"{url}: API error {r.status_code} (check the service account access and GSC_SITE)")
            continue
        res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
        verdict, state = res.get("verdict", "?"), res.get("coverageState", "?")
        print(f"{url}  age {age}d  {verdict}  {state}")
        if verdict != "PASS" and age >= a.grace:
            problems.append(f"{url}: {state} (age {age} days)")
    if problems:
        if a.report:
            with open(a.report, "w", encoding="utf-8") as f:
                f.write("\n".join(f"- {p}" for p in problems) + "\n")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
