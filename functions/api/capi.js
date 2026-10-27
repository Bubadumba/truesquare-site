// Cloudflare Pages Function: POST /api/capi
// Sends the website "Lead" to the Meta Conversions API with the same event_id as the browser Pixel,
// so Meta counts it once (deduplication) and matches it better (hashed phone/name/ZIP + IP + browser + fbp/fbc).
// Needs the encrypted secret META_CAPI_TOKEN (Cloudflare > Workers & Pages > truesquareremodel > Settings > Variables and Secrets).
// Without the token it does nothing. Optional plain variable META_TEST_CODE sends events to Events Manager > Test events.
// Never logs personal data. Never put the token in this repository (it is public).

const PIXEL_ID = "843066468533246";
const GRAPH = "v24.0";
const SITE = /^https:\/\/([a-z0-9-]+\.)?truesquareremodel\.(com|pages\.dev)(\/|$)/;

async function sha256(v) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(v));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
const clean = (v) => String(v || "").trim().toLowerCase();

export async function onRequestPost({ request, env }) {
  const token = env.META_CAPI_TOKEN;
  if (!token) return new Response(null, { status: 204 });
  const origin = request.headers.get("Origin") || "";
  if (origin && !SITE.test(origin + "/")) return new Response(null, { status: 403 });

  let b;
  try { b = await request.json(); } catch { return new Response(null, { status: 400 }); }
  const url = String(b.page_url || "");
  const id = String(b.event_id || "");
  const ph = String(b.phone || "").replace(/\D/g, "");
  if (!SITE.test(url) || !/^tsr-\d{10,14}-[a-z0-9]{3,10}$/.test(id) || ph.length !== 10) {
    return new Response(null, { status: 400 });
  }

  const user_data = {
    ph: [await sha256("1" + ph)],
    country: [await sha256("us")],
    client_ip_address: request.headers.get("CF-Connecting-IP") || undefined,
    client_user_agent: request.headers.get("User-Agent") || undefined,
  };
  if (clean(b.first)) user_data.fn = [await sha256(clean(b.first))];
  if (clean(b.last)) user_data.ln = [await sha256(clean(b.last))];
  if (/^\d{5}$/.test(String(b.zip || ""))) user_data.zp = [await sha256(String(b.zip))];
  if (/^fb\.\d\.\d+\./.test(String(b.fbp || ""))) user_data.fbp = String(b.fbp).slice(0, 200);
  if (/^fb\.\d\.\d+\./.test(String(b.fbc || ""))) user_data.fbc = String(b.fbc).slice(0, 500);

  const body = {
    data: [{
      event_name: "Lead",
      event_time: Math.floor(Date.now() / 1000),
      event_id: id,
      action_source: "website",
      event_source_url: url.slice(0, 1000),
      user_data,
      custom_data: { content_name: String(b.project || "").slice(0, 80) },
    }],
  };
  if (env.META_TEST_CODE) body.test_event_code = String(env.META_TEST_CODE);

  const r = await fetch(`https://graph.facebook.com/${GRAPH}/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return new Response(null, { status: r.ok ? 204 : 502 });
}

export function onRequest() {
  return new Response(null, { status: 405, headers: { Allow: "POST" } });
}
