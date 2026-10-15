import {test} from 'node:test';
import assert from 'node:assert/strict';
import {BR} from '../src/systems';
import {buildInkLayers,brushStrokeStyle,brushInkParticles} from '../src/brush-ink';
const path=[{x:20,y:80},{x:90,y:20},{x:180,y:90},{x:290,y:40}];
for(const [id,brush] of Object.entries(BR))test(id+' obeys its rarity visual budget',()=>{
 const before=JSON.stringify(path),style=brushStrokeStyle(id),layers=buildInkLayers(id,path,10);
 assert.equal(style.rarity,brush.rarity);assert.ok(layers.length>0);
 if(brush.rarity==='common'){assert.equal(layers.length,1);assert.equal(layers[0].color,brush.look.p);}
 if(['common','rare'].includes(brush.rarity)){assert.equal(style.animated,false);assert.deepEqual(brushInkParticles(id,path,10),[]);assert.ok(layers.every(l=>!l.pulse&&l.glow===0));}
 else {assert.equal(style.animated,true);assert.ok(layers.some(l=>l.pulse));assert.ok(brushInkParticles(id,path,10).length>0);}
 if(brush.rarity==='epic'){assert.ok(layers.every(l=>l.glow<=.2));assert.ok(brushInkParticles(id,[{x:0,y:0},{x:100000,y:0}],1).length<=8);}
 if(brush.rarity==='legendary')assert.ok(layers.some(l=>l.glow>=1));
 assert.equal(JSON.stringify(path),before);
});
test('all shapes remain finite and bounded for degenerate, sharp and long routes',()=>{
 for(const id of Object.keys(BR))for(const points of [[],[{x:1,y:1}],[{x:1,y:1},{x:1,y:1}],path,[{x:0,y:0},{x:200000,y:0}]]){
  const layers=buildInkLayers(id,points,8);assert.ok(layers.reduce((n,l)=>n+l.polygons.length,0)<6500);
  for(const l of layers)for(const poly of l.polygons)for(const p of poly)assert.ok(Number.isFinite(p.x)&&Number.isFinite(p.y));
 }
});
test('shape spacing does not depend on input event density',()=>{
 const sparse=[{x:0,y:0},{x:200,y:0}],dense=Array.from({length:101},(_,i)=>({x:i*2,y:0}));
 const rounded=(value:unknown)=>JSON.parse(JSON.stringify(value,(_key,v)=>typeof v==='number'?Math.round(v*1e8)/1e8:v));
 for(const id of Object.keys(BR))assert.deepEqual(rounded(buildInkLayers(id,sparse,8)),rounded(buildInkLayers(id,dense,8))); 
});
test('epic and legendary particles are finite and never mutate the route',()=>{
 const before=JSON.stringify(path);for(const id of ['golden','willow','trail','phoenix'])for(const time of [0,.2,50,100000])for(const p of brushInkParticles(id,path,time)){
  assert.ok([p.x,p.y,p.rise,p.size,p.alpha].every(Number.isFinite));assert.ok(p.alpha>=0&&p.alpha<=1);
 }assert.equal(JSON.stringify(path),before);
});
