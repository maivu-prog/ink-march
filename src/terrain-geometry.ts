import {ShapeUtils,Vector2} from 'three';
import {inRegion,terrainHeight,type Region,type XY} from './environment-layout';
export type TerrainCut={x:number;y:number;w:number;h:number};
export type TerrainPoint={x:number;y:number};
const area=(p:TerrainPoint[])=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.y-b.x*a.y;},0))/2;
function clip(poly:TerrainPoint[],distance:(p:TerrainPoint)=>number){const out:TerrainPoint[]=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],da=distance(a),db=distance(b),ia=da>=-1e-7,ib=db>=-1e-7;if(ia)out.push(a);if(ia!==ib){const t=da/(da-db);out.push({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});}}return out;}
/** Exact subtraction keeps raised patches from bridging water or ravines. */
export function terrainFootprint(t:Region,cuts:TerrainCut[]=[]){
 const outline=t.points.map(([x,y])=>({x,y})),indices=ShapeUtils.triangulateShape(outline.map(p=>new Vector2(p.x,p.y)),[]);
 let pieces=indices.map(tri=>tri.map(i=>outline[i]));
 for(const c of cuts){const planes=[(p:TerrainPoint)=>p.x-c.x,(p:TerrainPoint)=>c.x+c.w-p.x,(p:TerrainPoint)=>p.y-c.y,(p:TerrainPoint)=>c.y+c.h-p.y],next:TerrainPoint[][]=[];
  for(const poly of pieces){let rest=poly;for(const plane of planes){if(rest.length<3)break;const outside=clip(rest,p=>-plane(p));if(outside.length>=3&&area(outside)>.0001)next.push(outside);rest=clip(rest,plane);}}
  pieces=next;
 }
 return pieces;
}
const middle=(a:TerrainPoint,b:TerrainPoint)=>({x:(a.x+b.x)/2,y:(a.y+b.y)/2});
export function terrainTriangles(t:Region,cuts:TerrainCut[]=[]){
 const out:TerrainPoint[][]=[];
 const split=(a:TerrainPoint,b:TerrainPoint,c:TerrainPoint,depth=0)=>{const edge=Math.max(Math.hypot(a.x-b.x,a.y-b.y),Math.hypot(b.x-c.x,b.y-c.y),Math.hypot(c.x-a.x,c.y-a.y));if(edge<=38||depth>=5){out.push([a,b,c]);return;}const ab=middle(a,b),bc=middle(b,c),ca=middle(c,a);split(a,ab,ca,depth+1);split(ab,b,bc,depth+1);split(ca,bc,c,depth+1);split(ab,bc,ca,depth+1);};
 for(const poly of terrainFootprint(t,cuts))for(let i=1;i<poly.length-1;i++)split(poly[0],poly[i],poly[i+1]);return out;
}
export function terrainContains(t:Region,cuts:TerrainCut[],p:XY){return inRegion(p,t.points)&&!cuts.some(c=>p.x>c.x+1e-6&&p.x<c.x+c.w-1e-6&&p.y>c.y+1e-6&&p.y<c.y+c.h-1e-6);}
/** Exposed contour segments include the walls around holes cut out of a patch. */
export function terrainEdges(t:Region,cuts:TerrainCut[]=[]){
 const loops=[t.points,...cuts.map(c=>[[c.x,c.y],[c.x+c.w,c.y],[c.x+c.w,c.y+c.h],[c.x,c.y+c.h]])],segments=loops.flatMap(poly=>poly.map(([x,y],i)=>[{x,y},{x:poly[(i+1)%poly.length][0],y:poly[(i+1)%poly.length][1]}]));
 const out:{a:TerrainPoint;b:TerrainPoint;nx:number;ny:number}[]=[],seen=new Set<string>();
 for(const [a,b] of segments){const dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy);if(len<.001)continue;const splits=[0,1];
  for(const [c,d] of segments){const ex=d.x-c.x,ey=d.y-c.y,den=dx*ey-dy*ex;if(Math.abs(den)<1e-8)continue;const u=((c.x-a.x)*ey-(c.y-a.y)*ex)/den,v=((c.x-a.x)*dy-(c.y-a.y)*dx)/den;if(u>1e-6&&u<1-1e-6&&v>=-1e-6&&v<=1+1e-6)splits.push(u);}
  splits.sort((x,y)=>x-y);
  for(let i=1;i<splits.length;i++){const u=splits[i-1],v=splits[i];if(v-u<1e-6)continue;const p={x:a.x+dx*u,y:a.y+dy*u},q={x:a.x+dx*v,y:a.y+dy*v},m=middle(p,q),nx=-dy/len,ny=dx/len,left=terrainContains(t,cuts,{x:m.x+nx*.01,y:m.y+ny*.01}),right=terrainContains(t,cuts,{x:m.x-nx*.01,y:m.y-ny*.01});if(left===right)continue;
   const key=[p,q].map(k=>k.x.toFixed(4)+','+k.y.toFixed(4)).sort().join(':');if(seen.has(key))continue;seen.add(key);out.push({a:p,b:q,nx:nx*(left?1:-1),ny:ny*(left?1:-1)});
  }
 }
 return out;
}
export function terrainSurfaceVertices(t:Region,cuts:TerrainCut[]=[]){return terrainTriangles(t,cuts).flatMap(tri=>tri.flatMap(p=>[p.x,terrainHeight(t,p),p.y]));}
