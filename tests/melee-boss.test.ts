import {test} from 'node:test';
import assert from 'node:assert/strict';
import {maps,Battle,C,fresh,type Run} from '../src/systems';
import {drawPool} from '../tools/mapTools';

// Đường vẽ được tính là chạm boss khi cách boss tới bossSnapRadius, xa hơn vùng aggro của lính cận chiến.
// Tới cuối đường thì đội phải tự lao vào boss, kể cả khi chỉ còn Shieldbearer/Swordsman.
test('a melee-only squad still damages the boss at the end of its line',()=>{
 const map={...maps.c2_s2,baseInk:99999},pool=drawPool(map,map.referenceSolution);
 const save=fresh();Object.keys(save.levels).forEach(k=>save.levels[k]=3);
 const run:Run={chapter:map.chapter,layer:0,teams:[['shield','sword','sword']],brush:'quill',xp:0,level:0,coins:0,goldInk:0,buffs:{},extras:[0,0,0,0,0,0],nextHp:1,bonus:false,picks:0,maps:[],earned:0};
 const b=new Battle(map,pool,run,save),start=b.bosses[0].maxHp;
 for(let i=0;i<C.battleTimeoutSec*60&&!b.result;i++)b.step(1/60);
 assert.ok(b.bosses[0].hp<start*.5||b.result==='win',`boss hp ${Math.round(b.bosses[0].hp)}/${start}, result ${b.result}`);
});
