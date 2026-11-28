// Cloudflare Pages Function: POST /api/lead  (calc-v1, 28.11; council round 5: the browser must know the lead really arrived)
// The calculator posts its lead here (same origin), this function forwards it to the same GHL inbound webhook that
// site.js uses and returns {ok:true} only when GHL answers 2xx. The thank-you screen and the Meta Lead event wait for it.
// Used only by public/js/calc.js. lp.js (V3, Q, /bathroom-remodel-cost) and site.js keep posting straight to GHL as before.
// Never logs personal data. A repeated submission ID within 10 minutes is answered ok without a second forward (no double SMS).

const WEBHOOK = "https://services.leadconnectorhq.com/hooks/H42lV2iiJ2m872quvLqA/webhook-trigger/0c2edfc6-f5c4-468b-8362-84c3d005ff83"; // same URL as WEBHOOK_URL in public/js/site.js
const SITE = /^https:\/\/([a-z0-9-]+\.)?truesquareremodel\.(com|pages\.dev)(\/|$)/;
const seen = new Map(); // submission id -> time (per isolate; best effort, the browser also blocks double taps)

// Server-side price check (council round 6): the range texted to the homeowner is recalculated here from the same table as the page.
// The table between the markers is written by tools/build_lp_calc.py from tools/calc/prices.json. Do not edit it by hand.
// PRICES-BEGIN
const P = {"version":"2026-11-28","base":{"full":{"S":21000,"M":28500,"L":38000},"tub":{"S":12000,"L":14000},"shower":{"S":10500,"L":12500}},"finish":{"full":{"e":0.765,"m":1,"p":1.4},"tub":{"e":0.88,"m":1,"p":1.35},"shower":{"e":0.88,"m":1,"p":1.35}},"extras":{"layout":6000,"walkin":2000,"curbless":2500,"heat":{"S":1500,"M":2000,"L":2800},"double":2500,"bench":900,"grab":450},"avail":{"layout":["full"],"walkin":["full"],"heat":["full"],"double":["full:M","full:L"],"bench":["full","tub","shower"],"curbless":["full","tub","shower"],"grab":["tub","shower"]},"spread":1.15};
// PRICES-END
const kindOf = (t) => (t === "tub" ? "tub" : t === "shower" ? "shower" : "full");
const sizeOf = (k, s) => (k === "full" ? (s === "S" ? "S" : s === "L" ? "L" : "M") : s === "SL" ? "L" : "S");
const avail = (n, k, sk) => { const a = P.avail[n] || []; return a.includes(k) || a.includes(k + ":" + sk); };
const money = (v) => "$" + v.toLocaleString("en-US");
function calc(t, s, f, keys) {
  const k = kindOf(t), sk = sizeOf(k, s), fin = P.finish[k][f] ? f : "m";
  let x = 0;
  for (const n of keys) if (P.extras[n] !== undefined && avail(n, k, sk)) x += n === "heat" ? P.extras.heat[sk] : P.extras[n];
  const v = P.base[k][sk] * P.finish[k][fin] + x;
  const lo = Math.floor(v / 500) * 500, hi = Math.ceil((v * P.spread) / 500) * 500;
  return { lo, hi, text: money(lo) + "-" + money(hi) };
}

const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });

export async function onRequestPost({ request }) {
  const origin = request.headers.get("Origin") || "";
  if (origin && !SITE.test(origin + "/")) return json({ ok: false, error: "origin" }, 403);
  let form;
  try { form = await request.formData(); } catch { return json({ ok: false, error: "body" }, 400); }
  const id = String(form.get("event_id") || "");
  const ph = String(form.get("phone") || "").replace(/\D/g, "");
  if (!/^tsr-\d{10,14}-[a-z0-9]{3,10}$/.test(id) || ph.length !== 11 || String(form.get("page_angle") || "") === "") {
    return json({ ok: false, error: "invalid" }, 400);
  }
  const now = Date.now();
  for (const [k, t] of seen) if (now - t > 600000) seen.delete(k);
  if (seen.has(id)) return json({ ok: true, dup: true });

  // recalculate (calc pages only: page_variant=calc); the server value wins if the browser sent something else
  if (String(form.get("page_variant") || "") === "calc" && P.base) {
    const t = String(form.get("calc_type") || "full"), keys = String(form.get("calc_extras_keys") || "").split(",").filter(Boolean);
    const r = calc(t, String(form.get("calc_size_key") || ""), String(form.get("calc_finish_key") || "m"), keys);
    const alt = t === "unsure" ? calc("tub", "SS", String(form.get("calc_finish_key") || "m"), []) : null;
    if (form.get("calc_range") !== r.text) {
      form.set("calc_range_browser", String(form.get("calc_range") || ""));
      form.set("project_type", String(form.get("project_type") || "").replace(/Estimate \$[0-9,]+-\$[0-9,]+/, "Estimate " + r.text));
    }
    form.set("calc_range", r.text); form.set("calc_low", String(r.lo)); form.set("calc_high", String(r.hi));
    form.set("calc_alt_range", alt ? alt.text : "");
    form.set("pricing_version", P.version);
  }
  const body = new URLSearchParams();
  for (const [k, v] of form.entries()) if (typeof v === "string") body.append(k, v.slice(0, 2000));
  try {
    const r = await fetch(WEBHOOK, { method: "POST", body, headers: { "Content-Type": "application/x-www-form-urlencoded" } });
    if (!r.ok) return json({ ok: false, error: "crm", status: r.status }, 502);
    seen.set(id, now);
    return json({ ok: true });
  } catch {
    return json({ ok: false, error: "network" }, 502);
  }
}
