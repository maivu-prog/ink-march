import {C,InkPool,Battle,fresh,inside,dist,length,lerp,burnRate,brushFx,NO_BRUSH,fieldOf,type BrushFx,type MapData,type P,type Run} from '../src/systems';

const GRID=8,CLEAR=12;
export const STARTER_TEAMS=[['shield','sword','archer'],['shield','sword','archer']];

function blockedAt(map:MapData,p:P,open:Set<string>,clear=CLEAR){
  const f=fieldOf(map);if(p.x<f.x+10||p.x>f.x+f.w-10||p.y<f.y+10||p.y>f.y+f.h-10)return true;
  const probes=[p,...[0,1,2,3,4,5,6,7].map(k=>({x:p.x+Math.cos(k*Math.PI/4)*clear,y:p.y+Math.sin(k*Math.PI/4)*clear}))];
  return probes.some(q=>map.obstacles.some(o=>inside(q,o))||map.items.some(o=>o.type==='gate'&&!open.has(o.color)&&inside(q,o)));
}
// Chi phí mực của một đoạn thẳng (lấy mẫu theo địa hình)
export function segCost(map:MapData,a:P,b:P,fx:BrushFx){const n=Math.max(1,Math.ceil(dist(a,b)/8));let c=0;for(let i=0;i<n;i++){const p=lerp(a,b,(i+.5)/n);c+=dist(a,b)/n*burnRate(map,p,fx);}return c;}
export function pathCost(map:MapData,pts:P[],fx:BrushFx){let c=0;for(let i=1;i<pts.length;i++)c+=segCost(map,pts[i-1],pts[i],fx);return c;}
function clearLine(map:MapData,a:P,b:P,open:Set<string>){const n=Math.ceil(dist(a,b)/4);for(let i=0;i<=n;i++){if(blockedAt(map,lerp(a,b,i/n),open,6))return false;}return true;}

// A* trên lưới 8 px theo chi phí mực, rồi kéo thẳng khi đường thẳng không tốn mực hơn
export function route(map:MapData,from:P,to:P,open=new Set<string>(),goalRadius=6,fx:BrushFx=NO_BRUSH):P[]|null{
  const W=Math.ceil(720/GRID)+1,H=Math.ceil(1000/GRID)+1,key=(i:number,j:number)=>j*W+i;
  const si=Math.round(from.x/GRID),sj=Math.round(from.y/GRID);
  const g=new Float64Array(W*H).fill(Infinity),prev=new Int32Array(W*H).fill(-1),closed=new Uint8Array(W*H);
  const heap:[number,number][]=[];
  const push=(f:number,k:number)=>{heap.push([f,k]);let i=heap.length-1;while(i>0){const p=(i-1)>>1;if(heap[p][0]<=heap[i][0])break;[heap[p],heap[i]]=[heap[i],heap[p]];i=p;}};
  const pop=()=>{const top=heap[0],last=heap.pop()!;if(heap.length){heap[0]=last;let i=0;for(;;){const l=2*i+1,r=l+1;let m=i;if(l<heap.length&&heap[l][0]<heap[m][0])m=l;if(r<heap.length&&heap[r][0]<heap[m][0])m=r;if(m===i)break;[heap[m],heap[i]]=[heap[i],heap[m]];i=m;}}return top;};
  const minRate=Math.min(fx.burn*.4,1);
  g[key(si,sj)]=0;push(0,key(si,sj));let goal=-1;
  while(heap.length){
    const [,k]=pop();if(closed[k])continue;closed[k]=1;
    const i=k%W,j=Math.floor(k/W),p={x:i*GRID,y:j*GRID};
    if(dist(p,to)<=goalRadius+GRID){goal=k;break;}
    for(const [di,dj] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){
      const ni=i+di,nj=j+dj;if(ni<0||nj<0||ni>=W||nj>=H)continue;const nk=key(ni,nj);if(closed[nk])continue;
      const q={x:ni*GRID,y:nj*GRID};if(k!==key(si,sj)&&blockedAt(map,q,open))continue;
      const ng=g[k]+Math.hypot(di,dj)*GRID*burnRate(map,lerp(p,q,.5),fx);if(ng<g[nk]){g[nk]=ng;prev[nk]=k;push(ng+dist(q,to)*minRate,nk);}
    }
  }
  if(goal<0)return null;
  const raw:P[]=[];for(let c=goal;c>=0;c=prev[c])raw.unshift({x:(c%W)*GRID,y:Math.floor(c/W)*GRID});
  raw[0]={...from};const out:P[]=[raw[0]];let a=0;
  while(a<raw.length-1){let b=raw.length-1;while(b>a+1&&!(clearLine(map,raw[a],raw[b],open)&&segCost(map,raw[a],raw[b],fx)<=pathCost(map,raw.slice(a,b+1),fx)*1.01))b--;out.push(raw[b]);a=b;}
  return out;
}

export function drawPool(map:MapData,paths:(number[][]|P[])[],fx:BrushFx=NO_BRUSH,gold=0){const pool=new InkPool(map,gold,fx);paths.forEach((pts,t)=>pts.forEach((q:any)=>pool.paths[t]?.add(Array.isArray(q)?{x:q[0],y:q[1]}:q)));return pool;}
export const free=(m:MapData):MapData=>({...m,baseInk:99999});
export const levelFor=(m:MapData)=>1+Math.floor((m.chapter-1)*.8);

export function simulate(map:MapData,pool:InkPool,level=levelFor(map),teams=STARTER_TEAMS){
  const save=fresh();Object.keys(save.levels).forEach(k=>save.levels[k]=level);
  const run:Run={chapter:map.chapter,layer:0,teams,brush:'quill',xp:0,level:0,coins:0,goldInk:0,buffs:{},extras:[0,0,0,0,0,0],nextHp:1,bonus:false,picks:0,maps:[],earned:0};
  const b=new Battle(map,pool,run,save);
  for(let i=0;i<C.battleTimeoutSec*60+1&&!b.result;i++)b.step(1/60);
  const alive=b.soldiers.filter(s=>s.team===0&&s.hp>0).length,total=b.soldiers.filter(s=>s.team===0).length;
  return {result:b.result,time:Math.round(b.time),alive,total,camps:b.campsDestroyed,enraged:b.enraged,stolen:b.stolen.size};
}

// Đội t nhắm boss nào: có 2 boss thì mỗi đội một boss, gần cờ của đội nhất
export const bossFor=(map:MapData,t:number)=>map.bosses.length>1?map.bosses[t]:map.bosses[0];

// Tuyến của một đội: đi qua danh sách mục tiêu theo thứ tự rồi tới boss
export function teamRoute(map:MapData,t:number,targets:any[],fx:BrushFx=NO_BRUSH){
  const open=new Set<string>();let cur:P=map.starts[t];const pts:P[]=[cur];
  for(const o of targets){const radius=o.camp?45:o.type==='key'||o.type==='chest'?C.pickupRadius-14:C.pickupRadius-10;const leg=route(map,cur,o,open,radius,fx);if(!leg)return null;pts.push(...leg.slice(1));cur=leg.at(-1)!;if(o.type==='key')open.add(o.color);}
  const leg=route(map,cur,bossFor(map,t),open,C.bossSnapRadius-12,fx);if(!leg)return null;pts.push(...leg.slice(1));return pts;
}
export function lazyPool(map:MapData,fx:BrushFx=NO_BRUSH){const keys=map.items.filter(o=>o.type==='key');const paths=map.starts.map((_,t)=>teamRoute(map,t,[],fx)||teamRoute(map,t,keys,fx));if(paths.some(p=>!p))return null;return drawPool(map,paths as P[][],fx);}
export const easyMaps=new Set<string>();
export {brushFx};
