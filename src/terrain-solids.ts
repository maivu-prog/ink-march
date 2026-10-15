import * as T from 'three';
import {regionBounds,terrainHeight,terrainSpec,type Region} from './environment-layout';
import {terrainTriangles,terrainEdges,terrainContains,type TerrainCut,type TerrainPoint} from './terrain-geometry';
import type {MapData} from './systems';
type V=[number,number,number];
const palette:Record<string,{top:string;side:string;rim:string}>={sand:{top:'#e9c474',side:'#b58343',rim:'#f5d894'},swamp:{top:'#386f69',side:'#66563f',rim:'#8d8050'},road:{top:'#84785e',side:'#75654b',rim:'#b1a887'},hill:{top:'#7b9c54',side:'#876245',rim:'#b4c979'},slope:{top:'#b4ab69',side:'#956d48',rim:'#e1d193'}};
class Batch{
 positions:number[]=[];colors:number[]=[];
 polygon(points:V[],color:string){const c=new T.Color(color);for(let i=1;i<points.length-1;i++)for(const p of [points[0],points[i],points[i+1]]){this.positions.push(...p);this.colors.push(c.r,c.g,c.b);}}
 mesh(parent:T.Group,name:string,roughness=1,shadow=false){if(!this.positions.length)return;const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(this.positions,3));g.setAttribute('color',new T.Float32BufferAttribute(this.colors,3));g.computeVertexNormals();const m=new T.Mesh(g,new T.MeshStandardMaterial({vertexColors:true,roughness,side:T.DoubleSide}));m.name=name;m.receiveShadow=true;m.castShadow=shadow;parent.add(m);return m;}
}
/** Chunky terrain pieces follow the exact playable polygon and share its height profile. */
export function addTerrainSolid(parent:T.Group,t:Region,map?:MapData){
 const p=palette[t.kind];if(!p)return;
 const cuts:TerrainCut[]=(map?.obstacles||[]).filter((o:any)=>o.type==='rect'&&['chasm','water'].includes(o.kind)).map((o:any)=>({x:o.x,y:o.y,w:o.w,h:o.h}));
 const group=new T.Group();group.name='Terrain '+t.kind;group.userData.terrainKind=t.kind;parent.add(group);
 const top=new Batch(),sides=new Batch(),rim=new Batch(),detail=new Batch(),b=regionBounds(t.points),edges=terrainEdges(t,cuts);
 const at=(a:TerrainPoint,offset=0):V=>[a.x,terrainHeight(t,a)+offset,a.y];
 const valid=(poly:TerrainPoint[])=>poly.every(a=>terrainContains(t,cuts,a));
 const groundPoly=(poly:TerrainPoint[],color:string,offset=.4)=>{if(valid(poly))detail.polygon(poly.map(a=>at(a,offset)),color);};
 for(const tri of terrainTriangles(t,cuts)){
  let color=p.top;if(t.kind==='hill'){const center={x:tri.reduce((s,a)=>s+a.x,0)/3,y:tri.reduce((s,a)=>s+a.y,0)/3},f=terrainHeight(t,center)/terrainSpec(t).height;color='#'+new T.Color('#a89c62').lerp(new T.Color(p.top),f).getHexString();}
  top.polygon(tri.map(a=>at(a,t.kind==='road'?-.2:0)),color);
 }
 for(const e of edges){const dx=e.b.x-e.a.x,dy=e.b.y-e.a.y,n=Math.max(1,Math.ceil(Math.hypot(dx,dy)/28));
  for(let i=0;i<n;i++){const a={x:e.a.x+dx*i/n,y:e.a.y+dy*i/n},c={x:e.a.x+dx*(i+1)/n,y:e.a.y+dy*(i+1)/n},ha=terrainHeight(t,a),hc=terrainHeight(t,c);
   sides.polygon([[a.x,0,a.y],[c.x,0,c.y],[c.x,hc,c.y],[a.x,ha,a.y]],p.side);
   if(t.kind==='hill'||t.kind==='slope')sides.polygon([[a.x,ha*.28,a.y],[c.x,hc*.28,c.y],[c.x,hc*.43,c.y],[a.x,ha*.43,a.y]],'#b28d5d');
   const width=t.kind==='swamp'?5:3,innerA={x:a.x+e.nx*width,y:a.y+e.ny*width},innerC={x:c.x+e.nx*width,y:c.y+e.ny*width},raise=t.kind==='swamp'?1.4:.35;
   rim.polygon([at(a,raise),at(c,raise),at(innerC,raise),at(innerA,raise)],p.rim);
  }
 }
 if(t.kind==='sand'){
  let row=0;for(let z=b.z+27;z<b.z+b.d-12;z+=62,row++)for(let x=b.x+16+(row%2)*34;x<b.x+b.w-20;x+=105){for(let i=0;i<11;i++){const a={x:x+i*6,y:z+Math.sin(i/10*Math.PI)*8},c={x:x+(i+1)*6,y:z+Math.sin((i+1)/10*Math.PI)*8};groundPoly([{x:a.x,y:a.y-2},a,c,{x:c.x,y:c.y-2}],row%2?'#f6d894':'#e1b669',.7);}}
 }else if(t.kind==='road'){
  let row=0;for(let z=b.z+3;z<b.z+b.d-5;z+=48,row++)for(let x=b.x+3;x<b.x+b.w-5;x+=42){const w=Math.min(38,b.x+b.w-3-x),d=Math.min(44,b.z+b.d-3-z);if(w<9||d<9)continue;const r=4,poly=[{x:x+r,y:z},{x:x+w-r,y:z},{x:x+w,y:z+r},{x:x+w,y:z+d-r},{x:x+w-r,y:z+d},{x:x+r,y:z+d},{x,y:z+d-r},{x,y:z+r}];groundPoly(poly,(row+Math.floor(x/42))%3===0?'#d1c9ac':(row+Math.floor(x/42))%3===1?'#bcb99f':'#c4c2a7',0);}
 }else if(t.kind==='swamp'){
  let count=0;for(let z=b.z+28;z<b.z+b.d-15;z+=77)for(let x=b.x+28+(count%2)*13;x<b.x+b.w-15;x+=94,count++){
   const r=7+(count%3)*2,poly=Array.from({length:12},(_,i)=>({x:x+Math.cos(i*Math.PI/6)*r,y:z+Math.sin(i*Math.PI/6)*r*.7}));groundPoly(poly,count%2?'#94a961':'#6e9256',.55);
   for(let i=0;i<12;i++){const a=i/12*Math.PI*2,c=(i+1)/12*Math.PI*2;groundPoly([{x:x+Math.cos(a)*(r+4),y:z+Math.sin(a)*(r+4)*.7},{x:x+Math.cos(c)*(r+4),y:z+Math.sin(c)*(r+4)*.7},{x:x+Math.cos(c)*(r+5),y:z+Math.sin(c)*(r+5)*.7},{x:x+Math.cos(a)*(r+5),y:z+Math.sin(a)*(r+5)*.7}],'#648b75',.25);}
  }
  let reeds=0;for(const e of edges){if(reeds>=12)break;const len=Math.hypot(e.b.x-e.a.x,e.b.y-e.a.y);for(let d=35;d<len&&reeds<12;d+=112,reeds++){const f=d/len,a={x:e.a.x+(e.b.x-e.a.x)*f+e.nx*9,y:e.a.y+(e.b.y-e.a.y)*f+e.ny*9};if(!terrainContains(t,cuts,a))continue;const h=terrainHeight(t,a);for(const s of [-1,1])detail.polygon([[a.x+s*3-1,h,a.y],[a.x+s*3+1,h,a.y],[a.x+s*6,h+15+(reeds%3)*2,a.y+2],[a.x+s*4,h+13,a.y+2]],s===1?'#c1bb78':'#8f9f60');}}
 }else if(t.kind==='slope'){
  const up=t.up||[0,-1],n=Math.hypot(...up)||1,ux=up[0]/n,uy=up[1]/n,extent=Math.abs(ux)*b.w/2+Math.abs(uy)*b.d/2;
  for(const f of [-.48,0,.48]){const x=b.cx+ux*extent*f,y=b.cz+uy*extent*f;groundPoly([[-20,-7],[0,12],[20,-7],[20,-18],[0,1],[-20,-18]].map(([side,forward])=>({x:x-uy*side+ux*forward,y:y+ux*side+uy*forward})),'#fff0bd',.8);}
 }else if(t.kind==='hill'){
  for(let z=b.z+55;z<b.z+b.d-20;z+=108)for(let x=b.x+52;x<b.x+b.w-20;x+=126)groundPoly([{x:x-7,y:z},{x:x-2,y:z-4},{x:x+6,y:z-1},{x:x+8,y:z+3},{x:x+1,y:z+5}],'#b3c380',.35);
 }
 sides.mesh(group,'Terrain cut walls',1,true);top.mesh(group,'Terrain walk surface',t.kind==='swamp'?.48:1,true);rim.mesh(group,'Terrain sculpted border',1,true);detail.mesh(group,'Terrain material details',t.kind==='swamp'?.65:1);
 return group;
}
