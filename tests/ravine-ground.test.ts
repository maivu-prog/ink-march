import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as T from 'three';
import {maps,fieldOf} from '../src/systems';
import {clayBoard,islandWithRavines} from '../src/clay-world';
const ray=new T.Raycaster();
function hits(g:T.Group,x:number,z:number){g.updateMatrixWorld(true);ray.set(new T.Vector3(x,100,z),new T.Vector3(0,-1,0));return ray.intersectObjects(g.children,true);}
for(const map of Object.values(maps).filter(m=>m.obstacles.some(o=>o.kind==='chasm')))test(map.id+': every soil layer is open above the ravine; nearby ground stays solid',()=>{const g=new T.Group();clayBoard(g,map);const chasms=map.obstacles.filter(o=>o.kind==='chasm');assert.equal(islandWithRavines(map,16).holes.length,chasms.length);for(const o of chasms){for(const [u,v] of [[.2,.2],[.5,.5],[.8,.8]])assert.equal(hits(g,o.x+o.w*u,o.y+o.h*v).length,0,'Ground must not fill the ravine');}const start=map.starts[0];assert.ok(hits(g,start.x,start.y).length>=3,'All ground layers remain under START');for(const o of g.children){const mesh=o as T.Mesh;mesh.geometry.dispose();(mesh.material as T.Material).dispose();}});
test('The Ravine: the narrow crossing is solid and ground does not cover water/ink at y=1',()=>{const g=new T.Group();clayBoard(g,maps.c1_s5);const intersections=hits(g,269,503);assert.ok(intersections.length>=3);assert.ok(Math.max(...intersections.map(h=>h.point.y))<1);});

test('ground layer tops are separated above and below the ravine, avoiding coplanar flicker',()=>{const g=new T.Group();clayBoard(g,maps.c1_s5);for(const [x,z] of [[360,300],[269,503],[360,700]]){const top=g.children.map(layer=>{const group=new T.Group();const copy=layer.clone();group.add(copy);return hits(group,x,z)[0]?.point.y;}).filter((y):y is number=>y!==undefined).sort((a,b)=>b-a);assert.equal(top.length,3);assert.ok(top[0]-top[1]>5);assert.ok(top[1]-top[2]>5);}});
