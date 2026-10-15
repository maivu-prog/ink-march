import {test} from 'node:test';
import assert from 'node:assert/strict';
import {phoenixEmbers} from '../src/phoenix-ink';
test('Phoenix is bounded, finite and follows the route without changing it',()=>{
 const points=[{x:0,y:40},{x:100000,y:40}],before=JSON.stringify(points);
 for(const time of [0,.5,10,10000]){const embers=phoenixEmbers(points,time);assert.equal(embers.length,36);for(const p of embers){assert.ok(Object.values(p).every(Number.isFinite));assert.ok(p.x>=-4&&p.x<=100004);assert.ok(Math.abs(p.y-40)<=2);assert.ok(p.heat>=0&&p.heat<=1);assert.ok(p.size>=0&&p.size<=2.4);}}
 assert.equal(JSON.stringify(points),before);
});
test('Phoenix has no particles for empty or zero-length strokes',()=>{assert.deepEqual(phoenixEmbers([],0),[]);assert.deepEqual(phoenixEmbers([{x:1,y:1},{x:1,y:1}],0),[]);});
test('Phoenix embers rise over time and can use battlefield scale',()=>{const points=[{x:0,y:0},{x:100,y:0}],a=phoenixEmbers(points,0)[0],b=phoenixEmbers(points,.2)[0],large=phoenixEmbers(points,0,2)[0];assert.ok(b.rise>a.rise);assert.ok(b.size<a.size);assert.equal(large.rise,a.rise*2);});
