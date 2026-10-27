#!/usr/bin/env python3
"""TrueSquare site builder.

Edit the content below (or tools/content/*.html), then run:
    python3 tools/build.py
It rewrites the pages in public/. Commit + push to GitHub: Cloudflare Pages deploys public/ automatically.
Shared look lives in public/css/site.css, shared behavior + settings in public/js/site.js.
"""
import json, html, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
CONTENT = os.path.join(ROOT, "tools", "content")
SITE = "https://truesquareremodel.com"
PHONE_T = "+12062222328"
PHONE = "(206) 222-2328"
LNI = "TRUESRL759QK"
LNI_URL = "https://secure.lni.wa.gov/verify/Detail.aspx?UBI=606001506&amp;LIC=TRUESRL759QK&amp;SAW="
GOOGLE = "https://www.google.com/maps?cid=7556474326958598816"
THUMBTACK = "https://www.thumbtack.com/wa/seattle/bathroom-remodeling/truesquare-remodel-llc/service/562919809761304593"
CITIES = ["Seattle", "Bellevue", "Kirkland", "Redmond", "Sammamish", "Issaquah", "Mercer Island",
          "Renton", "Bothell", "Woodinville", "Newcastle", "Shoreline"]
BIZ_ID = SITE + "/#business"
ASSET_V = "9"
def _site_css():
    # speed pass 26.10: site.css is inlined into every page (no render-blocking request), same rules
    import re as _re
    c = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "css", "site.css"), encoding="utf-8").read()
    c = _re.sub(r"/\*.*?\*/", "", c, flags=_re.S)
    return _re.sub(r"\s*\n\s*", "", c)
SITE_CSS = _site_css()  # bump to bust browser cache of css/js
TRUST = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "partials", "trust.html"), encoding="utf-8").read().strip()  # rating badge + secure shield under every form

def read(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as f:
        return f.read()

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- shared parts
NAV_SERVICES = [
    ("/bathroom-remodeling", "Full Bathroom Remodeling", "Everything out, new tile, fixtures, vanity"),
    ("/tub-to-walk-in-shower", "Tub to Walk-In Shower", "Old tub out, tiled walk-in shower in"),
    ("/shower-remodeling", "Shower Remodeling", "Rebuild your existing shower"),
    ("/kitchen-renovations", "Kitchen Remodeling", "Cabinets, counters, backsplash"),
    ("/tile-flooring", "Tile Installation", "Floors, showers, backsplashes"),
]
NAV_MAIN = [("/portfolio", "Projects"), ("/about", "About"), ("/reviews", "Reviews"), ("/#faq", "FAQ")]

SVG_DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F69A72"/><stop offset=".5" stop-color="#F47A61"/><stop offset="1" stop-color="#EC6463"/></linearGradient>
<symbol id="star" viewBox="0 0 24 24"><path d="M12 2l3 6.9 7.5.6-5.7 4.9 1.8 7.3L12 17.8 5.4 21.7l1.8-7.3L1.5 9.5 9 8.9z"/></symbol>
<symbol id="chk" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="#121314" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</defs></svg>"""

def header(path):
    def cur(h):
        return ' aria-current="page"' if h == path else ''
    dd = "\n".join(f'        <a href="{h}"{cur(h)}>{t}<small>{s}</small></a>' for h, t, s in NAV_SERVICES)
    main = "\n".join(f'    <a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV_MAIN)
    dsvc = "\n".join(f'    <a class="dl sub" href="{h}">{t}</a>' for h, t, s in NAV_SERVICES)
    dmain = "\n".join(f'    <a class="dl" href="{h}">{t}</a>' for h, t in NAV_MAIN)
    return f"""<header class="top"><div class="wrap hbar">
  <a class="logo" href="/" aria-label="TrueSquare Remodel, home"><img src="/img/logo.svg" alt="TrueSquare Bathroom Remodeling" width="242" height="60"></a>
  <nav class="desk" aria-label="Main">
    <div class="dd"><button type="button" aria-haspopup="true">Services</button>
      <div class="ddm">
{dd}
        <a href="/services"{cur('/services')}>All services<small>Compare what we do</small></a>
      </div>
    </div>
{main}
  </nav>
  <div class="desk-right">
    <a class="hphone" href="tel:{PHONE_T}">{PHONE}</a>
    <a class="btn" href="#book" data-cta="header">Free visit <span class="arr">→</span></a>
  </div>
  <div class="hright">
    <a class="callbtn" href="tel:{PHONE_T}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>Call</a>
    <button class="burger" type="button" id="openMenu" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span></button>
  </div>
</div></header>

<div class="drawer" id="drawer" hidden>
  <div class="dpanel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="dtop"><img src="/img/logo.svg" alt="TrueSquare" width="130" height="32"><button class="dclose" type="button" id="closeMenu" aria-label="Close menu">×</button></div>
    <p class="dgroup">Services</p>
{dsvc}
    <a class="dl sub" href="/services">All services</a>
    <p class="dgroup">TrueSquare</p>
    <a class="dl" href="/">Home</a>
{dmain}
    <div class="dcta">
      <a class="btn block" href="#book" data-cta="menu">Request a free visit <span class="arr">→</span></a>
      <a class="btn outline block" href="tel:{PHONE_T}">Call {PHONE}</a>
    </div>
  </div>
</div>"""

def footer():
    svc = "".join(f'<a href="{h}">{t}</a>' for h, t, s in NAV_SERVICES)
    return f"""<footer><div class="wrap">
  <div class="fgrid">
    <div class="fbrand"><img src="/img/logo-reverse.svg" alt="TrueSquare Bathroom Remodeling" width="242" height="60" loading="lazy"><p>TrueSquare Remodel LLC. Bathroom remodeling in the Seattle area.</p></div>
    <div class="fcols">
      <div class="fcol"><h4>Services</h4>{svc}<a href="/services">All services</a></div>
      <div class="fcol"><h4>Explore</h4><a href="/portfolio">Projects</a><a href="/blog/">Blog</a><a href="/about">About TrueSquare</a><a href="/reviews">Reviews</a><a href="/#process">How It Works</a><a href="/#faq">FAQ</a><a href="#book">Contact</a></div>
    </div>
    <div class="fcontact">
      <h4 style="margin:0 0 4px;font:700 12.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:#fff">Contact</h4>
      <span>Call <a href="tel:{PHONE_T}"><b>{PHONE}</b></a></span>
      <span>info@truesquareremodel.com</span>
      <span>WA Registered Contractor · <b>{LNI}</b> · <span class="nw">Owner-led</span></span>
      <a href="{LNI_URL}" target="_blank" rel="noopener">Verify registration →</a>
    </div>
  </div>
  <p class="areas" id="areas"><b>Service areas:</b> {", ".join(CITIES[:-1])} and {CITIES[-1]}.</p>
  <div class="legal"><a href="/privacy">Privacy Policy</a><a href="/terms">Terms of Service</a><span>© {datetime.date.today().year} TrueSquare Remodel LLC</span></div>
</div></footer>

<div class="sticky" id="sticky" aria-hidden="true">
  <a class="s1" href="#book" data-cta="sticky">Request free visit</a>
  <a class="s2" href="tel:{PHONE_T}">Call Serhii</a>
</div>

<div class="lb" id="lb" hidden role="dialog" aria-label="Photo"><img id="lbImg" alt=""><button type="button" id="lbClose" aria-label="Close">×</button></div>"""

BATH_TILES = ["Full bathroom remodel", "Tub to walk-in shower", "Shower remodel", "Not sure yet"]

def book(tiles=BATH_TILES, default="", title='Get your price <span class="grad-text">in writing.</span>',
         lead="Tell us what you're planning. Serhii will call to arrange a free on-site visit. No pressure."):
    t = "\n".join(f'          <button type="button" class="tile" data-v="{esc(v)}" aria-pressed="false">{esc(v)}</button>' for v in tiles)
    dflt = f' data-default="{esc(default)}"' if default else ''
    return f"""<section class="book on-ink" id="book"><div class="wrap bgrid">
  <div>
    <p class="kicker">Request your free visit</p>
    <h2 style="margin-top:10px">{title}</h2>
    <p class="lead" style="margin-top:10px">{lead}</p>
    <p class="callline">Prefer to talk? Call or text <a href="tel:{PHONE_T}">{PHONE}</a></p>
  </div>
  <form class="form" id="bookForm" novalidate data-clarity-mask="True"{dflt}>
    <div id="formBody">
      <fieldset>
        <legend>What are you planning?</legend>
        <div class="tiles" id="tiles">
{t}
        </div>
      </fieldset>
      <div class="fields">
        <label class="f" for="fName">Your name<input class="t" id="fName" name="full_name" autocomplete="name"></label>
        <label class="f" for="fPhone">Phone <small>(so Serhii can call you back)</small><input class="t" id="fPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel"></label>
        <label class="f" for="fZip">ZIP code<input class="t" id="fZip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5"></label>
        <label class="consent" for="fMkt"><input type="checkbox" id="fMkt" name="marketing_consent"><span id="mktText">Also send me occasional bathroom tips and offers by text (optional).</span></label>
        <p class="err" id="fErr" hidden></p>
        <button class="btn block" type="submit" id="fSubmit"><span id="fLabel">Request my free visit</span> <span class="arr">→</span></button>
        <p class="legal-mini" id="consentText">By tapping Request my free visit, you agree TrueSquare Remodel may call and text you about your request at the number you entered. Msg &amp; data rates may apply. Reply STOP to opt out. <a href="/privacy" target="_blank">Privacy Policy</a> · <a href="/terms" target="_blank">Terms</a></p>
        <p class="next">Serhii will call to arrange a time. No obligation.</p>
        {TRUST}
      </div>
    </div>
    <div class="done" id="formDone" hidden>
      <p class="kicker">Request received</p>
      <p class="big" id="doneTitle">Thanks. We received your request. Serhii will call to arrange a time.</p>
      <p style="color:var(--text)">He calls from <span class="phone">{PHONE}</span>. Have photos? Text 2–3 to that number.</p>
      <a class="btn block" href="tel:{PHONE_T}">Call now</a>
    </div>
  </form>
</div></section>"""

def biz_node(full=False):
    n = {"@type": "HomeAndConstructionBusiness", "@id": BIZ_ID, "name": "TrueSquare Remodel LLC",
         "url": SITE + "/", "telephone": "+1-206-222-2328"}
    if full:
        n.update({"email": "info@truesquareremodel.com", "logo": SITE + "/img/logo.svg", "image": SITE + "/img/serhii.jpg",
                  "description": "Bathroom remodeling in the Seattle area: full bathroom remodels, tub to walk-in shower conversions and shower remodels. Also kitchen remodeling and tile installation.",
                  "founder": {"@type": "Person", "name": "Serhii Tomilov"},
                  "areaServed": [{"@type": "City", "name": c + ", WA"} for c in CITIES],
                  "sameAs": [GOOGLE, THUMBTACK]})
    return n

def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}

def faq_ld(faqs):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]}

def faq_html(faqs, title="Questions about this project.", kicker="Questions"):
    items = "\n".join(f"    <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    return f"""<section class="alt" id="faq"><div class="wrap">
  <div class="head"><p class="kicker">{kicker}</p><h2>{title}</h2></div>
  <div class="faq">
{items}
  </div>
</div></section>"""

def sheet_html(body):
    """Pop-up form shell (28.10): on every page with the form, the free-visit buttons open it in this sheet (site.js)."""
    if 'id="book"' not in body:
        return ""
    import re as _re
    m = _re.search(r'id="book".*?<h2[^>]*>(.*?)</h2>', body, _re.S)
    title = m.group(1).strip() if m else 'Request Your <span class="grad-text">Free Visit</span>'
    return f"""
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheetTitle" hidden>
  <div class="sheet-panel" id="sheetPanel">
    <div class="sheet-head">
      <p class="sheet-title" id="sheetTitle" tabindex="-1">{title}</p>
      <button type="button" class="sheet-x" id="sheetClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="sheet-who"><img src="/img/serhii-avatar.jpg" alt="" width="44" height="44" loading="lazy"><p><b>Serhii will call you to set a time.</b><span>Free visit. No obligation.</span></p></div>
    <div class="sheet-body" id="sheetBody"></div>
  </div>
</div>
"""

def page(path, title, desc, body, ld_extra=(), crumbs=None, page_id="home", robots="index,follow",
         og_image="/img/serhii.jpg", full_biz=False, og_type="website", head_extra="", body_class=""):
    """Wrap a page body in the shared head/header/footer. og_type, head_extra and body_class are used by
    tools/build_blog.py; their defaults reproduce the main pages byte for byte."""
    url = SITE + path
    body_attr = f' class="{body_class}"' if body_class else ""
    extra = ("\n" + head_extra) if head_extra else ""
    graph = [biz_node(full_biz),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "TrueSquare Remodel", "publisher": {"@id": BIZ_ID}},
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
              "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": BIZ_ID}}]
    if crumbs:
        graph.append(crumbs_ld(crumbs))
    graph += list(ld_extra)
    if 'id="book"' not in body:
        body = body.replace('href="#book"', 'href="/#book"')
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
<meta property="og:site_name" content="TrueSquare Remodel">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<link rel="preload" href="/fonts/bricolage-700-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-400-700.woff2" as="font" type="font/woff2" crossorigin>
<style>@font-face{{font-family:"Bricolage Grotesque";font-style:normal;font-weight:700 800;font-display:swap;src:url(/fonts/bricolage-700-800.woff2) format("woff2")}}@font-face{{font-family:"Inter";font-style:normal;font-weight:400 700;font-display:swap;src:url(/fonts/inter-400-700.woff2) format("woff2")}}@font-face{{font-family:"Caveat";font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/caveat-600.woff2) format("woff2")}}</style>
<style>{SITE_CSS}</style>
<script type="application/ld+json">{ld}</script>{extra}
</head>
<body data-page="{page_id}"{body_attr}>
{SVG_DEFS}

{header(path) if 'id="book"' in body else header(path).replace('href="#book"', 'href="/#book"')}

<main id="top">
{body}
</main>

{footer() if 'id="book"' in body else footer().replace('href="#book"', 'href="/#book"')}
{sheet_html(body)}
<script src="/js/site.js?v={ASSET_V}" defer></script>
<script src="https://stats.bigresultsai.com/t.js?c=tsr" defer></script>
</body>
</html>
"""

def phero(crumb_trail, kicker, h1, sub, img=None, img_alt="", cta_label="Request a free visit"):
    cr = "".join(
        (f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(crumb_trail) - 1 else f'<li aria-current="page">{esc(n)}</li>')
        for i, (n, u) in enumerate(crumb_trail))
    pic = (f'<figure class="phimg" style="margin:0"><img src="{img}" alt="{esc(img_alt)}" width="1200" height="900" fetchpriority="high"></figure>'
           if img else "")
    return f"""<section class="phero on-ink">
  <div class="wrap phgrid">
    <div class="phtext">
      <nav aria-label="Breadcrumb"><ol class="crumbs">{cr}</ol></nav>
      <p class="kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p class="sub">{sub}</p>
      <div class="hcta">
        <a class="btn" href="#book" data-cta="hero">{cta_label} <span class="arr">→</span></a>
        <a class="btn outline" href="tel:{PHONE_T}">Call {PHONE}</a>
      </div>
      <p class="lic-line">WA Registered Contractor · <b>{LNI}</b> · <span class="nw">Owner-led</span></p>
    </div>
    {pic}
  </div>
</section>"""

def gallery(items, cls="pgal", grid_id=None):
    gid = f' id="{grid_id}"' if grid_id else ""
    out = []
    for it in items:
        src, alt, cap = it[0], it[1], it[2]
        cat = f' data-cat="{it[3]}"' if len(it) > 3 else ""
        out.append(f'<button class="ph" type="button" data-full="/img/p/{src}"{cat}><img src="/img/p/{src}" alt="{esc(alt)}" loading="lazy" width="900" height="1200"><span class="cap"><i></i>{esc(cap)}</span></button>')
    return f'<div class="{cls}"{gid}>' + "\n".join(out) + "</div>"

def incl(items):
    return '<ul class="incl">' + "".join(
        f'<li><span class="tick"><svg><use href="#chk"/></svg></span><span><b>{a}</b><span>{b}</span></span></li>' for a, b in items) + "</ul>"

PRICE_BLOCK = """<section id="pricing"><div class="wrap pgrid">
  <div>
    <div class="head" style="margin-bottom:22px">
      <p class="kicker">Your price, on paper</p>
      <h2>{h2}</h2>
      <p class="lead">{lead}</p>
    </div>
    <a class="btn" href="#book" data-cta="pricing">Request a free visit <span class="arr">→</span></a>
  </div>
  <div class="panel">
    <div class="ph-head"><img src="/img/logo.svg" alt="TrueSquare" width="105" height="26"><b>What you get</b></div>
    <ul class="checks">
      <li><span class="tick"><svg><use href="#chk"/></svg></span>Written scope of work</li>
      <li><span class="tick"><svg><use href="#chk"/></svg></span>Your price in writing</li>
      <li><span class="tick"><svg><use href="#chk"/></svg></span>No obligation to move forward</li>
    </ul>
    <div class="stays"><b>Your price stays your price.</b><p>The price only changes if you choose an upgrade or hidden damage is found. You see the change in writing and approve it before additional work begins.</p></div>
  </div>
</div></section>"""

def price_block(h2='Your price, in writing. <span class="uline">Within 5 hours.</span>',
                lead="After Serhii measures, you receive the scope of work and your price in writing, so you can compare quotes without guessing."):
    return PRICE_BLOCK.format(h2=h2, lead=lead)

def steps(last="Within 5 hours after the visit, you receive your price in writing. No obligation.",
          note="Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing."):
    n = f'<p class="after-steps"><i></i>{note}</p>' if note else ""
    return f"""<section class="alt" id="process"><div class="wrap">
  <div class="head"><p class="kicker">What happens next</p><h2>Three steps. No guessing.</h2></div>
  <div class="steps">
    <div class="step"><span class="n">1</span><div><h3>Request a free visit</h3><p>Send your details or call. Serhii will arrange a time with you.</p></div></div>
    <div class="step"><span class="n">2</span><div><h3>Serhii measures</h3><p>He visits your home, measures, and talks through what you want to change.</p></div></div>
    <div class="step"><span class="n">3</span><div><h3>Get your written price</h3><p>{last}</p></div></div>
  </div>
  {n}
</div></section>"""

def related(cards, title="Other projects we take on.", three=False):
    c = "".join(f'<a class="rcard" href="{h}"><img src="/img/p/{img}" alt="{esc(alt)}" loading="lazy" width="1200" height="750"><div><h3>{t}</h3><p>{p}</p><span class="go">Learn more →</span></div></a>'
                for h, img, alt, t, p in cards)
    return f"""<section><div class="wrap">
  <div class="head"><p class="kicker">Related</p><h2>{title}</h2></div>
  <div class="rel{' three' if three else ''}">{c}</div>
</div></section>"""

CARD = {
    "/bathroom-remodeling": ("/bathroom-remodeling", "b13.jpg", "Remodeled bathroom with a dark wood vanity and a large lit mirror", "Full bathroom remodeling", "Everything out. New tile, fixtures and vanity."),
    "/tub-to-walk-in-shower": ("/tub-to-walk-in-shower", "ba01.jpg", "Before and after: tub replaced with a tiled walk-in shower", "Tub to walk-in shower", "Old tub out. A tiled walk-in shower in its place."),
    "/shower-remodeling": ("/shower-remodeling", "b17.jpg", "Walk-in shower with large marble-look tile and a lit niche", "Shower remodeling", "New tile, fixtures and glass for your existing shower."),
    "/kitchen-renovations": ("/kitchen-renovations", "k06.jpg", "White kitchen with quartz counters and a marble-look backsplash", "Kitchen remodeling", "Cabinets, counters, backsplash and fixtures."),
    "/tile-flooring": ("/tile-flooring", "b15.jpg", "Hexagon mosaic tile floor in a laundry room", "Tile installation", "Tile floors, shower walls and backsplashes."),
}

def svc_ld(name, path, desc, stype):
    return {"@type": "Service", "@id": SITE + path + "#service", "name": name, "serviceType": stype, "description": desc,
            "url": SITE + path, "provider": {"@id": BIZ_ID},
            "areaServed": [{"@type": "City", "name": c + ", WA"} for c in CITIES]}

SERVICE_POLY = [[47.777,-122.382],[47.777,-122.29],[47.79,-122.21],[47.785,-122.10],[47.72,-122.02],[47.63,-121.98],
                [47.55,-121.98],[47.50,-122.02],[47.46,-122.10],[47.43,-122.18],[47.46,-122.25],[47.495,-122.30],
                [47.50,-122.40],[47.58,-122.42],[47.66,-122.43],[47.72,-122.39]]

def areas_section(alt=False, sid="service-areas"):
    chips = '<ul class="cities">' + "".join(f"<li>{c}</li>" for c in CITIES) + "</ul>"
    poly = json.dumps(SERVICE_POLY)
    return f"""<section class="{'alt' if alt else ''}" id="{sid}"><div class="wrap areas-grid">
  <div class="areas-text">
    <p class="kicker">Service area</p>
    <h2>Serving Seattle <span class="grad-text">and the Eastside.</span></h2>
    <p class="lead">We remodel bathrooms in Seattle and nearby cities, from Shoreline and Bothell down to Renton, and east to Redmond, Sammamish and Issaquah.</p>
    {chips}
  </div>
  <figure class="areamap" style="margin:0">
    <div id="areaMap" data-poly='{poly}' role="img" aria-label="Map of the TrueSquare Remodel service area around Seattle"></div>
    <figcaption>Map shows an approximate service area. Call or text <a href="tel:{PHONE_T}">{PHONE}</a> to confirm your address.</figcaption>
  </figure>
</div></section>"""

PAGES = {}

# ---------------------------------------------------------------- HOME
home_main = read("home.main.html")
PAGES["index.html"] = page(
    "/", "Bathroom Remodeling in Seattle, WA | TrueSquare Remodel",
    "Seattle-area bathroom remodeling by TrueSquare Remodel. Owner Serhii measures your bathroom and provides a written price within 5 hours. Free on-site visit.",
    home_main.replace("<!--AREAS-->", areas_section()) + book(), full_biz=True)

# ---------------------------------------------------------------- FULL BATHROOM
faq_bath = [
    ("How long does a full bathroom remodel take?", "Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing."),
    ("Can I keep my layout?", "Yes. You decide. Keeping the toilet, tub or shower where they are is usually the simpler option. Moving plumbing is possible and is done with a permit."),
    ("What if you find damage behind the old tile?", "We stop, send you photos and a written price for the fix. Nothing moves forward without your OK. The rest of your price stays the same."),
    ("Do you pull permits?", "Yes. When your remodel includes plumbing or electrical work, we do it with a permit and handle the paperwork."),
    ("Can I see how the work is going?", "Yes. If you want them, you get progress photos every day."),
]
crumb = [("Home", "/"), ("Services", "/services"), ("Full Bathroom Remodeling", "/bathroom-remodeling")]
PAGES["bathroom-remodeling.html"] = page(
    "/bathroom-remodeling", "Full Bathroom Remodel in Seattle, WA | TrueSquare Remodel",
    "Full bathroom remodeling in Seattle and the Eastside. New tile, tub or shower, vanity and fixtures. The owner measures and you get a written price within 5 hours.",
    phero(crumb, "Full bathroom remodeling", 'Full bathroom remodeling <span class="grad-text">in Seattle.</span>',
          "Everything out. New tile, fixtures and vanity. Serhii, the owner, measures your bathroom himself. You get your price in writing within 5 hours after the visit.",
          "/img/p/b13.jpg", "Remodeled bathroom with a dark wood vanity, quartz top and lit mirror") +
    f"""
<section><div class="wrap two">
  <div class="prose">
    <p class="kicker">What it means</p>
    <h2>A full remodel, start to finish.</h2>
    <p>A full bathroom remodel means the old room comes out down to the studs or subfloor where needed, and a new bathroom goes in. You choose what changes: the tile, the tub or shower, the vanity, the toilet, the lighting.</p>
    <p>Serhii comes to your home, measures, and talks through what you want. Then you get a written scope of work and one price. You know what is included before anything starts.</p>
    <p>Our crew does the remodeling work. Serhii stays your one point of contact from the first visit to the final walk-through.</p>
  </div>
  <div>
    {incl([
        ("Demolition and haul-away", "Old tile, tub or shower, vanity and toilet come out."),
        ("New tile", "Floor, shower walls or tub surround, niches."),
        ("Tub, shower or walk-in shower", "Keep a tub, or switch to a tiled walk-in shower."),
        ("Vanity, toilet and fixtures", "Faucets, shower valve and trim, mirror, accessories."),
        ("Plumbing and electrical", "Done with permits when your project needs them."),
        ("Hidden damage handled in writing", "Photos and a written price before any extra work."),
    ])}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Full bathroom remodels we've done.</h2><p class="lead">Seattle-area bathrooms remodeled by TrueSquare. Tap a photo to see it larger.</p></div>
  {gallery([
      ("b06.jpg", "Bathroom with wood vanity, round mirror and marble-look floor tile", "Full bathroom remodel"),
      ("b10.jpg", "Double vanity with a large mirror and glass shower behind it", "Full bathroom remodel"),
      ("b14.jpg", "Vanity with vessel sink and large-format wall tile", "Full bathroom remodel"),
      ("b07.jpg", "Bathroom with skylight, glass shower and patterned tile", "Full bathroom remodel"),
      ("b01.jpg", "Bathroom with floating vanity, black mirror, toilet and light floor tile", "Full bathroom remodel"),
      ("b18.jpg", "Floating vanity with a vessel sink and black mirror", "Full bathroom remodel"),
  ])}
  <p style="margin-top:16px"><a class="tlink" href="/portfolio">See all projects →</a></p>
</div></section>
""" + price_block() + steps() + faq_html(faq_bath, "Full remodel questions.") +
    related([CARD["/tub-to-walk-in-shower"], CARD["/shower-remodeling"]]) +
    book(default="Full bathroom remodel"),
    ld_extra=[svc_ld("Full Bathroom Remodeling", "/bathroom-remodeling", "Full bathroom remodels in the Seattle area: demolition, new tile, tub or shower, vanity, toilet and fixtures, with plumbing and electrical work done under permit.", "Bathroom remodeling"), faq_ld(faq_bath)],
    crumbs=crumb, page_id="bathroom-remodeling", og_image="/img/p/b13.jpg")

# ---------------------------------------------------------------- TUB TO SHOWER
faq_tub = [
    ("How long does a tub to shower conversion take?", "Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing."),
    ("Can you keep the rest of my bathroom as it is?", "Yes. We can change only the tub area, or remodel the whole bathroom. You decide, and the written scope shows exactly what is included."),
    ("What about the plumbing?", "The drain and shower valve usually need to change for a walk-in shower. Plumbing work is done with a permit."),
    ("What if there is damage under the old tub?", "We stop, send you photos and a written price for the fix. Nothing moves forward without your OK."),
    ("Do I choose the tile and glass?", "Yes. You pick the tile, the fixtures and the glass. Your written price lists what is included."),
]
crumb = [("Home", "/"), ("Services", "/services"), ("Tub to Walk-In Shower", "/tub-to-walk-in-shower")]
PAGES["tub-to-walk-in-shower.html"] = page(
    "/tub-to-walk-in-shower", "Tub to Walk-In Shower Conversion in Seattle | TrueSquare Remodel",
    "Replace your old bathtub with a tiled walk-in shower. Seattle-area tub to shower conversions. The owner measures and you get a written price within 5 hours.",
    phero(crumb, "Tub to walk-in shower", 'Tub to walk-in shower <span class="grad-text">in Seattle.</span>',
          "Still stepping over that tub wall? We take the old tub out and build a tiled walk-in shower. Serhii measures himself. Price in writing within 5 hours after the visit.",
          "/img/p/ba01.jpg", "Before and after: an old tub replaced with a tiled walk-in shower and glass door") +
    f"""
<section><div class="wrap two">
  <div class="prose">
    <p class="kicker">Why people switch</p>
    <h2>No more stepping over the tub.</h2>
    <p>Many homes around Seattle still have the original tub that nobody uses for baths. A walk-in shower is easier to step into every day and easier to clean.</p>
    <p>We remove the tub, check what is underneath, and build a tiled shower in its place. You choose the tile, the niche, the fixtures and the glass.</p>
    <p>Serhii measures the space and writes your price. Our crew does the work. If we find damage under the old tub, you get photos and a written price before anything extra is done.</p>
  </div>
  <div>
    {incl([
        ("Old tub out", "Tub and old surround removed and hauled away."),
        ("Shower base and waterproofing", "The new shower floor and walls are prepared for tile."),
        ("Tile walls and floor", "Your choice of tile, with a niche for bottles."),
        ("Shower valve and fixtures", "Plumbing changes are done with a permit."),
        ("Glass door or panel", "Pick the glass that fits your space."),
        ("Written price, no surprises", "Changes only for upgrades you choose or hidden damage."),
    ])}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Tubs we've turned into showers.</h2><p class="lead">Before and after photos from TrueSquare projects.</p></div>
  {gallery([
      ("ba01.jpg", "Before and after: tub replaced with a tiled walk-in shower", "Tub to walk-in shower"),
      ("ba02.jpg", "Before and after: shower rebuilt with blue tile and a niche", "Before and after"),
      ("b23.jpg", "Walk-in shower with a sliding glass door and niche", "Walk-in shower"),
      ("b20.jpg", "Corner glass shower with a pebble floor", "Walk-in shower"),
      ("b17.jpg", "Walk-in shower with marble-look tile and a lit niche", "Walk-in shower"),
      ("b09.jpg", "Glass shower under a skylight", "Walk-in shower"),
  ])}
  <p style="margin-top:16px"><a class="tlink" href="/portfolio">See all projects →</a></p>
</div></section>
""" + price_block() + steps() + faq_html(faq_tub, "Tub to shower questions.") +
    related([CARD["/bathroom-remodeling"], CARD["/shower-remodeling"]]) +
    book(default="Tub to walk-in shower"),
    ld_extra=[svc_ld("Tub to Walk-In Shower Conversion", "/tub-to-walk-in-shower", "Bathtub removal and a new tiled walk-in shower: shower base, tile, valve and fixtures, and glass. Plumbing work done under permit.", "Tub to shower conversion"), faq_ld(faq_tub)],
    crumbs=crumb, page_id="tub-to-walk-in-shower", og_image="/img/p/ba01.jpg")

# ---------------------------------------------------------------- SHOWER
faq_shower = [
    ("Can you remodel just the shower?", "Yes. We can rebuild only the shower, or the whole bathroom. Your written scope shows exactly what is included."),
    ("How long does a shower remodel take?", "Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing."),
    ("My shower leaks behind the tile. Can you fix that?", "We open it up, show you what we find with photos, and give you a written price for the fix before we continue."),
    ("Do you replace the shower valve?", "Yes, when your project needs it. Plumbing work is done with a permit."),
]
crumb = [("Home", "/"), ("Services", "/services"), ("Shower Remodeling", "/shower-remodeling")]
PAGES["shower-remodeling.html"] = page(
    "/shower-remodeling", "Shower Remodeling in Seattle, WA | TrueSquare Remodel",
    "Seattle-area shower remodeling: new tile, valve and fixtures, niche and glass for your existing shower. The owner measures and you get a written price within 5 hours.",
    phero(crumb, "Shower remodeling", 'Shower remodeling <span class="grad-text">in Seattle.</span>',
          "Old tile, stained grout or a leak behind the wall? We rebuild your shower with new tile, fixtures and glass. Serhii measures himself. Price in writing within 5 hours after the visit.",
          "/img/p/b17.jpg", "Remodeled walk-in shower with large marble-look tile and a lit niche") +
    f"""
<section><div class="wrap two">
  <div class="prose">
    <p class="kicker">What changes</p>
    <h2>A new shower in the same spot.</h2>
    <p>A shower remodel keeps the shower where it is and replaces what wore out: the tile, the grout, the valve, the door. It is a good fit when the rest of the bathroom is fine.</p>
    <p>We take the old shower down to the framing, check what is behind it, and build it back with fresh tile and fixtures. If we find damage, you get photos and a written price first.</p>
  </div>
  <div>
    {incl([
        ("Old tile and surround out", "Down to the framing so we can see what is behind it."),
        ("New tile and niche", "Walls and floor in the tile you choose."),
        ("Valve, shower head and trim", "Plumbing work is done with a permit."),
        ("Glass door or panel", "Sliding, hinged or fixed panel."),
        ("Hidden damage handled in writing", "Photos and a written price before any extra work."),
    ])}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Showers we've remodeled.</h2></div>
  {gallery([
      ("b02.jpg", "Shower with large gray tile and a half wall", "Shower remodel"),
      ("b11.jpg", "Bathroom with marble-look tile and a lit mirror", "Shower remodel"),
      ("b20.jpg", "Corner glass shower with a pebble floor", "Shower remodel"),
      ("b04.jpg", "Shower niche with black hexagon mosaic tile", "Shower niche"),
      ("b05.jpg", "Shower floor with black mosaic tile and hexagon floor tile", "Shower floor"),
      ("b03.jpg", "Shower niche with marble-look tile and LED light", "Lit niche"),
  ])}
  <p style="margin-top:16px"><a class="tlink" href="/portfolio">See all projects →</a></p>
</div></section>
""" + price_block() + steps() + faq_html(faq_shower, "Shower remodel questions.") +
    related([CARD["/tub-to-walk-in-shower"], CARD["/bathroom-remodeling"]]) +
    book(default="Shower remodel"),
    ld_extra=[svc_ld("Shower Remodeling", "/shower-remodeling", "Remodeling of an existing shower: tear-out, new tile and niche, shower valve and fixtures, and glass. Plumbing work done under permit.", "Shower remodeling"), faq_ld(faq_shower)],
    crumbs=crumb, page_id="shower-remodeling", og_image="/img/p/b17.jpg")

# ---------------------------------------------------------------- KITCHEN
KIT_TILES = ["Kitchen remodel", "Backsplash or counters", "Bathroom remodel", "Not sure yet"]
faq_kit = [
    ("Do you remodel kitchens or only bathrooms?", "Most of our work is bathrooms, and we also remodel kitchens: cabinets, countertops, backsplash and fixtures."),
    ("Can you replace only the countertops or backsplash?", "Tell us what you have in mind. Serhii will tell you on the call if it is a fit, and the written price lists exactly what is included."),
    ("Do you handle electrical and plumbing in the kitchen?", "Yes. When your project includes plumbing or electrical work, we do it with a permit."),
    ("What if you find a problem behind the old cabinets?", "We stop, send you photos and a written price for the fix. Nothing moves forward without your OK."),
]
crumb = [("Home", "/"), ("Services", "/services"), ("Kitchen Remodeling", "/kitchen-renovations")]
PAGES["kitchen-renovations.html"] = page(
    "/kitchen-renovations", "Kitchen Remodeling in Seattle, WA | TrueSquare Remodel",
    "Kitchen remodeling in the Seattle area: cabinets, quartz countertops, tile backsplash, sink and fixtures. The owner measures and you get your price in writing.",
    phero(crumb, "Kitchen remodeling", 'Kitchen remodeling <span class="grad-text">in Seattle.</span>',
          "New cabinets, countertops and backsplash. Serhii, the owner, measures your kitchen himself and you get your price in writing after the visit.",
          "/img/p/k06.jpg", "White shaker kitchen with quartz counters and a marble-look backsplash") +
    f"""
<section><div class="wrap two">
  <div class="prose">
    <p class="kicker">What we do</p>
    <h2>A kitchen you know the price of.</h2>
    <p>Most of our work is bathrooms. We also remodel kitchens the same way: the owner measures, you get a written scope and one price, and our crew does the work.</p>
    <p>You choose what changes. Some kitchens need everything new. Others need new counters and a backsplash. The written price lists exactly what is included, so you can compare quotes.</p>
  </div>
  <div>
    {incl([
        ("Cabinets", "New cabinets and hardware."),
        ("Countertops", "Quartz or butcher block."),
        ("Tile backsplash", "From subway tile to full-height slab look."),
        ("Sink, faucet and fixtures", "Plumbing work done with a permit."),
        ("Lighting and outlets", "Electrical work done with a permit."),
        ("Changes only in writing", "Upgrades or hidden damage: photos and a written price first."),
    ])}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Kitchens we've remodeled.</h2></div>
  {gallery([
      ("k05.jpg", "White kitchen with glass-front cabinets and quartz counters", "Kitchen remodel"),
      ("k07.jpg", "Galley kitchen with white cabinets and wood floors", "Kitchen remodel"),
      ("k02.jpg", "Dark lower cabinets with white quartz and a patterned backsplash", "Kitchen remodel"),
      ("k11.jpg", "Butcher block counter with a gold faucet and tile backsplash", "Counters and backsplash"),
      ("k13.jpg", "White cabinets with quartz counters and a tile backsplash", "Kitchen remodel"),
      ("k09.jpg", "Marble-look slab backsplash with white cabinets", "Backsplash"),
  ])}
  <p style="margin-top:16px"><a class="tlink" href="/portfolio">See all projects →</a></p>
</div></section>
""" + price_block(h2='Your price, <span class="uline">in writing.</span>',
                  lead="After Serhii measures, you receive the scope of work and your price in writing, so you can compare quotes without guessing.") +
    steps(last="After the visit, you receive your price in writing. No obligation.", note="") +
    faq_html(faq_kit, "Kitchen questions.") +
    related([CARD["/bathroom-remodeling"], CARD["/tile-flooring"]]) +
    book(tiles=KIT_TILES, default="Kitchen remodel", lead="Tell us what you're planning. Serhii will call to arrange a free on-site visit."),
    ld_extra=[svc_ld("Kitchen Remodeling", "/kitchen-renovations", "Kitchen remodeling in the Seattle area: cabinets, countertops, tile backsplash, sink and fixtures, with plumbing and electrical work done under permit.", "Kitchen remodeling"), faq_ld(faq_kit)],
    crumbs=crumb, page_id="kitchen-renovations", og_image="/img/p/k06.jpg")

# ---------------------------------------------------------------- TILE
TILE_TILES = ["Tile floor", "Shower or tub tile", "Backsplash", "Not sure yet"]
faq_tile = [
    ("What kind of tile work do you do?", "Bathroom floors, shower walls and floors, tub surrounds, niches, kitchen backsplashes and fireplace surrounds."),
    ("Do you work with large-format tile?", "Yes. Our photos show large-format porcelain set with a leveling system."),
    ("Are materials included in the price?", "Your written price lists which materials are included, so you know before work starts."),
    ("What if the floor under the old tile is damaged?", "We stop, send you photos and a written price for the fix. Nothing moves forward without your OK."),
]
crumb = [("Home", "/"), ("Services", "/services"), ("Tile Installation", "/tile-flooring")]
PAGES["tile-flooring.html"] = page(
    "/tile-flooring", "Tile Installation in Seattle: Floors, Showers, Backsplashes | TrueSquare",
    "Tile installation in the Seattle area: bathroom floors, shower walls, tub surrounds, backsplashes and fireplace surrounds. Free visit and a written price.",
    phero(crumb, "Tile installation", 'Tile floors, showers <span class="grad-text">and backsplashes.</span>',
          "Clean lines, flat floors and straight grout. Serhii measures the space himself and you get your price in writing after the visit.",
          "/img/p/b15.jpg", "Hexagon mosaic tile floor in a bright laundry room") +
    f"""
<section><div class="wrap two">
  <div class="prose">
    <p class="kicker">Where we tile</p>
    <h2>Tile is most of what you see.</h2>
    <p>In a bathroom, tile is the first thing you notice and the first thing that shows a mistake. Flat floors, even grout lines and clean edges at niches and corners matter.</p>
    <p>Most of our tile work is part of a bathroom or kitchen remodel. We also take on tile projects on their own: a new bathroom floor, a backsplash or a fireplace surround.</p>
  </div>
  <div>
    {incl([
        ("Bathroom and laundry floors", "Porcelain, mosaic and hexagon tile."),
        ("Shower walls and floors", "Including niches and lit niches."),
        ("Tub surrounds", "Subway, large-format and stone-look tile."),
        ("Kitchen backsplashes", "From subway tile to slab look."),
        ("Fireplace surrounds", "Tile and stacked stone."),
        ("Written price", "You know the price before work starts."),
    ])}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Tile work we've done.</h2></div>
  {gallery([
      ("b03.jpg", "Marble-look large-format shower tile with a lit niche", "Shower tile"),
      ("b04.jpg", "Shower niche with black hexagon mosaic", "Niche"),
      ("b05.jpg", "Black mosaic shower floor and hexagon floor tile", "Shower floor"),
      ("k12.jpg", "Hexagon marble backsplash behind a gold faucet", "Backsplash"),
      ("o04.jpg", "White tile fireplace surround with a wood mantel", "Fireplace"),
      ("o02.jpg", "Fireplace with patterned tile surround", "Fireplace"),
  ])}
  <p style="margin-top:16px"><a class="tlink" href="/portfolio">See all projects →</a></p>
</div></section>
""" + price_block(h2='Your price, <span class="uline">in writing.</span>',
                  lead="After Serhii measures, you receive the scope of work and your price in writing, so you can compare quotes without guessing.") +
    steps(last="After the visit, you receive your price in writing. No obligation.", note="") +
    faq_html(faq_tile, "Tile questions.") +
    related([CARD["/shower-remodeling"], CARD["/kitchen-renovations"]]) +
    book(tiles=TILE_TILES, default="Tile floor", lead="Tell us what you're planning. Serhii will call to arrange a free on-site visit."),
    ld_extra=[svc_ld("Tile Installation", "/tile-flooring", "Tile installation in the Seattle area: bathroom and laundry floors, shower walls and floors, tub surrounds, kitchen backsplashes and fireplace surrounds.", "Tile installation"), faq_ld(faq_tile)],
    crumbs=crumb, page_id="tile-flooring", og_image="/img/p/b15.jpg")

# ---------------------------------------------------------------- SERVICES HUB
crumb = [("Home", "/"), ("Services", "/services")]
cards_all = [CARD[k] for k in ["/bathroom-remodeling", "/tub-to-walk-in-shower", "/shower-remodeling", "/kitchen-renovations", "/tile-flooring"]]
PAGES["services.html"] = page(
    "/services", "Remodeling Services in Seattle | TrueSquare Remodel",
    "Bathroom remodeling, tub to walk-in shower conversions, shower remodels, kitchen remodeling and tile installation in Seattle and the Eastside.",
    phero(crumb, "Services", 'What we <span class="grad-text">remodel.</span>',
          "Mostly bathrooms. Also kitchens and tile work. Every project starts the same way: Serhii measures and you get your price in writing.",
          "/img/p/b10.jpg", "Remodeled bathroom with a double vanity and glass shower") +
    f"""
<section><div class="wrap">
  <div class="head"><p class="kicker">Pick your project</p><h2>Five kinds of projects.</h2><p class="lead">Each page explains what is included, shows real photos and answers common questions.</p></div>
  <div class="rel three">{"".join(f'<a class="rcard" href="{h}"><img src="/img/p/{img}" alt="{esc(alt)}" loading="lazy" width="1200" height="750"><div><h3>{t}</h3><p>{p}</p><span class="go">Learn more →</span></div></a>' for h, img, alt, t, p in cards_all)}</div>
</div></section>
""" + price_block() + steps() + book(tiles=["Full bathroom remodel", "Tub to walk-in shower", "Shower remodel", "Kitchen or tile"]),
    ld_extra=[{"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + c[0], "name": c[3]} for i, c in enumerate(cards_all)]}],
    crumbs=crumb, page_id="services", og_image="/img/p/b10.jpg")

# ---------------------------------------------------------------- PORTFOLIO
P = [
    ("ba01.jpg", "Before and after: tub replaced with a tiled walk-in shower", "Tub to walk-in shower", "shower"),
    ("b13.jpg", "Dark wood vanity with a quartz top and lit mirror", "Full bathroom remodel", "bath"),
    ("b17.jpg", "Walk-in shower with marble-look tile and lit niche", "Shower remodel", "shower"),
    ("k05.jpg", "White kitchen with glass-front cabinets", "Kitchen remodel", "kitchen"),
    ("b06.jpg", "Wood vanity, round mirror and marble-look floor", "Full bathroom remodel", "bath"),
    ("ba02.jpg", "Before and after: shower rebuilt with blue tile", "Before and after", "shower"),
    ("b10.jpg", "Double vanity with a large mirror", "Full bathroom remodel", "bath"),
    ("b15.jpg", "Hexagon mosaic laundry room floor", "Tile floor", "tile"),
    ("k07.jpg", "Galley kitchen with white cabinets", "Kitchen remodel", "kitchen"),
    ("b23.jpg", "Walk-in shower with sliding glass door", "Walk-in shower", "shower"),
    ("b14.jpg", "Vanity with vessel sink and large-format tile", "Full bathroom remodel", "bath"),
    ("b03.jpg", "Large-format marble-look tile with a lit niche", "Tile work", "tile"),
    ("k02.jpg", "Dark cabinets with white quartz counters", "Kitchen remodel", "kitchen"),
    ("b07.jpg", "Bathroom with skylight and glass shower", "Full bathroom remodel", "bath"),
    ("b20.jpg", "Corner glass shower with pebble floor", "Shower remodel", "shower"),
    ("k11.jpg", "Butcher block counter with tile backsplash", "Kitchen remodel", "kitchen"),
    ("b19.jpg", "Green subway tile tub surround", "Full bathroom remodel", "bath"),
    ("b04.jpg", "Shower niche with black hexagon mosaic", "Tile work", "tile"),
    ("b18.jpg", "Floating vanity with vessel sink", "Full bathroom remodel", "bath"),
    ("b09.jpg", "Glass shower under a skylight", "Shower remodel", "shower"),
    ("k13.jpg", "White cabinets with tile backsplash", "Kitchen remodel", "kitchen"),
    ("b16.jpg", "Vanity with dark wood-look wall tile", "Full bathroom remodel", "bath"),
    ("o04.jpg", "White tile fireplace surround", "Tile work", "tile"),
    ("b11.jpg", "Marble-look tile and lit mirror", "Full bathroom remodel", "bath"),
    ("b22.jpg", "Tub with marble-look tile surround", "Full bathroom remodel", "bath"),
    ("k06.jpg", "White kitchen with quartz counters", "Kitchen remodel", "kitchen"),
    ("b02.jpg", "Gray large-format shower tile", "Shower remodel", "shower"),
    ("b05.jpg", "Black mosaic shower floor", "Tile work", "tile"),
    ("k14.jpg", "White cabinets with gray tile backsplash", "Kitchen remodel", "kitchen"),
    ("b01.jpg", "Floating white vanity with black mirror", "Full bathroom remodel", "bath"),
    ("o02.jpg", "Patterned tile fireplace surround", "Tile work", "tile"),
    ("b12.jpg", "Tub with marble-look tile and mosaic niche", "Full bathroom remodel", "bath"),
]
crumb = [("Home", "/"), ("Projects", "/portfolio")]
chips = '<div class="chips" id="pfilter" role="toolbar" aria-label="Filter projects">' + "".join(
    f'<button type="button" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>'
    for k, v in [("all", "All"), ("bath", "Bathrooms"), ("shower", "Showers"), ("kitchen", "Kitchens"), ("tile", "Tile")]) + "</div>"
PAGES["portfolio.html"] = page(
    "/portfolio", "Remodeling Projects in Seattle: Photos | TrueSquare Remodel",
    "Photos of bathroom remodels, walk-in showers, kitchens and tile work by TrueSquare Remodel in the Seattle area.",
    phero(crumb, "Projects", 'Real TrueSquare <span class="grad-text">projects.</span>',
          "Bathrooms, showers, kitchens and tile work we've done in the Seattle area. Tap a photo to see it larger.",
          "/img/p/b13.jpg", "Remodeled bathroom with a dark wood vanity and lit mirror", cta_label="Start your project") +
    f"""
<section><div class="wrap">
  {chips}
  {gallery(P, cls="pgal four", grid_id="pgrid")}
</div></section>
""" + book(tiles=["Full bathroom remodel", "Tub to walk-in shower", "Shower remodel", "Kitchen or tile"], title='Like what you see? <span class="grad-text">Get your price.</span>'),
    ld_extra=[{"@type": "ImageGallery", "name": "TrueSquare Remodel projects", "url": SITE + "/portfolio",
               "image": [{"@type": "ImageObject", "contentUrl": SITE + "/img/p/" + p[0], "caption": p[2] + ": " + p[1]} for p in P]}],
    crumbs=crumb, page_id="portfolio", og_image="/img/p/b13.jpg")

# ---------------------------------------------------------------- ABOUT
crumb = [("Home", "/"), ("About", "/about")]
cities_html = '<ul class="cities">' + "".join(f"<li>{c}</li>" for c in CITIES) + "</ul>"
PAGES["about.html"] = page(
    "/about", "About TrueSquare Remodel | Owner-Led Remodeling in Seattle",
    "TrueSquare Remodel LLC is an owner-led remodeling company in Seattle. Serhii measures every project and writes every price. WA Registered Contractor TRUESRL759QK.",
    phero(crumb, "About TrueSquare", 'One owner. <span class="grad-text">One price.</span> One person to call.',
          "TrueSquare Remodel is a Seattle remodeling company run by its owner, Serhii. He measures your project, writes your price and stays your point of contact.",
          "/img/serhii.jpg?v=3", "Serhii, owner of TrueSquare Remodel", cta_label="Meet Serhii at your home") +
    f"""
<section><div class="wrap two">
  <div class="prose">
    <p class="kicker">How we work</p>
    <h2>The person who gives you the price is the owner.</h2>
    <p>With many remodelers, a salesperson visits, gives a number, and you never see them again. At TrueSquare, Serhii comes to your home himself. He measures, listens to what you want, and writes your price.</p>
    <p>Our crew does the remodeling work. Serhii stays your one contact from the first visit to the final walk-through. One contract, one price, one warranty.</p>
    <p>The price in your agreement is the price you pay. It only changes if you choose an upgrade or we find hidden damage, and you see that change in writing and approve it first.</p>
  </div>
  <div class="facts">
    <div class="fact"><b>WA Registered Contractor</b><span>{LNI}</span></div>
    <div class="fact"><b>Owner-led</b><span>Serhii measures and leads every project</span></div>
    <div class="fact"><b>1-year</b><span>workmanship warranty + manufacturer warranties</span></div>
    <div class="fact"><b>Permits</b><span>for plumbing and electrical work</span></div>
    <div class="fact"><b>Written price</b><span>within 5 hours after a bathroom visit</span></div>
    <div class="fact"><b>Typically 2–4 weeks</b><span>of construction, depending on scope</span></div>
    <div class="fact"><b>Daily photos</b><span>of the progress, if you want them</span></div>
    <div class="fact"><b>Deposit at signing</b><span>final payment after the walk-through</span></div>
  </div>
</div></section>

<section class="owner on-ink"><div class="wrap ogrid">
  <div class="ophoto"><img src="/img/process-tile.jpg" alt="Large-format tile being set with leveling clips on a TrueSquare project" loading="lazy" width="675" height="1200"></div>
  <div>
    <p class="kicker">Check us</p>
    <h2 style="margin-top:10px">Don't take our word for it. <span class="grad-text">Verify it.</span></h2>
    <p class="lead" style="margin-top:12px">Every Washington contractor must be registered with the Department of Labor &amp; Industries. You can look up our registration, bond and insurance on the L&amp;I website.</p>
    <p class="sig grad-text">— Serhii</p>
    <p class="sigsub">Owner, TrueSquare Remodel LLC</p>
    <a class="verify" href="{LNI_URL}" target="_blank" rel="noopener">
      <span class="vi"><svg viewBox="0 0 24 24" fill="none" stroke="#121314" stroke-width="2.4"><path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg></span>
      <span><b>WA L&amp;I · {LNI}</b><span>Verify our contractor registration →</span></span>
    </a>
  </div>
</div></section>

{areas_section(alt=True)}
""" + book(tiles=["Full bathroom remodel", "Tub to walk-in shower", "Shower remodel", "Kitchen or tile"]),
    ld_extra=[{"@type": "AboutPage", "@id": SITE + "/about#about", "url": SITE + "/about", "about": {"@id": BIZ_ID}},
              {"@type": "Person", "@id": SITE + "/about#person", "name": "Serhii Tomilov", "jobTitle": "Owner", "url": SITE + "/about", "worksFor": {"@id": BIZ_ID}, "image": SITE + "/img/serhii.jpg", "sameAs": [GOOGLE, THUMBTACK]}],
    crumbs=crumb, page_id="about", og_image="/img/serhii.jpg")

# ---------------------------------------------------------------- REVIEWS
crumb = [("Home", "/"), ("Reviews", "/reviews")]
star5 = '<span class="st" aria-hidden="true">' + '<svg><use href="#star"/></svg>' * 5 + "</span>"
PAGES["reviews.html"] = page(
    "/reviews", "TrueSquare Remodel Reviews | Google and Thumbtack",
    "Read reviews of TrueSquare Remodel on Google and Thumbtack. Seattle-area bathroom remodeling.",
    phero(crumb, "Reviews", 'What homeowners <span class="grad-text">say.</span>',
          "Read reviews from TrueSquare customers on Google and Thumbtack. Reviews open on those sites.",
          None) +
    f"""
<section><div class="wrap">
  <div class="rvcards">
    <a class="rvcard" href="{GOOGLE}" target="_blank" rel="noopener"><p class="kicker">Google</p>{star5}<span class="big">5.0</span><span class="go">Read our Google reviews ↗</span></a>
    <a class="rvcard" href="{THUMBTACK}" target="_blank" rel="noopener"><p class="kicker">Thumbtack</p>{star5}<span class="big">5.0</span><span class="go">Read our Thumbtack reviews ↗</span></a>
  </div>
  <p style="margin-top:22px;color:var(--text);max-width:64ch">Worked with us? A short review on Google helps other homeowners find an honest contractor. Thank you.</p>
</div></section>
""" + book(),
    crumbs=crumb, page_id="reviews", robots="noindex,follow")

# ---------------------------------------------------------------- LEGAL
def legal(slug, name, desc, updated=""):
    crumb = [("Home", "/"), (name, "/" + slug)]
    body = f"""<section class="phero on-ink"><div class="wrap phgrid" style="grid-template-columns:1fr">
  <div class="phtext"><nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="/">Home</a></li><li aria-current="page">{name}</li></ol></nav>
  <p class="kicker">Legal</p><h1>{name}</h1><p class="sub">TrueSquare Remodel LLC · Effective October 21, 2026{(" · Updated " + updated) if updated else ""}</p></div>
</div></section>
<section><div class="wrap legalbody">
{read(slug + '.body.html')}
</div></section>"""
    return page("/" + slug, f"{name} | TrueSquare Remodel", desc, body, crumbs=crumb, page_id=slug)

PAGES["privacy.html"] = legal("privacy", "Privacy Policy", "How TrueSquare Remodel LLC collects, uses and protects your information, including SMS consent.", updated="October 26, 2026")
PAGES["terms.html"] = legal("terms", "Terms of Service", "Terms of Service for the TrueSquare Remodel website, estimates and text messages.")

# ---------------------------------------------------------------- 404
PAGES["404.html"] = page(
    "/404", "Page not found | TrueSquare Remodel", "This page does not exist.",
    phero([("Home", "/"), ("Not found", "/404")], "404", 'This page <span class="grad-text">moved.</span>',
          "The page you were looking for isn't here. Start from the home page or request a free visit.", None) +
    related([CARD["/bathroom-remodeling"], CARD["/tub-to-walk-in-shower"], CARD["/shower-remodeling"]], title="Popular pages.", three=True) + book(),
    page_id="404", robots="noindex")

# ---------------------------------------------------------------- sitemap data
# Main-page URLs for the sitemap, in order. The sitemap itself is written by tools/build_blog.py
# (run `python3 tools/build_all.py` to build everything). Dates come from tools/lastmod.json, which
# main() below updates only when a page's generated HTML actually changes, so <lastmod> stays honest.
SITEMAP_URLS = ["/", "/bathroom-remodeling", "/tub-to-walk-in-shower", "/shower-remodeling", "/services",
                "/kitchen-renovations", "/tile-flooring", "/portfolio", "/about", "/privacy", "/terms"]
LASTMOD_FILE = os.path.join(ROOT, "tools", "lastmod.json")

# Files written by main() that map to a sitemap URL (404 is excluded on purpose).
PAGE_URL = {"index.html": "/", "privacy.html": "/privacy", "terms.html": "/terms"}
for _n in PAGES:
    if _n not in PAGE_URL and _n != "404.html":
        PAGE_URL[_n] = "/" + _n[:-5]


def content_hash(html_text):
    """sha256 of a page with the volatile parts masked (footer year, asset version), so cache-busting
    and the turn of the year do not count as content changes."""
    import hashlib, re
    masked = re.sub(r"© \d{4} TrueSquare", "© YEAR TrueSquare", html_text)
    masked = re.sub(r"\?v=\d+", "?v=N", masked)
    return hashlib.sha256(masked.encode("utf-8")).hexdigest()


def update_lastmod(pages):
    """Record today's date for every main page whose content hash changed (or is new)."""
    today = datetime.date.today().isoformat()
    try:
        with open(LASTMOD_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    changed = []
    for name, html_text in pages.items():
        url = PAGE_URL.get(name)
        if not url:
            continue
        h = content_hash(html_text)
        entry = data.get(url)
        if not entry or entry.get("sha256") != h:
            data[url] = {"sha256": h, "lastmod": today}
            changed.append(url)
    with open(LASTMOD_FILE, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(data.items())), f, indent=2)
        f.write("\n")
    return changed


def main():
    for name, s in PAGES.items():
        with open(os.path.join(PUB, name), "w", encoding="utf-8") as f:
            f.write(s)
    changed = update_lastmod(PAGES)
    with open(os.path.join(PUB, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(PAGES), "pages;", "lastmod updated for:", ", ".join(changed) if changed else "nothing")


if __name__ == "__main__":
    main()
