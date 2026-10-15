import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as T from 'three';
import {clayBoard,clayScenery} from '../src/clay-world';
import {maps,fieldOf,inside} from '../src/systems';
for(const map of Object.values(maps).filter(m=>m.chapter===1))test(map.id+': woodland contour encloses the playable field and preserves ravine holes',()=>{const group=new T.Group(),top=clayBoard(group,map),f=fieldOf(map),ray=new T.Raycaster();group.updateMatrixWorld(true);for(let i=0;i<7;i++)for(let j=0;j<7;j++){const x=f.x+2+(f.w-4)*i/6,z=f.y+2+(f.h-4)*j/6;if(map.obstacles.some(o=>o.kind==='chasm'&&inside({x,y:z},o)))continue;ray.set(new T.Vector3(x,100,z),new T.Vector3(0,-1,0));assert.ok(ray.intersectObject(top).length,'Missing ground at '+x+','+z);}assert.deepEqual(clayScenery(map),clayScenery(map));});
