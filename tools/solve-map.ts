// Bộ giải map v2: npx tsx tools/solve-map.ts <mapId> [--write]
// 1) scale boss thấp nhất mà đường lười thua
// 2) ở mức đó phải có tuyến thắng, và có tuyến phá đủ trại (3 sao) mà vẫn thắng
// 3) mực gốc: thắng được bằng Quill; 3 sao cần brush theo bậc chương (1–3 Quill, 4–6 Rare, 7–10 Epic)
import {readFileSync,writeFileSync} from 'node:fs';
import {maps,BR,dist,type MapData,type P} from '../src/systems';
import {teamRoute,drawPool,simulate,lazyPool,pathCost,free,bossFor,brushFx} from './mapTools';
import {NO_BRUSH} from '../src/systems';

const id=process.argv[2],write=process.argv.includes('--write'),base=maps[id];
const tutorial=id.endsWith('_s1')&&base.chapter===1;
const scaled=(s:number):MapData=>({...base,bosses:base.bosses.map(b=>({...b,scale:+s.toFixed(2)}))});

// Mục tiêu của từng đội: trại + vật phẩm phía bên đội đó
const objects=[...base.camps.map(c=>({...c,camp:true})),...base.items.filter(o=>o.type!=='gate'&&o.type!=='skull')];
const sideOf=(o:P)=>base.starts.length<2?0:dist(o,base.starts[0])+dist(o,bossFor(base,0))<=dist(o,base.starts[1])+dist(o,bossFor(base,1))?0:1;
type Cand={seq:any[],points:P[],cost:number,camps:number};
function candidates(t:number){const mine=objects.filter(o=>sideOf(o)===t),camps=mine.filter((o:any)=>o.camp),out:Cand[]=[],best=new Map<string,Cand>();
 const add=(seq:any[])=>{if(seq.filter(o=>o.type==='chest').some(c=>!seq.slice(0,seq.indexOf(c)).some(k=>k.type==='key'&&k.color===c.color)))return;let pts=teamRoute(base,t,seq);if(!pts)return;let cost=pathCost(base,pts,NO_BRUSH)-seq.filter(o=>o.type==='ink_bottle').reduce((n,o)=>n+o.value,0);let key=seq.map(o=>objects.indexOf(o)).join(','),c={seq,points:pts,cost,camps:seq.filter((o:any)=>o.camp).length};let old=best.get(key);if(!old||old.cost>c.cost)best.set(key,c);};
 const perm=(rest:any[],seq:any[],depth:number)=>{add(seq);if(!depth)return;for(const o of rest)perm(rest.filter(x=>x!==o),[...seq,o],depth-1);};
 perm(mine,[],Math.min(3,mine.length));
 // tour phá hết trại của phía này, có thể ghé thêm 1 vật phẩm
 const tours=(rest:any[],seq:any[])=>{if(!rest.length){add(seq);for(const o of mine.filter(o=>!(o as any).camp))add([...seq,o]);return;}for(const c of rest)tours(rest.filter(x=>x!==c),[...seq,c]);};if(camps.length>3)return [...best.values()];tours([...camps,...mine.filter(o=>o.type==='key')],[]);
 return [...best.values()].sort((a,b)=>a.cost-b.cost);}
const perTeam=base.starts.map((_,t)=>candidates(t));
// ghép tuyến hai đội: lấy top theo số trại và theo chi phí
function combos(){if(perTeam.length===1){const L=perTeam[0],most=Math.max(...L.map(c=>c.camps));return [...new Set([...L.slice(0,45),...L.filter(c=>c.camps===most).slice(0,20)])].map(c=>[c]);}const pickTop=(list:Cand[])=>{let byCamps=[...list].sort((a,b)=>b.camps-a.camps||a.cost-b.cost).slice(0,5),cheap=list.slice(0,5);return [...new Set([...byCamps,...cheap])];};let A=pickTop(perTeam[0]),B=pickTop(perTeam[1]),out:Cand[][]=[];for(const a of A)for(const b of B)out.push([a,b]);return out;}
const lazy=lazyPool(free(base));
const all=combos(),totalCamps=base.camps.length;
const tours=all.filter(c=>c.reduce((n,x)=>n+x.camps,0)>=totalCamps).sort((a,b)=>a.reduce((n,x)=>n+x.cost,0)-b.reduce((n,x)=>n+x.cost,0)).slice(0,40);
const run=(s:number,c:Cand[])=>simulate(scaled(s),drawPool(free(scaled(s)),c.map(x=>x.points)));
// scale cao nhất mà vẫn có tuyến phá đủ trại và thắng, còn >= 20% quân
const threeWins=(s:number)=>{for(const c of tours){const r=run(s,c);if(r.result==='win'&&r.camps>=totalCamps&&r.alive>=Math.ceil(r.total*.15))return {c,r};}return null;};
if(!tours.length){console.log(id,'NO 3-CAMP ROUTE');process.exit(1);}
let lo=.15,hi=4;if(!threeWins(lo)){console.log(`${id}: even at scale ${lo} no 3-camp route wins (camps too strong)`);process.exit(0);}
for(let i=0;i<8;i++){const mid=(lo+hi)/2;if(threeWins(mid))lo=mid;else hi=mid;}
const ease=tutorial?.55:[.7,.8,.85,.9,.9,.9,.97,.97,.97,.97][base.chapter-1];let s=+(lo*ease).toFixed(2),three=threeWins(s)!;
let win:any=null;for(const c of [...all].sort((a,b)=>a.reduce((n,x)=>n+x.cost,0)-b.reduce((n,x)=>n+x.cost,0))){const r=run(s,c);if(r.result==='win'){win={c,r};break;}}
const lazyR=lazy?run(s,lazy.paths.map(p=>({points:p.points} as any))):null;
console.log(`scale ${s} · 3★ route alive ${three.r.alive}/${three.r.total} · cheapest win alive ${win.r.alive}/${win.r.total} · lazy ${lazyR?.result}`);
const chosen={s,win,three};
// bậc brush cần cho 3 sao
const tier=base.chapter<=3?['quill']:base.chapter<=6?Object.keys(BR).filter(k=>['common','rare'].includes(BR[k].rarity)):Object.keys(BR).filter(k=>BR[k].rarity!=='legendary');
const costWith=(c:Cand[],fx:any)=>c.reduce((n,x)=>n+pathCost(base,x.points,fx)-x.seq.filter((o:any)=>o.type==='ink_bottle').reduce((s:number,o:any)=>s+o.value,0),0);
const winCost=costWith(chosen.win.c,NO_BRUSH),threeRoute=chosen.three?.c;let threeBrush='quill',threeCost=threeRoute?costWith(threeRoute,NO_BRUSH):0;
if(threeRoute)for(const b of tier){const c=costWith(threeRoute,brushFx(b,1));if(c<threeCost){threeCost=c;threeBrush=b;}}
const baseInk=Math.ceil(Math.max(winCost*1.06,threeCost*1.02)/10)*10,quillThree=threeRoute?costWith(threeRoute,NO_BRUSH):0;
console.log(`${id}: scale ${chosen.s.toFixed(2)} · win route ${Math.round(winCost)} ink (alive ${chosen.win.r.alive}/${chosen.win.r.total}) · 3★ ${threeRoute?Math.round(quillThree)+' with quill, '+Math.round(threeCost)+' with '+threeBrush:'n/a'} · baseInk ${baseInk}${threeRoute&&quillThree>baseInk?' → 3★ needs a better brush':''}`);
if(write){const file=new URL(`../src/data/maps/${id}.json`,import.meta.url),json=JSON.parse(readFileSync(file,'utf8'));json.bosses.forEach((b:any)=>b.scale=+chosen!.s.toFixed(2));json.baseInk=baseInk;const ref=(threeRoute||chosen.win.c).map((c:Cand)=>c.points.map(p=>[Math.round(p.x),Math.round(p.y)]));json.referenceSolution=ref;json.design={winInk:Math.round(winCost),threeStarInk:Math.round(quillThree),threeStarBrush:threeBrush};writeFileSync(file,JSON.stringify(json,null,2)+'\n');console.log('written');}
