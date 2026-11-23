"""Meta Pixel base code for the <head> of the ad landing pages (owner 17.11, research 24 §3).

Meta counts a Landing Page View only when the Pixel has loaded and sent PageView. With the speed pass (03.11) the Pixel
started on the first scroll / tap or 4 s after load, so short visits were lost (PageView ~9 s on slow 4G). Now the Pixel
and its PageView start at once, async, from the <head>; GTM and Clarity stay delayed in site.js.
site.js sees window.TSR_PIXEL_HEAD and does not init the Pixel or send PageView a second time.
Lead and InitiateCheckout still go through fbq (lp.js / site.js) with the same event_id as /api/capi."""

PIXEL_ID = "843066468533246"  # the same id as META_PIXEL_ID in public/js/site.js

HEAD_PIXEL = (
    "<script>/* Meta Pixel (17.11): base code + PageView at once, async; GTM and Clarity stay delayed in site.js */\n"
    "!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
    "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;"
    "s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');\n"
    f"window.TSR_PIXEL_HEAD=1;fbq('init','{PIXEL_ID}');fbq('track','PageView');</script>\n"
)
