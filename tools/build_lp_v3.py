# build_lp_v3.py: standalone builder for /bathroom-remodel-cost-v3 (love-v3).
# Copied from branch love-v3-preview so main's tools/build_lp.py and the other landings stay untouched.
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
V = "10"  # cache version for lp.js (10 = two-step form, 28.10; 9 = new thank-you state, 26.10)
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
    for f in (os.path.join(PUB, "css", "site.css"), os.path.join(ROOT, "tools", "css", "lp-v3.css")):
        with open(f, encoding="utf-8") as fh:
            c = fh.read()
        c = re.sub(r"/\*.*?\*/", "", c, flags=re.S)
        c = re.sub(r"\s*\n\s*", "", c)
        out.append(c)
    return "".join(out)

def shell(path, title, desc, angle, body, preload=None, body_class="lp", sticky_label="Get My Price", footer_html=None):
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
{PRE}<link rel="preload" href="/fonts/bricolage-700-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-400-700.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONT_FACES}{CSS}</style>
</head>
<body class="{body_class}" data-page="lp-{angle}" data-angle="{angle}">
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
  <span><a href="tel:{PHONE_T}">{PHONE}</a> · info@truesquareremodel.com · Seattle, WA</span>
  <span class="links"><a href="/">About TrueSquare</a><a href="/privacy">Privacy Policy</a><a href="/terms">Terms of Service</a></span>
</div></footer>

<div class="sticky" id="sticky" aria-hidden="true">
  <a class="s2" href="tel:{PHONE_T}" data-cta="sticky-call">Call</a>
  <a class="s1" href="#book" data-cta="sticky">{sticky_label}</a>
</div>

<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheetTitle" hidden>
  <div class="sheet-panel" id="sheetPanel">
    <div class="sheet-head">
      <p class="sheet-title" id="sheetTitle" tabindex="-1">Get Your <span class="grad-text">Written Price</span></p>
      <button type="button" class="sheet-x" id="sheetClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="v3who sheet-who"><img src="/img/serhii-avatar.jpg" alt="" width="44" height="44" loading="lazy"><p><b>Serhii will call you to set a time.</b><span>Starts with a free visit. No decision at the visit.</span></p></div>
    <div class="sheet-body" id="sheetBody"></div>
  </div>
</div>

<div class="lb" id="lb" hidden role="dialog" aria-label="Photo"><img id="lbImg" alt=""><button type="button" id="lbClose" aria-label="Close">×</button></div>

<script>
/* analytics + shared behavior load after the page has painted (keeps LCP fast) */
(function(){{function go(){{var a=document.createElement('script');a.src='/js/site.js?v=8';a.onload=function(){{var b=document.createElement('script');b.src='/js/lp.js?v={V}';document.body.appendChild(b);}};document.body.appendChild(a);}}
if(document.readyState==='complete'){{go();}}else addEventListener('load',go);}})();
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

def hero_love():
    def li(t): return f'<li><span class="tick"><svg><use href="#chk"/></svg></span>{t}</li>'
    return f"""<section class="hero on-ink">
  <div class="wrap hgrid">
    <div class="htext">
      <p class="kicker">Seattle-area bathroom remodeling</p>
      <h1>Love the House. <span class="grad-text">Not the Bathroom?</span></h1>
      <p class="hrange">Full Bathroom Remodels: <b class="nw">{RANGE}</b> + WA sales tax<small>Smaller bathrooms fall at the lower end. Price depends on scope.</small></p>
      <ul class="hlist">
        {li("Itemized written scope and price within 5 hours after your visit — yours to keep")}
        {li("One phone/text contact from first visit to final walkthrough")}
        {li("Your written OK before any extra work")}
      </ul>
      <div class="hcta">
        <a class="btn" href="#book" data-cta="hero">Request My Free Bathroom Visit <span class="arr">→</span></a>
      </div>
      <p class="under">No decision required at the visit.</p>
      <div class="trust" aria-label="Why homeowners trust us">
        <div class="rate">
          <a href="{GOOGLE}" target="_blank" rel="noopener">{stars()}<b>5.0</b> Google (12 reviews) <small>↗</small></a>
          <span class="sep" aria-hidden="true"></span>
          <a href="{THUMBTACK}" target="_blank" rel="noopener">{stars()}<b>5.0</b> Thumbtack (24 reviews) <small>↗</small></a>
        </div>
        <p class="lic-line">WA Registered Contractor · <b>{LNI}</b><br>1-year written workmanship warranty</p>
      </div>
    </div>
    <figure class="hphoto">
      <div class="in"><img src="/img/lp-hero.jpg" srcset="/img/lp-hero-460.jpg 460w, /img/lp-hero.jpg 675w" sizes="(min-width:960px) 520px, 92vw" alt="Finished full bathroom remodel: glass walk-in shower, vanity and new tile" width="675" height="844" fetchpriority="high" decoding="async"><figcaption class="cap-over">{CAP}</figcaption></div>
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

WORK = f"""<section id="work"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Real Bathrooms, Before and After</h2><p class="cap-note">{CAP}</p></div>
  <div class="gal">
    <button class="ph main" type="button" data-full="/img/p/b06.jpg"><img src="/img/p/b06.jpg" alt="Full bathroom remodel: new vanity, toilet, mirror, lighting and floor tile" loading="lazy" width="675" height="1200" style="object-position:50% 72%"></button>
    <button class="ph s" type="button" data-full="/img/p/b13.jpg"><img src="/img/p/b13.jpg" alt="Full bathroom remodel: double vanity, lit mirror and large-format tile" loading="lazy" width="900" height="1200"></button>
    <button class="ph s" type="button" data-full="/img/p/b18.jpg"><img src="/img/p/b18.jpg" alt="Full bathroom remodel: floating vanity, vessel sink, toilet and new lighting" loading="lazy" width="900" height="1200"></button>
  </div>
</div></section>"""

TRUST = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "partials", "trust.html"), encoding="utf-8").read().strip()  # rating badge + secure shield under every form

def form_section(show_lic=True, h2='Get Your <span class="grad-text">Written Price</span>', lead="Tell us what you're planning. Serhii will call to set up your free visit.", extra="", submit="Request My Free Visit", who="", tile_opts=None, tile_help="", phone_label="Mobile phone", consent_name="TrueSquare Remodel", steps=False):
    # a tile is "value" or ("value", "small hint"); the value is what goes to GHL as project_type
    def _tile(t):
        v, hint = (t if isinstance(t, tuple) else (t, ""))
        label = v.replace("tub-to-shower", '<span class="nw">tub-to-shower</span>')
        return f'<button type="button" class="tile" data-v="{v}" aria-pressed="false">{label}{("<small>" + hint + "</small>") if hint else ""}</button>'
    tiles = "".join(_tile(t) for t in (tile_opts or ["Full bathroom remodel", "Tub to walk-in shower", "Shower remodel", "Not sure yet"]))
    # two-step form (decision 28.10, V3 only): step 1 = tiles, a tap opens step 2 = name / phone / ZIP
    fcls = "form steps" if steps else "form"
    step1 = '\n      <p class="fstep">Step 1 of 2</p>' if steps else ""
    chosen = '\n      <p class="fchosen" id="fChosen"><span>Step 2 of 2 ·</span> <b id="fChoice"></b> <button type="button" class="fback" id="fBack">Change</button></p>' if steps else ""
    trust_in, trust_out = ("", "\n      " + TRUST) if steps else (TRUST, "")
    return f"""<section class="book on-ink" id="book"><div class="wrap bgrid">
  <div>
    <p class="kicker">Free visit</p>
    <h2 style="margin-top:10px">{h2}</h2>
    <p class="lead" style="margin-top:10px">{lead}</p>{extra}{who}
    <p class="callline">Prefer to talk? Call <a href="tel:{PHONE_T}">{PHONE}</a></p>
    {'<p class="formlic">WA Registered Contractor · <b>' + LNI + '</b> · <span class="nw">Owner-led</span></p>' if show_lic else ''}
  </div>
  <form class="{fcls}" id="lpForm" novalidate>
    <div id="formBody">{step1}
      <fieldset>
        <legend>What are you planning?</legend>{('<p class="thelp">' + tile_help + '</p>') if tile_help else ''}
        <div class="tiles" id="tiles">{tiles}</div>
      </fieldset>{chosen}
      <div class="fields">
        <label class="f" for="fName">Full name<input class="t" id="fName" name="full_name" autocomplete="name" autocapitalize="words" autocorrect="off" spellcheck="false" enterkeyhint="next"></label>
        <label class="f" for="fPhone">{phone_label}<input class="t" id="fPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel" enterkeyhint="next"><span class="why">We'll call or text only about your visit.</span></label>
        <label class="f" for="fZip">ZIP code<input class="t" id="fZip" name="zip" inputmode="numeric" pattern="[0-9]*" autocomplete="postal-code" maxlength="5" enterkeyhint="send"></label>
                <p class="err" id="fErr" hidden></p>
        <button class="btn block" type="submit" id="fSubmit" data-cta="form"><span id="fLabel">{submit}</span> <span class="arr">→</span></button>
        <p class="legal-mini" id="consentText">By tapping {submit}, you agree {consent_name} may call and text you about your request at the number you entered. Msg &amp; data rates may apply. Reply STOP to opt out. <a href="/privacy" target="_blank">Privacy Policy</a> · <a href="/terms" target="_blank">Terms</a></p>
        <p class="next">No payment. No obligation.</p>
        {trust_in}
      </div>{trust_out}
    </div>
    <div class="done v3done" id="formDone" hidden>
      <div class="dcheck" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
      <p class="big" id="doneHi">Thanks! Your request is in.</p>
      <p class="dwhen" id="doneWhen">Serhii will call you shortly to set up your free visit.</p>
      <p class="dnum" id="doneNum" hidden>We'll call <b id="donePhone"></b>. Wrong number? Call or text <a href="tel:{PHONE_T}" class="nw">{PHONE}</a>.</p>
      <ol class="dsteps">
        <li><span class="n">1</span>Serhii calls to set a time</li>
        <li><span class="n">2</span>Free visit: we discuss and measure your bathroom</li>
        <li><span class="n">3</span>Your written price within 5 hours after the visit</li>
      </ol>
      <a class="btn block" href="/truesquare-remodel.vcf" data-cta="save-contact" id="doneSave">Save Our Number <span class="arr">↓</span></a>
      <p class="dtip">So you know it's us when we call.</p>
      <a class="dcall" href="tel:{PHONE_T}" data-cta="done-call">Or call now: <span class="nw">{PHONE}</span></a>
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
  <div class="ophoto"><img src="/img/serhii.jpg?v=2" alt="Serhii, owner of TrueSquare Remodel" loading="lazy" width="1024" height="1536"></div>
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
    ("Who will I deal with?", "Serhii is your phone/text contact from the first visit to the final walkthrough. Our subcontractor crew does the work. Any extra work needs your written OK first."),
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

def landing(path, angle, sub, under, title, hero_html=None):
    body = "\n".join([hero_html or hero(sub, under), FACTORS, WORK, form_section(), WRITTEN, OWNER, STEPS, FAQ, FINAL])
    return shell(path, title, f"Full bathroom remodels in the Seattle area: {RANGE}, plus WA sales tax, scope dependent. Free visit, itemized written price within 5 hours.", angle, body, preload="/img/lp-hero.jpg")

# ---------------------------------------------------------------- V2 TEST LANDING (board review 26.10, love-v2)
V2_CAP_ONE = "The subcontractor crew we work with completed this bathroom."  # [ЖДЁТ РЕШЕНИЯ Сергея: подтвердить]
V2_CAP_MANY = "The subcontractor crew we work with completed these bathrooms."

def v2_page():
    def li(t): return f'<li><span class="tick"><svg><use href="#chk"/></svg></span>{t}</li>'
    hero = f"""<section class="hero on-ink v2hero">
  <div class="wrap">
    <p class="kicker">Seattle-area bathroom remodels</p>
    <h1>Love the House. <span class="grad-text">Not the Bathroom?</span></h1>
    <p class="hrange">Full Bathroom Remodels: <b class="nw">{RANGE}</b> + WA sales tax<small>Smaller bathrooms fall at the lower end. Price depends on scope.</small></p>
    <ul class="hlist">
      {li("Itemized written scope and price within 5 hours after your visit")}
      {li("One phone/text contact throughout your project")}
      {li("Your written OK before extra work")}
    </ul>
    <div class="hcta"><a class="btn block" href="#book" data-cta="hero">Request My Free Visit <span class="arr">→</span></a></div>
    <p class="under">No decision required at the visit.</p>
  </div>
</section>"""
    trust = f"""<section class="v2trust"><div class="wrap">
  <div class="tline rates">
    <a href="{GOOGLE}" target="_blank" rel="noopener"><i>{stars()}<b>5.0</b> Google</i><span>12 reviews</span></a>
    <a href="{THUMBTACK}" target="_blank" rel="noopener"><i>{stars()}<b>5.0</b> Thumbtack</i><span>24 reviews</span></a>
  </div>
  <div class="tline facts"><span>WA Registered Contractor · <b>{LNI}</b></span><span>1-year written workmanship warranty</span></div>
  <figure class="v2photo"><button class="ph" type="button" data-full="/img/p/b13.jpg"><img src="/img/p/b13.jpg" alt="Remodeled bathroom with a double vanity and a large lit mirror" width="900" height="1200" decoding="async"><span class="zoom" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5M11 8v6M8 11h6"/></svg></span></button>
    <figcaption>{V2_CAP_ONE}</figcaption></figure>
</div></section>"""
    form = form_section(show_lic=False, h2='Request Your <span class="grad-text">Free Bathroom Visit</span>',
                        lead="We'll call to schedule your free visit. Your itemized written scope and price follow within 5 hours after the visit.")
    work = f"""<section class="v2work"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Bathrooms Completed by Our Subcontractor Crew</h2></div>
  <div class="v2gal">
    <button class="ph" type="button" data-full="/img/lp-hero.jpg"><img src="/img/lp-hero-460.jpg" alt="Finished walk-in shower with glass door, vanity and toilet" loading="lazy" width="460" height="575"></button>
    <button class="ph" type="button" data-full="/img/p/b18.jpg"><img src="/img/p/b18.jpg" alt="Floating vanity with vessel sink, black mirror and toilet" loading="lazy" width="900" height="1200"></button>
  </div>
  <p class="v2cap">{V2_CAP_MANY}</p>
</div></section>"""
    written = f"""<section class="alt v2written"><div class="wrap">
  <div class="head"><p class="kicker">On paper</p><h2>What You Get in Writing</h2><p class="lead">Your itemized scope lists the planned work, materials and total price before you decide.</p></div>
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
    <p class="exnote">Example only. Your itemized price follows the free visit.</p>
  </div>
</div></section>"""
    owner = """<section class="owner on-ink v2owner"><div class="wrap">
  <div class="v2own">
    <img src="/img/serhii.jpg?v=2" alt="Serhii, owner of TrueSquare Remodel" loading="lazy" width="1024" height="1536">
    <div>
      <p class="kicker">Your contact</p>
      <h2>One Person to Call, <span class="grad-text">Start to Finish</span></h2>
    </div>
  </div>
  <p class="lead">Serhii, the owner, visits to measure your bathroom and stays your contact by phone or text throughout the project. He coordinates the work with our subcontractor crew, who handle the construction.</p>
  <ol class="v2steps">
    <li><span class="n">1</span>Request your free visit</li>
    <li><span class="n">2</span>Discuss and measure your bathroom</li>
    <li><span class="n">3</span>Get your written price within 5 hours after the visit</li>
  </ol>
</div></section>"""
    faq_items = [
        ("Can I get an exact price before the visit?", f"The {RANGE} range is not a quote for your home, and WA sales tax is extra. Your itemized written price follows within 5 hours after the free visit."),
        ("What happens if you find hidden damage?", "We'll explain the issue and give you a price for extra work in writing. Nothing extra starts without your written OK."),
        ("Who does the remodeling work?", "Our subcontractor crew does the construction. Serhii coordinates the project and is your phone/text contact."),
        ("How do payments work?", "You pay a deposit at signing, another payment after the rough-in inspection, and the final payment after the walkthrough."),
        ("How long does construction take, and what is the warranty?", "Construction typically takes 2–4 weeks, depending on scope. There's a 1-year written workmanship warranty."),
    ]
    faq = """<section id="faq" class="v2faq"><div class="wrap">
  <div class="head"><p class="kicker">Your price</p><h2>What Changes Your Bathroom Remodel Price?</h2><p class="lead">Layout changes, materials and finishes, and hidden damage can affect the final price. Larger or more complex projects may exceed the listed range.</p></div>
  <div class="faq">
""" + "\n".join(f"    <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items) + """
  </div>
</div></section>"""
    final = f"""<section class="alt final"><div class="wrap">
  <h2>Ready for Your Written Price?</h2>
  <a class="btn" href="#book" data-cta="final">Request My Free Visit <span class="arr">→</span></a>
  <p class="or">or call <a href="tel:{PHONE_T}">{PHONE}</a></p>
</div></section>"""
    body = "\n".join([hero, trust, form, work, written, owner, faq, final])
    return shell("/bathroom-remodel-cost-v2", "Full Bathroom Remodels in Seattle: $16,000–$28,500 | TrueSquare",
                 f"Full bathroom remodels in the Seattle area: {RANGE}, plus WA sales tax. Free visit, itemized written price within 5 hours.",
                 "love-v2", body, body_class="lp lp2", sticky_label="Free Visit")

# ===== love-v3: final 3-council summit (26.10). Preview only, not in ads. =====
# 26.10 Serhii: no "subcontractor" caption under V3 photos ("they are members of our team")
def v3_page():
    def li(t): return f'<li><span class="tick"><svg><use href="#chk"/></svg></span>{t}</li>'
    hero = f"""<section class="hero on-ink v2hero v3hero">
  <div class="wrap">
    <p class="v3rate"><a href="{GOOGLE}" target="_blank" rel="noopener">{stars()}<b>5.0</b> Google <span>(12)</span></a><a href="{THUMBTACK}" target="_blank" rel="noopener">{stars()}<b>5.0</b> Thumbtack <span>(24)</span></a></p>
    <h1>Love the House. <span class="grad-text">Not the Bathroom?</span></h1>
    <p class="v3sub">Let's fix that.</p>
    <p class="hrange">Seattle-area full bathroom remodels: <b class="nw">{RANGE}</b> + WA sales tax<small>Smaller bathrooms fall at the lower end. Price depends on scope. Larger or more complex projects may exceed this range.</small></p>
    <ul class="hlist">
      {li("Itemized written scope and price within 5 hours after your visit")}
      {li("One phone/text contact throughout your project")}
      {li("Your written OK before extra work")}
    </ul>
    <div class="hcta"><a class="btn block" href="#book" data-cta="hero">Get My Written Price <span class="arr">→</span></a></div>
    <p class="under v3under">Starts with a free visit. We'll call to set a time.<br>No decision at the visit.</p>
  </div>
</section>"""
    band = f"""<section class="v3band"><div class="wrap">
  <figure class="v2photo v3photo"><button class="ph" type="button" data-full="/img/p/b13.jpg"><img src="/img/p/b13-band.jpg" alt="Remodeled bathroom with a double vanity and a large lit mirror" width="760" height="388" fetchpriority="high"><span class="zoom" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5M11 8v6M8 11h6"/></svg></span></button></figure>
  <div class="tline facts"><span>WA Registered Contractor · <b>{LNI}</b></span><span>1-year written workmanship warranty</span></div>
</div></section>"""
    who = """
    <div class="v3who"><img src="/img/serhii-avatar.jpg" alt="Serhii, owner of TrueSquare Remodel" width="56" height="56"><p><b>Serhii will call you to set a time.</b><span>Owner. Your phone/text contact.</span></p></div>"""
    form = form_section(show_lic=False, h2='Get Your <span class="grad-text">Written Price</span>',
                        lead="It starts with a free visit. Your detailed written scope and price follow within 5 hours after the visit.",
                        submit="Get My Written Price", who=who,
                        tile_opts=["Full remodel, same layout", "Full remodel, new layout", "Tub to walk-in shower", "Shower remodel", ("Partial update", "Vanity, tile or fixtures"), "Not sure yet"], phone_label="Phone number", consent_name="TrueSquare Remodel LLC", steps=True)
    work = f"""<section class="v2work"><div class="wrap">
  <div class="head"><p class="kicker">Real work</p><h2>Bathrooms Completed by Our Crew</h2></div>
  <div class="v2gal">
    <button class="ph" type="button" data-full="/img/lp-hero.jpg"><img src="/img/lp-hero-sq.jpg" alt="Finished walk-in shower with glass door, vanity and toilet" loading="lazy" width="360" height="360"></button>
    <button class="ph" type="button" data-full="/img/p/b18.jpg"><img src="/img/p/b18-sq.jpg" alt="Floating vanity with vessel sink, black mirror and toilet" loading="lazy" width="360" height="360"></button>
  </div>
</div></section>"""
    written = f"""<section class="alt v2written"><div class="wrap">
  <div class="head"><p class="kicker">On paper</p><h2>Don't Guess. <span class="grad-text">Get It in Writing.</span></h2><p class="lead">Within 5 hours after your visit: everything included, spelled out in writing, with one total price. Extra work needs your written OK.</p></div>
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
</div></section>"""
    owner = """<section class="owner on-ink v2owner"><div class="wrap">
  <div class="v2own">
    <img src="/img/serhii-ts-wide.jpg" alt="Serhii, owner of TrueSquare Remodel" loading="lazy" width="744" height="408">
    <div>
      <p class="kicker">Your contact</p>
      <h2>No Sales Reps. <span class="grad-text">Just Serhii.</span></h2>
    </div>
  </div>
  <p class="lead">Serhii, the owner, visits to measure your bathroom and stays your contact by phone or text throughout the project. He coordinates the work with our subcontractor crew, who handle the construction.</p>
  <ol class="v2steps">
    <li><span class="n">1</span>Request your free visit</li>
    <li><span class="n">2</span>Discuss and measure your bathroom</li>
    <li><span class="n">3</span>Get your written price within 5 hours after the visit</li>
  </ol>
</div></section>"""
    faq_items = [
        ("Why can't you price it over the phone?", f"We need to see and measure the room first. The {RANGE} range is not a quote for your home, and WA sales tax is extra. Your written price follows within 5 hours after the free visit."),
        ("Will the price jump once the walls are open?", "Only if we find hidden damage or you change the scope. We stop, show you photos, and give you a written price. Nothing happens without your written OK."),
        ("Are you the one swinging the hammer?", "No. Our subcontractor crew does the construction. Serhii coordinates the project and is your phone/text contact."),
        ("Do I pay everything up front?", "No. You pay a deposit at signing, another payment after the rough-in inspection, and the final payment after the walkthrough."),
        ("How long will I be without a bathroom?", "Typically 2–4 weeks of construction, depending on scope and what we find. You get the start date in writing."),
        ("What if something fails after you leave?", "You get a 1-year written workmanship warranty, plus the manufacturer warranties on fixtures and materials."),
    ]
    faq = """<section id="faq" class="v2faq"><div class="wrap">
  <div class="head"><p class="kicker">Straight answers</p><h2>Ask Us the <span class="grad-text">Awkward Questions.</span></h2><p class="lead">Layout changes, materials and finishes, and hidden damage can affect the final price. Larger or more complex projects may exceed the listed range.</p></div>
  <div class="faq">
""" + "\n".join(f"    <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items) + """
  </div>
</div></section>"""
    final = f"""<section class="alt final"><div class="wrap">
  <h2>Your Bathroom Won't <span class="grad-text">Fix Itself.</span></h2>
  <a class="btn" href="#book" data-cta="final">Get My Written Price <span class="arr">→</span></a>
  <p class="v3first">Starts with a free visit.</p>
  <p class="or">or call <a href="tel:{PHONE_T}">{PHONE}</a></p>
</div></section>"""
    body = "\n".join([hero, band, form, work, written, owner, faq, final])
    return shell("/bathroom-remodel-cost-v3", "Full Bathroom Remodels in Seattle: $16,000–$28,500 | TrueSquare",
                 f"Full bathroom remodels in the Seattle area: {RANGE}, plus WA sales tax. Free visit, written price within 5 hours.",
                 "love-v3", body, body_class="lp lp2 lp3", sticky_label="Get My Price")

# Only the V3 ad landing is built from this file (26.10 summit). Other landings: tools/build_lp.py.
PAGES = {
    "bathroom-remodel-cost-v3.html": v3_page(),
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
