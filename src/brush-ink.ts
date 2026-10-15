import {Color} from 'three';
import {BR,along,length,type P} from './systems';
import {phoenixEmbers} from './phoenix-ink';
export type InkEffect='none'|'glint'|'pollen'|'motes'|'flame';
export type InkLayer={color:string;polygons:P[][];glow:number;pulse:boolean};
type Sample=P&{d:number;tx:number;ty:number;nx:number;ny:number};
const shapes:Record<string,string>={marsh:'Scalloped ink',broad:'Flat bristle',swift:'Swift ribbon',atlas:'Survey rails',golden:'Golden braid',willow:'Willow vine',trail:'Trail ribbon',phoenix:'Phoenix flame'};
export function brushStrokeStyle(id:string){
 const b=BR[id]||BR.quill,rarity=b.rarity;
 const effect:InkEffect=rarity==='legendary'?'flame':rarity==='epic'?({golden:'glint',willow:'pollen',trail:'motes'} as Record<string,InkEffect>)[id]||'glint':'none';
 return {rarity,color:b.look.p,shape:rarity==='common'?'Plain ink':shapes[id]||'Ribbon ink',effect,animated:effect!=='none'};
}
const mix=(a:string,b:string,t:number)=>'#'+new Color(a).lerp(new Color(b),t).getHexString();
/** Arc-length sampling makes detail spacing independent of pointer event frequency. */
function samples(points:P[],w:number):Sample[]{
 const total=length(points);if(!points.length)return [];
 if(total<.01)return [{...points[0],d:0,tx:1,ty:0,nx:0,ny:1}];
 const count=Math.min(1024,Math.max(2,Math.ceil(total/Math.max(1,w*.32))+1)),out:Sample[]=[];
 let segment=1,walked=0;
 for(let i=0;i<count;i++){
  const d=total*i/(count-1);let a=points[segment-1],b=points[segment],len=Math.hypot(b.x-a.x,b.y-a.y);
  while(segment<points.length-1&&walked+len<d){walked+=len;segment++;a=points[segment-1];b=points[segment];len=Math.hypot(b.x-a.x,b.y-a.y);}
  const t=len?Math.min(1,(d-walked)/len):0,tx=len?(b.x-a.x)/len:1,ty=len?(b.y-a.y)/len:0;
  out.push({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,d,tx,ty,nx:-ty,ny:tx});
 }
 return out;
}
const point=(s:Sample,forward:number,side:number):P=>({x:s.x+s.tx*forward+s.nx*side,y:s.y+s.ty*forward+s.ny*side});
function disc(p:P,r:number){return Array.from({length:12},(_,i)=>({x:p.x+Math.cos(i*Math.PI/6)*r,y:p.y+Math.sin(i*Math.PI/6)*r}));}
function band(s:Sample[],width:(d:number)=>number,offset:(d:number)=>number=()=>0,round=true):P[][]{
 if(!s.length)return [];if(s.length===1)return [disc(point(s[0],0,offset(0)),width(0)/2)];
 const out:P[][]=[];
 for(let i=1;i<s.length;i++){const a=s[i-1],b=s[i],aw=width(a.d)/2,bw=width(b.d)/2;out.push([point(a,0,offset(a.d)+aw),point(a,0,offset(a.d)-aw),point(b,0,offset(b.d)-bw),point(b,0,offset(b.d)+bw)]);}
 if(round)for(const p of [s[0],s.at(-1)!])out.push(disc(point(p,0,offset(p.d)),width(p.d)/2));
 return out;
}
/** Pure artwork. Widths, leaves and hatch marks never affect the logical route. */
export function buildInkLayers(id:string,points:P[],width:number):InkLayer[]{
 const style=brushStrokeStyle(id),c=style.color,s=samples(points,width),out:InkLayer[]=[];
 const add=(color:string,polygons:P[][],glow=0,pulse=false)=>{if(polygons.length)out.push({color,polygons,glow,pulse});};
 const ribbon=(factor=1,profile:(d:number)=>number=()=>1,offset:(d:number)=>number=()=>0,round=true)=>band(s,d=>width*factor*profile(d),offset,round);
 const light=mix(c,'#fff3c8',.42),dark=mix(c,'#244b46',.28);
 if(style.rarity==='common'){add(c,ribbon());return out;}
 if(id==='phoenix'||style.rarity==='legendary'){add('#bf3430',ribbon(1.45),.55);add('#ff9c38',ribbon(.85),.9);add('#fff1a1',ribbon(.3),1.3,true);return out;}
 if(id==='atlas'){
  add(dark,ribbon(.38,()=>1,()=>-width*.35));add(c,ribbon(.38,()=>1,()=>width*.35));
  const ties:P[][]=[];for(const p of s)if(p.d%(width*2.8)<width*.35)ties.push([point(p,-width*.08,-width*.45),point(p,width*.08,-width*.45),point(p,width*.08,width*.45),point(p,-width*.08,width*.45)]);add(light,ties);return out;
 }
 if(id==='broad'){add(dark,ribbon(1.45,()=>1,()=>0,false));add(c,ribbon(1.23,()=>1,()=>0,false));add(light,ribbon(.09,()=>1,()=>-width*.34,false));add(light,ribbon(.09,()=>1,()=>width*.34,false));return out;}
 if(id==='marsh'){const scallop=(d:number)=>.85+.2*Math.cos(d/(width*.65));add(dark,ribbon(1.18,scallop));add(c,ribbon(.94,scallop));add(light,ribbon(.14));return out;}
 if(id==='swift'||id==='trail'){
  const teeth=(d:number)=>.7+.3*(1-((d/(width*2.8))%1));
  add(dark,ribbon(1.3,teeth));add(c,ribbon(1.06,teeth));add(light,ribbon(.17),id==='trail'?.13:0,id==='trail');
  const marks:P[][]=[];for(let i=0;i<s.length;i++){const p=s[i];if(i&&Math.floor(p.d/(width*5))===Math.floor(s[i-1].d/(width*5)))continue;marks.push([point(p,width*.48,0),point(p,-width*.25,-width*.28),point(p,-width*.25,width*.28)]);}add(light,marks);return out;
 }
 if(id==='golden'){
  add(dark,ribbon(1.18));add(c,ribbon(.94),.12);
  add(light,ribbon(.22,()=>1,d=>Math.sin(d/(width*1.7))*width*.3),.18,true);
  add(mix(c,'#fff3c8',.2),ribbon(.19,()=>1,d=>-Math.sin(d/(width*1.7))*width*.3),.1);
  const stars:P[][]=[];for(let i=0;i<s.length;i++){const p=s[i];if(i&&Math.floor(p.d/(width*7))===Math.floor(s[i-1].d/(width*7)))continue;stars.push([point(p,width*.5,0),point(p,0,-width*.25),point(p,-width*.5,0),point(p,0,width*.25)]);}add('#ffe7a3',stars,.2);return out;
 }
 if(id==='willow'){
  add(dark,ribbon(1.08));add(c,ribbon(.8),.1);add(light,ribbon(.13),.15,true);
  const leaves:P[][]=[];
  let last=-1;for(const p of s){const index=Math.floor(p.d/(width*3));if(index===last)continue;last=index;const side=index%2?1:-1;leaves.push([point(p,0,0),point(p,width*.5,side*width*.65),point(p,width*.15,side*width*1.05),point(p,-width*.3,side*width*.5)]);}
  add(mix(c,'#bde58b',.35),leaves,.08);return out;
 }
 add(dark,ribbon(1.15));add(c,ribbon());
 return out;
}
export function brushInkParticles(id:string,points:P[],time:number,scale=1){
 const style=brushStrokeStyle(id),total=length(points);
 if(style.effect==='none'||points.length<2||total<1)return [];
 if(style.effect==='flame')return phoenixEmbers(points,time,scale).map(p=>({...p,alpha:p.heat,color:p.heat>.5?'#fff4ab':'#f77a36'}));
 const count=Math.min(8,Math.max(1,Math.ceil(total/(80*scale))));
 return Array.from({length:count},(_,i)=>{
  const phase=((time*.22+i*.61803398875)%1+1)%1;
  const at=style.effect==='motes'?phase:(i+.5)/count,p=along(points,total*at);
  const glint=style.effect==='glint',heat=glint?.25+.55*Math.pow(Math.sin((time+i)*1.7),2):Math.sin(phase*Math.PI)*.65;
  return {x:p.x+Math.sin(time+i*3)*2*scale,y:p.y,rise:(glint?1:phase*6)*scale,size:(glint?1.7:1.5)*scale,heat,alpha:heat,color:glint?'#fff0ae':style.effect==='pollen'?'#c5edab':'#ffe0a1'};
 });
}
export function drawBrushInk(ctx:CanvasRenderingContext2D,id:string,points:P[],width:number,time:number,reduced=false){
 const style=brushStrokeStyle(id);
 for(const layer of buildInkLayers(id,points,width)){
  ctx.fillStyle=layer.color;ctx.globalAlpha=1;
  if(layer.pulse&&!reduced)ctx.globalAlpha=.9+Math.sin(time*2.3)*.1;
  ctx.shadowColor=layer.color;ctx.shadowBlur=style.effect==='flame'&&layer.glow>0?5:0;
  ctx.beginPath();for(const poly of layer.polygons){poly.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();}ctx.fill();ctx.shadowBlur=0;
 }
 if(!reduced)for(const p of brushInkParticles(id,points,time)){
  ctx.globalAlpha=p.alpha;ctx.fillStyle=p.color;ctx.beginPath();
  if(style.effect==='glint'){ctx.moveTo(p.x,p.y-p.rise-p.size*1.8);ctx.lineTo(p.x+p.size,p.y-p.rise);ctx.lineTo(p.x,p.y-p.rise+p.size*1.8);ctx.lineTo(p.x-p.size,p.y-p.rise);ctx.closePath();}
  else ctx.ellipse(p.x,p.y-p.rise,p.size,Math.max(.2,p.size*(style.effect==='flame'?1.7:1)),.3,0,Math.PI*2);
  ctx.fill();
 }
 ctx.globalAlpha=1;ctx.shadowBlur=0;
}
