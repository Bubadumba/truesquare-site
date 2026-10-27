#!/usr/bin/env python3
"""Render the blog: content/blog/*.md -> public/blog/, plus /how-we-write/, the sitemap and _redirects.

    python3 tools/build_blog.py          (run tools/build.py first, or use tools/build_all.py)

Everything is wrapped in the same page() as the main site, so header, footer, fonts and JSON-LD match.
Drafts and noindex posts are rendered (so a preview shows them) but stay out of the index, RSS and sitemap.
"""
import datetime
import json
import os
import shutil
import sys
from xml.sax.saxutils import escape as xesc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402  (the site builder: page(), book(), constants)
import blogcore as bc  # noqa: E402

BLOG_PUB = os.path.join(bc.PUB, "blog")


def _blog_css():
    """public/css/blog.css, minified like build.py minifies site.css, inlined only on blog pages so the
    main pages stay byte-identical to what tools/build.py alone produces."""
    import re as _re
    c = open(os.path.join(bc.PUB, "css", "blog.css"), encoding="utf-8").read()
    c = _re.sub(r"/\*.*?\*/", "", c, flags=_re.S)
    return _re.sub(r"\s*\n\s*", "", c)


BLOG_CSS_TAG = "<style>" + _blog_css() + "</style>"
PER_PAGE = 10
REVIEWED_BY = "Reviewed by Serhii Tomilov, TrueSquare Remodel LLC, WA L&amp;I # TRUESRL759QK"
HOW_WE_WRITE = (
    "Every guide on this site is written for homeowners in Seattle and nearby cities. Prices come from our own "
    "estimates and written subcontractor quotes, not from national averages. Permit, tax and code facts are checked "
    "against the official city, county and state pages we link to, with the month we checked them. Drafts are prepared "
    "with AI tools from our job notes and sources, then read, corrected and approved by Serhii Tomilov before they are "
    "published. If you find a mistake, email info@truesquareremodel.com."
)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def crumbs_html(trail):
    items = []
    for i, (name, url) in enumerate(trail):
        if i < len(trail) - 1:
            items.append(f'<li><a href="{url}">{bc.esc(name)}</a></li>')
        else:
            items.append(f'<li aria-current="page">{bc.esc(name)}</li>')
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">' + "".join(items) + "</ol></nav>"


def hero_section(trail, kicker, h1, sub):
    return f"""<section class="phero on-ink"><div class="wrap phgrid" style="grid-template-columns:1fr">
  <div class="phtext">{crumbs_html(trail)}
  <p class="kicker">{kicker}</p><h1>{bc.esc(h1)}</h1><p class="sub">{sub}</p></div>
</div></section>"""


def card(post, photos):
    m = post["meta"]
    hero = photos[m["heroPhoto"]]
    pub = bc.as_date(m["pubDate"])
    return (f'<a class="rcard" href="/blog/{post["slug"]}/"><img src="{bc.esc(hero["file"])}" alt="{bc.esc(hero.get("altDefault") or hero.get("shows", ""))}" '
            f'loading="lazy" width="{hero["width"]}" height="{hero["height"]}"><div><h3>{bc.esc(m["title"])}</h3>'
            f'<p>{bc.esc(m["description"])}</p><span class="go">{bc.human_date(pub)} · Read →</span></div></a>')


def related_posts(post, published, photos):
    tags = set(post["meta"].get("tags") or [])
    scored = []
    for other in published:
        if other["slug"] == post["slug"]:
            continue
        shared = len(tags & set(other["meta"].get("tags") or []))
        if shared:
            scored.append((shared, bc.as_date(other["meta"]["pubDate"]), other))
    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    picks = [t[2] for t in scored[:3]]
    if not picks:
        return ""
    cards = "".join(card(p, photos) for p in picks)
    return f"""<section><div class="wrap">
  <div class="head"><p class="kicker">Related</p><h2>More guides on this topic.</h2></div>
  <div class="rel{' three' if len(picks) == 3 else ''}">{cards}</div>
</div></section>"""


def render_post(post, published, photos):
    m = post["meta"]
    slug = post["slug"]
    path = f"/blog/{slug}/"
    url = build.SITE + path
    hero = photos[m["heroPhoto"]]
    pub = bc.as_date(m["pubDate"])
    upd = bc.as_date(m.get("updatedDate")) if m.get("updatedDate") else None
    body_html = bc.render_body(post["body"], photos)
    meta_line = f"Published {bc.human_date(pub)}" + (f" · Updated {bc.human_date(upd)}" if upd else "")
    trail = [("Home", "/"), ("Blog", "/blog/"), (m["title"], path)]
    hero_alt = hero.get("altDefault") or hero.get("shows", "")
    src_attr = ' data-source="ai"' if hero.get("source") == "ai" else ""
    body = hero_section(trail, "Blog", m["title"], meta_line) + f"""
<section><div class="wrap">
<article class="prose blogpost">
<figure class="bhero"{src_attr}><img src="{bc.esc(hero["file"])}" width="{hero["width"]}" height="{hero["height"]}" alt="{bc.esc(hero_alt)}" fetchpriority="high" decoding="async"></figure>
{body_html}
<div class="box reviewed"><p><b>{REVIEWED_BY}</b></p><p><a href="/about">About Serhii</a> · <a href="/how-we-write/">How we write these guides</a></p></div>
</article>
</div></section>
{related_posts(post, published, photos)}
{build.book()}"""
    noindex = bool(m.get("noindex") or m.get("draft"))
    head_extra = (BLOG_CSS_TAG + '\n' +
                  f'<meta property="article:published_time" content="{bc.seattle_iso(pub)}">\n'
                  f'<meta property="article:modified_time" content="{bc.seattle_iso(upd or pub)}">\n'
                  '<link rel="alternate" type="application/rss+xml" title="TrueSquare Remodel blog" href="/blog/rss.xml">')
    ld = {"@type": "BlogPosting", "@id": url + "#article", "headline": m["title"], "description": m["description"],
          "datePublished": bc.seattle_iso(pub), "dateModified": bc.seattle_iso(upd or pub),
          "author": {"@type": "Person", "@id": build.SITE + "/about#person", "name": "Serhii Tomilov", "url": build.SITE + "/about"},
          "publisher": {"@id": build.BIZ_ID}, "image": [build.SITE + hero["file"]],
          "mainEntityOfPage": {"@id": url + "#webpage"}, "inLanguage": "en-US"}
    return build.page(path, m["title"], m["description"], body, ld_extra=[ld], crumbs=trail, page_id="blog",
                      robots="noindex,nofollow" if noindex else "index,follow", og_image=hero["file"],
                      og_type="article", head_extra=head_extra, body_class="blog")


def render_index(published, photos, page_no, total_pages):
    path = "/blog/" if page_no == 1 else f"/blog/page/{page_no}/"
    start = (page_no - 1) * PER_PAGE
    items = published[start:start + PER_PAGE]
    cards = "".join(card(p, photos) for p in items)
    nav = []
    if page_no > 1:
        nav.append(f'<a class="btn outline" href="{"/blog/" if page_no == 2 else f"/blog/page/{page_no - 1}/"}">← Newer</a>')
    if page_no < total_pages:
        nav.append(f'<a class="btn outline" href="/blog/page/{page_no + 1}/">Older →</a>')
    pager = f'<p class="pager">{" ".join(nav)}</p>' if nav else ""
    empty = '<p class="lead">The first guides are on their way.</p>' if not items else ""
    trail = [("Home", "/"), ("Blog", "/blog/")] if page_no == 1 else [("Home", "/"), ("Blog", "/blog/"), (f"Page {page_no}", path)]
    body = hero_section(trail, "Blog", "Bathroom remodeling guides for Seattle homeowners.",
                        "Permits, costs, timelines and what we find behind old tile. Written from our jobs and checked against the official sources.") + f"""
<section><div class="wrap">
  {empty}<div class="rel bindex">{cards}</div>
  {pager}
</div></section>
{build.book()}"""
    head_extra = BLOG_CSS_TAG + '\n<link rel="alternate" type="application/rss+xml" title="TrueSquare Remodel blog" href="/blog/rss.xml">'
    if page_no > 1:
        head_extra += f'\n<link rel="prev" href="{build.SITE}{"/blog/" if page_no == 2 else f"/blog/page/{page_no - 1}/"}">'
    if page_no < total_pages:
        head_extra += f'\n<link rel="next" href="{build.SITE}/blog/page/{page_no + 1}/">'
    title = "Bathroom Remodeling Guides for Seattle | TrueSquare Remodel" if page_no == 1 else f"Blog, page {page_no} | TrueSquare Remodel"
    desc = "Guides on bathroom remodeling in Seattle: permits, costs, timelines and what we find behind old tile. Written from our jobs, checked against official sources."
    return path, build.page(path, title, desc, body, crumbs=trail, page_id="blog", head_extra=head_extra, body_class="blog",
                            robots="index,follow" if page_no == 1 else "noindex,follow")


def render_rss(published, photos):
    items = []
    for p in published[:20]:
        m = p["meta"]
        pub = bc.as_date(m["pubDate"])
        dt = datetime.datetime(pub.year, pub.month, pub.day, 12, 0)
        rfc = dt.strftime("%a, %d %b %Y %H:%M:%S") + " -0700"
        link = f"{build.SITE}/blog/{p['slug']}/"
        items.append(f"<item><title>{xesc(m['title'])}</title><link>{link}</link><guid isPermaLink=\"true\">{link}</guid>"
                     f"<description>{xesc(m['description'])}</description><pubDate>{rfc}</pubDate></item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f"<title>TrueSquare Remodel blog</title><link>{build.SITE}/blog/</link>"
            "<description>Bathroom remodeling guides for Seattle homeowners.</description><language>en-us</language>"
            + "".join(items) + "</channel></rss>\n")


def render_how_we_write():
    path = "/how-we-write/"
    trail = [("Home", "/"), ("How we write these guides", path)]
    body = hero_section(trail, "About the blog", "How we write these guides.", "What goes into every article before it is published.") + f"""
<section><div class="wrap legalbody">
<p>{HOW_WE_WRITE}</p>
<p>Questions about a specific guide? <a href="/#book">Request a free visit</a> or call <a href="tel:{build.PHONE_T}">{build.PHONE}</a>.</p>
</div></section>"""
    return path, build.page(path, "How We Write These Guides | TrueSquare Remodel",
                            "How TrueSquare Remodel writes its bathroom remodeling guides: our own estimates and quotes, official permit and tax pages, and the owner's review before publishing.",
                            body, crumbs=trail, page_id="how-we-write", head_extra=BLOG_CSS_TAG, body_class="blog")


def render_sitemap(published):
    try:
        with open(build.LASTMOD_FILE, encoding="utf-8") as f:
            lastmod = json.load(f)
    except (OSError, ValueError):
        lastmod = {}
    today = datetime.date.today().isoformat()
    rows = []
    for u in build.SITEMAP_URLS:
        rows.append((u, (lastmod.get(u) or {}).get("lastmod", today)))
    post_dates = []
    for p in published:
        m = p["meta"]
        d = bc.as_date(m.get("updatedDate")) if m.get("updatedDate") else bc.as_date(m["pubDate"])
        post_dates.append(d.isoformat())
    if published:
        rows.append(("/blog/", max(post_dates)))
    for p, d in zip(published, post_dates):
        rows.append((f"/blog/{p['slug']}/", d))
    rows.append(("/how-we-write/", (lastmod.get("/how-we-write/") or {}).get("lastmod", today)))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{build.SITE}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in rows]
    sm.append("</urlset>")
    return "\n".join(sm) + "\n"


def render_redirects():
    entries = bc.load_yaml(os.path.join(bc.CONTENT, "redirects.yaml"), []) or []
    lines = []
    for e in entries:
        if not isinstance(e, dict) or not e.get("from") or not e.get("to"):
            raise bc.ContentError("redirects.yaml entries need from and to")
        lines.append(f"{e['from']} {e['to']} {int(e.get('status', 301))}")
    return ("\n".join(lines) + "\n") if lines else ""


def remember_how_we_write(html_text):
    """Keep /how-we-write/ honest in the sitemap: record its content hash in tools/lastmod.json like build.py does."""
    try:
        with open(build.LASTMOD_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    h = build.content_hash(html_text)
    if (data.get("/how-we-write/") or {}).get("sha256") != h:
        data["/how-we-write/"] = {"sha256": h, "lastmod": datetime.date.today().isoformat()}
        with open(build.LASTMOD_FILE, "w", encoding="utf-8") as f:
            json.dump(dict(sorted(data.items())), f, indent=2)
            f.write("\n")


def main():
    cfg = bc.load_config()
    photos, _ = bc.load_photos()
    linkmap = bc.load_linkmap()
    posts = []
    for path in bc.list_post_files():
        post = bc.parse_post(path)
        errs = bc.check_meta(post["meta"], linkmap, photos)
        if errs:
            raise bc.ContentError(f"{os.path.basename(path)}: " + "; ".join(errs))
        posts.append(post)
    posts.sort(key=lambda p: (bc.as_date(p["meta"]["pubDate"]), p["slug"]), reverse=True)
    published = [p for p in posts if bc.is_published(p)]

    # remove generated folders for posts that no longer exist
    if os.path.isdir(BLOG_PUB):
        keep = {p["slug"] for p in posts} | {"page"}
        for name in os.listdir(BLOG_PUB):
            full = os.path.join(BLOG_PUB, name)
            if os.path.isdir(full) and name not in keep:
                shutil.rmtree(full)
        page_dir = os.path.join(BLOG_PUB, "page")
        if os.path.isdir(page_dir):
            shutil.rmtree(page_dir)

    for p in posts:
        write(os.path.join(BLOG_PUB, p["slug"], "index.html"), render_post(p, published, photos))
    total_pages = max(1, -(-len(published) // PER_PAGE))
    for n in range(1, total_pages + 1):
        path, html_text = render_index(published, photos, n, total_pages)
        write(os.path.join(bc.PUB, path.strip("/"), "index.html"), html_text)
    write(os.path.join(BLOG_PUB, "rss.xml"), render_rss(published, photos))
    hw_path, hw_html = render_how_we_write()
    write(os.path.join(bc.PUB, "how-we-write", "index.html"), hw_html)
    remember_how_we_write(hw_html)
    write(os.path.join(bc.PUB, "sitemap.xml"), render_sitemap(published))
    write(os.path.join(bc.PUB, "_redirects"), render_redirects())
    print(f"blog: {len(posts)} posts ({len(published)} published, {len(posts) - len(published)} draft/noindex), "
          f"{total_pages} index page(s), rss, how-we-write, sitemap ({len(build.SITEMAP_URLS) + 1 + len(published) + (1 if published else 0)} urls), _redirects")


if __name__ == "__main__":
    try:
        main()
    except bc.ContentError as e:
        print("BUILD ERROR:", e, file=sys.stderr)
        sys.exit(1)
