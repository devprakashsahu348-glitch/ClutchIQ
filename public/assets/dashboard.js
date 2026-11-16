(async()=>{const $=s=>document.querySelector(s),box=$("#board");let D,tab="batters";
const cols={batters:[["rank","#"],["name","Player"],["rating","Rating"],["matches","Matches"],["pressure_balls","Balls"],["sr_pressure","SR (pressure)"],["sr_normal","SR (normal)"],["impact100","Impact/100"],["consistency","Consistency"]],
bowlers:[["rank","#"],["name","Player"],["rating","Rating"],["matches","Matches"],["pressure_balls","Balls"],["wickets","Wkts"],["econ_pressure","Econ (pressure)"],["econ_normal","Econ (normal)"],["consistency","Consistency"]]};
const draw=()=>{const rows=D[tab];box.innerHTML=`<div class="tw"><table><thead><tr>${cols[tab].map(c=>`<th>${c[1]}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>`<tr class="${r.rank===10?"cut":""}">${cols[tab].map(c=>`<td>${c[0]==="consistency"?Math.round(r[c[0]]*100)+"%":r[c[0]]}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
$("#top10").value=rows.slice(0,10).map(r=>r.rank+". "+r.name).join("\n")};
try{const r=await fetch("/api/rankings");if(r.status===401){location.href="/login?next=dashboard";return}D=await r.json();
$("#who").textContent=D.user.name.split(" ")[0];const m=D.meta,c=m.compare;
$("#cmp").innerHTML=`<tr><td>Ordinary balls</td><td>${(c.False.runs_per_ball).toFixed(2)}</td><td>${(c.False.wicket_rate*100).toFixed(1)}%</td><td>${c.False.balls.toLocaleString()}</td></tr><tr><td>Pressure balls</td><td>${(c.True.runs_per_ball).toFixed(2)}</td><td>${(c.True.wicket_rate*100).toFixed(1)}%</td><td>${c.True.balls.toLocaleString()}</td></tr>`;
draw();document.querySelectorAll(".tabs button").forEach(b=>b.onclick=()=>{tab=b.dataset.tab;document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected",x===b));draw()})}
catch{box.innerHTML='<p class="form-error">Could not load rankings. Please refresh.</p>'}})();
