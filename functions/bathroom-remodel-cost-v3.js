// Landing split on one ad URL (owner 29.10, council R4-R6): every new visitor gets V3 or Q, evenly, and keeps it (cookie).
// QA: add ?v=v3 or ?v=q (plus &test=1 so BRM Stats marks the browser) to force a version; a forced visit sets no cookie.
// If anything fails, the visitor gets the normal V3 page.
// City line (owner 29.10): the line above the H1 says "Bathroom remodeling in <city>" when Cloudflare places the visitor's IP
// in a city on the owner's map (same list as CITY_GROUPS in tools/build.py); otherwise it stays "in the Seattle area".
// QA: ?geo=Tacoma shows how it looks for a city on the list.
// W3 first screens (owner 02.11, TZ Реклама/ТЗ_САЙТ_W3_СТРАНИЦЫ_ПОД_ОБЪЯВЛЕНИЯ_2026-11-02.md): every W3 ad links here with
// utm_content={{ad.name}}; a code inside the ad name picks the first screen (H1, subtitle, price plate, promises, tile picked
// in the form). No code = the default page. Works on both V3 and Q. QA: ?ad=owner|tub|price|love|hire (or any code below).
const VARIANTS = { v3: "/bathroom-remodel-cost-v3", q: "/bathroom-remodel-cost-v3-q" };
const WEIGHTS = { v3: 1, q: 1 };
const COOKIE = "tsr_lpv";
const CITIES = ["Seattle", "Bellevue", "Kirkland", "Redmond", "Sammamish", "Issaquah", "Mercer Island", "Shoreline",
  "Bothell", "Woodinville", "Renton", "Kent", "Auburn", "Federal Way", "Burien", "Tukwila",
  "Everett", "Lynnwood", "Edmonds", "Mill Creek", "Mukilteo", "Marysville", "Lake Stevens", "Snohomish",
  "Tacoma", "Lakewood", "University Place", "Puyallup", "Sumner", "Gig Harbor",
  "Olympia", "Lacey", "Tumwater", "Bremerton", "Port Orchard", "Shelton"];
const findCity = (name) => CITIES.find((c) => c.toLowerCase() === String(name || "").trim().toLowerCase()) || "";

// ---- W3 first screens. Texts word for word from the TZ (§2, §6). price: "from" = from $9,690 plate, "free" = no price
// (tub to shower: no price next to tub / walk-in, decision 31.10), missing = the plate stays as on the default page (the range).
const P = {
  owner: ["Free in-home visit with Serhii, the owner.", "Itemized written price within 5 hours after your visit.", "No pressure. No decision at the visit."],
  tub: ["Free in-home visit with Serhii, the owner.", "No decision at the visit."],
  price: ["We measure first. No guessing over the phone.", "Itemized written price within 5 hours after your visit.", "The price is yours to keep and compare."],
  hire: ["Free in-home visit with Serhii, the owner.", "Nothing extra without your written OK.", "No pressure. No decision at the visit."],
};
const H_PRICE = 'How Much Does a Bathroom Remodel <span class="grad-text">Cost?</span>';
const S_PRICE = "Where you land depends on your bathroom, not on a sales pitch.";
const AD = {
  owner: { noUnder: true, lpv: "owner", h1: 'Local Bathroom Remodel <span class="grad-text">Contractor</span>', sub: "Hi, I'm Serhii, the owner of TrueSquare Remodel.", price: "from", list: P.owner },
  tub: { noUnder: true, lpv: "tub", h1: 'Tub to Shower <span class="grad-text">Conversion</span>', sub: "We take the old tub out and build a tiled walk-in shower. Real tile, not a liner.", price: "free", list: P.tub, pick: "Tub to walk-in shower" },
  price: { lpv: "price", h1: H_PRICE, sub: S_PRICE, price: "from", list: P.price },
  handnote: { lpv: "price-handnote", h1: H_PRICE, sub: S_PRICE, list: P.price },
  love: { lpv: "love" },
  newhouse: { lpv: "love", sub: "Just bought a house? Full bathroom remodels with a written price." },
  stuck: { lpv: "love-stuck", sub: "Bathroom stuck in 1995? You don't need a new house. You need a bathroom that works." },
  hire: { noUnder: true, lpv: "hire", h1: 'Before You Hire a <span class="grad-text">Bathroom Remodel Contractor</span>', sub: "Get an itemized written price within 5 hours. Every line. Yours to keep.", price: "from", list: P.hire },
  cheapest: { noUnder: true, lpv: "hire-cheapest", h1: 'Not the Cheapest. <span class="grad-text">Every Line in Writing.</span>', sub: "Cheap quotes are one line long. Then the extras start. With us, every line is in writing before anything starts.", list: P.hire },
  included: { noUnder: true, lpv: "hire-included", h1: 'What\'s in a <span class="grad-text">Full Bathroom Remodel?</span>', sub: "We send an itemized written price within 5 hours after your visit. Every line: demo, waterproofing, tile, plumbing, vanity and more.", price: "from", list: P.hire },
};
// first match wins: photo ads (§6) first, then video ads (§1), top to bottom, case-insensitive
const CODES = [
  ["CHEAPEST", "cheapest"], ["INCLUDED", "included"], ["STUCK", "stuck"], ["DONTMOVE", "love"], ["PICKSHOWER", "tub"],
  ["HANDNOTE", "handnote"], ["COSTQUIZ", "price"], ["ONELINE", "hire"],
  ["OWNERREAL", "owner"], ["OWNERLIVE", "owner"], ["SAMEROOM", "owner"], ["3WAYS", "owner"],
  ["TUB2SHOWER", "tub"], ["TUB_AV", "tub"],
  ["WHITEBOARD", "price"], ["PRICE_AV", "price"], ["SMALL5X8", "price"],
  ["NEWHOUSE", "newhouse"],
  ["TOUCH", "hire"], ["HIRE_AV", "hire"], ["BUDGET", "hire"],
  ["DOOR", "love"], ["6HOMES", "love"], // own texts later [ЖДЁТ РЕШЕНИЯ]; for now the default first screen
];
function findAd(s) {
  const u = String(s || "").toUpperCase();
  if (!u) return null;
  for (const [code, key] of CODES) if (u.includes(code)) return AD[key];
  return null;
}
function pickAd(params) {
  const a = (params.get("ad") || "").trim().toLowerCase();
  return (a && ["owner", "tub", "price", "love", "hire"].includes(a) ? AD[a] : findAd(a)) || findAd(params.get("utm_content"));
}
// owner 02.11 15:38: no "+ tax" on the site (ads keep it)
const PLATE = {
  from: '<p class="v3plab">Bathroom remodels</p><p class="v3prow"><b class="v3pnum grad-text nw">from $9,690</b></p><p class="v3pnote">Full remodels $16,000–$28,500 · Price depends on scope.</p>',
  free: '<p class="v3pfree"><span class="grad-text">Free visit</span> · Itemized written price within 5 hours</p>',
};
const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function pick() {
  const keys = Object.keys(WEIGHTS);
  const total = keys.reduce((a, k) => a + WEIGHTS[k], 0);
  let r = Math.random() * total;
  for (const k of keys) { if ((r -= WEIGHTS[k]) < 0) return k; }
  return keys[0];
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method !== "GET" && request.method !== "HEAD") return context.next();
  try {
    const url = new URL(request.url);
    const forced = (url.searchParams.get("v") || "").toLowerCase();
    let v, isNew = false;
    if (VARIANTS[forced]) {
      v = forced;
    } else {
      const m = (request.headers.get("Cookie") || "").match(/(?:^|;\s*)tsr_lpv=([a-z0-9]+)/);
      if (m && VARIANTS[m[1]]) v = m[1]; else { v = pick(); isNew = true; }
    }
    const asset = await env.ASSETS.fetch(new Request(new URL(VARIANTS[v], url.origin), { method: request.method }));
    if (!asset.ok) return context.next();
    let res = new Response(asset.body, asset);
    res.headers.set("Cache-Control", "private, no-store");
    res.headers.set("Vary", "Cookie");
    res.headers.set("X-TSR-Variant", v);
    if (isNew) res.headers.append("Set-Cookie", `${COOKIE}=${v}; Path=/; Max-Age=7776000; SameSite=Lax; Secure`);
    const cf = request.cf || {};
    const city = findCity(url.searchParams.get("geo")) || (cf.regionCode === "WA" ? findCity(cf.city) : "");
    const ad = pickAd(url.searchParams);
    const lpv = ad ? ad.lpv : "default";
    res.headers.set("X-TSR-Ad", lpv);
    if (request.method !== "GET") return res;
    if (city) res.headers.set("X-TSR-City", city);
    const rw = new HTMLRewriter().on("body", { element(e) { e.setAttribute("data-lpv", lpv); } });
    if (city) {
      rw.on("[data-geo]", { element(e) { e.setInnerContent(`Bathroom remodeling in ${city}`); } })
        .on("[data-geo-lab]", { element(e) { if (city !== "Seattle") e.setInnerContent("Full bathroom remodels"); } });
    }
    if (ad) {
      rw.on("[data-lp-h1]", {
        element(e) {
          if (ad.h1) { e.setInnerContent(ad.h1, { html: true }); e.setAttribute("class", "v3h1w"); }
          if (ad.sub) e.after(`<p class="v3sub">${esc(ad.sub)}</p>`, { html: true });
        },
      });
      if (ad.price) rw.on("[data-lp-price]", { element(e) { e.setInnerContent(PLATE[ad.price], { html: true }); } });
      if (ad.list) {
        rw.on("[data-lp-list]", {
          element(e) {
            const tick = e.getAttribute("data-lp-list") === "tick";
            e.setInnerContent(ad.list.map((t) => tick
              ? `<li><span class="tick"><svg><use href="#chk"/></svg></span>${esc(t)}</li>`
              : `<li>${esc(t)}</li>`).join(""), { html: true });
          },
        });
      }
      // owner 02.11 16:09: in A, B, E the promises already say "No decision at the visit", so the line under the V3 button goes
      if (ad.noUnder) rw.on(".v3hero .v3under", { element(e) { e.remove(); } });
      if (ad.pick) {
        // two-step form opens on step 2 with this project chosen; "Change" brings the tiles back (lp.js reads the pressed tile)
        rw.on("form#lpForm", { element(e) { e.setAttribute("class", `${e.getAttribute("class") || ""} on2`.trim()); } })
          .on(`#tiles .tile[data-v="${ad.pick}"]`, { element(e) { e.setAttribute("aria-pressed", "true"); } })
          .on("#fChoice", { element(e) { e.setInnerContent(ad.pick); } });
      }
    }
    return rw.transform(res);
  } catch (e) {
    return context.next();
  }
}
