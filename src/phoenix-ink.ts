import {along,length,type P} from './systems';
/** Bounded decorative embers sampled by distance; never edits the route. */
export function phoenixEmbers(points:P[],time:number,scale=1){
 const total=length(points);if(points.length<2||total<1)return [];
 const count=Math.min(36,Math.max(1,Math.ceil(total/(18*scale))));
 return Array.from({length:count},(_,i)=>{
  const phase=((time*.65+i*.61803398875)%1+1)%1;
  const p=along(points,total*(i+.5)/count);
  return {x:p.x+Math.sin(i*2.4+phase*5)*4*scale,y:p.y+Math.cos(i*1.7)*2*scale,rise:(3+phase*18)*scale,size:(1-phase)*2.4*scale,heat:1-phase};
 });
}
