import {test} from 'node:test';
import assert from 'node:assert/strict';
import {maps,Battle,C,fresh,type Run} from '../src/systems';
import {drawPool} from '../tools/mapTools';
const battle=(id:string)=>{const map={...maps[id],baseInk:99999} as any,save=fresh();Object.keys(save.levels).forEach(k=>save.levels[k]=6);
 const run:Run={chapter:map.chapter,layer:0,teams:[['shield','sword','archer'],['spear','mage','healer']],brush:'quill',xp:0,level:0,coins:0,goldInk:0,buffs:{},extras:[0,0,0,0,0,0],nextHp:1,bonus:false,picks:0,maps:[],earned:0};
 return new Battle(map,drawPool(map,map.referenceSolution),run,save);};
test('Sealbreaker blocks 70% from the front, not from behind',()=>{const b=battle('c1_s4'),boss=b.bosses[0],f=b.bossState[0].facing!;
 const front={x:boss.x+Math.sin(f)*60,y:boss.y+Math.cos(f)*60},back={x:boss.x-Math.sin(f)*60,y:boss.y-Math.cos(f)*60};
 assert.equal(b.blockMul(boss,front),1-.7);assert.equal(b.blockMul(boss,back),1);});
test('Inkpot Ogre spills pools and Crimson Scribe shifts runes during the fight',()=>{
 for(const [id,check] of [['c4_s4',(b:Battle)=>b.bossState.some(s=>(s.pools||[]).length>0)],['c7_s5',(b:Battle)=>b.bossState.some(s=>(s.phase||0)>0)]] as const){const b=battle(id);let ok=false;for(let i=0;i<C.battleTimeoutSec*60&&!b.result&&!ok;i++){b.step(1/60);ok=check(b);}assert.ok(ok,id);}
});
