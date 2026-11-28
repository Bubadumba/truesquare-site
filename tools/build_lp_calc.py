# build_lp_calc.py: standalone builder for /bathroom-remodel-cost-calc (calc-v1, Meta W23 price calculator, 27.11).
# A copy of the V3 shell (build_lp_v3.py) on purpose: V3, Q and the other landings are never touched by this file (owner rule 27.11).
#!/usr/bin/env python3
"""Landing pages for Meta ads. Separate from build.py on purpose: it never touches
the main site pages, shared CSS/JS or sitemap.

    python3 tools/build_lp.py

Writes: public/bathroom-remodel-cost.html (M0), public/bathroom-remodel-guarantee.html (M1),
public/guarantee-terms.html. All noindex, none in sitemap.
"""
import os, html
import profiles  # profiles on other sites (owner 30.10)
from pixel import HEAD_PIXEL  # Meta Pixel in <head> (owner 17.11)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
SITE = "https://truesquareremodel.com"
PHONE_T, PHONE = "+12062222328", "(206) 222-2328"
LNI = "TRUESRL759QK"
GOOGLE = "https://www.google.com/maps?cid=7556474326958598816"
THUMBTACK = "https://www.thumbtack.com/wa/seattle/bathroom-remodeling/truesquare-remodel-llc/service/562919809761304593"
V = "1"  # cache version for calc.js (1 = first version 27.11). Old note copied from V3: lp.js (15 = consent text from the phone hint when there is no consent block + minimal thank-you, 02.11; 14 = lp_variant + W3 tile picked by the server, 02.11; 12 = landing split variant on every event, 29.10; 11 = form_source + Clarity + CAPI)
RANGE = "$16,000–$28,500"
CAPTION = os.environ.get("TSR_CAP", "a")  # crew-photo caption variant for preview: a | b [ЖДЁТ РЕШЕНИЯ]
CAPTIONS = {
    "a": "Past work completed by our subcontractor's crew before TrueSquare Remodel LLC.",
    "b": "Real bathroom remodel by the subcontractor crew that works on TrueSquare projects.",
}
CAP = CAPTIONS[CAPTION]

def esc(s): return html.escape(s, quote=True)

PHONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
SVG_DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F69A72"/><stop offset=".5" stop-color="#F47A61"/><stop offset="1" stop-color="#EC6463"/></linearGradient>
<symbol id="star" viewBox="0 0 24 24"><path d="M12 2l3 6.9 7.5.6-5.7 4.9 1.8 7.3L12 17.8 5.4 21.7l1.8-7.3L1.5 9.5 9 8.9z"/></symbol>
<symbol id="chk" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="#121314" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</defs></svg>"""

FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;600;700&family=Caveat:wght@600&display=swap"

FONT_FACES = ('@font-face{font-family:"Bricolage Grotesque";font-style:normal;font-weight:700 800;font-display:swap;src:url(/fonts/bricolage-700-800.woff2) format("woff2")}'
              '@font-face{font-family:"Inter";font-style:normal;font-weight:400 700;font-display:swap;src:url(/fonts/inter-400-700.woff2) format("woff2")}')

def css_inline():
    # read-only use of the shared site.css; landing extras from lp.css
    import re
    out = []
    for f in (os.path.join(PUB, "css", "site.css"), os.path.join(ROOT, "tools", "css", "lp-calc.css")):
        with open(f, encoding="utf-8") as fh:
            c = fh.read()
        c = re.sub(r"/\*.*?\*/", "", c, flags=re.S)
        c = re.sub(r"\s*\n\s*", "", c)
        out.append(c)
    return "".join(out)

def shell(path, title, desc, angle, body, preload=None, body_class="lp", sticky_label="Get My Price", footer_html=None, variant=""):
    CSS = css_inline()
    # speed pass 03.11: the first-screen photo is the LCP on V3 since the short first screen; preload it first, AVIF only
    PRE = (f'<link rel="preload" as="image" href="{preload}-760.avif" imagesrcset="{preload}-480.avif 480w, {preload}-760.avif 760w" '
           f'imagesizes="{BAND_SIZES}" type="image/avif" fetchpriority="high">\n') if preload and "." not in preload else ""
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
{PRE}<link rel="preload" href="/fonts/bricolage-700-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-400-700.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONT_FACES}{CSS}</style>
{HEAD_PIXEL}</head>
<body class="{body_class}" data-page="lp-{angle}" data-angle="{angle}"{(' data-variant="' + variant + '"') if variant else ''}>
{SVG_DEFS}

<header class="top"><div class="wrap hbar">
  <a class="logo" href="#top" aria-label="TrueSquare Remodel"><img src="/img/logo.svg" alt="TrueSquare Bathroom Remodeling" width="242" height="60"></a>
  <a class="lp-call" href="tel:{PHONE_T}" data-cta="header-call">{PHONE_ICON}<span class="word">Call</span><span class="num">Call {PHONE}</span></a>
</div></header>

<main id="top">
{body}
</main>

<footer><div class="wrap lpf">
  <span><b>TrueSquare Remodel LLC</b> · WA Registered Contractor · <b>{LNI}</b>{'' if 'lp2' in body_class else ' · <span class="nw">Owner-led</span>'}</span>
  <span><a href="tel:{PHONE_T}">{PHONE}</a> · <!--email_off-->info@truesquareremodel.com<!--/email_off--> · Seattle, WA</span>
  <span class="links"><b style="color:#fff">Find us on:</b>{profiles.footer_links()}</span>
  <span class="links"><a href="/">About TrueSquare</a><a href="/privacy">Privacy Policy</a><a href="/terms">Terms of Service</a></span>
</div></footer>

<div class="sticky" id="sticky" aria-hidden="true">
  <a class="s2" href="tel:{PHONE_T}" data-cta="sticky-call">Call</a>
  <a class="s1" href="#book" data-cta="sticky">{sticky_label}</a>
</div>

<div class="lb" id="lb" hidden role="dialog" aria-label="Photo"><img id="lbImg" alt=""><button type="button" id="lbClose" aria-label="Close">×</button></div>

<script>
/* calc-v1 (27.11): same tag plan as V3 (Pixel + PageView in <head>, GTM/Clarity after the first touch or 4 s). site.js starts at DOMContentLoaded;
   the calculator (calc.js) loads on its own with defer, so the first question works before any tag. calc.js reads WEBHOOK_URL from site.js only at submit. */
window.TSR_TAGS_WAIT=4000;
(function(){{function go(){{var a=document.createElement('script');a.src='/js/site.js?v=14';document.body.appendChild(a);}}
if(document.readyState!=='loading'){{go();}}else addEventListener('DOMContentLoaded',go);}})();
</script>
<script src="/js/calc.js?v={V}" defer></script>
<script src="https://stats.bigresultsai.com/t.js?c=tsr" defer></script>
</body>
</html>
"""

# speed pass 03.11: AVIF + WebP copies (made once with sharp, next to the JPG) in <picture>; the JPG stays as the fallback
BAND_SIZES = "(min-width: 960px) 760px, calc(100vw - 40px)"
def pic(src, alt, w, h, widths, sizes, attrs=""):
    base = src.split("?")[0].rsplit(".", 1)[0]
    def ss(ext): return ", ".join(f"{base}-{x}.{ext} {x}w" for x in widths)
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="{src}" alt="{alt}" width="{w}" height="{h}"{attrs}></picture>')

def stars():
    return '<span class="st" aria-hidden="true"><svg><use href="#star"/></svg></span>'

TRUST = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "partials", "trust.html"), encoding="utf-8").read().strip()  # rating badge + secure shield under every form
def chk(t): return f'<li><span class="tick"><svg><use href="#chk"/></svg></span>{t}</li>'

# ===== calc-v1: price calculator for Meta W23 (Shtab task 27.11, owner 27.11 23:04) =====
# First screen = the bathroom picture + the first question. The price is texted, not shown before the phone (owner 27.11 23:04).
CONSENT = ("By tapping Text Me My Estimate, you agree TrueSquare Remodel LLC may text and call you about your request at the number "
           "you entered. Msg &amp; data rates may apply. Reply STOP to opt out.")

def opt(v, label, hint="", extra=""):
    return (f'<button type="button" class="cqopt" data-v="{v}" aria-pressed="false"{extra}><b>{label}</b>'
            f'{("<small>" + hint + "</small>") if hint else ""}</button>')

def calc_block():
    sw = lambda c: f'<i class="sw" style="background:{c}"></i>'
    styles = {"modern": ("Modern", "#7A4E33,#1F1F1F,#FBFBFA"), "classic": ("Classic", "#2C3E57,#B9C1C9,#FFFFFF"),
              "warm": ("Warm natural", "#C29567,#B98A3E,#E9D7C1"), "spa": ("Dark spa", "#4C5156,#C8A468,#D2BC9C")}
    style_opts = "".join(opt(k, f'<span class="sws">{"".join(sw(c) for c in cs.split(","))}</span>{n}', extra=' data-k="style"') for k, (n, cs) in styles.items())
    return f"""<section class="hero on-ink cqhero" id="book"><div class="wrap">
  <div class="calc" id="calc">
    <div class="cqhead">
      <h1>Bathroom Remodel <span class="grad-text">Price Calculator</span></h1>
      <p class="cqsub">7 quick taps. Your price by text in 1 minute.</p>
    </div>
    <figure class="cqfig"><div class="cqviz" aria-hidden="true"></div><figcaption><span class="cqtag"></span><span class="cqill">Illustration</span></figcaption></figure>
    <p class="cqdebug" id="cqDebug" hidden></p>
    <div class="cqnav hcta"><button type="button" class="cqback" id="cqBack" hidden>← Back</button><span class="cqcount">Step <b id="cqNum">1</b> of 7</span><span class="cqbar"><i id="cqProg"></i></span></div>

    <fieldset class="cqstep" data-step="type"><legend tabindex="-1">What are you planning?</legend><div class="cqopts">
      {opt("full", "Full bathroom remodel")}{opt("tub", "Tub to walk-in shower")}{opt("shower", "Shower remodel", "New tile and pan")}{opt("unsure", "Not sure yet")}
    </div></fieldset>

    <fieldset class="cqstep" data-step="size" hidden><legend tabindex="-1">How big is the bathroom?</legend><div class="cqopts">
      <span data-for="full" class="cqgrp">{opt("S", "Small", "Up to 40 sq ft, about 5×8")}{opt("M", "Medium", "40–70 sq ft")}{opt("L", "Large", "70+ sq ft, primary bath")}{opt("U", "Not sure")}</span>
      <span data-for="shower" class="cqgrp">{opt("SS", "Standard", "Fits the old 5 ft tub space")}{opt("SL", "Larger", "Bigger than 5 ft")}</span>
    </div></fieldset>

    <fieldset class="cqstep" data-step="style" hidden><legend tabindex="-1">Which style do you like?</legend><div class="cqopts">{style_opts}</div></fieldset>

    <fieldset class="cqstep" data-step="finish" hidden><legend tabindex="-1">Quality of materials?</legend><div class="cqopts cq1">
      {opt("e", "Essential", "Simple tile, stock vanity")}{opt("m", "Mid-range", "Most popular. Porcelain tile, frameless glass")}{opt("p", "Premium", "Large tile, floating vanity, designer fixtures")}
    </div></fieldset>

    <fieldset class="cqstep" data-step="extras" hidden><legend tabindex="-1">Anything extra? <small>Pick any or none</small></legend><div class="cqopts cqx">
      {opt("walkin", "Walk-in shower instead of tub", extra=' data-x="walkin"')}{opt("layout", "Move toilet, shower or vanity", extra=' data-x="layout"')}{opt("heat", "Heated floor", extra=' data-x="heat"')}{opt("double", "Double vanity", extra=' data-x="double"')}{opt("bench", "Shower bench", extra=' data-x="bench"')}{opt("curbless", "No-step shower entry", extra=' data-x="curbless"')}{opt("grab", "Grab bars", extra=' data-x="grab"')}
    </div><button type="button" class="btn block cqnext" id="cqNext"><span id="cqNextL">No extras, continue</span> <span class="arr">→</span></button></fieldset>

    <fieldset class="cqstep" data-step="start" hidden><legend tabindex="-1">When do you want to start?</legend><div class="cqopts">
      {opt("asap", "As soon as possible")}{opt("m1", "In 1–3 months")}{opt("m3", "In 3+ months")}{opt("look", "Just checking prices")}
    </div></fieldset>

    <form class="cqstep cqform" data-step="contact" id="cqForm" novalidate data-clarity-mask="True" hidden>
      <h2 tabindex="-1">Your estimate is ready. <span class="grad-text">Where should we text it?</span></h2>
      <p class="cqmin"><b>Your price arrives by text within 1 minute.</b></p>
      <div class="fields">
        <label class="f" for="fName">Full name<input class="t" id="fName" name="full_name" autocomplete="name" autocapitalize="words" autocorrect="off" spellcheck="false" enterkeyhint="next"></label>
        <label class="f" for="fPhone">Mobile number<input class="t" id="fPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel" enterkeyhint="next"></label>
        <label class="f" for="fZip">ZIP code<input class="t" id="fZip" name="zip" inputmode="numeric" pattern="[0-9]*" autocomplete="postal-code" maxlength="5" enterkeyhint="send"></label>
        <p class="err" id="fErr" hidden></p>
        <button class="btn block" type="submit" id="fSubmit" data-cta="calc"><span id="fLabel">Text Me My Estimate</span> <span class="arr">→</span></button>
        <p class="legal-mini" id="consentText">{CONSENT} <a href="/privacy" target="_blank">Privacy</a> · <a href="/terms" target="_blank">Terms</a></p>
        {TRUST}
      </div>
    </form>

    <div class="cqdone" id="cqDone" hidden>
      <div class="dcheck" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
      <p class="big" id="doneHi" tabindex="-1">Check your phone!</p>
      <p class="dwhen">Your estimate is on its way by text to <b id="donePhone" class="nw"></b>.</p>
      <p class="dnum">No text in 2 minutes? Text us at <a href="sms:{PHONE_T}" class="nw">{PHONE}</a>.</p>
      <p class="dnext" id="doneWhen">Serhii will call you to confirm the details and set up a free visit.</p>
      <a class="btn block" href="/truesquare-remodel.vcf" data-cta="save-contact" id="doneSave">Save Serhii's Number <span class="arr">↓</span></a>
    </div>

    <p class="cqlic"><span>{stars()}<b>5.0</b> Google (12) · Thumbtack (24)</span><span>Licensed &amp; Bonded · WA L&amp;I <b>{LNI}</b></span></p>
  </div>
</div></section>"""

def calc_page():
    def ph(full, img, alt, w, h):
        return f'<button class="ph" type="button" data-full="{full}">{pic(img, alt, w, h, [w], "150px", ' loading="lazy"')}</button>'
    work = f"""<section class="v2work v3work"><div class="wrap">
  <div class="head"><p class="kicker">Before &amp; after</p><h2>From Dated <span class="grad-text">to Done.</span></h2></div>
  <figure class="v3cmp" style="--pos:40%">
    {pic("/img/p/ill-after.jpg?v=2", "After: the same bathroom with a walk-in glass shower, vertical white tile, walnut floating vanity and a round black mirror", 931, 698, [700, 931], BAND_SIZES, ' class="v3cmp-a" loading="lazy"')}
    <div class="v3cmp-b">{pic("/img/p/ill-before.jpg?v=2", "Before: a dated bathroom with an almond tub-shower combo, oak vanity and brass fixtures", 931, 698, [700, 931], BAND_SIZES, ' loading="lazy"')}</div>
    <span class="v3tag v3tag-b" aria-hidden="true">Before</span><span class="v3tag v3tag-a" aria-hidden="true">After</span>
    <span class="v3knob" aria-hidden="true"></span>
    <input type="range" min="0" max="100" value="40" aria-label="Drag to compare before and after" oninput="this.parentNode.style.setProperty('--pos',this.value+'%')">
  </figure>
  <p class="v3cmpcap">Drag to compare. Example of a typical full remodel.</p>
  <h3 class="v3real">Bathrooms completed by our crew</h3>
  <div class="v3swipe">
    {ph("/img/lp-hero.jpg", "/img/lp-hero-sq.jpg", "Finished walk-in shower with glass door, vanity and toilet", 360, 360)}
    {ph("/img/p/b18.jpg", "/img/p/b18-sq.jpg", "Floating vanity with vessel sink, black mirror and toilet", 360, 360)}
    {ph("/img/p/b05.jpg", "/img/p/b05-sq.jpg", "Shower floor in black hexagon tile with white wall tile", 300, 300)}
    {ph("/img/g-glass-corner.jpg", "/img/g-glass-corner-sq.jpg", "Corner shower with a frameless glass enclosure", 300, 300)}
  </div>
  <p class="v3swipenote" aria-hidden="true">Swipe for more photos →</p>
</div></section>"""
    written = f"""<section class="alt v2written"><div class="wrap">
  <div class="head"><p class="kicker">After the estimate</p><h2>Your Estimate. <span class="grad-text">Then It's in Writing.</span></h2><p class="lead">The calculator gives you a range. After a free visit, you get an itemized written price within 5 hours. Extra work needs your written OK.</p></div>
  <div class="panel">
    <div class="ph-head"><img src="/img/logo.svg" alt="TrueSquare" width="105" height="26" loading="lazy"><b>Example Written Scope</b></div>
    <ul class="checks">
      {chk("Demolition and haul-away")}
      {chk("Waterproofing")}
      {chk("Plumbing and electrical, with permits where required")}
      {chk("Tile, vanity, fixtures and glass")}
      {chk("Cleanup")}
      {chk("1-year written workmanship warranty")}
      {chk("WA sales tax shown separately")}
    </ul>
    <p class="exnote">Example only. Your written price follows the free visit.</p>
  </div>
  <div class="v3mid"><a class="btn block" href="#book" data-cta="scope">Get My Price <span class="arr">→</span></a><p class="v3midunder">7 quick taps. Price by text in 1 minute.</p></div>
</div></section>"""
    owner = f"""<section class="owner on-ink v2owner"><div class="wrap">
  <div class="v2own">
    {pic("/img/serhii-ts-wide.jpg", "Serhii, owner of TrueSquare Remodel", 744, 408, [744], BAND_SIZES, ' loading="lazy"')}
    <div>
      <p class="kicker">Your contact</p>
      <h2>No Sales Reps. <span class="grad-text">Just Serhii.</span></h2>
    </div>
  </div>
  <p class="lead">Serhii, the owner, visits to measure your bathroom and stays your contact by phone or text throughout the project. He coordinates the work with our subcontractor crew, who handle the construction.</p>
  <ol class="v2steps">
    <li><span class="n">1</span>Get your price range by text</li>
    <li><span class="n">2</span>Free visit: Serhii measures the room</li>
    <li><span class="n">3</span>Written price within 5 hours after the visit</li>
  </ol>
  <div class="v3rev">
    <blockquote><p class="st5" role="img" aria-label="5 out of 5 stars">★★★★★</p><p>“I had TrueSquare handle my outdated bathroom in Lynnwood, and wow, what a difference! Sergey and the crew were friendly and really listened to my ideas, turning a cramped space into something open and modern…”</p><cite>Artyom S. · Google review</cite></blockquote>
    <blockquote><p class="st5" role="img" aria-label="5 out of 5 stars">★★★★★</p><p>“From the first time we talked, I didn't feel pressured to hire them, but I'm really glad I did. Sergey and Andrew did an awesome job… They were super professional and worked really hard.”</p><cite>Vitaliy S. · Google review</cite></blockquote>
    <a class="v3revall" href="{GOOGLE}" target="_blank" rel="noopener">Read all reviews on Google →</a>
  </div>
</div></section>"""
    faq_items = [
        ("How accurate is the calculator?", "It gives a realistic range for a bathroom like the one you picked: labor, materials and permits included, WA sales tax extra. Your exact price comes in writing within 5 hours after a free visit, because the layout and what's behind the walls change the number."),
        ("Will the price jump once the walls are open?", "Only if we find hidden damage or you change the scope. We stop, show you photos, and give you a written price. Nothing happens without your written OK."),
        ("Are you the one swinging the hammer?", "No. Our subcontractor crew does the construction. Serhii coordinates the project and is your phone/text contact."),
        ("Do I pay everything up front?", "No. You pay a deposit at signing, another payment after the rough-in inspection, and the final payment after the walkthrough."),
        ("How long will I be without a bathroom?", "Typically 1–3 weeks of construction, depending on scope and what we find. You get the start date in writing."),
        ("What if something fails after you leave?", "You get a 1-year written workmanship warranty, plus the manufacturer warranties on fixtures and materials."),
    ]
    faq = """<section id="faq" class="v2faq"><div class="wrap">
  <div class="head"><p class="kicker">Straight answers</p><h2>Ask Us the <span class="grad-text">Awkward Questions.</span></h2></div>
  <div class="faq">
""" + "\n".join(f"    <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items) + """
  </div>
</div></section>"""
    final = f"""<section class="alt final"><div class="wrap">
  <h2>What Would <span class="grad-text">Your Bathroom</span> Cost?</h2>
  <a class="btn" href="#book" data-cta="final">Get My Price <span class="arr">→</span></a>
  <p class="v3first">7 quick taps. Price by text in 1 minute.</p>
  <p class="or">or call <a href="tel:{PHONE_T}">{PHONE}</a></p>
</div></section>"""
    body = "\n".join([calc_block(), work, written, owner, faq, final])
    return shell("/bathroom-remodel-cost-calc", "Bathroom Remodel Price Calculator, Seattle Area | TrueSquare",
                 "Pick your bathroom, style and materials. Get your price range by text in 1 minute. Licensed & Bonded, WA L&I TRUESRL759QK.",
                 "calc-v1", body, body_class="lp lp2 lp3 lpcalc", sticky_label="Get My Price", variant="calc")

PAGES = {"bathroom-remodel-cost-calc.html": calc_page()}

if __name__ == "__main__":
    import sys
    only = sys.argv[1:]
    for name, s in PAGES.items():
        if only and name not in only:
            continue
        with open(os.path.join(PUB, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)
