// Kiểu bố cục từng màn (Mai duyệt 19/10): START và boss không còn cố định dưới/trên.
// D dọc · C chéo góc · N ngang · K kẹp tóc · P pháo đài giữa · 2S hai đội song song · 2L hai đội lệch góc · P2L pháo đài + hai đội.
// Script đặt lại START/boss theo kiểu, đổi chỗ vật thể đang đứng ở vị trí mới, hướng đường địch về boss mới.
// Chạy 1 lần trên map gốc: npx tsx tools/layouts.ts  → mazify → link-camps → solve-map.
import {readFileSync,writeFileSync} from 'node:fs';
import {inside,dist,type P} from '../src/systems';

export const LAYOUT:Record<string,string>={
 c1_s1:'D',c1_s2:'D',c1_s3:'D',c1_s5:'D',c1_s4:'P',
 c2_s1:'C',c2_s2:'N',c2_s4:'C',c2_s5:'K',c2_s3:'P',
 c3_s1:'N',c3_s2:'K',c3_s3:'P',c3_s5:'C',c3_s4:'N',
 c4_s1:'2S',c4_s2:'N',c4_s3:'2L',c4_s5:'2S',c4_s4:'2L',
 c5_s1:'D',c5_s2:'K',c5_s3:'N',c5_s5:'C',c5_s4:'P',
 c6_s1:'2L',c6_s2:'K',c6_s3:'2S',c6_s5:'C',c6_s4:'N',
 c7_s1:'C',c7_s2:'K',c7_s3:'2L',c7_s4:'D',c7_s5:'N',
 c8_s1:'N',c8_s2:'2L',c8_s3:'D',c8_s4:'C',c8_s5:'P',
 c9_s1:'N',c9_s2:'2S',c9_s3:'P',c9_s4:'2L',c9_s5:'2L', // Witch Hunt có 2 đội: K → 2L
 c10_s1:'D',c10_s2:'P2L',c10_s3:'K',c10_s4:'2L',c10_s5:'P2L', // Ink Moat P → P2L, Last Stand C → 2L (đều 2 đội)
};

const flip=(id:string)=>[...id].reduce((h,c)=>h*31+c.charCodeAt(0),7)%2===1; // lật trái/phải cho đa dạng
if(import.meta.url===`file:///${process.argv[1].replace(/\\/g,'/')}`||process.argv[1]?.endsWith('layouts.ts')){
 const ids=process.argv.slice(2);
 for(const [id,kind] of Object.entries(LAYOUT)){
  if(ids.length&&!ids.includes(id))continue;
  const file=new URL(`../src/data/maps/${id}.json`,import.meta.url),m=JSON.parse(readFileSync(file,'utf8'));
  if(m.layout){console.log(id,'already',m.layout);continue;}
  m.layout=kind;
  if(kind==='D'||kind==='2S'){writeFileSync(file,JSON.stringify(m,null,2)+'\n');console.log(id,kind);continue;}
  const f=m.field,L=f.x,T=f.y,W=f.w,H=f.h,cx=L+W/2,fl=flip(id),X=(u:number)=>Math.round(fl?L+W*(1-u):L+W*u),Y=(v:number)=>Math.round(T+H*v);
  const oldStarts=m.starts.map((s:any)=>({...s})),oldBosses=m.bosses.map((b:any)=>({x:b.x,y:b.y}));
  let starts:P[],bosses:P[];
  if(kind==='C'){starts=[{x:X(.18),y:Y(.93)}];bosses=[{x:X(.8),y:Y(.08)}];}
  else if(kind==='N'){starts=[{x:X(.09),y:Y(.62)}];bosses=[{x:X(.9),y:Y(.38)}];}
  else if(kind==='K'){starts=[{x:X(.22),y:Y(.93)}];bosses=[{x:X(.78),y:Y(.86)}];}
  else if(kind==='P'){starts=[{x:Math.round(cx),y:Y(.93)}];bosses=[{x:Math.round(cx),y:Y(.46)}];}
  else{ // 2L, P2L: hai đội ở hai góc đối nhau, boss ở giữa
   starts=[{x:X(.16),y:Y(.93)},{x:X(.84),y:Y(.07)}];
   bosses=m.bosses.length>1?[{x:X(.36),y:Y(.5)},{x:X(.64),y:Y(.5)}]:[{x:Math.round(cx),y:Y(.5)}];
  }
  if(m.starts.length!==starts.length){console.log(id,'SKIP start count',m.starts.length,'vs',starts.length);continue;}
  // vật thể đứng chỗ boss/START mới → đổi sang chỗ cũ của boss/START
  const movable=[...m.camps,...m.items.filter((o:any)=>o.type!=='gate')];
  const swapAway=(target:P,clear:number,home:P)=>{for(const o of movable)if(dist(o,target)<clear){const d=dist(o,home);if(d<1)continue;o.x=Math.round(Math.max(L+45,Math.min(L+W-45,home.x+(o.x-target.x))));o.y=Math.round(Math.max(T+45,Math.min(T+H-45,home.y+(o.y-target.y))));}};
  bosses.forEach((b,i)=>swapAway(b,95,oldBosses[i]??oldBosses[0]));
  starts.forEach((s,i)=>swapAway(s,135,oldStarts[i]??oldStarts[0]));
  // vật cản đè lên boss/START mới: bỏ (trừ cổng); vật cản trong vòng 40 cũng bỏ
  const near=(o:any,p:P,r:number)=>o.type==='circle'?dist(o,p)<o.r+r:o.type==='rect'?(p.x>o.x-r&&p.x<o.x+o.w+r&&p.y>o.y-r&&p.y<o.y+o.h+r):inside(p,o);
  const before=m.obstacles.length;
  m.obstacles=m.obstacles.filter((o:any)=>![...bosses,...starts].some(p=>near(o,p,45)));
  m.starts=m.starts.map((s:any,i:number)=>({...s,...starts[i]}));
  m.bosses=m.bosses.map((b:any,i:number)=>({...b,...bosses[i]}));
  // đường địch kết thúc ở boss gần nhất
  for(const q of m.enemySquads){const end={x:q.route.at(-1)[0],y:q.route.at(-1)[1]},b=m.bosses.reduce((a:any,c:any)=>dist(c,end)<dist(a,end)?c:a);q.route=[q.route[0],[b.x,b.y]];}
  m.referenceSolution=m.starts.map((s:any,t:number)=>{const b=m.bosses.length>1?m.bosses[t]:m.bosses[0];return [[s.x,s.y],[b.x,b.y]];});
  writeFileSync(file,JSON.stringify(m,null,2)+'\n');
  console.log(id,kind,'removed obstacles',before-m.obstacles.length);
 }
}
