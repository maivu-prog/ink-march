import * as T from 'three';
import type {P} from './systems';
import {brushInkParticles} from './brush-ink';
/** A fixed particle budget shared by Epic and Legendary strokes. */
export class BrushFieldInk{
 readonly mesh:T.InstancedMesh;private paths:P[][]=[];private id='quill';private dummy=new T.Object3D();private color=new T.Color();
 constructor(parent:T.Group){this.mesh=new T.InstancedMesh(new T.IcosahedronGeometry(1,0),new T.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.8,depthWrite:false,blending:T.AdditiveBlending}),72);this.mesh.count=0;this.mesh.frustumCulled=false;this.mesh.instanceMatrix.setUsage(T.DynamicDrawUsage);parent.add(this.mesh);}
 setPaths(paths:P[][],id:string){this.paths=paths;this.id=id;}
 reset(){this.paths=[];this.mesh.count=0;}
 update(time:number,elevation:(p:P)=>number,reduced=false){
  let count=0;if(!reduced)for(const path of this.paths)for(const p of brushInkParticles(this.id,path,time,2)){
   if(count>=72)break;
   const size=p.size*Math.sqrt(p.alpha);
   this.dummy.position.set(p.x,elevation(p)+5+p.rise,p.y);this.dummy.scale.set(size*.7,size*(this.id==='phoenix'?1.5:1),size*.7);this.dummy.rotation.z=Math.sin(time+p.x)*.4;this.dummy.updateMatrix();this.mesh.setMatrixAt(count,this.dummy.matrix);this.color.set(p.color);this.mesh.setColorAt(count,this.color);count++;
  }
  this.mesh.count=count;this.mesh.instanceMatrix.needsUpdate=true;if(this.mesh.instanceColor)this.mesh.instanceColor.needsUpdate=true;
 }
}
