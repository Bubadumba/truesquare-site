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

# ===== calc-v1: price calculator for Meta W23 (Shtab task 27.11, owner 27.11 23:04; v2 after the 7-round council 28.11) =====
# First screen = headline + the first question in a light card. Pictures sit ON the answers (icons, same-scale floor plans,
# example photos), nothing depends on hover. The price is texted, not shown before the phone (owner 27.11 23:04).
import json, re as _re
PRICES = json.load(open(os.path.join(ROOT, "tools", "calc", "prices.json"), encoding="utf-8"))
_LP = open(os.path.join(PUB, "js", "lp.js"), encoding="utf-8").read()
AREA = _re.search(r"var AREA='([0-9,]+)'", _LP).group(1)  # service-area ZIPs: same list as lp.js (read-only)
CONSENT = ("By tapping Text Me My Estimate, you agree TrueSquare Remodel LLC may text and call you about your request at the number "
           "you entered. Msg &amp; data rates may apply. Reply STOP to opt out.")
INK, CORAL = "#20242A", "#B54735"

def _svg(body, vb="0 0 48 48", cls="cqico"):
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

ICONS = {
    "full": _svg(f'<rect x="8" y="6" width="14" height="12" rx="2" stroke="{CORAL}"/><rect x="5" y="24" width="20" height="13" rx="2"/><path d="M5 28h20M8 37v4M22 37v4M15 24v-3h3"/>'
                 '<rect x="30" y="13" width="12" height="9" rx="1.5"/><path d="M28.5 25h15c0 5.5-3.2 8.5-7.5 8.5s-7.5-3-7.5-8.5zM32.5 33.5l-.8 7.5h8.6l-.8-7.5"/>'),
    "tub": _svg(f'<path d="M3 25h18v5a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M6 35l-1 3M18 35l1 3M5 25v-8a3 3 0 0 1 6 0"/>'
                f'<path d="M23.5 29h6M27 26l3 3-3 3" stroke="{CORAL}"/><rect x="33" y="9" width="12" height="31" rx="1"/><path d="M37 13h4M39 13v-3"/><path d="M37 18v3M41 18v3M39 21v3" stroke="{CORAL}"/>'),
    "shower": _svg(f'<path d="M30 5v6h-6M19 13h10"/><path d="M20 17v3M24 17v4M28 17v3M22 23v3M26 23v3" stroke="{CORAL}"/><rect x="9" y="29" width="30" height="13" rx="1"/><path d="M9 35.5h30M19 29v13M29 29v13"/>'),
    "unsure": _svg(f'<path d="M8 10h32a3 3 0 0 1 3 3v17a3 3 0 0 1-3 3H22l-8 7v-7H8a3 3 0 0 1-3-3V13a3 3 0 0 1 3-3z"/><path d="M20 18a4 4 0 1 1 5.5 3.7c-1 .5-1.5 1.2-1.5 2.3v.5" stroke="{CORAL}"/><circle cx="24" cy="28.5" r=".6" fill="{CORAL}" stroke="{CORAL}"/>'),
}

def plan(w_ft, h_ft, shower=False, unknown=False):
    # top-down floor plan at ONE scale for every tile (4 px per ft, bottom-left aligned) so the size difference is real
    k, W, H = 4.2, 58, 46
    w, h = w_ft * k, h_ft * k
    x0, y0 = 4, H - 2 - h
    if unknown:
        return _svg(f'<rect x="{x0}" y="{H-2-8*k*.8:.1f}" width="{8*k:.1f}" height="{8*k*.8:.1f}" rx="1.5" stroke-dasharray="3 3" stroke="#8B929A"/><text x="{x0+8*k/2:.1f}" y="{H-2-8*k*.4+5:.1f}" text-anchor="middle" font-size="15" font-weight="700" fill="{CORAL}" stroke="none">?</text>', f"0 0 {W} {H}", "cqplan")
    if shower:
        return _svg(f'<rect x="{x0}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1" stroke="{INK}"/><path d="M{x0} {y0+h:.1f}h{w:.1f}" stroke="{CORAL}" stroke-width="2.4"/><circle cx="{x0+w/2:.1f}" cy="{y0+h/2:.1f}" r="1.6" fill="{INK}" stroke="none"/>', f"0 0 {W} {H}", "cqplan")
    tub_w = min(w - 2, 5 * k)
    return _svg(f'<rect x="{x0}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1.2"/>'
                f'<rect x="{x0+1:.1f}" y="{y0+1:.1f}" width="{tub_w:.1f}" height="{2.5*k:.1f}" rx="2" stroke="{CORAL}" stroke-width="1.6"/>'
                f'<circle cx="{x0+w-6:.1f}" cy="{y0+h-7:.1f}" r="2.6" stroke-width="1.6"/><rect x="{x0+w-8.6:.1f}" y="{y0+h-3.4:.1f}" width="5.2" height="2" rx=".6" stroke-width="1.4"/>'
                f'<rect x="{x0+1.5:.1f}" y="{y0+h-5:.1f}" width="9" height="3.6" rx="1" stroke-width="1.4"/>', f"0 0 {W} {H}", "cqplan")

def opt(v, label, hint="", extra="", pic="", cls=""):
    return (f'<button type="button" class="cqopt{(" " + cls) if cls else ""}" data-v="{v}" aria-pressed="false"{extra}>{pic}<span class="cqt"><b>{label}</b>'
            f'{("<small>" + hint + "</small>") if hint else ""}</span><i class="cqchk" aria-hidden="true"></i></button>')

# finish tiers: text = what the price includes [ЖДЁТ РЕШЕНИЯ Сергея: точные включения]; photos only after the owner approves them
TIERS = {
    "full": [("e", "Essential", "Subway tile, stock vanity, chrome fixtures, shower curtain"), ("m", "Mid-range", "Porcelain tile, quartz top, glass shower panel, upgraded fixtures"), ("p", "Premium", "Large-format tile, custom wood vanity, matte black fixtures, glass panel")],
    "shower": [("e", "Essential", "Subway tile, chrome fixtures, framed sliding glass door"), ("m", "Mid-range", "Porcelain tile, recessed niche, frameless glass door"), ("p", "Premium", "Large-format tile, niche, rain head + handheld, frameless glass")],
}
TIER_IMG = os.path.join(PUB, "img", "calc")  # tier photos: /img/calc/{full|shower}-{e|m|p}-330.avif/.webp/.jpg (330x248, 3x of the 110x82 tile) (only when they exist)

def tier_pic(kind, k):
    base = f"/img/calc/{kind}-{k}"
    if not os.path.exists(os.path.join(TIER_IMG, f"{kind}-{k}-330.jpg")):
        return ""
    return (f'<span class="cqph"><picture><source type="image/avif" srcset="{base}-330.avif"><source type="image/webp" srcset="{base}-330.webp">'
            f'<img src="{base}-330.jpg" alt="" width="110" height="82" loading="lazy" decoding="async"></picture><em>Example</em></span>')

def calc_block():
    tiers = ""
    for kind, rows in TIERS.items():
        tiers += f'<span class="cqgrp" data-for="{"full" if kind == "full" else "shower"}">' + "".join(
            opt(k, n, h, pic=tier_pic(kind, k), cls="cqrow") for k, n, h in rows) + "</span>"
    has_photos = "cqhasph" if tier_pic("full", "m") else ""
    prices = json.dumps({k: PRICES[k] for k in ("version", "base", "finish", "extras", "avail", "spread")}, separators=(",", ":"))
    return f"""<section class="hero on-ink cqhero" id="book"><div class="wrap">
  <div class="cqtop">
    <h1>What Will Your Bathroom <span class="grad-text">Remodel Cost?</span></h1>
    <p class="cqsub">Seattle-area prices. Your price range by text within 1 minute of submitting.</p>
    <p class="cqinc"><span>Labor, materials &amp; permits included</span><span>WA sales tax extra</span></p>
  </div>
  <div class="calc" id="calc" data-area="{AREA}">
    <div class="cqnav"><button type="button" class="cqback" id="cqBack" hidden>← Back</button><span class="cqcount">Step <b id="cqNum">1</b> of 6</span><span class="cqbar"><i id="cqProg"></i></span></div>
    <p class="cqdebug" id="cqDebug" hidden></p>

    <div class="cqstep" data-step="type"><h2 class="cqq" tabindex="-1">What are you planning?</h2><div class="cqopts cq2 cqtiles">
      {opt("full", "Full bathroom remodel", pic=ICONS["full"])}{opt("tub", "Tub to walk-in shower", pic=ICONS["tub"])}{opt("shower", "Shower remodel", pic=ICONS["shower"])}{opt("unsure", "Not sure yet", pic=ICONS["unsure"])}
    </div><p class="cqhint">Tap an option to continue</p></div>

    <div class="cqstep" data-step="size" hidden>
      <h2 class="cqq" tabindex="-1"><span data-for="full">How big is your bathroom?</span><span data-for="shower">How big is the shower area?</span></h2>
      <div class="cqopts cq2 cqtiles cqsize">
        <span class="cqgrp" data-for="full">{opt("S", "Small", "About 5 × 8 ft · typical hall bath", pic=plan(8, 5))}{opt("M", "Medium", "About 8 × 8 ft", pic=plan(8, 8))}{opt("L", "Large", "About 10 × 10 ft or larger", pic=plan(10, 10))}{opt("U", "Not sure", "We'll use an average size", pic=plan(0, 0, unknown=True))}</span>
        <span class="cqgrp" data-for="shower">{opt("SS", "Standard", "About the size of a 5-ft tub", pic=plan(5, 2.6, shower=True))}{opt("SL", "Large", "Bigger than a 5-ft tub area", pic=plan(6.5, 3.6, shower=True))}{opt("SU", "Not sure", "We'll use a standard size", pic=plan(0, 0, unknown=True))}</span>
      </div></div>

    <div class="cqstep" data-step="finish" hidden><h2 class="cqq" tabindex="-1">Which finish level do you prefer?</h2><div class="cqopts cq1 {has_photos}">{tiers}</div>
      <p class="cqhint">{"Illustrative examples. Actual materials and selections may vary." if has_photos else "Your choice of materials. You pick the exact items with Serhii later."}</p></div>

    <div class="cqstep" data-step="extras" hidden><h2 class="cqq" tabindex="-1">Any additional upgrades? <small>Select all that apply</small></h2><div class="cqopts cq2 cqx">
      {opt("walkin", "Walk-in shower instead of tub", extra=' data-x="walkin"')}{opt("layout", "Move plumbing fixtures", extra=' data-x="layout"')}{opt("heat", "Heated tile floor", extra=' data-x="heat"')}{opt("double", "Double-sink vanity", extra=' data-x="double"')}{opt("bench", "Built-in shower bench", extra=' data-x="bench"')}{opt("curbless", "Curbless shower entry", extra=' data-x="curbless"')}{opt("grab", "Grab bars", extra=' data-x="grab"')}
    </div><button type="button" class="btn block cqnext" id="cqNext"><span id="cqNextL">No extras - Continue</span> <span class="arr">→</span></button>
      <p class="cqhint">Selected upgrades are included in your estimate.</p></div>

    <div class="cqstep" data-step="start" hidden><h2 class="cqq" tabindex="-1">When would you like to start?</h2><div class="cqopts cq1">
      {opt("m0", "Within the next month", cls="cqline")}{opt("m1", "In 1–3 months", cls="cqline")}{opt("m3", "More than 3 months from now", cls="cqline")}{opt("look", "Just researching prices", cls="cqline")}
    </div><p class="cqhint">It's fine if you don't have a date in mind yet.</p></div>

    <form class="cqstep cqform" data-step="contact" id="cqForm" novalidate data-clarity-mask="True" hidden>
      <p class="cqsum"><span class="cqsuml">Your project</span><span id="cqSum"></span><button type="button" class="cqedit" id="cqEdit">Edit</button></p>
      <h2 class="cqq" tabindex="-1">Your estimate is ready. <span class="cqacc">Where should we text your price range?</span></h2>
      <p class="cqfol">Serhii, the owner, will follow up to answer questions. No obligation.</p>
      <p class="cqfix" id="cqFixNote" hidden>Enter the correct mobile number and tap the button again.</p>
      <div class="fields">
        <label class="f" for="fName">First name<input class="t" id="fName" name="first_name" autocomplete="given-name" autocapitalize="words" autocorrect="off" spellcheck="false" enterkeyhint="next"></label>
        <label class="f" for="fPhone">Mobile number<input class="t" id="fPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel" enterkeyhint="next"></label>
        <label class="f" for="fZip">Project ZIP code<input class="t" id="fZip" name="zip" inputmode="numeric" pattern="[0-9]*" autocomplete="postal-code" maxlength="5" enterkeyhint="send"></label>
        <p class="err" id="fErr" hidden role="alert"></p>
        <button class="btn block" type="submit" id="fSubmit" data-cta="calc"><span id="fLabel">Text Me My Estimate</span> <span class="arr">→</span></button>
        <p class="cqfast">Usually arrives in under 1 minute.</p>
        <p class="legal-mini" id="consentText">{CONSENT} <a href="/privacy" target="_blank">Privacy</a> · <a href="/terms" target="_blank">Terms</a></p>
      </div>
    </form>

    <div class="cqdone" id="cqDone" hidden>
      <div class="dcheck" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
      <p class="big" id="doneHi" tabindex="-1">Check your phone!</p>
      <p class="dwhen">Your bathroom estimate is on its way.<br>We're texting it to <b id="donePhone" class="nw"></b>. <button type="button" class="cqedit" id="cqFix">Wrong number? Edit</button></p>
      <p class="dnum">Usually arrives in under 1 minute.</p>
      <p class="dnext" id="doneWhen">Serhii, the owner, will follow up to answer questions. No obligation.</p>
      <div class="cqcta2"><a class="btn outline" href="sms:{PHONE_T}" data-cta="done-text">Text Us</a><a class="btn outline" href="tel:{PHONE_T}" data-cta="done-call">Call Us</a></div>
      <p class="cqreveal" id="cqReveal" hidden>Didn't get the text? <button type="button" class="cqedit" id="cqRevealBtn">Show my estimate here</button></p>
      <div class="cqshow" id="cqShow" hidden><p class="cqrange" id="cqShowRange"></p><p class="cqalt" id="cqShowAlt"></p><p>Labor, materials and permits included. WA sales tax extra. After a free visit, you get an itemized written price within 5 hours.</p></div>
      <a class="cqsave" href="/truesquare-remodel.vcf" data-cta="save-contact" id="doneSave">Save Serhii's number ↓</a>
    </div>
  </div>
  <p class="cqlic"><span>{stars()}<b>5.0</b> on Google (12)</span><span>Licensed &amp; Bonded · WA L&amp;I <b>{LNI}</b></span></p>
</div></section>
<script>window.TSR_CALC_PRICES={prices};</script>"""

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

def write_lead_prices():
    # keeps functions/api/lead.js on the same price table as the page (server-side recalculation)
    p = os.path.join(ROOT, "functions", "api", "lead.js")
    src = open(p, encoding="utf-8").read()
    table = json.dumps({k: PRICES[k] for k in ("version", "base", "finish", "extras", "avail", "spread")}, separators=(",", ":"))
    out = _re.sub(r"// PRICES-BEGIN\n.*?\n// PRICES-END", "// PRICES-BEGIN\nconst P = " + table + ";\n// PRICES-END", src, flags=_re.S)
    if out != src:
        open(p, "w", encoding="utf-8").write(out)
        print("wrote functions/api/lead.js prices")

if __name__ == "__main__":
    import sys
    write_lead_prices()
    only = sys.argv[1:]
    for name, s in PAGES.items():
        if only and name not in only:
            continue
        with open(os.path.join(PUB, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)
