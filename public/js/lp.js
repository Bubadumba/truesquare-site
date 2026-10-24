/* Landing pages only. Uses the settings declared in site.js (WEBHOOK_URL, PREVIEW).
   site.js loads GTM + Pixel PageView, the sticky bar and the lightbox; this file runs the landing form. */
(function(){
var d=document,$=function(id){return d.getElementById(id);};
var form=$('lpForm'); if(!form) return;
var ANGLE=d.body.getAttribute('data-angle')||'lp';
var Q=new URLSearchParams(location.search);
var project='',cta='';
function pick(v){[].forEach.call(d.querySelectorAll('.tile'),function(x){x.setAttribute('aria-pressed',x.dataset.v===v?'true':'false');});project=v;}
[].forEach.call(d.querySelectorAll('[data-cta]'),function(a){a.addEventListener('click',function(){cta=a.dataset.cta;});});
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
  var parts=name.split(/\s+/),sms=true; /* landings: consent = submitting the form with the disclosure under the button (decision 23.10) */
  var id='tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var p={full_name:name,first_name:parts[0],last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:project,
    sms_consent:sms?'yes':'no',sms_consent_text:$('smsText').textContent.trim(),
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,cta:cta||'form',
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  var lab=$('fLabel'),btn=$('fSubmit'),label=lab.textContent;btn.disabled=true;lab.textContent='Sending…';
  function reset(){sending=false;btn.disabled=false;lab.textContent=label;}
  function done(){$('formBody').hidden=true;$('formDone').hidden=false;window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'generate_lead',project_type:project,page_angle:ANGLE,event_id:id});try{if(window.fbq)fbq('track','Lead',{content_name:project},{eventID:id});}catch(x){}}
  var url=window.WEBHOOK_URL||'';
  if(!url){ if(window.PREVIEW){done();return;} reset();err.innerHTML='Please call <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a>.';err.hidden=false;return;}
  fetch(url,{method:'POST',mode:'no-cors',body:new URLSearchParams(p),keepalive:true}).then(done).catch(function(){reset();err.textContent="That didn't go through. Please call or text (206) 222-2328.";err.hidden=false;});
});
})();
