/* Landing pages only. Uses the settings declared in site.js (WEBHOOK_URL, PREVIEW).
   site.js loads GTM + Pixel PageView, the sticky bar and the lightbox; this file runs the landing form. */
(function(){
var d=document,$=function(id){return d.getElementById(id);};
/* lp2: hide sticky bar while the final CTA or footer is on screen (board spec D9) */
if(d.body.classList.contains('lp2')&&'IntersectionObserver' in window){var st=$('sticky'),seen=new Set();var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?seen.add(e.target):seen.delete(e.target);});if(st)st.classList.toggle('away',seen.size>0);});[].forEach.call(d.querySelectorAll('.final,footer'),function(el){io.observe(el);});}
var form=$('lpForm'); if(!form) return;
var ANGLE=d.body.getAttribute('data-angle')||'lp';
var VARIANT=d.body.getAttribute('data-variant')||'';
/* service area (owner's map 29.10: Marysville/Lake Stevens to Olympia/Tumwater, Bremerton/Shelton to the Cascade foothills): ZIP is flagged, never blocked */
var AREA='98001,98002,98003,98004,98005,98006,98007,98008,98009,98010,98011,98012,98013,98014,98015,98019,98020,98021,98022,98023,98024,98025,98026,98027,98028,98029,98030,98031,98032,98033,98034,98035,98036,98037,98038,98039,98040,98041,98042,98043,98045,98046,98047,98050,98051,98052,98053,98054,98055,98056,98057,98058,98059,98061,98062,98063,98064,98065,98070,98071,98072,98073,98074,98075,98077,98082,98083,98087,98089,98092,98093,98101,98102,98103,98104,98105,98106,98107,98108,98109,98110,98111,98112,98113,98114,98115,98116,98117,98118,98119,98121,98122,98124,98125,98126,98127,98129,98131,98132,98133,98134,98136,98138,98139,98141,98144,98145,98146,98148,98151,98154,98155,98158,98160,98161,98164,98165,98166,98168,98170,98171,98174,98175,98177,98178,98181,98184,98185,98188,98189,98190,98191,98194,98195,98198,98199,98201,98203,98204,98205,98206,98207,98208,98213,98236,98249,98251,98252,98258,98260,98270,98271,98272,98275,98290,98291,98293,98294,98296,98303,98310,98311,98312,98314,98315,98321,98322,98323,98327,98328,98329,98332,98333,98335,98337,98338,98340,98342,98344,98345,98346,98349,98351,98352,98353,98354,98359,98360,98364,98366,98367,98370,98371,98372,98373,98374,98375,98378,98380,98383,98384,98385,98386,98387,98388,98390,98391,98392,98393,98394,98395,98396,98398,98401,98402,98403,98404,98405,98406,98407,98408,98409,98411,98412,98413,98415,98416,98417,98418,98419,98421,98422,98424,98430,98431,98433,98438,98439,98442,98443,98444,98445,98446,98447,98448,98450,98455,98460,98464,98465,98466,98467,98471,98477,98481,98490,98492,98493,98496,98497,98498,98499,98501,98502,98503,98504,98505,98506,98507,98508,98509,98511,98512,98513,98516,98524,98528,98540,98546,98558,98576,98580,98584,98589,98592,98597,98599';
function inArea(z){return AREA.indexOf(z)>-1&&z.length===5?'yes':'no';} /* landing split (29.10): v3 | q, sent with every form event and with the lead */
var Q=new URLSearchParams(location.search);
var project='',cta='';
function pick(v){[].forEach.call(d.querySelectorAll('.tile'),function(x){x.setAttribute('aria-pressed',x.dataset.v===v?'true':'false');});project=v;}
[].forEach.call(d.querySelectorAll('[data-cta]'),function(a){a.addEventListener('click',function(){if(!form.contains(a))cta=a.dataset.cta;});}); /* the submit button no longer overwrites the CTA that opened the form */
/* two-step form (V3, 28.10): a tap on a tile opens step 2 (name / phone / ZIP); "Change" goes back to the tiles */
var steps=form.classList.contains('steps');
function step2(){if(!steps)return;form.classList.add('on2');var c=$('fChoice');if(c)c.textContent=project;if(sheet&&!sheet.hidden&&panel)panel.scrollTop=0;track('form_step',{step:2});}
if(steps&&$('fBack'))$('fBack').addEventListener('click',function(){form.classList.remove('on2');if(sheet&&!sheet.hidden&&panel)panel.scrollTop=0;try{var t=d.querySelector('.tile[aria-pressed="true"]')||d.querySelector('.tile');t.focus({preventScroll:true});}catch(x){}});
$('tiles').addEventListener('click',function(e){var b=e.target.closest('.tile');if(!b)return;pick(b.dataset.v);step2();$('fName').focus();});
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
  var parts=name.split(/\s+/),ctext=$('consentText').textContent.trim(); /* landings: no checkbox; consent = submitting with the line under the button (decision 23.10) */
  var id='tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var p={full_name:name,first_name:parts[0],last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:project,
    sms_consent:'yes',sms_consent_text:ctext,consent_text:ctext,marketing_consent:'no',
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,page_variant:VARIANT,zip_in_area:inArea(zip.value),cta:cta||'form',form_source:fsrc,
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  var lab=$('fLabel'),btn=$('fSubmit'),label=lab.textContent;btn.disabled=true;lab.textContent='Sending…';
  function reset(){sending=false;btn.disabled=false;lab.textContent=label;}
  function done(){$('formBody').hidden=true;$('formDone').hidden=false;thanks(parts[0],ph);window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'generate_lead',project_type:project,page_angle:ANGLE,variant:VARIANT,event_id:id,cta:fcta,form_source:fsrc});try{if(window.fbq)fbq('track','Lead',{content_name:project},{eventID:id});}catch(x){}try{if(window.clarity){clarity('set','form_source',fsrc);clarity('event','generate_lead');}}catch(e){}if(window.tsrCapi)tsrCapi({event_id:id,phone:ph,first:parts[0],last:parts.slice(1).join(' '),zip:zip.value,project:project,page_url:location.href.split('#')[0]});}
  var url=window.WEBHOOK_URL||'';
  if(!url){ if(window.PREVIEW){done();return;} reset();err.innerHTML='Please call <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a>.';err.hidden=false;return;}
  fetch(url,{method:'POST',mode:'no-cors',body:new URLSearchParams(p),keepalive:true}).then(done).catch(function(){reset();err.textContent="That didn't go through. Please call or text (206) 222-2328.";err.hidden=false;});
});
/* V3 thank-you state (26.10): first name, the number we will call, and when (Seattle time; Mon-Sat 9 AM-7 PM) */
function thanks(first,ph){
  if(!$('doneWhen'))return;
  if(first)$('doneHi').textContent='Thanks, '+first.charAt(0).toUpperCase()+first.slice(1)+'! Your request is in.';
  if(ph&&ph.length===10){$('donePhone').textContent='('+ph.slice(0,3)+') '+ph.slice(3,6)+'-'+ph.slice(6);$('doneNum').hidden=false;}
  var when='shortly';
  try{var f=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',weekday:'short',hour:'numeric',hourCycle:'h23'}).formatToParts(new Date()),wd='',h=12;
    f.forEach(function(x){if(x.type==='weekday')wd=x.value;if(x.type==='hour')h=parseInt(x.value,10);});
    if(wd==='Sun'||(wd==='Sat'&&h>=19))when='Monday morning';else if(h>=19)when='tomorrow morning';else if(h<9)when='this morning';}catch(x){}
  $('doneWhen').textContent='Serhii will call you '+when+' to set up your free visit.';
  var t=$('sheetTitle');if(t&&sheet&&!sheet.hidden){t.innerHTML='Request <span class="grad-text">Received</span>';var w=d.querySelector('.sheet-who');if(w)w.hidden=true;}
  var sv=$('doneSave');if(sv&&!sv.__t){sv.__t=1;sv.addEventListener('click',function(){track('save_contact',{});});}
}
/* V3 pop-up form sheet (26.10): every #book button opens the same form in a sheet; it closes only with the X */
/* form_source (28.10): every form event says where the form was (modal = pop-up sheet, inline = form on the page) and, for the sheet, which button opened it (cta).
   cta is also what BRM Stats keeps: inline events carry cta 'inline', sheet events carry the opener's data-cta. */
var openCta='';
function where(){return sheet&&!sheet.hidden?'modal':'inline';}
function track(ev,o){window.dataLayer=window.dataLayer||[];var x={event:ev,page_angle:ANGLE};if(VARIANT)x.variant=VARIANT;for(var k in o)x[k]=o[k];if(!x.form_source)x.form_source=where();if(x.cta===undefined)x.cta=x.form_source==='modal'?(openCta||'modal'):'inline';window.dataLayer.push(x);try{if(window.clarity){clarity('set','form_source',x.form_source);clarity('event',ev);}}catch(e){}}
try{if(window.clarity){clarity('set','page_angle',ANGLE);if(VARIANT)clarity('set','ab_variant',VARIANT);}}catch(e){}
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
  [].forEach.call(d.querySelectorAll('a[href="#book"]'),function(a){a.addEventListener('click',function(e){e.preventDefault();opener=a;openSheet(a.getAttribute('data-cta'));});});
  $('sheetClose').addEventListener('click',closeSheet);
  /* the keyboard's Next key moves to the next field instead of sending a half-filled form */
  [['fName','fPhone'],['fPhone','fZip']].forEach(function(p){$(p[0]).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();$(p[1]).focus();}});});
  var start=function(){if(!started){started=true;track('form_start',steps?{step:2}:{});}};
  $('tiles').addEventListener('click',start);
  ['fName','fPhone','fZip'].forEach(function(id){$(id).addEventListener('focus',start);});
  $('fPhone').addEventListener('input',function(){var v=this.value.replace(/\D/g,'');if(v.length===11&&v[0]==='1')v=v.slice(1);if(!phoneOk&&v.length===10){phoneOk=true;track('form_phone',{});}});
}
})();
