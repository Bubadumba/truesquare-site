"""Shared parsing and rendering for the TrueSquare blog.

Used by tools/build_blog.py (renders content/blog/*.md into public/blog/) and tools/validate_content.py
(checks the same files before a build). Posts are Markdown with YAML frontmatter and exactly five custom blocks:

    :::costtable            YAML: title, updated, note, rows: [{item, low, high, note}]
    :::
    {{photo id="b13" caption="..." alt="..." size="full|half"}}
    :::callout note|warning|tip|owner
    Markdown
    :::
    {{cta}}
    :::faq                  YAML list of {q, a}
    :::

Anything else that looks like HTML or an unknown block is an error, so the design stays with the templates.
"""
import datetime
import html
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
BLOG_DIR = os.path.join(CONTENT, "blog")
PUB = os.path.join(ROOT, "public")

INTENTS = ["cost-guide", "comparison", "how-to", "permit-explainer", "project-story", "seasonal", "faq", "trust"]
CALLOUT_TYPES = {"note": "Note", "warning": "Watch out", "tip": "Tip", "owner": "From our jobs"}
BLOCK_NAMES = {"costtable", "callout", "faq"}
INLINE_NAMES = {"photo", "cta"}

FENCE_RE = re.compile(r"^:::([A-Za-z_-]+)(?:[ \t]+([A-Za-z_-]+))?[ \t]*\n(.*?)^:::[ \t]*$", re.M | re.S)
INLINE_RE = re.compile(r"\{\{\s*([A-Za-z_-]+)((?:\s+[A-Za-z_]+=\"[^\"]*\")*)\s*\}\}")
ATTR_RE = re.compile(r"([A-Za-z_]+)=\"([^\"]*)\"")
HTML_TAG_RE = re.compile(r"</?[A-Za-z!][^>]*>")
PLACEHOLDER = "TSQBLOCK{}END"


class ContentError(Exception):
    pass


# ---------------------------------------------------------------- loading

def load_yaml(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return default
    return data if data is not None else default


def load_config():
    return load_yaml(os.path.join(CONTENT, "config.yaml"), {})


def load_photos():
    import json
    with open(os.path.join(CONTENT, "photos.json"), encoding="utf-8") as f:
        items = json.load(f)
    return {p["id"]: p for p in items}, items


def load_linkmap():
    return load_yaml(os.path.join(CONTENT, "link-map.yaml"), {})


def list_post_files():
    if not os.path.isdir(BLOG_DIR):
        return []
    return sorted(os.path.join(BLOG_DIR, n) for n in os.listdir(BLOG_DIR) if n.endswith(".md"))


def parse_post(path):
    """Return {"slug", "path", "meta", "body"}. Raises ContentError on a malformed file."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---\n"):
        raise ContentError(f"{os.path.basename(path)}: file must start with a '---' frontmatter line")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ContentError(f"{os.path.basename(path)}: frontmatter is not closed with '---'")
    try:
        meta = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as e:
        raise ContentError(f"{os.path.basename(path)}: frontmatter is not valid YAML: {e}")
    body = text[end + 5:]
    slug = os.path.basename(path)[:-3]
    return {"slug": slug, "path": path, "meta": meta, "body": body}


def as_date(value):
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------- schema

def check_meta(meta, linkmap, photos):
    """Return a list of human-readable schema errors for one post's frontmatter."""
    errs = []
    title = meta.get("title")
    if not isinstance(title, str) or not 30 <= len(title.strip()) <= 70:
        errs.append("title must be a string of 30-70 characters")
    desc = meta.get("description")
    if not isinstance(desc, str) or not 80 <= len(desc.strip()) <= 160:
        errs.append("description must be a string of 80-160 characters")
    pub = as_date(meta.get("pubDate"))
    if pub is None:
        errs.append("pubDate must be YYYY-MM-DD")
    if "updatedDate" in meta and meta.get("updatedDate") is not None:
        upd = as_date(meta.get("updatedDate"))
        if upd is None:
            errs.append("updatedDate must be YYYY-MM-DD")
        elif pub and upd < pub:
            errs.append("updatedDate is earlier than pubDate")
    hero = meta.get("heroPhoto")
    if not isinstance(hero, str) or hero not in photos:
        errs.append(f"heroPhoto '{hero}' is not an id in content/photos.json")
    elif photos[hero].get("clientConsent") is not True:
        errs.append(f"heroPhoto '{hero}' has no client consent")
    tags = meta.get("tags")
    if not isinstance(tags, list) or not 1 <= len(tags) <= 6 or not all(isinstance(t, str) and t.strip() for t in tags):
        errs.append("tags must be a list of 1-6 strings")
    hub = meta.get("hub")
    if not isinstance(hub, str) or hub not in linkmap or hub in ("cta_phone", "estimate_url"):
        errs.append(f"hub '{hub}' is not a key of content/link-map.yaml")
    if meta.get("intent") not in INTENTS:
        errs.append(f"intent must be one of {', '.join(INTENTS)}")
    if not isinstance(meta.get("targetQuery"), str) or not meta.get("targetQuery").strip():
        errs.append("targetQuery is required")
    if "city" in meta and meta.get("city") is not None and not isinstance(meta.get("city"), str):
        errs.append("city must be a string when present")
    sources = meta.get("sources", [])
    if sources is None:
        sources = []
    if not isinstance(sources, list):
        errs.append("sources must be a list")
    else:
        for i, s in enumerate(sources):
            if not isinstance(s, dict) or not s.get("title") or not str(s.get("url", "")).startswith("http") or as_date(s.get("accessed")) is None:
                errs.append(f"sources[{i}] needs title, url (http...) and accessed (YYYY-MM-DD)")
    owner = meta.get("ownerFactsUsed", [])
    if owner is not None and not isinstance(owner, list):
        errs.append("ownerFactsUsed must be a list")
    for flag in ("draft", "noindex"):
        if flag in meta and not isinstance(meta.get(flag), bool):
            errs.append(f"{flag} must be true or false")
    return errs


# ---------------------------------------------------------------- blocks

def parse_attrs(raw):
    return dict(ATTR_RE.findall(raw or ""))


def extract_blocks(body):
    """Replace the five custom blocks with placeholders. Returns (text, blocks). blocks[i] = (kind, arg, payload)."""
    blocks = []

    def fence(m):
        kind, arg, content = m.group(1), m.group(2), m.group(3)
        if kind not in BLOCK_NAMES:
            raise ContentError(f"unknown block ':::{kind}' (allowed: costtable, callout, faq)")
        if kind == "callout":
            if arg not in CALLOUT_TYPES:
                raise ContentError(f":::callout needs a type: note, warning, tip or owner (got '{arg}')")
        elif arg:
            raise ContentError(f":::{kind} takes no argument")
        blocks.append((kind, arg, content))
        return "\n\n" + PLACEHOLDER.format(len(blocks) - 1) + "\n\n"

    text = FENCE_RE.sub(fence, body)
    if re.search(r"^:::", text, re.M):
        raise ContentError("a ':::' block is not closed or not at the start of a line")

    def inline(m):
        kind, attrs = m.group(1), parse_attrs(m.group(2))
        if kind not in INLINE_NAMES:
            raise ContentError(f"unknown block '{{{{{kind}}}}}' (allowed: photo, cta)")
        if kind == "photo" and not attrs.get("id"):
            raise ContentError("{{photo}} needs an id")
        if kind == "cta" and attrs:
            raise ContentError("{{cta}} takes no attributes")
        blocks.append((kind, None, attrs))
        return "\n\n" + PLACEHOLDER.format(len(blocks) - 1) + "\n\n"

    text = INLINE_RE.sub(inline, text)
    if "{{" in text or "}}" in text:
        raise ContentError("stray '{{' or '}}' in the body")
    return text, blocks


def find_raw_html(text):
    """Return the first HTML-looking tag in Markdown text (outside custom blocks), or None."""
    m = HTML_TAG_RE.search(text)
    return m.group(0) if m else None


# ---------------------------------------------------------------- rendering

def md(text):
    import markdown
    return markdown.markdown(text, extensions=["tables", "sane_lists"], output_format="html5")


def esc(s):
    return html.escape(str(s), quote=True)


def render_costtable(content):
    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        raise ContentError(f":::costtable YAML error: {e}")
    rows = data.get("rows") or []
    if not isinstance(rows, list) or not rows:
        raise ContentError(":::costtable needs rows")
    for k in ("title", "updated"):
        if not data.get(k):
            raise ContentError(f":::costtable needs '{k}'")
    body = "".join(
        f"<tr><td>{esc(r.get('item', ''))}</td><td>{esc(r.get('low', ''))}</td><td>{esc(r.get('high', ''))}</td><td>{esc(r.get('note', ''))}</td></tr>"
        for r in rows)
    note = f"<p>{esc(data['note'])}</p>" if data.get("note") else ""
    return (f'<figure class="costtable"><table><caption>{esc(data["title"])}</caption>'
            f"<thead><tr><th>Item</th><th>Low</th><th>High</th><th>Note</th></tr></thead><tbody>{body}</tbody></table>"
            f'<figcaption>{note}<p class="updated">Prices updated {esc(data["updated"])}.</p></figcaption></figure>')


def render_photo(attrs, photos):
    pid = attrs.get("id")
    p = photos.get(pid)
    if not p:
        raise ContentError(f"{{{{photo id=\"{pid}\"}}}}: unknown photo id")
    if p.get("clientConsent") is not True:
        raise ContentError(f"{{{{photo id=\"{pid}\"}}}}: no client consent")
    if not os.path.isfile(os.path.join(PUB, p["file"].lstrip("/"))):
        raise ContentError(f"{{{{photo id=\"{pid}\"}}}}: file {p['file']} is missing under public/")
    size = attrs.get("size", "full")
    if size not in ("full", "half"):
        raise ContentError(f"{{{{photo id=\"{pid}\"}}}}: size must be full or half")
    alt = attrs.get("alt") or p.get("altDefault") or p.get("shows") or ""
    cap = attrs.get("caption") or ""
    src_attr = ' data-source="ai"' if p.get("source") == "ai" else ""
    figcap = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
    return (f'<figure class="bphoto {size}"{src_attr}><img src="{esc(p["file"])}" width="{p["width"]}" height="{p["height"]}" '
            f'alt="{esc(alt)}" loading="lazy" decoding="async">{figcap}</figure>')


def render_callout(kind, content):
    label = CALLOUT_TYPES[kind]
    inner = md(content.strip())
    return f'<aside class="callout {kind}"><p class="clabel">{label}</p>{inner}</aside>'


def render_cta(phone_t="+12062222328", phone="+1 206-222-2328"):
    return ('<div class="box bcta"><p class="kicker">Planning a bathroom remodel in Seattle?</p>'
            "<p>Tell us about the room. Serhii will call to arrange a free visit, and you get your price in writing within 5 hours after the visit.</p>"
            '<p class="bcta-actions"><a class="btn" href="#book">Request a free visit <span class="arr">→</span></a> '
            f'<a class="btn outline" href="tel:{phone_t}">Call {phone}</a></p></div>')


def render_faq(content):
    try:
        items = yaml.safe_load(content) or []
    except yaml.YAMLError as e:
        raise ContentError(f":::faq YAML error: {e}")
    if not isinstance(items, list) or not items:
        raise ContentError(":::faq needs a list of {q, a}")
    out = []
    for it in items:
        if not isinstance(it, dict) or not it.get("q") or not it.get("a"):
            raise ContentError(":::faq items need q and a")
        out.append(f"<h3>{esc(it['q'])}</h3>{md(str(it['a']).strip())}")
    return '<section class="bfaq"><h2>Questions</h2>' + "".join(out) + "</section>"


def render_body(body, photos):
    """Markdown + the five blocks -> HTML. Raises ContentError on raw HTML or unknown blocks."""
    text, blocks = extract_blocks(body)
    tag = find_raw_html(text)
    if tag:
        raise ContentError(f"raw HTML is not allowed in articles: {tag}")
    if "![" in text:
        raise ContentError("markdown images are not allowed; use {{photo id=\"...\"}}")
    out = md(text)
    for i, (kind, arg, payload) in enumerate(blocks):
        if kind == "costtable":
            h = render_costtable(payload)
        elif kind == "photo":
            h = render_photo(payload, photos)
        elif kind == "callout":
            h = render_callout(arg, payload)
        elif kind == "cta":
            h = render_cta()
        elif kind == "faq":
            h = render_faq(payload)
        else:
            raise ContentError(f"unknown block {kind}")
        ph = PLACEHOLDER.format(i)
        if f"<p>{ph}</p>" in out:
            out = out.replace(f"<p>{ph}</p>", h, 1)
        elif ph in out:
            out = out.replace(ph, h, 1)
        else:
            raise ContentError(f"internal error: placeholder {ph} lost during rendering")
    if "TSQBLOCK" in out:
        raise ContentError("internal error: a block placeholder was not replaced")
    return out


# ---------------------------------------------------------------- helpers for both tools

def post_image_ids(post):
    """heroPhoto + every {{photo id}} in the body, in order (duplicates kept)."""
    ids = []
    hero = post["meta"].get("heroPhoto")
    if hero:
        ids.append(hero)
    for m in INLINE_RE.finditer(post["body"]):
        if m.group(1) == "photo":
            pid = parse_attrs(m.group(2)).get("id")
            if pid:
                ids.append(pid)
    return ids


def is_published(post):
    m = post["meta"]
    return not m.get("draft", False) and not m.get("noindex", False)


def seattle_iso(d):
    """ISO 8601 datetime at noon Seattle time for a date, with the right -07:00/-08:00 offset."""
    from zoneinfo import ZoneInfo
    dt = datetime.datetime(d.year, d.month, d.day, 12, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    return dt.isoformat()


def human_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"
