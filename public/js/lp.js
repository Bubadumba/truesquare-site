/* Landing pages only. Uses the settings declared in site.js (WEBHOOK_URL, PREVIEW).
   site.js loads GTM + Pixel PageView, the sticky bar and the lightbox; this file runs the landing form. */
(function(){
var d=document,$=function(id){return d.getElementById(id);};
/* lp2: hide sticky bar while the final CTA or footer is on screen (board spec D9) */
if(d.body.classList.contains('lp2')&&'IntersectionObserver' in window){var st=$('sticky'),seen=new Set();var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?seen.add(e.target):seen.delete(e.target);});if(st)st.classList.toggle('away',seen.size>0);});[].forEach.call(d.querySelectorAll('.final,footer'),function(el){io.observe(el);});}
var form=$('lpForm'); if(!form) return;
var ANGLE=d.body.getAttribute('data-angle')||'lp';
var Q=new URLSearchParams(location.search);
var project='',cta='';
function pick(v){[].forEach.call(d.querySelectorAll('.tile'),function(x){x.setAttribute('aria-pressed',x.dataset.v===v?'true':'false');});project=v;}
[].forEach.call(d.querySelectorAll('[data-cta]'),function(a){a.addEventListener('click',function(){if(!form.contains(a))cta=a.dataset.cta;});}); /* the submit button no longer overwrites the CTA that opened the form */
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
  var parts=name.split(/\s+/),ctext=$('consentText').textContent.trim(); /* landings: no checkbox; consent = submitting with the line under the button (decision 23.10) */
  var id='tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var p={full_name:name,first_name:parts[0],last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:project,
    sms_consent:'yes',sms_consent_text:ctext,consent_text:ctext,marketing_consent:'no',
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,cta:cta||'form',
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  var lab=$('fLabel'),btn=$('fSubmit'),label=lab.textContent;btn.disabled=true;lab.textContent='Sending…';
  function reset(){sending=false;btn.disabled=false;lab.textContent=label;}
  function done(){$('formBody').hidden=true;$('formDone').hidden=false;window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'generate_lead',project_type:project,page_angle:ANGLE,event_id:id,cta:cta||'form'});try{if(window.fbq)fbq('track','Lead',{content_name:project},{eventID:id});}catch(x){}}
  var url=window.WEBHOOK_URL||'';
  if(!url){ if(window.PREVIEW){done();return;} reset();err.innerHTML='Please call <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a>.';err.hidden=false;return;}
  fetch(url,{method:'POST',mode:'no-cors',body:new URLSearchParams(p),keepalive:true}).then(done).catch(function(){reset();err.textContent="That didn't go through. Please call or text (206) 222-2328.";err.hidden=false;});
});
/* V3 pop-up form sheet (26.10): every #book button opens the same form in a sheet; it closes only with the X */
function track(ev,o){window.dataLayer=window.dataLayer||[];var x={event:ev,page_angle:ANGLE};for(var k in o)x[k]=o[k];window.dataLayer.push(x);}
var sheet=$('sheet');
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
    track('form_open',{cta:src||''});
  };
  var closeSheet=function(){
    if(sheet.hidden)return;
    sheet.classList.remove('open');sheet.hidden=true;
    slot.parentNode.insertBefore(form,slot.nextSibling);
    d.documentElement.classList.remove('sheet-open');
    var bs=d.body.style;bs.position='';bs.top='';bs.left='';bs.right='';bs.width='';
    var de=d.documentElement,sb=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,y);de.style.scrollBehavior=sb;window.dispatchEvent(new Event('scroll'));
    try{if(opener)opener.focus({preventScroll:true});}catch(x){}
    track('form_close',{stage:!$('formDone').hidden?'sent':phoneOk?'phone':started?'started':'empty'});
  };
  [].forEach.call(d.querySelectorAll('a[href="#book"]'),function(a){a.addEventListener('click',function(e){e.preventDefault();opener=a;openSheet(a.getAttribute('data-cta'));});});
  $('sheetClose').addEventListener('click',closeSheet);
  /* the keyboard's Next key moves to the next field instead of sending a half-filled form */
  [['fName','fPhone'],['fPhone','fZip']].forEach(function(p){$(p[0]).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();$(p[1]).focus();}});});
  var start=function(){if(!started){started=true;track('form_start',{});}};
  $('tiles').addEventListener('click',start);
  ['fName','fPhone','fZip'].forEach(function(id){$(id).addEventListener('focus',start);});
  $('fPhone').addEventListener('input',function(){var v=this.value.replace(/\D/g,'');if(v.length===11&&v[0]==='1')v=v.slice(1);if(!phoneOk&&v.length===10){phoneOk=true;track('form_phone',{});}});
}
})();
