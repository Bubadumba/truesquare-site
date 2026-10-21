/* TrueSquare Remodel: shared script for every page.
   SETTINGS live here only. Change a value, push to GitHub, Cloudflare redeploys. */
var PREVIEW = false;          // true = shows preview-only blocks and fakes form success
var WEBHOOK_URL = "https://services.leadconnectorhq.com/hooks/H42lV2iiJ2m872quvLqA/webhook-trigger/0c2edfc6-f5c4-468b-8362-84c3d005ff83";         // GHL Inbound Webhook URL (from the "CRM + tech" chat)
var META_PIXEL_ID = "843066468533246";
var GTM_ID = "GTM-TNQM47NC";  // GA4 G-97XK2QM2FG loads inside GTM

(function(){
var d=document, $=function(id){return d.getElementById(id);};

/* preview-only blocks */
if(!PREVIEW){
  var rv=$('reviews'); if(rv) rv.hidden=true;
  [].forEach.call(d.querySelectorAll('[data-preview]'),function(e){e.remove();});
}

/* analytics */
window.dataLayer=window.dataLayer||[];
if(GTM_ID){(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f);})(window,d,'script','dataLayer',GTM_ID);}
if(META_PIXEL_ID){!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,d,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init',META_PIXEL_ID);fbq('track','PageView');}

/* per-ad hero line (home page only) */
var Q=new URLSearchParams(location.search);
var SUBS={tub:"Still stepping over that tub wall? We turn old tubs into tiled walk-in showers. Serhii measures himself. Price in writing within 5 hours after the visit.",
hidden:"Worried about what's behind the old tile? If we find damage, you get photos and a written price first. Serhii measures himself.",
license:"Licensed, bonded & insured. WA L&I TRUESRL759QK. Serhii measures himself. Price in writing within 5 hours after the visit.",
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
  if(msg){err.textContent=msg;err.hidden=false;return;}
  err.hidden=true; sending=true;
  var parts=name.split(/\s+/),sms=$('fSms').checked;
  var id='tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var p={full_name:name,first_name:parts[0],last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:project,
    sms_consent:sms?'yes':'no',sms_consent_text:sms?$('smsText').textContent.trim():'',
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,cta:cta||'form',
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  var lab=$('fLabel'),btn=$('fSubmit');btn.disabled=true;lab.textContent='Sending…';
  function reset(){sending=false;btn.disabled=false;lab.textContent='Request my free visit';}
  function done(){$('doneTitle').textContent='Thanks, '+parts[0]+'. We received your request. Serhii will call to arrange a time.';$('formBody').hidden=true;$('formDone').hidden=false;window.dataLayer.push({event:'generate_lead',project_type:project,event_id:id});try{if(window.fbq)fbq('track','Lead',{content_name:project},{eventID:id});}catch(x){}}
  if(!WEBHOOK_URL){ if(PREVIEW){done();return;} reset();err.innerHTML='Online requests open shortly. Please call or text <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a> and Serhii will set up your free visit.';err.hidden=false;return;}
  fetch(WEBHOOK_URL,{method:'POST',mode:'no-cors',body:new URLSearchParams(p),keepalive:true}).then(done).catch(function(){reset();err.textContent="That didn't go through. Please call or text (206) 222-2328.";err.hidden=false;});
});
})();
