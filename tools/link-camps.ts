// Gắn mỗi đạo địch vào một trại: đạo xuất phát từ trại sau thời gian tập hợp,
// tuyến tính lại bằng A* từ trại tới boss. Trại nào cũng có một món rơi.
// npx tsx tools/link-camps.ts [mapId...]
import {readFileSync,writeFileSync} from 'node:fs';
import {maps,dist,C} from '../src/systems';
import {route} from './mapTools';

const LOOT=['atk_up','coins','ink','hp_up','shield','coins'];
const ids=process.argv.slice(2);
for(const m of Object.values(maps).filter(m=>!ids.length||ids.includes(m.id))){
  const file=new URL(`../src/data/maps/${m.id}.json`,import.meta.url),json=JSON.parse(readFileSync(file,'utf8'));
  const used=new Set<number>();
  json.enemySquads.forEach((sq:any,k:number)=>{
    const start={x:sq.route[0][0],y:sq.route[0][1]},end={x:sq.route.at(-1)[0],y:sq.route.at(-1)[1]};
    const free=json.camps.map((c:any,i:number)=>i).filter((i:number)=>!used.has(i));
    if(!free.length){delete sq.camp;return;}
    const ci=free.sort((a:number,b:number)=>dist(json.camps[a],start)-dist(json.camps[b],start))[0],camp=json.camps[ci];
    const r=route(m,camp,end,new Set(),10);if(!r){delete sq.camp;return;}
    used.add(ci);sq.camp=ci;sq.route=r.map(p=>[Math.round(p.x),Math.round(p.y)]);
    sq.spawnDelay=(sq.origDelay??=sq.spawnDelay)+C.campMusterSec+k*4;
  });
  json.camps.forEach((c:any,i:number)=>c.loot=LOOT[(i+m.chapter)%LOOT.length]);
  writeFileSync(file,JSON.stringify(json,null,2)+'\n');
  console.log(m.id,json.enemySquads.map((s:any)=>`camp ${s.camp??'-'} @${s.spawnDelay}s`).join(', '));
}
