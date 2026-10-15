import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as T from 'three';
import {terrainHeight,terrainElevation,inRegion,type Region} from '../src/environment-layout';
import {terrainTriangles,terrainEdges} from '../src/terrain-geometry';
import {addTerrainSolid} from '../src/terrain-solids';
import {brushRack} from '../src/brush-workshop';
const points=[[0,0],[300,0],[300,260],[0,260]],cut={x:110,y:70,w:80,h:190};
test('owned brushes precede every uncollected brush without losing preview state',()=>{
 const html=brushRack('golden',{quill:1,phoenix:1,swift:2},'phoenix');
 const ids=[...html.matchAll(/data-id="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,12);assert.deepEqual(ids.slice(0,3),['quill','swift','phoenix']);assert.ok(html.includes('aria-label="Preview Golden Quill" aria-pressed="true"'));
});
for(const kind of ['sand','swamp','road','hill','slope'])test(kind+': surface is raised, finite and preserves the exact ravine opening',()=>{
 const t:Region={kind,points,up:[0,-1]},tris=terrainTriangles(t,[cut]);assert.ok(tris.length>0&&tris.length<16000);
 for(const tri of tris){const mid={x:tri.reduce((s,p)=>s+p.x,0)/3,y:tri.reduce((s,p)=>s+p.y,0)/3};assert.ok(inRegion(mid,points));assert.ok(!(mid.x>cut.x+.001&&mid.x<cut.x+cut.w-.001&&mid.y>cut.y+.001&&mid.y<cut.y+cut.h-.001),'No surface can span the cutout');for(const p of tri)assert.ok(Number.isFinite(terrainHeight(t,p)));}
 assert.ok(terrainElevation([t],{x:50,y:50})>0);assert.equal(terrainElevation([t],{x:-1,y:50}),0);
 assert.ok(terrainEdges(t,[cut]).some(e=>Math.abs(e.a.x-cut.x)<.001&&Math.abs(e.b.x-cut.x)<.001),'Ravine edge gets a visible vertical wall');
 const group=new T.Group(),solid=addTerrainSolid(group,t,{obstacles:[{type:'rect',kind:'chasm',...cut}]} as any)!;assert.equal(solid.userData.terrainKind,kind);assert.ok(solid.children.length<=4);solid.traverse(o=>{if(o instanceof T.Mesh){const pos=o.geometry.getAttribute('position');for(let i=0;i<pos.count;i++)assert.ok([pos.getX(i),pos.getY(i),pos.getZ(i)].every(Number.isFinite));}});
});
test('a cut spanning the whole patch leaves no ground or fake bridge',()=>{assert.equal(terrainTriangles({kind:'sand',points},[{x:-10,y:-10,w:320,h:280}]).length,0);assert.equal(terrainEdges({kind:'sand',points},[{x:-10,y:-10,w:320,h:280}]).length,0);});
test('slope high edge follows its actual uphill direction',()=>{for(const up of [[0,-1],[0,1],[1,0],[-1,0]]){const t:Region={kind:'slope',points,up},a={x:150+up[0]*80,y:130+up[1]*80},b={x:150-up[0]*80,y:130-up[1]*80};assert.ok(terrainHeight(t,a)>terrainHeight(t,b));}});
