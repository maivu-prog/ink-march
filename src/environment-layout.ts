export type Region={kind:string;points:number[][];up?:number[]};
export type XY={x:number;y:number};
export const BEAN_HEIGHT=72;
export const environmentTypes=['tower','rock','rock_cluster','tree','tree_round','wall','gate_red','gate_blue','chest','key_red','key_blue','flag_start','flag_start_orange','flag_clash','pedestal','bridge_gold','hill','hill_large','slope_ramp','chasm','chasm_corner','cliff_edge','field_border'];
export function regionBounds(points:number[][]){const xs=points.map(p=>p[0]),zs=points.map(p=>p[1]),x=Math.min(...xs),z=Math.min(...zs),w=Math.max(...xs)-x,d=Math.max(...zs)-z;return{x,z,w,d,cx:x+w/2,cz:z+d/2};}
export function inRegion(p:XY,points:number[][]){let hit=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const a=points[i],b=points[j];if((a[1]>p.y)!==(b[1]>p.y)&&p.x<(b[0]-a[0])*(p.y-a[1])/(b[1]-a[1])+a[0])hit=!hit;}return hit;}
export function terrainSpec(t:Region){const b=regionBounds(t.points),large=Math.max(b.w,b.d)>360;return{...b,id:t.kind==='slope'?'slope_ramp':large?'hill_large':'hill',height:BEAN_HEIGHT*(t.kind==='slope'?.6:large?.55:.42),angle:t.kind==='slope'?Math.atan2(t.up?.[0]||0,t.up?.[1]??-1):0};}
/** The visible surface profile is shared by terrain meshes, troops, picking and ink. */
export function terrainHeight(t:Region,p:XY){
 if(t.kind==='sand')return 10;if(t.kind==='swamp')return 6;if(t.kind==='road')return 8;
 const b=terrainSpec(t);if(!b.w||!b.d)return 0;
 if(t.kind==='hill'){
  let edge=Infinity;for(let i=0;i<t.points.length;i++){const a=t.points[i],c=t.points[(i+1)%t.points.length],dx=c[0]-a[0],dz=c[1]-a[1],f=Math.max(0,Math.min(1,((p.x-a[0])*dx+(p.y-a[1])*dz)/(dx*dx+dz*dz||1)));edge=Math.min(edge,Math.hypot(p.x-a[0]-dx*f,p.y-a[1]-dz*f));}
  const v=Math.min(1,edge/Math.min(34,b.w*.22,b.d*.22)),smooth=v*v*(3-2*v);return 6+(b.height-6)*smooth;
 }
 if(t.kind==='slope'){const up=t.up||[0,-1],n=Math.hypot(...up)||1,ux=up[0]/n,uz=up[1]/n,extent=Math.abs(ux)*b.w/2+Math.abs(uz)*b.d/2;return b.height*Math.max(0,Math.min(1,.5+((p.x-b.cx)*ux+(p.y-b.cz)*uz)/(extent*2)));}
 return 0;
}
export function terrainElevation(terrain:Region[],p:XY){let elevation=0;for(const t of terrain)if(inRegion(p,t.points))elevation=Math.max(elevation,terrainHeight(t,p));return elevation;}
export function surfaceElevation(map:{terrain:Region[];goldZones:{points:number[][]}[]},p:XY){return Math.max(terrainElevation(map.terrain||[],p),(map.goldZones||[]).some(z=>inRegion(p,z.points))?6:0);}
export function subdividePath(points:XY[],maxStep=10){return points.flatMap((p,i)=>{if(!i)return[p];const a=points[i-1],steps=Math.max(1,Math.ceil(Math.hypot(p.x-a.x,p.y-a.y)/maxStep));return Array.from({length:steps},(_,j)=>({x:a.x+(p.x-a.x)*(j+1)/steps,y:a.y+(p.y-a.y)*(j+1)/steps}));});}
