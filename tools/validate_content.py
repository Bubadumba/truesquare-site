#!/usr/bin/env python3
"""Validate every article in content/blog before a build.

    python3 tools/validate_content.py          exit 1 on any error; warnings are printed but do not fail

Checks the frontmatter schema, the five allowed blocks, raw HTML, links, dashes, banned terms, structure,
phone formats, numbers without sources, duplicate titles, and the image rules (counts, reuse, unique hero,
generated-image placement). The same rules are described for the agent in .claude/skills/seo-article/SKILL.md.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blogcore as bc  # noqa: E402

BANNED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banned-terms.txt")
LINK_RE = re.compile(r"\]\((/[^)\s]*)\)")
H2_RE = re.compile(r"^## +(.+)$", re.M)
H1_RE = re.compile(r"^# +", re.M)
PHONE_FULL = "+1 206-222-2328"
PHONE_LIKE_RE = re.compile(r"(?<![\d+])(\(?\d{3}\)?[ .-]?\d{3}[ .-]\d{4}|\b\d{3}-\d{4}\b)")
AI_FORBIDDEN_WORDS = ["our project", "our job", "our work", "we built", "we installed", "our crew built", "before", "after"]


def load_banned():
    pats = []
    with open(BANNED_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            pats.append((line, re.compile(line, re.I | re.M)))
    return pats


def completed_cities():
    """Cities listed under 'Cities with COMPLETED projects' in business-facts.md (none while the line is ⬜ FILL)."""
    path = os.path.join(bc.CONTENT, "business-facts.md")
    cities = []
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return cities
    m = re.search(r"Cities with COMPLETED projects[^\n]*\n((?:  .*\n)*)", text)
    block = (m.group(0) if m else "")
    if "⬜ FILL" in block.split("\n")[0]:
        return cities
    for line in block.split("\n")[1:]:
        mm = re.match(r"\s*-\s*([A-Z][A-Za-z .]+?),\s*WA", line)
        if mm:
            cities.append(mm.group(1).strip())
    return cities


def resolve_link(link, slugs):
    path = link.split("#", 1)[0].split("?", 1)[0]
    if path in ("", "/"):
        return True
    if path.startswith("/blog/"):
        slug = path[len("/blog/"):].strip("/")
        if slug == "" or slug in slugs or slug.startswith("page/") or slug == "rss.xml":
            return True
    rel = path.lstrip("/")
    candidates = [os.path.join(bc.PUB, rel), os.path.join(bc.PUB, rel + ".html"), os.path.join(bc.PUB, rel, "index.html")]
    return any(os.path.isfile(c) for c in candidates)


def sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def strip_blocks(body):
    text, _ = bc.extract_blocks(body)
    return text


def paragraph_around(body, needle):
    """Markdown paragraphs immediately before and after the line containing needle."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", body)]
    for i, p in enumerate(paras):
        if needle in p:
            around = [paras[i]]
            if i > 0:
                around.append(paras[i - 1])
            if i + 1 < len(paras):
                around.append(paras[i + 1])
            return " ".join(around)
    return ""


def main():
    errors, warnings = [], []
    cfg = bc.load_config()
    img_cfg = cfg.get("images", {})
    max_per = int(img_cfg.get("max_per_article", 6))
    default_per = int(img_cfg.get("default_per_article", 2))
    max_uses = int(img_cfg.get("max_uses_per_photo", 2))
    photos, _ = bc.load_photos()
    linkmap = bc.load_linkmap()
    banned = load_banned()
    cities_done = completed_cities()
    today = datetime.date.today()

    posts = []
    for path in bc.list_post_files():
        try:
            posts.append(bc.parse_post(path))
        except bc.ContentError as e:
            errors.append(str(e))
    slugs = {p["slug"] for p in posts}

    hero_owner = {}
    uses = {}
    titles, descs = {}, {}

    for post in posts:
        name = os.path.basename(post["path"])
        m, body = post["meta"], post["body"]
        E = lambda msg: errors.append(f"{name}: {msg}")
        W = lambda msg: warnings.append(f"{name}: {msg}")

        for e in bc.check_meta(m, linkmap, photos):
            E(e)
        pub = bc.as_date(m.get("pubDate"))
        if pub and pub > today:
            E("pubDate is in the future")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", post["slug"]):
            E("file name must be a lowercase hyphenated slug")

        # blocks, raw HTML, images
        try:
            text = strip_blocks(body)
            tag = bc.find_raw_html(text)
            if tag:
                E(f"raw HTML is not allowed: {tag}")
            if "![" in text:
                E("markdown images are not allowed; use {{photo id=\"...\"}}")
            if re.search(r"^(import|export) ", text, re.M):
                E("lines starting with import/export are not allowed")
            bc.render_body(body, photos)
        except bc.ContentError as e:
            E(str(e))
            text = body

        # dashes and banned terms
        if "—" in body or "–" in body or "--" in body:
            E("em dash, en dash or '--' found: use a period, comma, colon or parentheses")
        for raw, pat in banned:
            hit = pat.search(body)
            if hit:
                E(f"banned term '{hit.group(0).strip()}' (rule: {raw})")

        # structure
        if H1_RE.search(text):
            E("no H1 in the body; the layout prints the title")
        h2s = H2_RE.findall(text)
        if len(h2s) < 3:
            E(f"fewer than 3 H2 headings ({len(h2s)})")
        for h in h2s:
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", h) if len(w) > 3]
            if len(words) >= 3 and all(w[0].isupper() for w in words):
                W(f"H2 looks like Title Case: '{h}'")
        words_total = len(re.findall(r"\b\w+\b", text))
        min_words = 400 if m.get("intent") in ("project-story", "faq") else 700
        if words_total < min_words:
            if m.get("draft") is True:
                W(f"draft with only {words_total} words (minimum for a published {m.get('intent')} post is {min_words})")
            else:
                E(f"only {words_total} words; minimum for intent {m.get('intent')} is {min_words}")
        if "Reviewed by" in body:
            E("'Reviewed by' must not appear in the body; the layout prints it")
        if re.search(r"\$\s?\d|\d\s?%", body) and not (m.get("sources") or m.get("ownerFactsUsed")):
            E("the body has a $ amount or a % but sources and ownerFactsUsed are both empty")

        # links
        for link in LINK_RE.findall(text):
            if not resolve_link(link, slugs):
                E(f"internal link does not resolve: {link}")

        # phones: every phone-like string must be written as +1 XXX-XXX-XXXX
        for mm in PHONE_LIKE_RE.finditer(body):
            s = mm.group(0)
            prefix = body[max(0, mm.start() - 3):mm.start()]
            if prefix.endswith("+1 ") and re.fullmatch(r"\d{3}-\d{3}-\d{4}", s):
                continue
            E(f"phone number not in full +1 XXX-XXX-XXXX form: '{s.strip()}'")
            break

        # duplicates
        t, d = (m.get("title") or "").strip().lower(), (m.get("description") or "").strip().lower()
        if t in titles:
            E(f"title duplicates {titles[t]}")
        titles.setdefault(t, name)
        if d in descs:
            E(f"description duplicates {descs[d]}")
        descs.setdefault(d, name)

        # images
        ids = bc.post_image_ids(post)
        if len(ids) > max_per:
            E(f"{len(ids)} images; images.max_per_article is {max_per}")
        elif len(ids) > default_per:
            W(f"{len(ids)} images (default {default_per}); every extra image needs a one-line reason in the PR")
        hero = m.get("heroPhoto")
        if hero in photos:
            if hero in hero_owner:
                E(f"heroPhoto '{hero}' is already the hero of {hero_owner[hero]}")
            hero_owner.setdefault(hero, name)
        for pid in set(ids):
            p = photos.get(pid)
            if not p:
                continue
            uses.setdefault(pid, set()).add(post["slug"])
            if post["slug"] not in (p.get("usedIn") or []):
                E(f"photos.json: '{pid}' usedIn is missing '{post['slug']}'")
            if p.get("source") == "ai":
                if not str(p.get("file", "")).startswith("/img/blog/ai/"):
                    E(f"generated image '{pid}' must live under /img/blog/ai/")
                if m.get("intent") == "project-story":
                    E(f"generated image '{pid}' used in a project-story post")
                if p.get("pairWith"):
                    E(f"generated image '{pid}' is part of a before/after pair")
                context = (p.get("altDefault") or "") + " " + paragraph_around(body, f'id="{pid}"')
                for mm in bc.INLINE_RE.finditer(body):
                    attrs = bc.parse_attrs(mm.group(2))
                    if mm.group(1) == "photo" and attrs.get("id") == pid:
                        context += " " + attrs.get("caption", "") + " " + attrs.get("alt", "")
                if pid == hero:
                    context += " " + (text[:600])
                low = context.lower()
                for w in AI_FORBIDDEN_WORDS:
                    if re.search(r"\b" + re.escape(w) + r"\b", low):
                        E(f"generated image '{pid}': the words '{w}' appear in its caption, alt or surrounding text")
                        break
                for c in cities_done:
                    if c.lower() in low:
                        E(f"generated image '{pid}': city with completed projects '{c}' appears next to it")
                        break

        # readability warnings (the critic fails on the same patterns)
        paras = [p for p in re.split(r"\n\s*\n", text) if p.strip() and not p.lstrip().startswith(("#", "-", "*", "|", "1.", "TSQBLOCK"))]
        lists = len(re.findall(r"^\s*[-*] ", text, re.M))
        if words_total and lists / max(words_total, 1) * 1000 > 20:
            W("more than two bulleted lists per 1,000 words (approximate)")
        for p in paras:
            ss = sentences(p)
            if len(ss) > 6:
                W(f"paragraph with {len(ss)} sentences: '{ss[0][:50]}...'")
            starts = [s.split()[0].lower() for s in ss if s.split()]
            for i in range(len(starts) - 2):
                if starts[i] == starts[i + 1] == starts[i + 2]:
                    W(f"three sentences in a row start with '{starts[i]}'")
                    break
            lens = [len(s.split()) for s in ss]
            for i in range(len(lens) - 2):
                if max(lens[i:i + 3]) - min(lens[i:i + 3]) <= 3 and min(lens[i:i + 3]) >= 8:
                    W(f"three consecutive sentences of similar length ({lens[i:i + 3]} words): vary the rhythm")
                    break

    for pid, slugset in uses.items():
        p = photos.get(pid, {})
        if p.get("source") == "photo" and len(slugset) > max_uses:
            errors.append(f"photos.json: '{pid}' is used in {len(slugset)} posts; images.max_uses_per_photo is {max_uses}")

    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"validate: {len(posts)} post(s), {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
