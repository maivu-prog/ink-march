import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
for(const type of ['goblin_king','goblin_archer','orc','shaman','shadow_mage','tower','tree','rock'])test(`${type}: enemy bean set has mobile geometry, embedded 512 atlas and valid animation data`,()=>{
 const b=readFileSync(new URL(`../public/assets/models/bean-v3/${type}.glb`,import.meta.url));
 assert.equal(b.readUInt32LE(0),0x46546c67);assert.equal(b.readUInt32LE(4),2);assert.equal(b.length,b.readUInt32LE(8));
 const jsonLength=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+jsonLength).toString());
 const triangles=j.meshes.reduce((sum:number,m:any)=>sum+m.primitives.reduce((n:number,p:any)=>n+j.accessors[p.indices].count/3,0),0);
 assert.ok(triangles<3000,`${triangles} triangles`);assert.ok(j.meshes.length<=10);assert.equal(j.materials.length,1);assert.equal(j.images.length,1);
 const image=j.images[0];assert.equal(image.uri,undefined);assert.equal(image.mimeType,'image/png');
 const view=j.bufferViews[image.bufferView],data=b.subarray(20+jsonLength+8+view.byteOffset,20+jsonLength+8+view.byteOffset+view.byteLength);
 assert.equal(data.readUInt32BE(16),512);assert.equal(data.readUInt32BE(20),512);
 for(const name of (['tower','tree','rock'].includes(type)?[]:['Idle','Walk','Attack','Death'])){const clip=j.animations.find((a:any)=>a.name===name);assert.ok(clip?.channels.length);assert.ok(clip.samplers.some((s:any)=>j.accessors[s.input].count>1));
 const channels=clip.channels.map((c:any)=>`${c.target.node}:${c.target.path}`);assert.equal(new Set(channels).size,channels.length,'No duplicate transform channels');}
 const portrait=readFileSync(new URL(`../public/assets/portraits/bean-v3/${type}.png`,import.meta.url));assert.equal(portrait.readUInt32BE(16),512);assert.equal(portrait.readUInt32BE(20),512);
});



