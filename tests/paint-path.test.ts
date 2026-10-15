import {test} from 'node:test';
import assert from 'node:assert/strict';
import {paintPath} from '../src/paint-path';
import {maps,inside} from '../src/systems';
test('rounded paint keeps endpoints and never mutates the simulation route',()=>{const p=[{x:200,y:700},{x:200,y:500},{x:400,y:500}],before=JSON.stringify(p),q=paintPath(p,{...maps.c1_s1,obstacles:[],items:[]});assert.equal(JSON.stringify(p),before);assert.deepEqual(q[0],p[0]);assert.deepEqual(q.at(-1),p.at(-1));assert.ok(q.length>p.length);});
test('paint cannot round a safe corner through a blocking ravine or wall',()=>{const points=[{x:100,y:300},{x:100,y:100},{x:300,y:100}],obstacle={type:'rect',kind:'chasm',x:101,y:101,w:60,h:60},map={...maps.c1_s1,items:[],goldZones:[],obstacles:[obstacle]},q=paintPath(points,map);assert.ok(q.every(p=>!inside(p,obstacle)));assert.ok(q.some(p=>p.x===100&&p.y===100));});
