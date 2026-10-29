/* TrueSquare Remodel: shared script for every page.
   SETTINGS live here only. Change a value, push to GitHub, Cloudflare redeploys. */
var PREVIEW = false;          // true = shows preview-only blocks and fakes form success
var WEBHOOK_URL = "https://services.leadconnectorhq.com/hooks/H42lV2iiJ2m872quvLqA/webhook-trigger/0c2edfc6-f5c4-468b-8362-84c3d005ff83";         // GHL Inbound Webhook URL (from the "CRM + tech" chat)
var META_PIXEL_ID = "843066468533246";
var GTM_ID = "GTM-TNQM47NC";  // GA4 G-97XK2QM2FG loads inside GTM
var CLARITY_ID = "z42dmgqbaj"; // Microsoft Clarity project "TrueSquare Remodel LLC" (heatmaps, session recordings; form text masked)

(function(){
var d=document, $=function(id){return d.getElementById(id);};

/* preview-only blocks */
if(!PREVIEW){
  var rv=$('reviews'); if(rv) rv.hidden=true;
  [].forEach.call(d.querySelectorAll('[data-preview]'),function(e){e.remove();});
}

/* analytics: dataLayer and fbq queues start now; the tag scripts download after the page has loaded (speed pass 26.10) */
window.dataLayer=window.dataLayer||[];var tagJs=[];
if(GTM_ID){window.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});tagJs.push('https://www.googletagmanager.com/gtm.js?id='+GTM_ID);}
if(META_PIXEL_ID){!function(f){if(f.fbq)return;var n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];}(window);fbq('init',META_PIXEL_ID);fbq('track','PageView');tagJs.push('https://connect.facebook.net/en_US/fbevents.js');}
if(CLARITY_ID){window.clarity=window.clarity||function(){(window.clarity.q=window.clarity.q||[]).push(arguments)};tagJs.push('https://www.clarity.ms/tag/'+CLARITY_ID);}
/* Meta Conversions API: the same Lead goes server-side via /api/capi (Cloudflare Pages Function) with the Pixel's event_id, so Meta counts it once */
window.tsrCapi=function(o){try{var c=d.cookie,g=function(n){var m=c.match(new RegExp('(?:^|; )'+n+'=([^;]*)'));return m?decodeURIComponent(m[1]):'';},q=new URLSearchParams(location.search).get('fbclid');o.fbp=g('_fbp');o.fbc=g('_fbc')||(q?'fb.1.'+Date.now()+'.'+q:'');fetch('/api/capi',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o),keepalive:true}).catch(function(){});}catch(x){}};
function loadTags(){tagJs.forEach(function(u){var j=d.createElement('script');j.async=true;j.src=u;d.head.appendChild(j);});}
if(d.readyState==='complete')loadTags();else window.addEventListener('load',loadTags);

/* per-ad hero line (home page only) */
var Q=new URLSearchParams(location.search);
var SUBS={tub:"Still stepping over that tub wall? We turn old tubs into tiled walk-in showers. Serhii measures himself. Price in writing within 5 hours after the visit.",
hidden:"Worried about what's behind the old tile? If we find damage, you get photos and a written price first. Serhii measures himself.",
license:"WA Registered Contractor · TRUESRL759QK · Owner-led. Serhii measures himself. Price in writing within 5 hours after the visit.",
owner:"I'm Serhii, the owner. I measure your bathroom myself. Price in writing within 5 hours after the visit."};
var ANGLE=(Q.get('h')||'').toLowerCase();
if(!SUBS[ANGLE]){var ad=((Q.get('utm_content')||'')+' '+(Q.get('utm_campaign')||'')).toUpperCase();ANGLE=/TUB/.test(ad)?'tub':/HIDDEN/.test(ad)?'hidden':/LICENSE/.test(ad)?'license':/OWNER/.test(ad)?'owner':'';}
var hSub=$('hSub'); if(hSub&&SUBS[ANGLE]) hSub.textContent=SUBS[ANGLE];
var PAGE=d.body.getAttribute('data-page')||'home';
if(!ANGLE) ANGLE=PAGE==='home'?'main':'page:'+PAGE;

/* menu drawer */
var drawer=$('drawer'),openB=$('openMenu');
function closeMenu(){if(!drawer)return;drawer.hidden=true;d.body.classList.remove('lock');openB.setAttribute('aria-expanded','false');}
if(drawer&&openB){
  openB.addEventListener('click',function(){drawer.hidden=false;d.body.classList.add('lock');openB.setAttribute('aria-expanded','true');$('closeMenu').focus();});
  $('closeMenu').addEventListener('click',closeMenu);
  drawer.addEventListener('click',function(e){if(e.target===drawer||e.target.closest('a'))closeMenu();});
}

/* tiles + cta tracking */
var project='',cta='';
function pick(v){[].forEach.call(d.querySelectorAll('.tile'),function(x){x.setAttribute('aria-pressed',x.dataset.v===v?'true':'false');});project=v;}
[].forEach.call(d.querySelectorAll('[data-svc]'),function(a){a.addEventListener('click',function(){pick(a.dataset.svc);cta='service';});});
[].forEach.call(d.querySelectorAll('[data-cta]'),function(a){a.addEventListener('click',function(){cta=a.dataset.cta;});});

/* galleries + lightbox */
var lb=$('lb'),lbImg=$('lbImg');
function closeLb(){if(lb)lb.hidden=true;}
if(lb){
  d.addEventListener('click',function(e){var b=e.target.closest('.ph[data-full]');if(!b)return;lbImg.src=b.dataset.full;lbImg.alt=b.querySelector('img').alt;lb.hidden=false;});
  $('lbClose').addEventListener('click',closeLb);
  lb.addEventListener('click',function(e){if(e.target===lb)closeLb();});
}
addEventListener('keydown',function(e){if(e.key==='Escape'){closeLb();closeMenu();}});
var moreBtn=$('moreBtn'),more=$('morePhotos');
if(moreBtn&&more) moreBtn.addEventListener('click',function(){var o=more.hidden;more.hidden=!o;moreBtn.setAttribute('aria-expanded',o?'true':'false');moreBtn.textContent=o?'Show fewer photos ↑':'View more project photos →';});

/* portfolio filter */
var fbar=$('pfilter');
if(fbar) fbar.addEventListener('click',function(e){var b=e.target.closest('button[data-f]');if(!b)return;var f=b.dataset.f;
  [].forEach.call(fbar.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
  [].forEach.call(d.querySelectorAll('#pgrid .ph'),function(p){p.hidden=!(f==='all'||p.dataset.cat===f);});});

/* sticky bar: after hero CTA, hidden over the form */
var sticky=$('sticky'),heroCta=d.querySelector('.hcta'),book=$('book');
if(sticky&&heroCta&&book){
  var onScroll=function(){var past=heroCta.getBoundingClientRect().bottom<0,r=book.getBoundingClientRect(),inBook=r.top<innerHeight&&r.bottom>0;var on=past&&!inBook;sticky.classList.toggle('show',on);sticky.setAttribute('aria-hidden',on?'false':'true');};
  addEventListener('scroll',onScroll,{passive:true});onScroll();
}


/* service area map: loads Leaflet only when the map scrolls near */
var am=$('areaMap');
if(am){
  var initMap=function(){
    var poly=JSON.parse(am.getAttribute('data-poly'));
    var map=L.map(am,{scrollWheelZoom:false,dragging:!L.Browser.mobile,tap:false,zoomControl:true,attributionControl:true});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:15,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    var shape=L.polygon(poly,{color:'#C64237',weight:2.5,fillColor:'#F47A61',fillOpacity:.22}).addTo(map);
    map.fitBounds(shape.getBounds(),{padding:[18,18]});
  };
  var loadLeaflet=function(){
    if(window.L){initMap();return;}
    var c=d.createElement('link');c.rel='stylesheet';c.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';d.head.appendChild(c);
    var s=d.createElement('script');s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';s.onload=initMap;d.head.appendChild(s);
  };
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();loadLeaflet();}},{rootMargin:'400px'});io.observe(am);}else loadLeaflet();
}

/* form */
var form=$('bookForm'); if(!form) return;
var def=form.getAttribute('data-default'); if(def) pick(def);
$('tiles').addEventListener('click',function(e){var b=e.target.closest('.tile');if(!b)return;pick(b.dataset.v);$('fName').focus();});
var zip=$('fZip');
zip.addEventListener('input',function(){zip.value=zip.value.replace(/\D/g,'').slice(0,5);});
var sending=false;
form.addEventListener('submit',function(e){
  e.preventDefault(); if(sending) return;
  var err=$('fErr'),name=$('fName').value.trim();
  var ph=$('fPhone').value.replace(/\D/g,'');if(ph.length===11&&ph[0]==='1')ph=ph.slice(1);
  var msg='';
  if(!project)msg='Please pick what you are planning.';
  else if(name.length<2)msg='Please enter your name.';
  else if(ph.length!==10)msg='Please enter a 10-digit phone number.';
  else if(!/^\d{5}$/.test(zip.value))msg='Please enter a 5-digit ZIP code.';
  if(msg){err.textContent=msg;err.hidden=false;if(sheet)track('form_error',{msg:msg});return;}
  err.hidden=true; sending=true;
  var fsrc=where(),fcta=fsrc==='modal'?(openCta||'modal'):'inline';
  var parts=name.split(/\s+/),mkt=!!($('fMkt')&&$('fMkt').checked),ctext=$('consentText')?$('consentText').textContent.trim():'';
  var id='tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var p={full_name:name,first_name:parts[0],last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:project,
    sms_consent:'yes',sms_consent_text:ctext,consent_text:ctext,marketing_consent:mkt?'yes':'no',marketing_consent_text:mkt?$('mktText').textContent.trim():'',
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,cta:cta||'form',form_source:fsrc,
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  var lab=$('fLabel'),btn=$('fSubmit');btn.disabled=true;lab.textContent='Sending…';
  function reset(){sending=false;btn.disabled=false;lab.textContent='Request my free visit';}
  function done(){$('doneTitle').textContent='Thanks, '+parts[0]+'. We received your request. Serhii will call to arrange a time.';$('formBody').hidden=true;$('formDone').hidden=false;sheetDone();window.dataLayer.push({event:'generate_lead',project_type:project,page_angle:ANGLE,event_id:id,cta:fcta,form_source:fsrc});try{if(window.clarity){clarity('set','form_source',fsrc);clarity('event','generate_lead');}}catch(x){}try{if(window.fbq)fbq('track','Lead',{content_name:project},{eventID:id});}catch(x){}if(window.tsrCapi)tsrCapi({event_id:id,phone:ph,first:parts[0],last:parts.slice(1).join(' '),zip:zip.value,project:project,page_url:location.href.split('#')[0]});}
  if(!WEBHOOK_URL){ if(PREVIEW){done();return;} reset();err.innerHTML='Online requests open shortly. Please call or text <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a> and Serhii will set up your free visit.';err.hidden=false;return;}
  fetch(WEBHOOK_URL,{method:'POST',mode:'no-cors',body:new URLSearchParams(p),keepalive:true}).then(done).catch(function(){reset();err.textContent="That didn't go through. Please call or text (206) 222-2328.";err.hidden=false;});
});

/* pop-up form (28.10): every free-visit button ("#book" or "/#book") opens this page's form in a sheet; it closes only with the X.
   Pages without a form link to /#book: the home page then opens the sheet on load. Same events as the V3 landing. */
/* form_source (28.10): same as the V3 landing. modal = pop-up sheet (cta = the button that opened it), inline = form on the page (cta 'inline') */
var openCta='';
function where(){return sheet&&!sheet.hidden?'modal':'inline';}
function track(ev,o){var x={event:ev,page_angle:ANGLE};for(var k in o)x[k]=o[k];if(!x.form_source)x.form_source=where();if(x.cta===undefined)x.cta=x.form_source==='modal'?(openCta||'modal'):'inline';window.dataLayer.push(x);try{if(window.clarity){clarity('set','form_source',x.form_source);clarity('event',ev);}}catch(e){}}
var sheet=$('sheet');
function sheetDone(){var t=$('sheetTitle');if(t&&sheet&&!sheet.hidden){t.innerHTML='Request <span class="grad-text">Received</span>';var w=d.querySelector('.sheet-who');if(w)w.hidden=true;}}
if(sheet){
  var sbody=$('sheetBody'),panel=$('sheetPanel'),slot=d.createComment('form-slot'),opener=null,y=0,started=false,phoneOk=false;
  form.parentNode.insertBefore(slot,form);
  var openSheet=function(src){
    if(!sheet.hidden)return;
    y=window.pageYOffset||d.documentElement.scrollTop||0;
    sbody.appendChild(form);
    d.documentElement.classList.add('sheet-open');
    var bs=d.body.style;bs.position='fixed';bs.top=(-y)+'px';bs.left='0';bs.right='0';bs.width='100%';
    sheet.hidden=false;panel.scrollTop=0;
    requestAnimationFrame(function(){requestAnimationFrame(function(){sheet.classList.add('open');});});
    try{$('sheetTitle').focus({preventScroll:true});}catch(x){}
    openCta=src||'';
    track('form_open',{cta:openCta||'modal'});
  };
  var closeSheet=function(){
    if(sheet.hidden)return;
    sheet.classList.remove('open');sheet.hidden=true;
    slot.parentNode.insertBefore(form,slot.nextSibling);
    d.documentElement.classList.remove('sheet-open');
    var bs=d.body.style;bs.position='';bs.top='';bs.left='';bs.right='';bs.width='';
    var de=d.documentElement,sb=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,y);de.style.scrollBehavior=sb;window.dispatchEvent(new Event('scroll'));
    try{if(opener)opener.focus({preventScroll:true});}catch(x){}
    track('form_close',{form_source:'modal',cta:openCta||'modal',stage:!$('formDone').hidden?'sent':phoneOk?'phone':started?'started':'empty'});
    openCta='';
  };
  [].forEach.call(d.querySelectorAll('a[href="#book"],a[href="/#book"]'),function(a){a.addEventListener('click',function(e){e.preventDefault();opener=a;openSheet(a.getAttribute('data-cta')||'link');});});
  $('sheetClose').addEventListener('click',closeSheet);
  [['fName','fPhone'],['fPhone','fZip']].forEach(function(p){$(p[0]).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();$(p[1]).focus();}});});
  var start=function(){if(!started){started=true;track('form_start',{});}};
  $('tiles').addEventListener('click',start);
  ['fName','fPhone','fZip'].forEach(function(id){$(id).addEventListener('focus',start);});
  $('fPhone').addEventListener('input',function(){var v=this.value.replace(/\D/g,'');if(v.length===11&&v[0]==='1')v=v.slice(1);if(!phoneOk&&v.length===10){phoneOk=true;track('form_phone',{});}});
  if(location.hash==='#book')openSheet('link');
}
})();
