#!/usr/bin/env python3
"""Landing pages for Meta ads. Separate from build.py on purpose: it never touches
the main site pages, shared CSS/JS or sitemap.

    python3 tools/build_lp.py

Writes: public/bathroom-remodel-cost.html (M0), public/bathroom-remodel-guarantee.html (M1),
public/guarantee-terms.html. All noindex, none in sitemap.
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
SITE = "https://truesquareremodel.com"
PHONE_T, PHONE = "+12062222328", "(206) 222-2328"
LNI = "TRUESRL759QK"
GOOGLE = "https://www.google.com/maps?cid=7556474326958598816"
THUMBTACK = "https://www.thumbtack.com/wa/seattle/bathroom-remodeling/truesquare-remodel-llc/service/562919809761304593"
V = "5"  # cache version for lp.css / lp.js (5 = form_source tracking + Clarity, 28.10)
RANGE = "$16,000–$28,500"

def esc(s): return html.escape(s, quote=True)

PHONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
SVG_DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F69A72"/><stop offset=".5" stop-color="#F47A61"/><stop offset="1" stop-color="#EC6463"/></linearGradient>
<symbol id="star" viewBox="0 0 24 24"><path d="M12 2l3 6.9 7.5.6-5.7 4.9 1.8 7.3L12 17.8 5.4 21.7l1.8-7.3L1.5 9.5 9 8.9z"/></symbol>
<symbol id="chk" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="#121314" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</defs></svg>"""

FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;600;700&family=Caveat:wght@600&display=swap"

def css_inline():
    # read-only use of the shared site.css; landing extras from lp.css
    import re
    out = []
    for f in ("site.css", "lp.css"):
        with open(os.path.join(PUB, "css", f), encoding="utf-8") as fh:
            c = fh.read()
        c = re.sub(r"/\*.*?\*/", "", c, flags=re.S)
        c = re.sub(r"\s*\n\s*", "", c)
        out.append(c)
    return "".join(out)

def shell(path, title, desc, angle, body, preload=None):
    CSS = css_inline()
    PRE = ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/img/lp-hero.jpg">
{PRE}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<style>{CSS}</style>
</head>
<body class="lp" data-page="lp-{angle}" data-angle="{angle}">
{SVG_DEFS}

<header class="top"><div class="wrap hbar">
  <a class="logo" href="#top" aria-label="TrueSquare Remodel"><img src="/img/logo.svg" alt="TrueSquare Bathroom Remodeling" width="242" height="60"></a>
  <a class="lp-call" href="tel:{PHONE_T}" data-cta="header-call">{PHONE_ICON}<span class="word">Call</span><span class="num">Call {PHONE}</span></a>
</div></header>

<main id="top">
{body}
</main>

<footer><div class="wrap lpf">
  <span><b>TrueSquare Remodel LLC</b> · WA Registered Contractor · <b>{LNI}</b> · <span class="nw">Owner-led</span></span>
  <span><a href="tel:{PHONE_T}">{PHONE}</a> · info@truesquareremodel.com · Seattle, WA</span>
  <span class="links"><a href="/">About TrueSquare</a><a href="/privacy">Privacy Policy</a><a href="/terms">Terms of Service</a></span>
</div></footer>

<div class="sticky" id="sticky" aria-hidden="true">
  <a class="s2" href="tel:{PHONE_T}" data-cta="sticky-call">Call</a>
  <a class="s1" href="#book" data-cta="sticky">Get My Price</a>
</div>

<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheetTitle" hidden>
  <div class="sheet-panel" id="sheetPanel">
    <div class="sheet-head">
      <p class="sheet-title" id="sheetTitle" tabindex="-1">Get Your <span class="grad-text">Written Price</span></p>
      <button type="button" class="sheet-x" id="sheetClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="sheet-who"><img src="/img/serhii-avatar.jpg" alt="" width="44" height="44" loading="lazy"><p><b>Serhii will call you to set a time.</b><span>Free visit. No obligation.</span></p></div>
    <div class="sheet-body" id="sheetBody"></div>
  </div>
</div>

<div class="lb" id="lb" hidden role="dialog" aria-label="Photo"><img id="lbImg" alt=""><button type="button" id="lbClose" aria-label="Close">×</button></div>

<script>
/* analytics + shared behavior load after the page has painted (keeps LCP fast) */
(function(){{function go(){{var a=document.createElement('script');a.src='/js/site.js?v=9';a.onload=function(){{var b=document.createElement('script');b.src='/js/lp.js?v={V}';document.body.appendChild(b);}};document.body.appendChild(a);}}
function fonts(){{var l=document.createElement('link');l.rel='stylesheet';l.href='{FONTS}';document.head.appendChild(l);}}
if(document.readyState==='complete'){{fonts();go();}}else addEventListener('load',function(){{fonts();go();}});}})();
</script>
<script src="https://stats.bigresultsai.com/t.js?c=tsr" defer></script>
</body>
</html>
"""

def stars():
    return '<span class="st" aria-hidden="true"><svg><use href="#star"/></svg></span>'

def hero(sub, under):
    return f"""<section class="hero on-ink">
  <div class="wrap hgrid">
    <div class="htext">
      <p class="kicker">Seattle-area bathroom remodeling</p>
      <h1>Full Bathroom Remodels: <span class="grad-text">{RANGE}</span></h1>
      <span class="scope">Smaller bathrooms fall at the lower end. Price depends on scope. Plus WA sales tax.</span>
      <p class="sub">{sub}</p>
      <div class="hcta">
        <a class="btn" href="#book" data-cta="hero">Request My Free Bathroom Visit <span class="arr">→</span></a>
      </div>
      <p class="under">{under}</p>
      <div class="rate" aria-label="Ratings">
        <a href="{GOOGLE}" target="_blank" rel="noopener">{stars()}<b>5.0</b> on Google (12 reviews) <small>↗</small></a>
        <span class="sep" aria-hidden="true"></span>
        <a href="{THUMBTACK}" target="_blank" rel="noopener">{stars()}<b>5.0</b> on Thumbtack <small>↗</small></a>
      </div>
      <p class="lic-line">WA Registered Contractor · <b>{LNI}</b> · <span class="nw">Owner-led</span></p>
    </div>
    <figure class="hphoto">
      <div class="in"><img src="/img/lp-hero.jpg" srcset="/img/lp-hero-460.jpg 460w, /img/lp-hero.jpg 675w" sizes="(min-width:960px) 520px, 92vw" alt="Finished bathroom remodel with a glass walk-in shower" width="675" height="844" fetchpriority="high" decoding="async"></div>
    </figure>
  </div>
</section>"""

FACTORS = f"""<section class="alt"><div class="wrap">
  <div class="head"><p class="kicker">Your price</p><h2>Three Things Decide Your Price</h2></div>
  <div class="factors">
    <div class="factor"><span class="n">1</span><h3>Size and layout</h3><p>Keeping the toilet, shower and drain where they are costs less than moving them.</p></div>
    <div class="factor"><span class="n">2</span><h3>Your materials</h3><p>Tile, vanity, fixtures and glass. You choose. Every item is listed in your price.</p></div>
    <div class="factor"><span class="n">3</span><h3>What's behind the old walls</h3><p>Old leaks or rot show up after demo. If we find any, we stop, send you photos and a written price. Nothing extra happens without your written OK.</p></div>
  </div>
  <div class="rangebox">
    <b>Full bathroom remodel: {RANGE}</b>
    <small><span class="tax">Smaller bathrooms fall at the lower end. Price depends on scope. Plus WA sales tax.</span> Larger or more complex projects may exceed this range. This is our current price range, not a quote. Your exact price comes in writing after we see the room.</small>
  </div>
</div></section>"""

WORK = """<section id="work"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Real Bathrooms, Before and After</h2></div>
  <div class="gal">
    <button class="ph main" type="button" data-full="/img/p/b06.jpg"><img src="/img/p/b06.jpg" alt="Full bathroom remodel: new vanity, toilet, mirror, lighting and floor tile" loading="lazy" width="675" height="1200" style="object-position:50% 72%"></button>
    <button class="ph s" type="button" data-full="/img/p/b13.jpg"><img src="/img/p/b13.jpg" alt="Full bathroom remodel: double vanity, lit mirror and large-format tile" loading="lazy" width="900" height="1200"></button>
    <button class="ph s" type="button" data-full="/img/p/b18.jpg"><img src="/img/p/b18.jpg" alt="Full bathroom remodel: floating vanity, vessel sink, toilet and new lighting" loading="lazy" width="900" height="1200"></button>
  </div>
</div></section>"""

TRUST = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "partials", "trust.html"), encoding="utf-8").read().strip()  # rating badge + secure shield under every form

def form_section():
    tiles = "".join(f'<button type="button" class="tile" data-v="{v}" aria-pressed="false">{v}</button>' for v in
                    ["Full bathroom remodel", "Tub to walk-in shower", "Shower remodel", "Not sure yet"])
    return f"""<section class="book on-ink" id="book"><div class="wrap bgrid">
  <div>
    <p class="kicker">Free visit</p>
    <h2 style="margin-top:10px">Get Your <span class="grad-text">Written Price</span></h2>
    <p class="lead" style="margin-top:10px">Tell us what you're planning. Serhii will call to set up your free visit.</p>
    <p class="callline">Prefer to talk? Call <a href="tel:{PHONE_T}">{PHONE}</a></p>
    <p class="formlic">WA Registered Contractor · <b>{LNI}</b> · <span class="nw">Owner-led</span></p>
  </div>
  <form class="form" id="lpForm" novalidate data-clarity-mask="True">
    <div id="formBody">
      <fieldset>
        <legend>What are you planning?</legend>
        <div class="tiles" id="tiles">{tiles}</div>
      </fieldset>
      <div class="fields">
        <label class="f" for="fName">Full name<input class="t" id="fName" name="full_name" autocomplete="name"></label>
        <label class="f" for="fPhone">Mobile phone<input class="t" id="fPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel"><span class="why">We'll call or text only about your visit.</span></label>
        <label class="f" for="fZip">ZIP code<input class="t" id="fZip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5"></label>
                <p class="err" id="fErr" hidden></p>
        <button class="btn block" type="submit" id="fSubmit" data-cta="form"><span id="fLabel">Request My Free Visit</span> <span class="arr">→</span></button>
        <p class="legal-mini" id="consentText">By tapping Request My Free Visit, you agree TrueSquare Remodel may call and text you about your request at the number you entered. Msg &amp; data rates may apply. Reply STOP to opt out. <a href="/privacy" target="_blank">Privacy Policy</a> · <a href="/terms" target="_blank">Terms</a></p>
        <p class="next">No payment. No obligation.</p>
        {TRUST}
      </div>
    </div>
    <div class="done" id="formDone" hidden>
      <p class="kicker">Request received</p>
      <p class="big">Request received.</p>
      <p style="color:var(--text)">Serhii will call you shortly to set up your free visit.</p>
      <p style="color:var(--text)">Sent after 7 PM or on Sunday? We'll call the next working morning.</p>
      <p style="color:var(--text)">Need us sooner? Call <span class="phone">{PHONE}</span>.</p>
      <a class="btn block" href="tel:{PHONE_T}">Call now</a>
    </div>
  </form>
</div></section>"""

def chk(t): return f'<li><span class="tick"><svg><use href="#chk"/></svg></span>{t}</li>'
WRITTEN = f"""<section><div class="wrap wp">
  <div class="head" style="margin-bottom:0">
    <p class="kicker">On paper</p>
    <h2>What You Get in Writing</h2>
    <p class="lead">Your price lists every item. You see the full total before you decide.</p>
  </div>
  <div class="panel">
    <div class="ph-head"><img src="/img/logo.svg" alt="TrueSquare" width="105" height="26" loading="lazy"><b>Your written price</b></div>
    <ul class="checks">
      {chk("Demolition and haul-away")}
      {chk("Waterproofing")}
      {chk("Plumbing and electrical, with permits where required")}
      {chk("Tile, vanity, fixtures and glass")}
      {chk("Cleanup")}
      {chk("1-year workmanship warranty + manufacturer warranties")}
      {chk("WA sales tax on its own line")}
    </ul>
    <p class="total">You see the full total before you decide.</p>
  </div>
</div></section>"""

OWNER = """<section class="owner on-ink"><div class="wrap ogrid">
  <div class="ophoto"><img src="/img/serhii.jpg?v=3" alt="Serhii, owner of TrueSquare Remodel" loading="lazy" width="1024" height="1536"></div>
  <div>
    <p class="kicker">The owner</p>
    <h2 style="margin-top:10px">You Deal With <span class="grad-text">the Owner</span></h2>
    <p class="lead" style="margin-top:12px">I'm Serhii, the owner of TrueSquare Remodel. I measure your bathroom, write your price and lead your project from start to finish. Our crew does the remodeling work.</p>
    <p class="note">Progress photos every day, if you want them.</p>
    <p class="sig grad-text">— Serhii, Owner</p>
  </div>
</div></section>"""

STEPS = """<section class="alt" id="process"><div class="wrap">
  <div class="head"><p class="kicker">Simple</p><h2>How It Works</h2></div>
  <div class="steps">
    <div class="step"><span class="n">1</span><div><h3>Request a visit</h3><p>Serhii calls you to pick a time.</p></div></div>
    <div class="step"><span class="n">2</span><div><h3>Free visit</h3><p>Serhii measures the room and talks through what you want.</p></div></div>
    <div class="step"><span class="n">3</span><div><h3>Your price in writing</h3><p>Within 5 hours after the visit. Take your time to decide.</p></div></div>
  </div>
  <p class="after-steps"><i></i>Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing.</p>
</div></section>"""

FAQ_ITEMS = [
    ("Can you give me a price before the visit?", f"Our full remodels range from {RANGE}. Smaller bathrooms fall at the lower end. Larger or more complex projects may exceed this range. Price depends on scope. Plus WA sales tax. An exact price needs a visit, because the layout and what's behind the walls change the number. You get it in writing within 5 hours after the visit."),
    ("What if you find damage behind the wall?", "We stop, show you photos, and give you a written price. Nothing happens without your written OK."),
    ("How long does it take?", "Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing."),
    ("Is there a warranty?", "Yes. 1-year written workmanship warranty, plus the manufacturer warranties on fixtures and materials."),
    ("Who does the work?", "Our crew does the remodeling work. Serhii leads every project and is your one point of contact."),
    ("How do payments work?", "You pay a deposit when you sign the contract, the next payment after the rough-in inspection passes, and the final payment after our walkthrough together. The visit and the written price are free."),
    ("Do you do small repairs?", "We focus on full bathroom and shower remodels. Small repairs only when our schedule allows."),
]
FAQ = """<section id="faq"><div class="wrap">
  <div class="head"><p class="kicker">Questions</p><h2>Common Questions</h2></div>
  <div class="faq">
""" + "\n".join(f"    <details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ_ITEMS) + """
  </div>
</div></section>"""

FINAL = f"""<section class="alt final"><div class="wrap">
  <h2>Ready for Your Written Price?</h2>
  <a class="btn" href="#book" data-cta="final">Request My Free Visit <span class="arr">→</span></a>
  <p class="or">or call <a href="tel:{PHONE_T}">{PHONE}</a></p>
</div></section>"""

def landing(path, angle, sub, under, title):
    body = "\n".join([hero(sub, under), FACTORS, WORK, form_section(), WRITTEN, OWNER, STEPS, FAQ, FINAL])
    return shell(path, title, f"Full bathroom remodels in the Seattle area: {RANGE}, plus WA sales tax, scope dependent. Free visit, itemized written price within 5 hours.", angle, body, preload="/img/lp-hero.jpg")

PAGES = {
    "bathroom-remodel-cost.html": landing(
        "/bathroom-remodel-cost", "m0-v1",
        "Know exactly what's included. Get an itemized written scope &amp; price within 5 hours after your free on-site visit.",
        "No decision required at the visit.",
        "Full Bathroom Remodels in Seattle: $16,000–$28,500 | TrueSquare"),
    "bathroom-remodel-guarantee.html": landing(
        "/bathroom-remodel-guarantee", "m1-v1",
        "Get an itemized written scope &amp; price within 5 hours after your free on-site visit — or we pay you $200.",
        '$200 deadline guarantee <a href="/guarantee-terms">terms apply</a>. No purchase required.',
        "Written Bathroom Price in 5 Hours or $200 | TrueSquare Remodel"),
    "guarantee-terms.html": shell(
        "/guarantee-terms", "5-Hour Written Price Guarantee | TrueSquare Remodel",
        "Terms of the TrueSquare Remodel 5-hour written price guarantee.", "terms",
        f"""<section><div class="wrap terms">
  <p class="kicker">Guarantee terms</p>
  <h1 style="font-size:clamp(30px,6vw,46px);margin:10px 0 18px">Our 5-Hour Written Price Guarantee</h1>
  <ol>
    <li>The 5 hours start when your scheduled on-site visit ends.</li>
    <li>It applies to a full bathroom remodel project in our service area.</li>
    <li>Within 5 hours you receive a complete itemized written scope &amp; price, not a placeholder message.</li>
    <li>If we miss the deadline, we pay you $200 within 5 business days. You don't have to hire us.</li>
    <li>Visit end time and proposal send time are recorded in our system.</li>
  </ol>
  <p style="margin-top:22px;color:var(--text)">TrueSquare Remodel LLC · WA Contractor Reg. {LNI}</p>
  <p style="margin-top:22px"><a class="btn" href="/bathroom-remodel-guarantee#book">Request My Free Bathroom Visit <span class="arr">→</span></a></p>
</div></section>"""),
}

if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for name, s in PAGES.items():
        if only and name not in only:
            continue
        with open(os.path.join(PUB, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)
