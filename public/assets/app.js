(()=>{"use strict";
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)],root=document.documentElement;
const ls={get:k=>{try{return localStorage.getItem(k)}catch{return null}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch{}}};
const toast=m=>{const t=$("#toast");t.textContent=m;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2200)};
window.ciqToast=toast;
$("#theme")?.addEventListener("click",()=>{const t=root.dataset.theme==="dark"?"light":"dark";root.dataset.theme=t;ls.set("ciq-theme",t)});
const prog=$("#progress"),top_=$("#top");
const onScroll=()=>{const h=root.scrollHeight-innerHeight;prog.style.width=(h>0?scrollY/h*100:0)+"%";top_.classList.toggle("show",scrollY>600)};
addEventListener("scroll",onScroll,{passive:true});onScroll();
top_.addEventListener("click",()=>scrollTo({top:0}));
const burger=$("#burger"),nav=$("nav.main");
burger?.addEventListener("click",()=>{const o=nav.classList.toggle("open");burger.setAttribute("aria-expanded",o)});
// cookie banner + optional analytics (only after consent)
const loadGA=()=>{if(!window.CIQ_GA||window.__ga)return;window.__ga=1;const s=document.createElement("script");s.async=1;s.src="https://www.googletagmanager.com/gtag/js?id="+CIQ_GA;document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag("js",new Date());gtag("config",CIQ_GA,{anonymize_ip:true})};
const ck=$("#cookie"),c=ls.get("ciq-consent");
if(!c)ck.classList.add("show");else if(c==="yes")loadGA();
$$("[data-consent]",ck).forEach(b=>b.addEventListener("click",()=>{ls.set("ciq-consent",b.dataset.consent);ck.classList.remove("show");if(b.dataset.consent==="yes")loadGA()}));
// UTM first-touch
try{const p=new URLSearchParams(location.search),u={};["source","medium","campaign","term","content"].forEach(k=>{const v=p.get("utm_"+k);if(v)u[k]=v.slice(0,80)});if(Object.keys(u).length&&!ls.get("ciq-utm"))ls.set("ciq-utm",JSON.stringify(u))}catch{}
// site search
const q=$("#q"),res=$("#results");
q?.addEventListener("input",()=>{const v=q.value.trim().toLowerCase();if(!v){res.classList.remove("open");return}
const hits=(window.CIQ_PAGES||[]).filter(p=>(p.t+" "+p.d+" "+p.k).toLowerCase().includes(v)).slice(0,6);
res.innerHTML=hits.length?hits.map(p=>`<a href="${p.u}">${p.t}<small>${p.d}</small></a>`).join(""):"<a>No results</a>";res.classList.add("open")});
document.addEventListener("keydown",e=>{if(e.key==="Escape")res?.classList.remove("open")});
document.addEventListener("click",e=>{if(!e.target.closest(".search"))res?.classList.remove("open")});
// password toggle
$$("input[type=password]").forEach(i=>{const w=document.createElement("div");w.className="pw";i.before(w);w.append(i);const b=document.createElement("button");b.type="button";b.textContent="Show";b.setAttribute("aria-label","Show password");b.onclick=()=>{const s=i.type==="password";i.type=s?"text":"password";b.textContent=s?"Hide":"Show";b.setAttribute("aria-label",s?"Hide password":"Show password")};w.append(b)});
// copy buttons
$$("[data-copy]").forEach(b=>b.addEventListener("click",async()=>{const el=$(b.dataset.copy);try{await navigator.clipboard.writeText(el.value||el.innerText);toast("Copied to clipboard")}catch{toast("Copy failed")}}));
// confirm modal
const dlg=$("#modal");let pending=null;
document.addEventListener("click",e=>{const t=e.target.closest("[data-confirm]");if(!t)return;e.preventDefault();$("#modal-msg").textContent=t.dataset.confirm;pending=t.dataset.action;dlg.showModal()});
$("#modal-no")?.addEventListener("click",()=>dlg.close());
$("#modal-yes")?.addEventListener("click",async()=>{dlg.close();if(pending==="logout"){await fetch("/api/auth/logout",{method:"POST"});location.href="/"}});
// forms
$$("form[data-api]").forEach(f=>f.addEventListener("submit",async e=>{e.preventDefault();
const err=$(".form-error",f),ok=$(".form-ok",f),btn=$("button[type=submit]",f),show=(el,m)=>{el.textContent=m;el.hidden=false};
err.hidden=ok.hidden=true;const d=Object.fromEntries(new FormData(f));
if(d.confirmPassword!==undefined&&d.confirmPassword!==d.password)return show(err,"Passwords do not match.");
if(f.dataset.api.includes("signup"))d.utm=JSON.parse(ls.get("ciq-utm")||"null");
btn.classList.add("loading");btn.disabled=true;
try{const r=await fetch(f.dataset.api,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)});const j=await r.json().catch(()=>({}));
if(!r.ok)throw new Error(j.error||"Something went wrong. Please try again.");
if(f.dataset.redirect){location.href=f.dataset.redirect;return}
show(ok,j.message||"Done.");f.reset();}catch(x){show(err,x.message)}finally{btn.classList.remove("loading");btn.disabled=false}}));
// auth-aware header + notices
fetch("/api/auth/me").then(r=>r.ok?r.json():null).then(j=>{const a=$("#authlink");if(j&&a){a.textContent="Dashboard";a.href="/dashboard"}}).catch(()=>{});
const p=new URLSearchParams(location.search),n=$("#notice");
if(n){if(p.get("registered"))n.textContent="Account created. Please log in.";else if(p.get("reset"))n.textContent="Password updated. Please log in with your new password.";else n.remove()}
const tk=$("input[name=token]");if(tk)tk.value=p.get("token")||"";
})();
(()=>{const $$=(s)=>[...document.querySelectorAll(s)],rm=matchMedia("(prefers-reduced-motion:reduce)").matches;
if(rm)$$("animateMotion").forEach(a=>a.remove());
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const t=e.target;io.unobserve(t);t.classList.add("in");
if(t.dataset.count&&!rm){const end=+t.dataset.count,t0=performance.now();const f=n=>{const p=Math.min(1,(n-t0)/1400);t.textContent=Math.round(end*(1-Math.pow(1-p,3))).toLocaleString();if(p<1)requestAnimationFrame(f)};requestAnimationFrame(f)}}),{threshold:.25});
$$("main .card,main section.block h2,main .stat,main details").forEach((el,i)=>{if(!el.closest(".auth")){el.classList.add("reveal");el.style.setProperty("--d",(i%3)*.1+"s")}});
$$(".reveal,[data-count]").forEach(el=>io.observe(el));
const pv=document.getElementById("pv");if(pv){const S=[[.18,"Over 4 · need 52 off 96 · 1 down"],[.46,"Over 13 · need 71 off 42 · 4 down"],[.74,"Over 17 · need 38 off 18 · 6 down"],[.93,"Over 19 · need 21 off 6 · 8 down"]];let i=0;
const go=()=>{const[v,l]=S[i++%S.length];document.getElementById("pb").style.width=v*100+"%";pv.textContent=v.toFixed(2);document.getElementById("pl").textContent=l};setTimeout(()=>{go();if(!rm)setInterval(go,3200)},600)}})();
