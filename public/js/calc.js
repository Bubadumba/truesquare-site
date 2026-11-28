/* calc-v1 v2 (28.11, after the 7-round council): bathroom price calculator on /bathroom-remodel-cost-calc.
   Own file: lp.js (V3, Q, /bathroom-remodel-cost) is never touched.
   Flow (6 steps): project -> size -> finish -> extras -> start -> contact. One choice per screen, pictures on the answers
   (icons, scaled floor plans, example photos), no hover. The price is NOT shown before the phone: the lead goes to /api/lead
   (same origin), which recalculates the range on the server, forwards it to GHL and answers ok only when GHL accepted it;
   GHL texts the range. Thank-you screen + Meta Lead only after that ok.
   Prices: window.TSR_CALC_PRICES, written into the page by tools/build_lp_calc.py from tools/calc/prices.json. */
(function(){
var d=document,$=function(id){return d.getElementById(id);};
var root=$('calc'),P=window.TSR_CALC_PRICES;if(!root||!P)return;

var L={
  type:{full:'Full bathroom remodel',tub:'Tub to walk-in shower',shower:'Shower remodel',unsure:'Not sure yet'},
  size:{S:'Small (about 5x8)',M:'Medium (about 8x8)',L:'Large (10x10 or bigger)',U:'Not sure (priced as medium)',SS:'Standard shower (5 ft tub space)',SL:'Larger shower',SU:'Not sure (priced as standard)'},
  finish:{e:'Essential',m:'Mid-range',p:'Premium'},
  extras:{walkin:'Walk-in shower instead of tub',layout:'Move plumbing fixtures',heat:'Heated tile floor',double:'Double-sink vanity',bench:'Built-in shower bench',curbless:'Curbless shower entry',grab:'Grab bars'},
  start:{m0:'Within the next month',m1:'In 1-3 months',m3:'More than 3 months from now',look:'Just researching prices'}
};
var S={type:'',size:'',finish:'',extras:{},start:''},ANGLE=d.body.getAttribute('data-angle')||'calc-v1',Q=new URLSearchParams(location.search);
var SID='s'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
var DEBUG=/pages\.dev$|localhost|127\.0\.0\.1/.test(location.hostname); /* preview only: shows the computed range so the owner can check the numbers */

/* ===== price (same rules as functions/api/lead.js) ===== */
function kindOf(t){return t==='tub'?'tub':t==='shower'?'shower':'full';}
function sizeOf(k,s){if(k==='full')return s==='S'?'S':s==='L'?'L':'M';return s==='SL'?'L':'S';}
function avail(n,k,sk){var a=P.avail[n]||[];return a.indexOf(k)>-1||a.indexOf(k+':'+sk)>-1;}
function calc(t,s,f,ex){var k=kindOf(t),sk=sizeOf(k,s),b=P.base[k][sk]*P.finish[k][f||'m'],x=0;
  for(var n in ex){if(ex[n]&&avail(n,k,sk))x+=n==='heat'?P.extras.heat[sk]:P.extras[n];}
  var lo=Math.floor((b+x)/500)*500,hi=Math.ceil((b+x)*P.spread/500)*500;return {lo:lo,hi:hi,text:money(lo)+'-'+money(hi)};}
function money(v){return '$'+v.toLocaleString('en-US');}
function kind(){return kindOf(S.type);}
function sk(){return sizeOf(kind(),S.size);}
function chosenExtras(){return Object.keys(S.extras).filter(function(n){return S.extras[n]&&avail(n,kind(),sk());});}
function price(){return calc(S.type,S.size,S.finish,S.extras);}
function altPrice(){return S.type==='unsure'?calc('tub','SS',S.finish,{}):null;}

/* ===== steps ===== */
var ORDER=['type','size','finish','extras','start','contact'],cur=0,steps={};
[].forEach.call(root.querySelectorAll('.cqstep'),function(s){steps[s.dataset.step]=s;});
function track(ev,o){window.dataLayer=window.dataLayer||[];var x={event:ev,page_angle:ANGLE,form_source:'calc',cta:'calc',calc_session:SID,step:cur+1};for(var k in o)x[k]=o[k];window.dataLayer.push(x);try{if(window.clarity)clarity('event',ev);}catch(e){}}
function show(i,focus){
  cur=i;var name=ORDER[i],k=kind();
  ORDER.forEach(function(n){steps[n].hidden=n!==name;});
  root.dataset.kind=k;
  [].forEach.call(root.querySelectorAll('[data-for]'),function(el){var f=el.dataset.for;el.hidden=f==='full'?k!=='full':k==='full';});
  [].forEach.call(root.querySelectorAll('[data-x]'),function(el){var n=el.dataset.x,ok=avail(n,k,sk());el.hidden=!ok;if(!ok){delete S.extras[n];el.setAttribute('aria-pressed','false');}});
  $('cqNum').textContent=i+1;$('cqProg').style.width=((i+1)/ORDER.length*100)+'%';
  $('cqBack').hidden=i===0;
  var hero=d.querySelector('.cqhero');if(hero){hero.classList.toggle('started',i>0);hero.classList.toggle('on-contact',name==='contact');}
  if(name==='extras')updX();
  if(name==='contact')summary();
  if(DEBUG){var dbg=$('cqDebug');if(dbg&&S.type&&S.size&&S.finish){dbg.hidden=false;var a=altPrice();dbg.textContent='Preview only: '+price().text+(a?' | tub-to-shower option '+a.text:'');}}
  if(focus){var h=steps[name].querySelector('.cqq');try{h.focus({preventScroll:true});}catch(e){}var r=root.getBoundingClientRect();if(r.top<0)root.scrollIntoView({block:'start'});}
  track('step_view',{step:i+1,name:name});
}
function setPressed(st,v){[].forEach.call(steps[st].querySelectorAll('.cqopt'),function(b){b.setAttribute('aria-pressed',b.dataset.v===v?'true':'false');});}
var started=false,busy=false;
root.addEventListener('click',function(e){
  var b=e.target.closest('.cqopt');
  if(b&&!b.hidden){var st=b.closest('.cqstep').dataset.step,v=b.dataset.v;
    if(st==='extras'){var on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on?'true':'false');S.extras[v]=on;updX();track('step_answer',{name:'extras',value:v,on:on});return;}
    if(busy)return;
    if(st==='type'){if(S.type&&kindOf(S.type)!==kindOf(v)){S.size='';setPressed('size','');}S.type=v;}
    else if(st==='size')S.size=v;else if(st==='finish')S.finish=v;else if(st==='start')S.start=v;
    setPressed(st,v);
    if(!started){started=true;
      /* InitiateCheckout once per visit = "form start" on every TrueSquare landing (owner 29.10); CalculatorStart is the calculator's own custom event */
      (function ic(n){if(window.tsrIC){tsrIC(ANGLE,'calc');try{if(window.fbq)fbq('trackCustom','CalculatorStart',{content_name:v});}catch(x){}}else if(n<40)setTimeout(function(){ic(n+1);},250);})(0);
      track('calc_start',{value:v});}
    track('step_answer',{name:st,value:v});
    busy=true;setTimeout(function(){busy=false;show(cur+1,1);},150);return;}
  if(e.target.closest('#cqBack')){show(Math.max(0,cur-1),1);return;}
  if(e.target.closest('#cqNext')){track('step_answer',{name:'extras_done',value:chosenExtras().join(',')||'none'});show(cur+1,1);return;}
  if(e.target.closest('#cqEdit')){show(0,1);return;}
});
function updX(){var n=chosenExtras().length;$('cqNextL').textContent=n?'Continue ('+n+' selected)':'No extras - Continue';}
function summary(){var bits=[L.type[S.type],(L.size[S.size]||'').replace(/ \(.*\)$/,''),L.finish[S.finish]].concat(chosenExtras().map(function(n){return L.extras[n];}));$('cqSum').textContent=bits.filter(Boolean).join(' · ');}

/* ===== contact + lead ===== */
var AREA=(root.getAttribute('data-area')||'').split(','),form=$('cqForm'),zip=$('fZip'),sending=false,phoneOk=false,lead=null;
function inArea(z){return z.length===5&&AREA.indexOf(z)>-1?'yes':'no';}
zip.addEventListener('input',function(){zip.value=zip.value.replace(/\D/g,'').slice(0,5);});
$('fPhone').addEventListener('input',function(){var v=this.value.replace(/\D/g,'');if(v.length===11&&v[0]==='1')v=v.slice(1);if(!phoneOk&&v.length===10){phoneOk=true;track('phone_format_valid',{});}});
[['fName','fPhone'],['fPhone','fZip']].forEach(function(p){$(p[0]).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();$(p[1]).focus();}});});
['fName','fPhone','fZip'].forEach(function(id){$(id).addEventListener('focus',function(){if(!form.__f){form.__f=1;track('contact_focus',{});}});});
function fmt(ph){return '('+ph.slice(0,3)+') '+ph.slice(3,6)+'-'+ph.slice(6);}
form.addEventListener('submit',function(e){
  e.preventDefault();if(sending)return;
  var err=$('fErr'),name=$('fName').value.trim(),ph=$('fPhone').value.replace(/\D/g,'');if(ph.length===11&&ph[0]==='1')ph=ph.slice(1);
  var msg=name.length<1?'Please enter your first name.':ph.length!==10?'Please enter a 10-digit mobile number.':!/^\d{5}$/.test(zip.value)?'Please enter a 5-digit ZIP code.':'';
  if(msg){err.textContent=msg;err.hidden=false;track('form_error',{msg:msg});return;}
  err.hidden=true;
  var correction=!!lead; /* "Wrong number? Edit" after a successful submit: same answers, new number, no second Meta Lead */
  var pr=price(),alt=altPrice(),xs=chosenExtras().map(function(n){return L.extras[n];});
  var parts=name.split(/\s+/),first=parts[0].charAt(0).toUpperCase()+parts[0].slice(1),ct=$('consentText').textContent.trim();
  var id=(lead&&lead.id&&!correction)?lead.id:'tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var sum=[L.type[S.type],L.size[S.size],L.finish[S.finish]+' finishes'].concat(xs.length?['+ '+xs.join(', ')]:[]).concat(S.start?['Start: '+L.start[S.start]]:[]).join(' · ')+' · Estimate '+pr.text+(alt?' (tub-to-shower option '+alt.text+')':'');
  var p={full_name:name,first_name:first,last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:sum,
    sms_consent:'yes',sms_consent_text:ct,consent_text:ct,marketing_consent:'no',
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,page_variant:'calc',lp_variant:'calc',zip_in_area:inArea(zip.value),cta:'calc',form_source:'calc',
    calc_type:S.type,calc_size_key:S.size,calc_finish_key:S.finish,calc_extras_keys:chosenExtras().join(','),
    calc_project:L.type[S.type],calc_size:L.size[S.size],calc_size_assumed:(S.size==='U'||S.size==='SU')?'yes':'no',calc_finish:L.finish[S.finish],calc_extras:xs.join(', '),calc_start:S.start?L.start[S.start]:'',
    calc_range:pr.text,calc_low:String(pr.lo),calc_high:String(pr.hi),calc_alt_range:alt?alt.text:'',calc_summary:sum,calc_session:SID,calc_version:'calc-v1.2',pricing_version:P.version,
    correction_of:correction?lead.id:'',
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  sending=true;var lab=$('fLabel'),btn=$('fSubmit'),label=lab.textContent;btn.disabled=true;lab.textContent='Sending…';
  track(correction?'number_correction_attempt':'submit_attempt',{});
  function reset(){sending=false;btn.disabled=false;lab.textContent=label;}
  function fail(unknown){reset();track(unknown?'submit_unknown':'submit_fail',{});
    err.innerHTML=(unknown?"We couldn't confirm your request went through. Please try again, or ":"We couldn't send your request. Please try again, or ")+'call or text <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a>.';err.hidden=false;}
  function ok(){
    sending=false;btn.disabled=false;lab.textContent=label;
    var wasCorrection=correction;lead={id:wasCorrection?lead.id:id,range:pr.text,alt:alt?alt.text:'',t:Date.now()};
    steps.contact.hidden=true;$('cqDone').hidden=false;root.classList.add('is-done');var hh=d.querySelector('.cqhero');if(hh)hh.classList.remove('on-contact');
    $('doneHi').textContent='Check your phone, '+first+'!';$('donePhone').textContent=fmt(ph);
    $('doneWhen').textContent=followLine();
    $('cqReveal').hidden=true;$('cqShow').hidden=true;startReveal();
    try{$('doneHi').focus({preventScroll:true});}catch(x){}
    var r=root.getBoundingClientRect();if(r.top<0)root.scrollIntoView({block:'start',behavior:'smooth'});
    if(wasCorrection){track('number_corrected',{});return;}
    track('submit_ok',{});
    window.dataLayer.push({event:'generate_lead',project_type:L.type[S.type],page_angle:ANGLE,event_id:id,cta:'calc',form_source:'calc'});
    try{if(window.fbq)fbq('track','Lead',{content_name:L.type[S.type]},{eventID:id});}catch(x){}
    try{if(window.clarity)clarity('event','generate_lead');}catch(x){}
    if(window.tsrCapi)tsrCapi({event_id:id,phone:ph,first:first,last:parts.slice(1).join(' '),zip:zip.value,project:L.type[S.type],page_url:location.href.split('#')[0]});
  }
  if(window.TSR_CALC_TEST){window.TSR_CALC_TEST(p);ok();return;} /* QA hook: the test script intercepts the lead */
  var ctl=('AbortController' in window)?new AbortController():null,timer=setTimeout(function(){if(ctl)ctl.abort();},15000);
  fetch('/api/lead',{method:'POST',body:new URLSearchParams(p),signal:ctl?ctl.signal:undefined}).then(function(r){clearTimeout(timer);
    return r.json().catch(function(){return {};}).then(function(j){if(r.ok&&j.ok)ok();else fail(r.status>=500&&j.error==='network');});
  }).catch(function(){clearTimeout(timer);fail(true);});
});
function followLine(){var when='soon';
  try{var f=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',weekday:'short',hour:'numeric',hourCycle:'h23'}).formatToParts(new Date()),wd='',h=12;
    f.forEach(function(x){if(x.type==='weekday')wd=x.value;if(x.type==='hour')h=parseInt(x.value,10);});
    if(wd==='Sun'||(wd==='Sat'&&h>=19))when='on Monday morning';else if(h>=19)when='tomorrow morning';else if(h<9)when='this morning';else when='soon';}catch(x){}
  return 'Serhii, the owner, will follow up '+when+' to answer questions. No obligation.';}
/* 2-minute fallback (council R4-R5): elapsed time since the confirmed submit, survives app switching; opening it sends nothing */
var revT=null;
function startReveal(){clearInterval(revT);revT=setInterval(function(){if(lead&&Date.now()-lead.t>=120000){clearInterval(revT);$('cqReveal').hidden=false;}},1000);}
$('cqRevealBtn').addEventListener('click',function(){if(!lead)return;$('cqShowRange').textContent=lead.range;$('cqShowAlt').textContent=lead.alt?'Tub to walk-in shower option: '+lead.alt:'';$('cqShow').hidden=false;$('cqReveal').hidden=true;track('fallback_opened',{});});
$('cqFix').addEventListener('click',function(){$('cqDone').hidden=true;root.classList.remove('is-done');steps.contact.hidden=false;$('fPhone').value='';$('fPhone').focus();$('fLabel').textContent='Text Me My Estimate';$('cqFixNote').hidden=false;track('number_fix_open',{});});
var sv=$('doneSave');if(sv)sv.addEventListener('click',function(){track('save_contact',{});});

/* sticky bar: hidden while the calculator is on screen; "Continue My Estimate" once started; hidden after submit */
var st=$('sticky'),s1=st&&st.querySelector('.s1');
if(st&&'IntersectionObserver' in window){var vis=true;new IntersectionObserver(function(es){vis=es[0].isIntersecting;upd();},{threshold:0.15}).observe(root);
  var upd=function(){var on=!vis&&!lead;st.classList.toggle('show',on);st.setAttribute('aria-hidden',on?'false':'true');if(s1)s1.textContent=started?'Continue My Estimate':'Get My Price';};
  root.addEventListener('click',function(){setTimeout(upd,0);});}
if(s1)s1.addEventListener('click',function(e){e.preventDefault();root.scrollIntoView({block:'start',behavior:'smooth'});});
[].forEach.call(d.querySelectorAll('a[href="#book"]'),function(a){if(a===s1)return;a.addEventListener('click',function(e){e.preventDefault();root.scrollIntoView({block:'start',behavior:'smooth'});});});

track('calc_view',{});show(0);
})();
