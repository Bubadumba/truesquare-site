// Landing split on one ad URL (owner 29.10, council R4-R6): every new visitor gets V3 or Q, evenly, and keeps it (cookie).
// QA: add ?v=v3 or ?v=q (plus &test=1 so BRM Stats marks the browser) to force a version; a forced visit sets no cookie.
// If anything fails, the visitor gets the normal V3 page.
// City line (owner 29.10): the line above the H1 says "Bathroom remodeling in <city>" when Cloudflare places the visitor's IP
// in a city on the owner's map (same list as CITY_GROUPS in tools/build.py); otherwise it stays "in the Seattle area".
// QA: ?geo=Tacoma shows how it looks for a city on the list.
const VARIANTS = { v3: "/bathroom-remodel-cost-v3", q: "/bathroom-remodel-cost-v3-q" };
const WEIGHTS = { v3: 1, q: 1 };
const COOKIE = "tsr_lpv";
const CITIES = ["Seattle", "Bellevue", "Kirkland", "Redmond", "Sammamish", "Issaquah", "Mercer Island", "Shoreline",
  "Bothell", "Woodinville", "Renton", "Kent", "Auburn", "Federal Way", "Burien", "Tukwila",
  "Everett", "Lynnwood", "Edmonds", "Mill Creek", "Mukilteo", "Marysville", "Lake Stevens", "Snohomish",
  "Tacoma", "Lakewood", "University Place", "Puyallup", "Sumner", "Gig Harbor",
  "Olympia", "Lacey", "Tumwater", "Bremerton", "Port Orchard", "Shelton"];
const findCity = (name) => CITIES.find((c) => c.toLowerCase() === String(name || "").trim().toLowerCase()) || "";

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
    if (city && request.method === "GET") {
      res.headers.set("X-TSR-City", city);
      res = new HTMLRewriter()
        .on("[data-geo]", { element(e) { e.setInnerContent(`Bathroom remodeling in ${city}`); } })
        .on("[data-geo-lab]", { element(e) { if (city !== "Seattle") e.setInnerContent("Full bathroom remodels"); } })
        .transform(res);
    }
    return res;
  } catch (e) {
    return context.next();
  }
}
