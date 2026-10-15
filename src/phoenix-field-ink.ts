import * as T from 'three';
import type {P} from './systems';
import {phoenixEmbers} from './phoenix-ink';
/** A fixed pool of decorative particles, separate from path validity and combat. */
export class PhoenixFieldInk{
 readonly mesh:T.InstancedMesh;private paths:P[][]=[];private dummy=new T.Object3D();private color=new T.Color();
 constructor(parent:T.Group){
  this.mesh=new T.InstancedMesh(new T.IcosahedronGeometry(1,0),new T.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.9,depthWrite:false,blending:T.AdditiveBlending}),72);
  this.mesh.count=0;this.mesh.frustumCulled=false;this.mesh.instanceMatrix.setUsage(T.DynamicDrawUsage);parent.add(this.mesh);
 }
 setPaths(paths:P[][]){this.paths=paths;}
 reset(){this.paths=[];this.mesh.count=0;}
 update(time:number,elevation:(p:P)=>number,reduced=false){
  let count=0;
  if(!reduced)for(const path of this.paths)for(const p of phoenixEmbers(path,time,2)){
   if(count>=72)break;
   this.dummy.position.set(p.x,elevation(p)+5+p.rise,p.y);this.dummy.scale.set(p.size*.65,p.size*1.5,p.size*.65);this.dummy.rotation.z=Math.sin(time+p.x)*.4;this.dummy.updateMatrix();
   this.mesh.setMatrixAt(count,this.dummy.matrix);this.color.set(p.heat>.5?0xffef9a:0xff7938);this.mesh.setColorAt(count,this.color);count++;
  }
  this.mesh.count=count;this.mesh.instanceMatrix.needsUpdate=true;if(this.mesh.instanceColor)this.mesh.instanceColor.needsUpdate=true;
 }
}
