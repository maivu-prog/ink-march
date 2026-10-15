import * as T from 'three';
/** A fixed particle pool: combat feedback never allocates geometry in a frame. */
export class BattleJuice {
 private geometry=new T.IcosahedronGeometry(1,0);
 private particles:{mesh:T.Mesh<T.IcosahedronGeometry,T.MeshBasicMaterial>;velocity:T.Vector3;life:number;duration:number;size:number}[]=[];
 private cursor=0;private serial=0;
 constructor(parent:T.Group){for(let i=0;i<96;i++){const mesh=new T.Mesh(this.geometry,new T.MeshBasicMaterial({color:0xffe1a0,transparent:true,depthWrite:false}));mesh.visible=false;parent.add(mesh);this.particles.push({mesh,velocity:new T.Vector3(),life:0,duration:1,size:1});}}
 burst(x:number,y:number,z:number,kind:'hit'|'dust'|'loot'|'break'){
  const count=kind==='break'?18:kind==='loot'?12:kind==='dust'?2:5;
  for(let i=0;i<count;i++){const p=this.particles[this.cursor++%this.particles.length],a=(++this.serial*2.39996),speed=kind==='dust'?9:20+(i%4)*12;
   p.duration=p.life=kind==='dust'?.38:kind==='break'?.8:.42+(i%3)*.08;p.size=kind==='dust'?3:kind==='break'?5:3;
   p.mesh.position.set(x,y,z);p.velocity.set(Math.cos(a)*speed,kind==='dust'?8:28+(i%4)*13,Math.sin(a)*speed);p.mesh.material.color.setHex(kind==='loot'?0xffd56d:kind==='hit'?i%2?0xfff8dc:0xffc579:kind==='break'?0xc9a87a:0xdee0b0);p.mesh.material.opacity=1;p.mesh.visible=true;
  }
 }
 update(dt:number){for(const p of this.particles){if(p.life<=0)continue;p.life-=dt;if(p.life<=0){p.mesh.visible=false;continue;}p.velocity.y-=85*dt;p.mesh.position.addScaledVector(p.velocity,dt);p.mesh.rotation.x+=dt*4;p.mesh.rotation.z+=dt*3;const k=p.life/p.duration;p.mesh.scale.setScalar(p.size*(.35+k*.65));p.mesh.material.opacity=Math.min(1,k*2);}}
 reset(){for(const p of this.particles){p.life=0;p.mesh.visible=false;}}
}
