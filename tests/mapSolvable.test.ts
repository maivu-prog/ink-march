import {test} from 'node:test';import assert from 'node:assert/strict';
import {maps,burnRate,lerp,brushFx,NO_BRUSH,BR} from '../src/systems';
import {drawPool,simulate} from '../tools/mapTools';
import chapters from '../src/data/chapters.json';
test('10 chapters of 3 to 5 stages',()=>{assert.equal(chapters.length,10);for(const c of chapters){const n=c.stages.filter(id=>maps[id]).length;assert.ok(n>=3&&n<=5,c.name);}});
test('every stage has 3 camps',()=>{for(const m of Object.values(maps))assert.equal(m.camps.length,3,m.id);});
test('after the first stage, a straight line is blocked or crosses costly terrain',()=>{for(const m of Object.values(maps)){if(m.id==='c1_s1')continue;const target=(t:number)=>m.bosses[Math.min(t,m.bosses.length-1)];let p=drawPool({...m,baseInk:99999},m.starts.map((s,t)=>[[s.x,s.y],[target(t).x,target(t).y]]));let costly=m.starts.some((s,t)=>{for(let i=0;i<=40;i++)if(burnRate(m,lerp(s,target(t),i/40),NO_BRUSH)>1)return true;return false;});assert.ok(!p.valid||costly,m.id);}});
for(const m of Object.values(maps)){
 test(m.id+' 3-star reference is drawable with its design brush and destroys every camp',()=>{const brush=(m as any).design?.threeStarBrush||'quill';assert.ok(BR[brush]);const pool=drawPool(m,m.referenceSolution,brushFx(brush,1));assert.ok(pool.valid,`${m.id}: ${pool.error} with ${brush}`);const r=simulate(m,drawPool({...m,baseInk:99999},m.referenceSolution));assert.equal(r.result,'win',`${m.id}: ${JSON.stringify(r)}`);assert.equal(r.camps,m.camps.length,`${m.id}: ${JSON.stringify(r)}`);});
}
