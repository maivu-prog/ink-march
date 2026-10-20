// Siết mực (20/10, Mai: "dễ quá, không cần cân nhắc phương án, không có nhu cầu brush mới").
// Không giả lập lại trận: chỉ tính lại baseInk từ winInk đã lưu và đường mẫu 3 sao.
// - mực thắng = 74% → 88% mực gốc từ màn đầu tới màn boss của chương (màn khoá brush: tới 92%)
// - 3 sao bằng Quill = 95% mực gốc
// - từ chương 2: màn thứ 2, 4 và màn boss khoá 3 sao sau brush theo bậc chương (2–3 thường, 4–6 + rare, 7+ + epic)
// npx tsx tools/reink.ts [--write]
import {readFileSync,writeFileSync} from 'node:fs';
import chapters from '../src/data/chapters.json';
import {maps,BR,type MapData} from '../src/systems';
import {pathCost,brushFx} from './mapTools';
import {NO_BRUSH} from '../src/systems';

export function inkPlan(m:MapData,win:number,cost:(fx:any)=>number){
 const order=(chapters as any)[m.chapter-1].stages.filter((x:string)=>/^c\d+_s\d+$/.test(x)),idx=order.indexOf(m.id),last=order.length-1,pos=last>0?idx/last:1,isBoss=idx===last;
 const tutorial=m.id==='c1_s1',gated=m.chapter>=2&&(idx%2===1||isBoss);
 const rarities=m.chapter<=3?['common']:m.chapter<=6?['common','rare']:['common','rare','epic'];
 const tier=Object.keys(BR).filter(k=>k!=='quill'&&rarities.includes(BR[k].rarity));
 const quill=cost(NO_BRUSH);let brush='quill',three=quill;
 if(gated)for(const b of tier){const c=cost(brushFx(b,1));if(c<three-1){three=c;brush=b;}}
 const rWin=tutorial?.6:.74+.14*pos;
 let baseInk=Math.ceil(Math.max(win/rWin,quill/.95)/10)*10;
 /* màn khoá brush: mực gốc thấp nhất sao cho tuyến thắng ≤ 92% và brush lấy 3 sao ≤ 95%; chỉ khoá khi Quill cần ≥ 105% */
 if(brush!=='quill'){const g=Math.ceil(Math.max(win/.92,three/.95)/10)*10;if(quill>=g*1.05)baseInk=g;else{brush='quill';three=quill;}}
 return {baseInk,brush,quill,three,gated:brush!=='quill'&&quill>baseInk};
}
if(process.argv[1]?.endsWith('reink.ts')){
 const write=process.argv.includes('--write');let gatedN=0;
 for(const m of Object.values(maps)){
  const d=(m as any).design;if(!d)continue;
  const plan=inkPlan(m,d.winInk,fx=>m.referenceSolution.reduce((n:number,pts:any)=>n+pathCost(m,pts.map((p:number[])=>({x:p[0],y:p[1]})),fx),0));
  if(plan.gated)gatedN++;
  console.log(m.id.padEnd(7),'base',String(m.baseInk).padStart(5),'→',String(plan.baseInk).padStart(5),'win',Math.round(d.winInk/plan.baseInk*100)+'%','3★ quill',Math.round(plan.quill/plan.baseInk*100)+'%',plan.brush!=='quill'?plan.brush+' '+Math.round(plan.three/plan.baseInk*100)+'%':'');
  if(write){const file=new URL(`../src/data/maps/${m.id}.json`,import.meta.url),json=JSON.parse(readFileSync(file,'utf8'));json.baseInk=plan.baseInk;json.design={...json.design,threeStarBrush:plan.brush,winShare:+(d.winInk/plan.baseInk).toFixed(2),threeShare:+(plan.quill/plan.baseInk).toFixed(2)};writeFileSync(file,JSON.stringify(json,null,2)+'\n');}
 }
 console.log('3★ needs a brush on',gatedN,'stages');
}
