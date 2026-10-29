// Landing split on one ad URL (owner 29.10, council R4-R6): every new visitor gets V3 or Q, evenly, and keeps it (cookie).
// QA: add ?v=v3 or ?v=q (plus &test=1 so BRM Stats marks the browser) to force a version; a forced visit sets no cookie.
// If anything fails, the visitor gets the normal V3 page.
const VARIANTS = { v3: "/bathroom-remodel-cost-v3", q: "/bathroom-remodel-cost-v3-q" };
const WEIGHTS = { v3: 1, q: 1 };
const COOKIE = "tsr_lpv";

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
    const res = new Response(asset.body, asset);
    res.headers.set("Cache-Control", "private, no-store");
    res.headers.set("Vary", "Cookie");
    res.headers.set("X-TSR-Variant", v);
    if (isNew) res.headers.append("Set-Cookie", `${COOKIE}=${v}; Path=/; Max-Age=7776000; SameSite=Lax; Secure`);
    return res;
  } catch (e) {
    return context.next();
  }
}
