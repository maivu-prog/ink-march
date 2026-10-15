import {test} from 'node:test';
import assert from 'node:assert/strict';
import {Battle,InkPool,maps,fresh,dist,inside,type MapData,type Run} from '../src/systems';
import {battleLayout,bossTell} from '../src/battle-view';
const run=():Run=>({chapter:1,layer:0,teams:[['shield','sword','archer'],['shield','sword','archer']],brush:'quill',xp:0,level:0,coins:0,goldInk:0,buffs:{},extras:[0,0,0,0,0,0],nextHp:1,bonus:false,picks:0,maps:[],earned:0});
function fixture(extra:Partial<MapData>={}){const map:MapData={...maps.c1_s1,field:undefined,starts:[{x:360,y:900}],bosses:[{type:'goblin_king',x:360,y:120,scale:.6}],camps:[],enemySquads:[],items:[],obstacles:[],terrain:[],goldZones:[],baseInk:3000,...extra},pool=new InkPool(map);pool.paths[0].add(map.starts[0]);pool.paths[0].add(map.bosses[0]);return new Battle(map,pool,run(),fresh());}
test('display formation spreads an overlapping squad without changing simulation state',()=>{const b=fixture(),friends=b.soldiers.filter(s=>s.team===0);friends.forEach(s=>{s.x=360;s.y=500;});const snapshot=JSON.stringify(b.soldiers),layout=battleLayout(b);assert.equal(JSON.stringify(b.soldiers),snapshot);assert.ok(friends.some(s=>dist(s,layout.get(s.id)!)>10));for(const s of friends)assert.ok(dist(s,layout.get(s.id)!)<=44.01);});
test('cosmetic offsets respect walls and a ravine without a golden bridge',()=>{for(const obstacle of [{type:'circle',x:395,y:500,r:18},{type:'rect',kind:'chasm',x:375,y:470,w:50,h:60}]){const b=fixture({obstacles:[obstacle]}),friends=b.soldiers.filter(s=>s.team===0);friends.forEach((s,i)=>{s.x=360;s.y=500+(i%2)*4;});const layout=battleLayout(b);for(const s of friends)assert.equal(inside(layout.get(s.id)!,obstacle),false);}});
test('actual strike and hit cues carry the same source and target as combat damage',()=>{const b=fixture();b.fight[0]=true;const s=b.soldiers.find(s=>s.type==='sword')!;for(const p of b.soldiers.filter(p=>!p.team)){p.x=360;p.y=150;p.cool=100;}s.cool=0;b.boss.cool=100;b.step(1/60);const strike=b.cues.find(c=>c.kind==='strike'&&c.source===s.id)!,hit=b.cues.find(c=>c.kind==='hit'&&c.source===s.id)!;assert.ok(strike&&hit);assert.equal(strike.target,b.boss.id);assert.equal(s.target,b.boss.id);assert.equal(hit.target,strike.target);assert.ok(hit.amount!>0);assert.ok(strike.id<hit.id);});
test('boss warning is absent while dormant and anticipates the actual skill clock',()=>{const b=fixture();b.bossState[0].skill=5.6;assert.equal(bossTell(b,b.boss),null);b.fight[0]=true;for(const s of b.soldiers.filter(s=>!s.team)){s.x=360;s.y=165;s.cool=100;}assert.ok(bossTell(b,b.boss)!.skill>.4);b.step(.5);assert.ok(b.cues.some(c=>c.kind==='skill'&&c.style==='stomp'&&c.source===b.boss.id));assert.equal(bossTell(b,b.boss)!.skill,0);});
test('event history stays bounded over a long fight',()=>{const b=fixture(),target=b.boss;target.hp=target.maxHp=1e9;for(let i=0;i<600;i++)b.damage(target,1);assert.equal(b.cues.length,128);assert.ok(b.cues.every((c,i,a)=>!i||c.id>a[i-1].id));});

test('display separation cannot push a soldier through a closed gate',()=>{const gate={type:'gate',color:'red',x:390,y:500,rect:{x:375,y:470,w:40,h:60}},b=fixture({items:[gate]});b.soldiers.filter(s=>!s.team).forEach(s=>{s.x=360;s.y=500;});const layout=battleLayout(b);for(const s of b.soldiers.filter(s=>!s.team))assert.equal(inside(layout.get(s.id)!,gate),false);});

test('forecast can disable presentation cues without changing a battle outcome',()=>{const shown=fixture(),forecast=fixture();forecast.captureCues=false;for(let i=0;i<1800;i++){shown.step(1/60);forecast.step(1/60);}assert.equal(forecast.cues.length,0);assert.ok(shown.cues.length>0);assert.deepEqual(forecast.soldiers,shown.soldiers);assert.equal(forecast.result,shown.result);assert.equal(forecast.time,shown.time);});

test('reinforcement feedback reports actual stat gains once and expires',()=>{
 const b=fixture(),atk=b.boss.atk,hp=b.boss.hp,max=b.boss.maxHp;
 b.enrage(0);
 const pops=b.effects.filter(e=>e.kind==='reinforcement');
 assert.equal(pops.length,1);
 assert.equal(pops[0].text,'+'+Math.round(b.boss.atk-atk)+' ATK · +'+Math.round(b.boss.maxHp-max)+' HP');
 assert.ok(b.boss.atk>atk);assert.equal(b.boss.hp-hp,b.boss.maxHp-max);
 assert.equal(b.effects.some(e=>e.text.includes('ENRAGED')),false);
 for(let i=0;i<150;i++)b.step(1/60);
 assert.equal(b.effects.filter(e=>e.kind==='reinforcement').length,0);
});
test('a fallen boss cannot receive a reinforcement stat popup',()=>{const b=fixture();b.boss.hp=0;b.enrage(0);assert.equal(b.effects.filter(e=>e.kind==='reinforcement').length,0);});
