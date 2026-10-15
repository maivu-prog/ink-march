import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as T from 'three';
import {BR,InkPool,brushFx} from '../src/systems';
import {makeBrush,disposeBrush} from '../src/brush3d';
import {brushTestMap,brushComparison,brushInkColor,routeTravelSeconds,type TestTerrain} from '../src/brush-workshop';
for(const id of Object.keys(BR))test(id+': toy brush is finite, broad enough to read, and grounded at its nib',()=>{const g=makeBrush(id);g.updateMatrixWorld(true);const b=new T.Box3().setFromObject(g),size=b.getSize(new T.Vector3());assert.ok([...b.min,...b.max].every(Number.isFinite));assert.ok(size.x>28);assert.ok(size.y>100&&size.y<165);assert.ok(b.min.y>=-3);assert.equal(g.userData.brush,id);disposeBrush(g);});
for(const terrain of ['grass','sand','swamp','road'] as TestTerrain[])for(const id of Object.keys(BR))test(id+' on '+terrain+': workbench cost agrees with real InkPool at 1 and 3 stars',()=>{for(const stars of [1,3]){const map=brushTestMap(terrain),pool=new InkPool(map,0,brushFx(id,stars));pool.paths[0].add(map.starts[0]);pool.paths[0].add({x:120,y:120});assert.equal(Math.ceil(300-pool.ink-1e-8),brushComparison(id,stars,terrain).ink);}});
test('terrain specialists and stars demonstrate real savings without inflating the ink pot',()=>{const quill=brushComparison('quill',1,'sand'),reed=brushComparison('reed',1,'sand'),better=brushComparison('reed',3,'sand');assert.ok(reed.ink<quill.ink);assert.ok(better.ink<reed.ink);for(const id of Object.keys(BR))assert.equal(new InkPool(brushTestMap('grass'),0,brushFx(id,3)).ink,300);});
test('every brush has its own pigment, shared by its model and drawn ink',()=>{assert.equal(new Set(Object.keys(BR).map(brushInkColor)).size,Object.keys(BR).length);for(const id of Object.keys(BR)){assert.equal(brushInkColor(id),BR[id].look.p);assert.match(brushInkColor(id),/^#[a-f0-9]{6}$/);assert.notEqual(brushInkColor(id),'#f6c94f');}});

test('route travel estimate reflects the active brush and terrain',()=>{const points=[{x:20,y:120},{x:120,y:120}],meadow=brushTestMap('grass'),sand=brushTestMap('sand'),quill=routeTravelSeconds(meadow,points,brushFx('quill')),swift=routeTravelSeconds(meadow,points,brushFx('swift'));assert.ok(Math.abs(quill/swift-1.15)<1e-9);assert.ok(routeTravelSeconds(sand,points,brushFx('reed'))<routeTravelSeconds(sand,points,brushFx('quill')));});
