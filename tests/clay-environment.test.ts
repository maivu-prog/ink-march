import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {clayAssets,clayScenery,islandShape} from '../src/clay-world';
import {fieldOf,type MapData} from '../src/systems';
import map from '../src/data/maps/c1_s1.json';
for(const id of clayAssets)test(id+': clay GLB has smooth normals, compact embedded palette and static geometry',()=>{const b=readFileSync(new URL('../public/assets/models/clay-v5/'+id+'.glb',import.meta.url));const n=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+n).toString());assert.equal(b.readUInt32LE(0),0x46546c67);assert.equal(j.animations?.length||0,0);assert.equal(j.materials.length,1);assert.equal(j.images.length,1);assert.ok(!j.images[0].uri);assert.ok(b.length<150000);for(const m of j.meshes)for(const p of m.primitives)assert.ok(p.attributes.NORMAL!==undefined);const tris=j.meshes.reduce((s:number,m:any)=>s+m.primitives.reduce((s:number,p:any)=>s+j.accessors[p.indices].count/3,0),0);assert.ok(tris<4000);});
test('scenery is deterministic and anchors outside the unchanged playable area',()=>{const data=map as unknown as MapData,before=JSON.stringify(data),f=fieldOf(data),a=clayScenery(data);assert.deepEqual(a,clayScenery(data));assert.equal(JSON.stringify(data),before);assert.ok(a.length>=18);for(const p of a){assert.ok(p.x<f.x||p.x>f.x+f.w);assert.ok(p.z>f.y&&p.z<f.y+f.h+20);}});
test('rounded island contour is closed and encloses the playable rectangle',()=>{const s=islandShape(-16,-16,536,732,30),p=s.getPoints(12);assert.deepEqual(p[0],p.at(-1));assert.ok(p.length>20);});
