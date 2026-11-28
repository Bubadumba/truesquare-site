/* calc-v1 (Meta W23, 27.11): bathroom price calculator on /bathroom-remodel-cost-calc.
   Own file on purpose: lp.js (V3, Q, /bathroom-remodel-cost) is never touched. Reads WEBHOOK_URL / PREVIEW from site.js only at submit.
   Flow: project -> size -> style -> materials -> extras -> start -> phone. The price is NOT shown before the phone:
   the lead goes to the same GHL webhook with calc_range, and GHL texts the price (owner 27.11 23:04: "price by text within 1 minute").
   PRICES below are the only place the calculator's numbers live (all in: labor, materials, permits; WA sales tax extra). */
(function(){
var d=document,$=function(id){return d.getElementById(id);};
var root=$('calc');if(!root)return;

/* ===== PRICES (client prices, USD, before WA sales tax). [ЖДЁТ РЕШЕНИЯ Сергея: таблица в Сайт/ЦЕНЫ_КАЛЬКУЛЯТОР_*.md] =====
   base = "from" price at Mid-range finish; finish multiplies the base; extras are added on top.
   shown range = base*finish + extras, rounded down to $500 ... that x 1.15, rounded up to $500. */
var PRICES={
  base:{full:{S:20000,M:24000,L:28500},tub:{S:12000,L:13500},shower:{S:10500,L:12000}},
  finish:{full:{e:0.80,m:1,p:1.40},tub:{e:0.88,m:1,p:1.35},shower:{e:0.88,m:1,p:1.35}},
  extras:{layout:6000,walkin:1500,curbless:3500,heat:{S:1500,M:1900,L:2400},double:2500,bench:900,grab:450},
  spread:1.15
};

/* ===== labels (what goes to GHL and to the summary line) ===== */
var L={
  type:{full:'Full remodel',tub:'Tub to walk-in shower',shower:'Shower remodel',unsure:'Not sure yet'},
  size:{S:'Small',M:'Medium',L:'Large',U:'Not sure',SS:'Standard shower',SL:'Larger shower'},
  style:{modern:'Modern',classic:'Classic',warm:'Warm natural',spa:'Dark spa'},
  finish:{e:'Essential',m:'Mid-range',p:'Premium'},
  extras:{layout:'Move toilet/shower/vanity',walkin:'Walk-in shower instead of tub',curbless:'No-step shower entry',heat:'Heated floor',double:'Double vanity',bench:'Shower bench',grab:'Grab bars'},
  start:{asap:'As soon as possible',m1:'In 1–3 months',m3:'In 3+ months',look:'Just checking prices'}
};
var S={type:'full',size:'M',style:'modern',finish:'m',extras:{},start:''},answered={};
var ANGLE=d.body.getAttribute('data-angle')||'calc-v1',Q=new URLSearchParams(location.search);
var DEBUG=/pages\.dev$|localhost|127\.0\.0\.1/.test(location.hostname); /* preview only: shows the computed range on every step so the owner can check the numbers */

function kind(){return S.type==='tub'?'tub':S.type==='shower'?'shower':'full';}
function sizeKey(){var k=kind();if(k==='full')return S.size==='S'?'S':S.size==='L'?'L':'M';return S.size==='SL'?'L':'S';}
function price(){
  var k=kind(),sk=sizeKey(),b=PRICES.base[k][sk]*PRICES.finish[k][S.finish],x=0,e=PRICES.extras;
  for(var n in S.extras){if(!S.extras[n]||!avail(n))continue;x+=n==='heat'?e.heat[sk]:e[n];}
  var lo=Math.floor((b+x)/500)*500,hi=Math.ceil((b+x)*PRICES.spread/500)*500;
  return {lo:lo,hi:hi,text:'$'+lo.toLocaleString('en-US')+'–$'+hi.toLocaleString('en-US')};
}
/* which extras make sense for the current answers */
function avail(n){var k=kind(),sk=sizeKey();
  if(n==='walkin'||n==='heat'||n==='layout')return k==='full';
  if(n==='double')return k==='full'&&sk!=='S';
  if(n==='grab')return k!=='full';
  return true;}

/* ===== the bathroom picture (2.5D, inline SVG; style + materials + size + extras change it) ===== */
var PAL={
  modern:{wall:'#EEEEEB',tile:'#FBFBFA',grout:'#D6D6D2',tile2:'#F1F1EE',metal:'#1F1F1F',wood:'#7A4E33',wood2:'#5E3B26',floor:'#6B6C6E',fline:'#5A5B5D',acc:'#2F6F6A',pat:'stack'},
  classic:{wall:'#E9EEF3',tile:'#FFFFFF',grout:'#C7CED6',tile2:'#F3F5F8',metal:'#B9C1C9',wood:'#2C3E57',wood2:'#22324A',floor:'#E4E2DE',fline:'#BDB9B2',acc:'#7C8FA6',pat:'sub'},
  warm:{wall:'#F0E7DB',tile:'#E9D7C1',grout:'#D2BCA2',tile2:'#E1CCB2',metal:'#B98A3E',wood:'#C29567',wood2:'#A57B50',floor:'#C9A98A',fline:'#B08F70',acc:'#8C9A6A',pat:'zel'},
  spa:{wall:'#3B3E42',tile:'#4C5156',grout:'#3E4246',tile2:'#565B60',metal:'#C8A468',wood:'#D2BC9C',wood2:'#B9A381',floor:'#2E3033',fline:'#3C3F43',acc:'#9DB4A8',pat:'large'}
};
function shade(h,f){var n=parseInt(h.slice(1),16),r=n>>16,g=n>>8&255,b=n&255,t=f<0?0:255,p=Math.abs(f);r=Math.round((t-r)*p+r);g=Math.round((t-g)*p+g);b=Math.round((t-b)*p+b);return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);}
function R(x,y,w,h,f,o){return '<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+w.toFixed(1)+'" height="'+h.toFixed(1)+'" fill="'+f+'"'+(o||'')+'/>';}
function draw(){
  var p=PAL[S.style],k=kind(),sk=sizeKey(),fin=S.finish,ex=S.extras,prem=fin==='p',ess=fin==='e';
  var Wd=k==='full'?{S:196,M:232,L:266}[sk]:232,bx0=180-Wd/2,bx1=180+Wd/2,yt=6,yb=146,H=210;
  var pat=prem&&p.pat!=='sub'?'large':p.pat;
  var o=[];
  o.push('<defs>');
  o.push('<pattern id="tp" width="'+({sub:16,stack:7,zel:18,large:30}[pat])+'" height="'+({sub:8,stack:20,zel:9,large:30}[pat])+'" patternUnits="userSpaceOnUse">');
  if(pat==='sub')o.push(R(0,0,16,8,p.tile)+'<path d="M0 .25H16M0 4.25H16M.25 0V4M8.25 4V8" stroke="'+p.grout+'" stroke-width=".6"/>');
  if(pat==='stack')o.push(R(0,0,7,20,p.tile)+'<path d="M.25 0V20M0 .25H7" stroke="'+p.grout+'" stroke-width=".6"/>');
  if(pat==='zel')o.push(R(0,0,18,9,p.tile)+R(9,0,9,9,p.tile2)+R(3,3,3,3,shade(p.tile,-.03))+'<path d="M.3 0V9M9.3 0V9M0 .3H18" stroke="'+p.grout+'" stroke-width=".7"/>');
  if(pat==='large')o.push(R(0,0,30,30,p.tile)+R(0,0,30,30,'url(#vein)',' opacity=".5"')+'<path d="M.2 0V30M0 .2H30" stroke="'+p.grout+'" stroke-width=".5"/>');
  o.push('</pattern><linearGradient id="vein" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".08"/></linearGradient>');
  o.push('<radialGradient id="glow"><stop offset="0" stop-color="#FFE9BF" stop-opacity=".9"/><stop offset="1" stop-color="#FFE9BF" stop-opacity="0"/></radialGradient>');
  o.push('<linearGradient id="heat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A5A" stop-opacity="0"/><stop offset="1" stop-color="#FF8A4A" stop-opacity=".35"/></linearGradient>');
  o.push('<linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".45" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".22"/></linearGradient></defs>');
  /* walls + floor */
  o.push(R(0,0,360,H,shade(p.wall,-.12)));
  o.push('<path d="M0 0L'+bx0+' '+yt+'V'+yb+'L0 '+H+'Z" fill="'+shade(p.wall,-.07)+'"/><path d="M360 0L'+bx1+' '+yt+'V'+yb+'L360 '+H+'Z" fill="'+shade(p.wall,-.14)+'"/>');
  o.push(R(bx0,yt,Wd,yb-yt,p.wall));
  var sw=k==='full'?Wd*.40:Wd*.50,sx=bx0;
  /* tile: essential = shower only, mid = shower + wainscot, premium = whole wall */
  if(prem)o.push(R(bx0,yt,Wd,yb-yt,'url(#tp)'));
  else{ if(!ess)o.push(R(bx0,92,Wd,yb-92,'url(#tp)')+R(bx0,91,Wd,1.6,shade(p.grout,-.1)));o.push(R(sx,yt,sw,yb-yt,'url(#tp)'));}
  o.push('<path d="M'+bx0+' '+yb+'H'+bx1+'L360 '+H+'H0Z" fill="'+p.floor+'"/>');
  var N=prem?7:9,fl='';for(var i=0;i<=N;i++){fl+='M'+(bx0+i*Wd/N).toFixed(1)+' '+yb+'L'+(i*360/N).toFixed(1)+' '+H;}
  [151,158,167,179,194].forEach(function(y){fl+='M0 '+y+'H360';});
  o.push('<path d="'+fl+'" stroke="'+p.fline+'" stroke-width=".7" opacity=".7" clip-path="url(#fc)"/><clipPath id="fc"><path d="M'+bx0+' '+yb+'H'+bx1+'L360 '+H+'H0Z"/></clipPath>');
  if(ex.heat&&avail('heat'))o.push('<path d="M'+bx0+' '+yb+'H'+bx1+'L360 '+H+'H0Z" fill="url(#heat)"/>');
  o.push('<path d="M'+bx0+' '+yb+'H'+bx1+'" stroke="'+shade(p.wall,-.25)+'" stroke-width="1"/>');
  /* tub or walk-in shower */
  var hasTub=k==='full'&&!ex.walkin;
  var hx=sx+sw*.32;
  if(hasTub){
    o.push(R(sx+2,yb-31,sw-4,31,'#FAFAF8',' rx="5" stroke="#D4D4D0" stroke-width=".8"')+R(sx+5,yb-27,sw-10,1.4,'#E3E3DF'));
    o.push('<ellipse cx="'+(sx+sw/2)+'" cy="'+(yb+1)+'" rx="'+(sw/2)+'" ry="3" fill="#000" opacity=".12"/>');
    o.push('<path d="M'+(sx+10)+' '+(yb-34)+'h7v4" stroke="'+p.metal+'" stroke-width="2" fill="none"/>');
    o.push('<path d="M'+hx+' 26v8" stroke="'+p.metal+'" stroke-width="2"/><ellipse cx="'+hx+'" cy="36" rx="6" ry="2.6" fill="'+p.metal+'"/>');
    if(ess){o.push('<path d="M'+(sx+sw*.46)+' 22H'+(sx+sw-2)+'" stroke="'+p.metal+'" stroke-width="1.6"/>');
      var cx0=sx+sw*.5,cw=sw*.5-3,cp='M'+cx0+' 23';for(var j=0;j<=6;j++){cp+='Q'+(cx0+cw*(j+.5)/6)+' '+(j%2?25:21)+' '+(cx0+cw*(j+1)/6)+' 23';}
      o.push('<path d="'+cp+'V'+(yb-34)+'H'+cx0+'Z" fill="'+p.acc+'" opacity=".92"/>');
      for(j=1;j<6;j++)o.push('<path d="M'+(cx0+cw*j/6)+' 25V'+(yb-34)+'" stroke="'+shade(p.acc,-.18)+'" stroke-width=".8"/>');}
    else o.push(R(sx+sw*.42,24,sw*.58-3,yb-56,'url(#gl)',' stroke="#fff" stroke-opacity=".8" stroke-width=".9"'));
  }else{
    if(!ex.curbless)o.push(R(sx+1,yb-5,sw-2,5,shade(p.tile,-.06),' stroke="'+p.grout+'" stroke-width=".5"'));
    o.push(R(sx+sw*.45,yb-2,9,1.4,p.metal));
    if(prem){o.push(R(hx-12,14,24,3,p.metal)+'<path d="M'+hx+' '+yt+'V14" stroke="'+p.metal+'" stroke-width="1.6"/>');
      for(j=0;j<7;j++)o.push('<path d="M'+(hx-9+j*3)+' 20v'+(10+j%3*6)+'" stroke="#9EC7E8" stroke-width=".7" opacity=".55"/>');}
    else o.push('<path d="M'+(sx+5)+' 34h'+(sw*.2)+'v4" stroke="'+p.metal+'" stroke-width="1.8" fill="none"/><ellipse cx="'+(sx+5+sw*.2)+'" cy="39" rx="5" ry="2.2" fill="'+p.metal+'"/>');
    o.push('<circle cx="'+(sx+9)+'" cy="80" r="4" fill="'+p.metal+'"/><circle cx="'+(sx+9)+'" cy="80" r="1.6" fill="'+shade(p.metal,.4)+'"/>');
    if(!ess)o.push(R(sx+sw*.18,58,24,15,shade(p.tile,-.16),' rx="1"')+R(sx+sw*.18+4,63,5,10,'#FFFFFF',' rx="1" opacity=".85"')+R(sx+sw*.18+11,65,5,8,p.acc,' rx="1"'));
    if(ex.bench)o.push(R(sx+3,yb-25,sw*.34,20,shade(p.tile,-.08),' stroke="'+p.grout+'" stroke-width=".6"')+R(sx+3,yb-26,sw*.34,2.4,shade(p.tile,.06)));
    if(ex.grab&&avail('grab'))o.push('<path d="M'+(sx+sw*.15)+' 96h26" stroke="'+p.metal+'" stroke-width="2.6" stroke-linecap="round"/>');
    var gx=sx+sw*.36,gw=sw*.64-2;
    o.push(R(gx,18,gw,yb-20-(ex.curbless?0:5),'url(#gl)',' stroke="'+(ess?p.metal:'#fff')+'" stroke-opacity="'+(ess?1:.85)+'" stroke-width="'+(ess?2.2:.9)+'"'));
    if(ess)o.push(R(gx+gw-7,70,2.2,22,p.metal,' rx="1"'));
    else o.push(R(gx-1,46,2,6,p.metal)+R(gx-1,108,2,6,p.metal));
  }
  /* toilet + vanity (for shower-only jobs they stay as they are: drawn faded) */
  var keep=k!=='full'?' opacity=".5"':'';
  var dbl=ex.double&&avail('double'),vw=Wd*(dbl?.44:.30),vx=bx1-5-vw,tc=sx+sw+(vx-(sx+sw))/2;
  o.push('<g'+keep+'>');
  o.push('<ellipse cx="'+tc+'" cy="'+(yb+1)+'" rx="12" ry="2.6" fill="#000" opacity=".12"/>');
  o.push(R(tc-11,yb-50,22,19,'#FBFBF9',' rx="2.5" stroke="#D2D2CE" stroke-width=".7"')+R(tc-12,yb-52,24,3,'#F2F2EF',' rx="1"')+R(tc+5,yb-49,4,1.8,p.metal));
  o.push('<path d="M'+(tc-8)+' '+(yb-22)+'L'+(tc-5.5)+' '+yb+'H'+(tc+5.5)+'L'+(tc+8)+' '+(yb-22)+'Z" fill="#F4F4F1" stroke="#D2D2CE" stroke-width=".6"/><ellipse cx="'+tc+'" cy="'+(yb-26)+'" rx="13" ry="5.5" fill="#FBFBF9" stroke="#D2D2CE" stroke-width=".7"/>');
  var sinks=dbl?[vx+vw*.27,vx+vw*.73]:[vx+vw/2];
  var vy=prem?yb-44:yb-36,vh=prem?23:36;
  if(prem){o.push('<ellipse cx="'+(vx+vw/2)+'" cy="'+(yb+2)+'" rx="'+(vw*.6)+'" ry="6" fill="url(#glow)" opacity=".8"/>'+R(vx+2,vy+vh,vw-4,1.6,'#FFE7B5',' opacity=".9"'));}
  else o.push('<ellipse cx="'+(vx+vw/2)+'" cy="'+(yb+1)+'" rx="'+(vw/2)+'" ry="2.6" fill="#000" opacity=".12"/>');
  o.push(R(vx,vy,vw,vh,p.wood,' rx="1.5"'));
  if(fin==='m'){o.push('<path d="M'+(vx+2)+' '+(vy+vh/2)+'H'+(vx+vw-2)+'" stroke="'+p.wood2+'" stroke-width=".8"/>');sinks.forEach(function(c){o.push(R(c-5,vy+vh/4-1,10,1.8,p.metal,' rx=".9"')+R(c-5,vy+vh*.75-1,10,1.8,p.metal,' rx=".9"'));});}
  else if(ess){o.push('<path d="M'+(vx+vw/2)+' '+(vy+3)+'V'+(vy+vh-3)+'" stroke="'+p.wood2+'" stroke-width=".8"/>'+R(vx+vw/2-4,vy+9,1.6,6,p.metal)+R(vx+vw/2+2.4,vy+9,1.6,6,p.metal));}
  else{o.push('<path d="M'+(vx+3)+' '+(vy+4)+'H'+(vx+vw-3)+'" stroke="'+p.wood2+'" stroke-width=".7"/>');}
  o.push(R(vx-2,vy-4,vw+4,4.2,prem?'#F6F5F2':ess?'#ECEBE7':'#F4F3F0',' rx="1"'));
  sinks.forEach(function(c){
    o.push('<ellipse cx="'+c+'" cy="'+(vy-3)+'" rx="8" ry="2" fill="#E6E6E2"/>');
    o.push('<path d="M'+c+' '+(vy-4)+'v-7h5" stroke="'+p.metal+'" stroke-width="1.8" fill="none" stroke-linecap="round"/>');
    var my=vy-52,mh=36;
    if(prem)o.push('<ellipse cx="'+c+'" cy="'+(my+mh/2)+'" rx="22" ry="25" fill="url(#glow)"/>');
    if(ess)o.push(R(c-14,my,28,mh,'#DCE7EE',' stroke="'+p.metal+'" stroke-width="1.6"'));
    else if(S.style==='classic')o.push('<path d="M'+(c-13)+' '+(my+mh)+'V'+(my+12)+'A13 13 0 0 1 '+(c+13)+' '+(my+12)+'V'+(my+mh)+'Z" fill="#DCE7EE" stroke="'+p.metal+'" stroke-width="1.8"/>');
    else if(S.style==='spa')o.push(R(c-14,my,28,mh,'#C9D6DD',' rx="5" stroke="'+(prem?'#FFE3A8':p.metal)+'" stroke-width="1.4"'));
    else o.push('<circle cx="'+c+'" cy="'+(my+mh/2)+'" r="16" fill="#DCE7EE" stroke="'+(S.style==='warm'?p.wood2:p.metal)+'" stroke-width="'+(S.style==='warm'?3:1.8)+'"/>');
    o.push('<path d="M'+(c-8)+' '+(my+6)+'l10 -4" stroke="#fff" stroke-width="2" opacity=".6" stroke-linecap="round"/>');
    if(prem){[c-20,c+20].forEach(function(lx){o.push('<path d="M'+lx+' '+yt+'V'+(my+4)+'" stroke="'+p.metal+'" stroke-width=".8"/><circle cx="'+lx+'" cy="'+(my+8)+'" r="4.5" fill="#FFE9BF" stroke="'+p.metal+'" stroke-width="1"/><circle cx="'+lx+'" cy="'+(my+8)+'" r="11" fill="url(#glow)" opacity=".7"/>');});}
    else o.push(R(c-12,my-9,24,3.4,p.metal,' rx="1.5"')+R(c-11,my-5.6,22,2,'#FFF4D8',' opacity=".8"'));
  });
  o.push('</g>');
  /* decor: towel (mid+), plant (premium) */
  if(!ess)o.push(R(sx+sw+4,58,1.6,1.6,p.metal)+R(sx+sw+2,59,14,26,p.acc,' rx="1.5"')+R(sx+sw+2,79,14,2,shade(p.acc,.25)));
  if(prem)o.push('<path d="M'+(bx1+10)+' 186h18l-3 18h-12z" fill="'+shade(p.wood,-.2)+'"/><path d="M'+(bx1+19)+' 186c-2-14-12-20-16-30c9 4 13 12 16 22c1-12 5-22 13-28c-3 11-7 20-11 36" fill="#5C8A5A"/>');
  root.querySelector('.cqviz').innerHTML='<svg viewBox="0 0 360 210" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration of the bathroom you chose"><g class="cqin">'+o.join('')+'</g></svg>';
  var t=root.querySelector('.cqtag');if(t)t.textContent=[L.type[S.type],L.size[S.size],L.style[S.style],L.finish[S.finish]].filter(Boolean).join(' · ');
  if(DEBUG){var dbg=$('cqDebug');if(dbg){dbg.hidden=false;dbg.textContent='Preview only: '+price().text;}}
}

/* ===== steps ===== */
var ORDER=['type','size','style','finish','extras','start','contact'],cur=0;
var steps={};[].forEach.call(root.querySelectorAll('.cqstep'),function(s){steps[s.dataset.step]=s;});
function track(ev,o){window.dataLayer=window.dataLayer||[];var x={event:ev,page_angle:ANGLE,form_source:'calc',cta:'calc'};for(var k in o)x[k]=o[k];window.dataLayer.push(x);try{if(window.clarity)clarity('event',ev);}catch(e){}}
function show(i,dir){
  cur=i;var name=ORDER[i],k=kind();
  ORDER.forEach(function(n){steps[n].hidden=n!==name;});
  /* size and extras options depend on the project */
  [].forEach.call(root.querySelectorAll('[data-for]'),function(el){var f=el.dataset.for;el.hidden=f==='full'?k!=='full':f==='shower'?k==='full':false;});
  [].forEach.call(root.querySelectorAll('[data-x]'),function(el){var n=el.dataset.x;el.hidden=!avail(n);if(!avail(n)){delete S.extras[n];el.setAttribute('aria-pressed','false');}});
  $('cqNum').textContent=(i+1);$('cqProg').style.width=((i+1)/ORDER.length*100)+'%';
  $('cqBack').hidden=i===0;
  root.classList.toggle('on-contact',name==='contact');root.classList.toggle('past1',i>0);root.classList.toggle('compact',i>=4);
  if(dir){var h=steps[name].querySelector('legend,h2');try{h.focus({preventScroll:true});}catch(e){}}
  var top=root.getBoundingClientRect().top;if(top<-40&&dir)root.scrollIntoView({block:'start'});
  draw();
}
function setPressed(step,v){[].forEach.call(steps[step].querySelectorAll('.cqopt'),function(b){b.setAttribute('aria-pressed',b.dataset.v===v?'true':'false');});}
root.addEventListener('click',function(e){
  var b=e.target.closest('.cqopt');
  if(b){var st=b.closest('.cqstep').dataset.step,v=b.dataset.v;
    if(st==='extras'){var on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on?'true':'false');S.extras[v]=on;draw();updX();track('calc_extra',{value:v,on:on});return;}
    if(st==='type'){S.type=v;if(v==='tub'||v==='shower'){if(S.size!=='SS'&&S.size!=='SL')S.size='SS';}else if(S.size==='SS'||S.size==='SL')S.size='M';}
    else if(st==='size')S.size=v;else if(st==='style')S.style=v;else if(st==='finish')S.finish=v;else if(st==='start')S.start=v;
    setPressed(st,v);draw();
    if(!answered.any){answered.any=1;(function ic(n){if(window.tsrIC)tsrIC(ANGLE,'calc');else if(n<40)setTimeout(function(){ic(n+1);},250);})(0);track('form_start',{step:1});} /* InitiateCheckout once per visit; waits for site.js if the first tap comes before it loads */
    track('calc_step',{step:cur+1,name:st,value:v});
    setTimeout(function(){show(cur+1,1);},170);return;}
  if(e.target.closest('#cqBack')){show(Math.max(0,cur-1),1);return;}
  if(e.target.closest('#cqNext')){track('calc_step',{step:cur+1,name:'extras',value:Object.keys(S.extras).filter(function(n){return S.extras[n];}).join(',')||'none'});show(cur+1,1);}
});
function updX(){var n=0;for(var k in S.extras)if(S.extras[k]&&avail(k))n++;$('cqNextL').textContent=n?'Continue':'No extras, continue';}
/* hover/focus preview on style and materials: the picture changes before the tap */
['style','finish'].forEach(function(st){[].forEach.call(steps[st].querySelectorAll('.cqopt'),function(b){
  var pv=function(){var old=S[st];S[st]=b.dataset.v;draw();S[st]=old;};
  b.addEventListener('mouseenter',pv);b.addEventListener('mouseleave',draw);});});

/* ===== contact + lead ===== */
var AREA='98001,98002,98003,98004,98005,98006,98007,98008,98009,98010,98011,98012,98013,98014,98015,98019,98020,98021,98022,98023,98024,98025,98026,98027,98028,98029,98030,98031,98032,98033,98034,98035,98036,98037,98038,98039,98040,98041,98042,98043,98045,98046,98047,98050,98051,98052,98053,98054,98055,98056,98057,98058,98059,98061,98062,98063,98064,98065,98070,98071,98072,98073,98074,98075,98077,98082,98083,98087,98089,98092,98093,98101,98102,98103,98104,98105,98106,98107,98108,98109,98110,98111,98112,98113,98114,98115,98116,98117,98118,98119,98121,98122,98124,98125,98126,98127,98129,98131,98132,98133,98134,98136,98138,98139,98141,98144,98145,98146,98148,98151,98154,98155,98158,98160,98161,98164,98165,98166,98168,98170,98171,98174,98175,98177,98178,98181,98184,98185,98188,98189,98190,98191,98194,98195,98198,98199,98201,98203,98204,98205,98206,98207,98208,98213,98236,98249,98251,98252,98258,98260,98270,98271,98272,98275,98290,98291,98293,98294,98296,98303,98310,98311,98312,98314,98315,98321,98322,98323,98327,98328,98329,98332,98333,98335,98337,98338,98340,98342,98344,98345,98346,98349,98351,98352,98353,98354,98359,98360,98364,98366,98367,98370,98371,98372,98373,98374,98375,98378,98380,98383,98384,98385,98386,98387,98388,98390,98391,98392,98393,98394,98395,98396,98398,98401,98402,98403,98404,98405,98406,98407,98408,98409,98411,98412,98413,98415,98416,98417,98418,98419,98421,98422,98424,98430,98431,98433,98438,98439,98442,98443,98444,98445,98446,98447,98448,98450,98455,98460,98464,98465,98466,98467,98471,98477,98481,98490,98492,98493,98496,98497,98498,98499,98501,98502,98503,98504,98505,98506,98507,98508,98509,98511,98512,98513,98516,98524,98528,98540,98546,98558,98576,98580,98584,98589,98592,98597,98599';
function inArea(z){return z.length===5&&AREA.indexOf(z)>-1?'yes':'no';}
var form=$('cqForm'),zip=$('fZip'),sending=false,phoneOk=false;
zip.addEventListener('input',function(){zip.value=zip.value.replace(/\D/g,'').slice(0,5);});
$('fPhone').addEventListener('input',function(){var v=this.value.replace(/\D/g,'');if(v.length===11&&v[0]==='1')v=v.slice(1);if(!phoneOk&&v.length===10){phoneOk=true;track('form_phone',{});}});
[['fName','fPhone'],['fPhone','fZip']].forEach(function(p){$(p[0]).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();$(p[1]).focus();}});});
form.addEventListener('submit',function(e){
  e.preventDefault();if(sending)return;
  var err=$('fErr'),name=$('fName').value.trim(),ph=$('fPhone').value.replace(/\D/g,'');if(ph.length===11&&ph[0]==='1')ph=ph.slice(1);
  var msg=name.length<2?'Please enter your name.':ph.length!==10?'Please enter a 10-digit mobile number.':!/^\d{5}$/.test(zip.value)?'Please enter a 5-digit ZIP code.':'';
  if(msg){err.textContent=msg;err.hidden=false;track('form_error',{msg:msg});return;}
  err.hidden=true;sending=true;
  var pr=price(),xs=Object.keys(S.extras).filter(function(n){return S.extras[n]&&avail(n);}).map(function(n){return L.extras[n];});
  var summary=[L.type[S.type]+(S.type==='unsure'?' (priced as full remodel)':''),L.size[S.size],L.style[S.style],L.finish[S.finish]+' materials'].concat(xs.length?['+ '+xs.join(', ')]:[]).concat(S.start?['Start: '+L.start[S.start]]:[]).join(' · ')+' · Estimate '+pr.text;
  var parts=name.split(/\s+/),ct=$('consentText').textContent.trim(),id='tsr-'+Date.now()+'-'+Math.random().toString(36).slice(2,8);
  var p={full_name:name,first_name:parts[0],last_name:parts.slice(1).join(' '),phone:'+1'+ph,zip:zip.value,project_type:summary,
    sms_consent:'yes',sms_consent_text:ct,consent_text:ct,marketing_consent:'no',
    lead_source:'Website - truesquareremodel.com',page_angle:ANGLE,page_variant:'calc',lp_variant:'calc',zip_in_area:inArea(zip.value),cta:'calc',form_source:'calc',
    calc_project:L.type[S.type],calc_size:L.size[S.size],calc_style:L.style[S.style],calc_finish:L.finish[S.finish],calc_extras:xs.join(', '),calc_start:S.start?L.start[S.start]:'',
    calc_range:pr.text,calc_low:String(pr.lo),calc_high:String(pr.hi),
    utm_source:Q.get('utm_source')||'',utm_medium:Q.get('utm_medium')||'',utm_campaign:Q.get('utm_campaign')||'',utm_content:Q.get('utm_content')||'',utm_term:Q.get('utm_term')||'',
    fbclid:Q.get('fbclid')||'',page_url:location.href.split('#')[0],event_id:id,submitted_at:new Date().toISOString()};
  var lab=$('fLabel'),btn=$('fSubmit'),label=lab.textContent;btn.disabled=true;lab.textContent='Sending…';
  function reset(){sending=false;btn.disabled=false;lab.textContent=label;}
  function done(){
    steps.contact.hidden=true;$('cqDone').hidden=false;root.classList.add('is-done');
    $('doneHi').textContent='Check your phone, '+parts[0].charAt(0).toUpperCase()+parts[0].slice(1)+'!';
    $('donePhone').textContent='('+ph.slice(0,3)+') '+ph.slice(3,6)+'-'+ph.slice(6);
    var when='shortly';
    try{var f=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',weekday:'short',hour:'numeric',hourCycle:'h23'}).formatToParts(new Date()),wd='',h=12;
      f.forEach(function(x){if(x.type==='weekday')wd=x.value;if(x.type==='hour')h=parseInt(x.value,10);});
      if(wd==='Sun'||(wd==='Sat'&&h>=19))when='Monday morning';else if(h>=19)when='tomorrow morning';else if(h<9)when='this morning';else when='in a few minutes';}catch(x){}
    $('doneWhen').textContent='Serhii will call you '+when+' to confirm the details and set up a free visit.';
    try{$('doneHi').focus({preventScroll:true});}catch(x){}
    var r=root.getBoundingClientRect();if(r.top<0)root.scrollIntoView({block:'start',behavior:'smooth'});
    window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'generate_lead',project_type:L.type[S.type],page_angle:ANGLE,event_id:id,cta:'calc',form_source:'calc'});
    try{if(window.fbq)fbq('track','Lead',{content_name:L.type[S.type]},{eventID:id});}catch(x){}
    try{if(window.clarity)clarity('event','generate_lead');}catch(x){}
    if(window.tsrCapi)tsrCapi({event_id:id,phone:ph,first:parts[0],last:parts.slice(1).join(' '),zip:zip.value,project:L.type[S.type],page_url:location.href.split('#')[0]});
  }
  var url=window.WEBHOOK_URL||'';
  if(window.TSR_CALC_TEST){window.TSR_CALC_TEST(p);done();return;} /* QA hook: the test script intercepts the lead instead of sending it */
  if(!url){if(window.PREVIEW){done();return;}reset();err.innerHTML='Please call <a href="tel:+12062222328" style="color:inherit;font-weight:700">(206) 222-2328</a>.';err.hidden=false;return;}
  fetch(url,{method:'POST',mode:'no-cors',body:new URLSearchParams(p),keepalive:true}).then(done).catch(function(){reset();err.textContent="That didn't go through. Please call or text (206) 222-2328.";err.hidden=false;});
});
['fName','fPhone','fZip'].forEach(function(id){$(id).addEventListener('focus',function(){if(!answered.contact){answered.contact=1;track('calc_contact',{});}});});
var sv=$('doneSave');if(sv)sv.addEventListener('click',function(){track('save_contact',{});});
updX();show(0);
})();
