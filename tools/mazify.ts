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
  const wantRows=wallCount(json.chapter,idx,last),f=json.field,R=rnd(json.id);
  const halves:number[][]=json.starts.length>1?[[f.x,f.x+f.w/2],[f.x+f.w/2,f.x+f.w]]:[[f.x,f.x+f.w]];
  // điểm cần né (toạ độ, bán kính)
  const pts:[number,number,number][]=[
    ...json.camps.map((c:any)=>[c.x,c.y,64]),...json.items.filter((o:any)=>o.type!=='gate').map((o:any)=>[o.x,o.y,40]),
    ...json.bosses.map((b:any)=>[b.x,b.y,90]),...json.starts.map((s:any)=>[s.x,s.y,80]),
  ];
  const boxes=[...json.obstacles.filter((o:any)=>!o.maze).map((o:any)=>o.type==='circle'?{x:o.x-o.r,y:o.y-o.r,w:o.r*2,h:o.r*2}:o.type==='rect'?o:null).filter(Boolean),
    ...json.items.filter((o:any)=>o.type==='gate').map((o:any)=>o.rect),
    ...json.goldZones.map((z:any)=>{const xs=z.points.map((p:number[])=>p[0]),ys=z.points.map((p:number[])=>p[1]);return {x:Math.min(...xs),y:Math.min(...ys),w:Math.max(...xs)-Math.min(...xs),h:Math.max(...ys)-Math.min(...ys)};})];
  const hard=pts.slice(json.camps.length+json.items.filter((o:any)=>o.type!=='gate').length); // boss + START: không cắt qua
  const soft=pts.slice(0,json.camps.length+json.items.filter((o:any)=>o.type!=='gate').length); // trại, vật phẩm: tường chừa khoảng quanh chúng
  const map=():MapData=>({...m0,obstacles:json.obstacles,camps:json.camps,items:json.items,goldZones:json.goldZones} as any);
  const reachable=()=>{const m=map();return json.starts.every((s:any,t:number)=>{const boss=json.bosses.length>1?json.bosses[t]:json.bosses[0];return !!route(m,s,boss,new Set(),40);})&&json.camps.every((c:any)=>json.starts.some((s:any)=>!!route(m,s,c,new Set(),45)));};
  const gapW=Math.max(70,Math.round(f.w*.15)),first=R()<.5?0:1,layout=json.layout||'D';
  // Một đoạn tường thẳng: v=false ngang tại toạ độ pos, chạy dọc trục [a,b]; gaps = các tâm khe. Cắt quanh trại/vật phẩm/vật cản.
  const line=(v:boolean,pos:number,a:number,b:number,gaps:number[])=>{
    const along=(p:any)=>v?p.y:p.x,across=(p:any)=>v?p.x:p.y;
    let segs:number[][]=[[a,b]];
    const cut=(u0:number,u1:number)=>{segs=segs.flatMap(([u,w])=>[[u,Math.min(w,u0)],[Math.max(u,u1),w]]);};
    for(const g of gaps)cut(g-gapW/2,g+gapW/2);
    for(const [px,py,rad] of [...soft,...json.starts.map((q:any)=>[q.x,q.y,80])]){const P2={x:px,y:py};if(Math.abs(across(P2)-(pos+T/2))<rad+T/2)cut(along(P2)-rad,along(P2)+rad);}
    for(const bx of boxes as any[]){const lo=v?bx.x:bx.y,hi=v?bx.x+bx.w:bx.y+bx.h;if(!(pos+T<lo||pos>hi))cut((v?bx.y:bx.x)-4,(v?bx.y+bx.h:bx.x+bx.w)+4);}
    return segs.filter(([u,w])=>w-u>24).map(([u,w])=>v?{type:'rect',x:Math.round(pos),y:Math.round(u),w:T,h:Math.round(w-u),maze:true}:{type:'rect',x:Math.round(u),y:Math.round(pos),w:Math.round(w-u),h:T,maze:true});
  };
  const clearGap=(v:boolean,pos:number,g:number)=>{for(let u=g-gapW/2+8;u<=g+gapW/2-8;u+=10)for(const d of [-30,T/2,T+30]){const q=v?{x:pos+d,y:u}:{x:u,y:pos+d};if(json.obstacles.some((o:any)=>inside(q,o)))return false;}return true;};
  let placed=0,want=0;
  const tryAdd=(walls:any[])=>{want++;if(!walls.length)return;json.obstacles.push(...walls);if(!reachable()){json.obstacles=json.obstacles.filter((o:any)=>!walls.includes(o));return;}placed++;};
  // hàng tường so le trong khoảng [lo,hi] theo trục ngang (v=false) hoặc dọc (v=true), mỗi khoảng con trong spans một khe
  const rows=(v:boolean,lo:number,hi:number,count:number,spans:number[][],avoidNear:any[])=>{
    const ps:number[]=[];const okPos=(q:number)=>avoidNear.every(([x,y,r]:any)=>Math.abs((v?x:y)-(q+T/2))>r+T/2)&&(boxes as any[]).every((bx:any)=>{const span=v?bx.h:bx.w,wide=span>=(v?f.h:f.w)*.22,lo2=v?bx.x:bx.y,hi2=v?bx.x+bx.w:bx.y+bx.h;return !wide||(q+T+48<lo2||q-48>hi2);});
    for(let k=0;k<count;k++){const target=hi-(k+1)*(hi-lo)/(count+1);let best=-1;for(let q=lo;q<=hi;q+=4)if(okPos(q)&&ps.every(z=>Math.abs(z-q)>=104)&&(best<0||Math.abs(q-target)<Math.abs(best-target)))best=q;if(best>=0)ps.push(best);}
    ps.sort((x,y)=>y-x).forEach((q,k)=>{const walls:any[]=[];for(const [a,b] of spans){const opts=[(k+first)%2?a+18+gapW/2:b-18-gapW/2,(a+b)/2,(k+first)%2?b-18-gapW/2:a+18+gapW/2];const g=opts.find(c=>clearGap(v,q,c));if(g===undefined)continue;walls.push(...line(v,q,a,b,[g]));}tryAdd(walls);});
  };
  // vòng tường vuông quanh tâm c, nửa cạnh r, khe ở các cạnh trong gapSides (N/S/W/E)
  // trước khi dựng vòng: trại/vật phẩm nằm sát vòng thì đẩy ra ngoài vòng (không khoét tường quanh chúng, tránh tạo lối tắt)
  const pushOut=(c:P,r:number)=>{for(const o of [...json.camps,...json.items.filter((o:any)=>o.type!=='gate')]){const dx=o.x-c.x,dy=o.y-c.y,mm=Math.max(Math.abs(dx),Math.abs(dy));if(mm<1||Math.abs(mm-r)>=72)continue;const k=(r+82)/mm;o.x=Math.round(Math.max(f.x+40,Math.min(f.x+f.w-40,c.x+dx*k)));o.y=Math.round(Math.max(f.y+40,Math.min(f.y+f.h-40,c.y+dy*k)));for(const st of json.starts)if(dist(o,st)<130)o.x=Math.round(Math.max(f.x+40,Math.min(f.x+f.w-40,st.x+(o.x>=st.x?150:-150))));}
    soft.splice(0,soft.length,...json.camps.map((c:any)=>[c.x,c.y,64]),...json.items.filter((o:any)=>o.type!=='gate').map((o:any)=>[o.x,o.y,40]));};
  const ring=(c:P,r:number,gapSides:string[])=>{pushOut(c,r);const x0=Math.max(f.x+10,c.x-r),x1=Math.min(f.x+f.w-10,c.x+r),y0=Math.max(f.y+10,c.y-r),y1=Math.min(f.y+f.h-10,c.y+r);
    tryAdd([...line(false,y0,x0,x1,gapSides.includes('N')?[(x0+x1)/2]:[]),...line(false,y1-T,x0,x1,gapSides.includes('S')?[(x0+x1)/2]:[]),...line(true,x0,y0,y1,gapSides.includes('W')?[(y0+y1)/2]:[]),...line(true,x1-T,y0,y1,gapSides.includes('E')?[(y0+y1)/2]:[])]);};
  const full=[[f.x,f.x+f.w]],cxF=f.x+f.w/2,center=json.bosses.length>1?{x:(json.bosses[0].x+json.bosses[1].x)/2,y:(json.bosses[0].y+json.bosses[1].y)/2}:json.bosses[0];
  const startY=Math.min(...json.starts.map((s:any)=>s.y)),bossY=Math.max(...json.bosses.map((b:any)=>b.y));
  if(layout==='D'||layout==='C'||layout==='2S')rows(false,bossY+95,startY-120,wantRows,json.starts.length>1?halves:full,hard);
  else if(layout==='N'){const xs=[json.starts[0].x,json.bosses[0].x].sort((a:number,b:number)=>a-b);rows(true,xs[0]+90,xs[1]-110,wantRows,[[f.y,f.y+f.h]],hard);}
  else if(layout==='K'){const dx=(json.starts[0].x+json.bosses[0].x)/2-T/2;for(const o of [...json.camps,...json.items.filter((o:any)=>o.type!=='gate')])if(o.y>f.y+f.h*.3-60&&Math.abs(o.x-(dx+T/2))<75)o.x=Math.round(o.x<dx+T/2?dx-80:dx+T+80);soft.splice(0,soft.length,...json.camps.map((c:any)=>[c.x,c.y,64]),...json.items.filter((o:any)=>o.type!=='gate').map((o:any)=>[o.x,o.y,40]));tryAdd(line(true,dx,f.y+f.h*.3,f.y+f.h,[]));const ka=[[f.x,dx],[dx+T,f.x+f.w]];rows(false,f.y+f.h*.36,startY-110,Math.max(1,wantRows-2),ka,hard);}
  else if(layout==='P'){const r1=Math.max(115,f.w*.2),r2=Math.max(205,f.w*.36);ring(center,r1,[first?'E':'W']);ring(center,r2,['N']);if(wantRows>=4)rows(false,center.y+r2+40,startY-100,1,full,hard);}
  else if(layout==='2L'){ring(center,f.w*.26,['N','S']);rows(false,center.y+f.w*.26+30,startY-100,1,[[f.x,cxF]],hard);rows(false,Math.min(...json.starts.map((s:any)=>s.y))+100,center.y-f.w*.26-60,1,[[cxF,f.x+f.w]],hard);}
  else if(layout==='P2L'){ring(center,f.w*.4,['W','E']);ring(center,f.w*.22,['N','S']);}
  // nhóm địch không gắn trại (đi tuần/cướp): tìm lại đường quanh tường mới
  const m=map();
  for(const sq of json.enemySquads){if(sq.camp!==undefined)continue;const wp=sq.route.map((p:number[])=>({x:p[0],y:p[1]})).filter((p:P)=>!json.obstacles.some((o:any)=>inside(p,o)));let out:P[]=[wp[0]];for(let i=1;i<wp.length;i++){const r=route(m,wp[i-1],wp[i],new Set(),10);if(r)out.push(...r.slice(1));else out.push(wp[i]);}sq.route=out.map(p=>[Math.round(p.x),Math.round(p.y)]);}
  writeFileSync(file,JSON.stringify(json,null,2)+'\n');
  console.log(json.id,json.layout||'D','walls',placed+'/'+want);
}
