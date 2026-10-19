// Thêm tường mê cung (19/10): các dải tường ngang giữa START và boss, mỗi dải chừa một khe, khe so le trái/phải
// để đường vẽ phải lượn. Màn 2 đội: mỗi nửa sân một khe. Tường né trại, vật phẩm, boss, START và các dải chắn cũ.
// Chạy lại được (xoá tường maze cũ trước). npx tsx tools/mazify.ts [mapId...]  → rồi link-camps + solve-map.
import {readFileSync,writeFileSync} from 'node:fs';
import chapters from '../src/data/chapters.json';
import {maps,inside,dist,type MapData,type P} from '../src/systems';
import {route} from './mapTools';

const T=26; // độ dày tường
const ids=process.argv.slice(2);
// số tường theo chương và vị trí trong chương: tăng nhanh ngay từ chương 1–2
function wallCount(ch:number,idx:number,last:number){
  if(ch===1)return [0,1,2,2,2][idx]??2;
  if(ch===2)return [2,2,3,3,3][idx]??3;
  return 3+(idx>=last-1?1:0);
}
const rnd=(seed:string)=>{let h=0;for(const c of seed)h=(h*31+c.charCodeAt(0))|0;return ()=>{h=(h*1103515245+12345)|0;return ((h>>>8)&0xffff)/0xffff;};};

for(const m0 of Object.values(maps).filter(m=>!ids.length||ids.includes(m.id))){
  const file=new URL(`../src/data/maps/${m0.id}.json`,import.meta.url),json=JSON.parse(readFileSync(file,'utf8'));
  json.obstacles=json.obstacles.filter((o:any)=>!o.maze);
  const order=(chapters as any)[json.chapter-1].stages.filter((x:string)=>/^c\d+_s\d+$/.test(x)),idx=order.indexOf(json.id),last=order.length-1;
  const want=wallCount(json.chapter,idx,last),f=json.field,R=rnd(json.id);
  const halves:number[][]=json.starts.length>1?[[f.x,f.x+f.w/2],[f.x+f.w/2,f.x+f.w]]:[[f.x,f.x+f.w]];
  // điểm cần né (toạ độ, bán kính)
  const pts:[number,number,number][]=[
    ...json.camps.map((c:any)=>[c.x,c.y,64]),...json.items.filter((o:any)=>o.type!=='gate').map((o:any)=>[o.x,o.y,40]),
    ...json.bosses.map((b:any)=>[b.x,b.y,90]),...json.starts.map((s:any)=>[s.x,s.y,80]),
  ];
  const boxes=[...json.obstacles.map((o:any)=>o.type==='circle'?{x:o.x-o.r,y:o.y-o.r,w:o.r*2,h:o.r*2}:o.type==='rect'?o:null).filter(Boolean),
    ...json.items.filter((o:any)=>o.type==='gate').map((o:any)=>o.rect),
    ...json.goldZones.map((z:any)=>{const xs=z.points.map((p:number[])=>p[0]),ys=z.points.map((p:number[])=>p[1]);return {x:Math.min(...xs),y:Math.min(...ys),w:Math.max(...xs)-Math.min(...xs),h:Math.max(...ys)-Math.min(...ys)};})];
  const yMin=Math.max(...json.bosses.map((b:any)=>b.y))+95,yMax=Math.min(...json.starts.map((s:any)=>s.y))-120;
  const hard=pts.slice(json.camps.length+json.items.filter((o:any)=>o.type!=='gate').length); // boss + START: không cắt qua
  const soft=pts.slice(0,json.camps.length+json.items.filter((o:any)=>o.type!=='gate').length); // trại, vật phẩm: tường chừa khoảng quanh chúng
  const free=(y:number)=>hard.every(([,py,r])=>Math.abs(py-(y+T/2))>r+T/2)&&boxes.every((b:any)=>{const wide=b.w>=f.w*.22;return !wide||(y+T+48<b.y||y-48>b.y+b.h);})&&boxes.every((b:any)=>y+T<b.y-6||y>b.y+b.h+6||b.w<f.w*.22);
  const ys:number[]=[];
  for(let k=0;k<want;k++){const target=yMax-(k+1)*(yMax-yMin)/(want+1);let best=-1;for(let y=yMin;y<=yMax;y+=4)if(free(y)&&ys.every(q=>Math.abs(q-y)>=104)&&(best<0||Math.abs(y-target)<Math.abs(best-target)))best=y;if(best>=0)ys.push(best);}
  ys.sort((a,b)=>b-a); // từ dưới (START) lên trên (boss)
  const map=():MapData=>({...m0,obstacles:json.obstacles,camps:json.camps,items:json.items,goldZones:json.goldZones} as any);
  const reachable=()=>{const m=map();return json.starts.every((s:any,t:number)=>{const boss=json.bosses.length>1?json.bosses[t]:json.bosses[0];return !!route(m,s,boss,new Set(),40);})&&json.camps.every((c:any)=>json.starts.some((s:any)=>!!route(m,s,c,new Set(),45)));};
  const gapW=Math.max(70,Math.round(f.w*.15)),first=R()<.5?0:1;let placed=0;
  ys.forEach((y,k)=>{
    const walls:any[]=[];
    for(const [a,b] of halves){
      const options=[(k+first)%2?a+18+gapW/2:b-18-gapW/2,(a+b)/2,(k+first)%2?b-18-gapW/2:a+18+gapW/2];
      const gx=options.find(cx=>{for(let x=cx-gapW/2+8;x<=cx+gapW/2-8;x+=10)for(const yy of [y-30,y+T/2,y+T+30])if(json.obstacles.some((o:any)=>inside({x,y:yy},o)))return false;return true;});
      if(gx===undefined)return;
      const l=Math.round(gx-gapW/2),r=Math.round(gx+gapW/2);
      let segs:number[][]=[[a,l],[r,b]];
      for(const [px,py,rad] of soft)if(Math.abs(py-(y+T/2))<rad+T/2)segs=segs.flatMap(([u,v])=>[[u,Math.min(v,px-rad)],[Math.max(u,px+rad),v]]);
      for(const bx of boxes as any[])if(!(y+T<bx.y||y>bx.y+bx.h))segs=segs.flatMap(([u,v])=>[[u,Math.min(v,bx.x-4)],[Math.max(u,bx.x+bx.w+4),v]]);
      for(const [u,v] of segs)if(v-u>24)walls.push({type:'rect',x:Math.round(u),y:Math.round(y),w:Math.round(v-u),h:T,maze:true});
    }
    json.obstacles.push(...walls);
    if(!reachable()){json.obstacles=json.obstacles.filter((o:any)=>!walls.includes(o));return;}
    placed++;
  });
  // nhóm địch không gắn trại (đi tuần/cướp): tìm lại đường quanh tường mới
  const m=map();
  for(const sq of json.enemySquads){if(sq.camp!==undefined)continue;const wp=sq.route.map((p:number[])=>({x:p[0],y:p[1]})).filter((p:P)=>!json.obstacles.some((o:any)=>inside(p,o)));let out:P[]=[wp[0]];for(let i=1;i<wp.length;i++){const r=route(m,wp[i-1],wp[i],new Set(),10);if(r)out.push(...r.slice(1));else out.push(wp[i]);}sq.route=out.map(p=>[Math.round(p.x),Math.round(p.y)]);}
  writeFileSync(file,JSON.stringify(json,null,2)+'\n');
  console.log(json.id,'walls',placed+'/'+want);
}
