import * as T from 'three';
import {BR} from './systems';
/** Rounded toy tools. Tip at y=0; broad faces look toward +Z. */
export function makeBrush(id:string):T.Group{
 const spec=BR[id]||BR.quill,l=spec.look,g=new T.Group(),materials=new Map<string,T.MeshStandardMaterial>();
 const material=(color:string,glow=false)=>{const key=color+glow;let m=materials.get(key);if(!m){m=new T.MeshStandardMaterial({color,roughness:.72,metalness:0,emissive:glow?color:0x000000,emissiveIntensity:glow?.13:0});materials.set(key,m);}return m;};
 const add=(geo:T.BufferGeometry,c:string,x=0,y=0,z=0,glow=false)=>{const m=new T.Mesh(geo,material(c,glow));m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;g.add(m);return m;};
 const ball=(x:number,y:number,z:number,rx:number,ry:number,rz:number,c:string)=>{const m=add(new T.SphereGeometry(1,18,12),c,x,y,z);m.scale.set(rx,ry,rz);return m;};
 const lathe=(profile:number[][],c:string,y=0,segments=24)=>add(new T.LatheGeometry(profile.map(([r,h])=>new T.Vector2(r,h)),segments),c,0,y);
 const ring=(y:number,r:number,c=l.b,thick=2)=>{const m=add(new T.TorusGeometry(r,thick,8,28),c,0,y);m.rotation.x=Math.PI/2;return m;};
 const rounded=(w:number,h:number,d:number,r:number,c:string,x:number,y:number,z=0)=>{const s=new T.Shape();s.moveTo(-w/2+r,-h/2);s.lineTo(w/2-r,-h/2);s.quadraticCurveTo(w/2,-h/2,w/2,-h/2+r);s.lineTo(w/2,h/2-r);s.quadraticCurveTo(w/2,h/2,w/2-r,h/2);s.lineTo(-w/2+r,h/2);s.quadraticCurveTo(-w/2,h/2,-w/2,h/2-r);s.lineTo(-w/2,-h/2+r);s.quadraticCurveTo(-w/2,-h/2,-w/2+r,-h/2);const geo=new T.ExtrudeGeometry(s,{depth:d,bevelEnabled:true,bevelSize:1.3,bevelThickness:1.3,bevelSegments:3,steps:1,curveSegments:5});geo.translate(0,0,-d/2);return add(geo,c,x,y,z);};
 const handle=(y:number,h:number,r:number,c=l.a)=>{lathe([[0,0],[r*.78,1],[r,7],[r*.96,h*.34],[r*.85,h*.73],[r*.69,h-3],[0,h]],c,y);ring(y+8,r*.99,l.b,1.6);ball(-r*.45,y+h*.46,r*.79,1.7,h*.18,1.0,new T.Color(c).lerp(new T.Color('#ffffff'),.3).getStyle());};
 const nib=(c:string)=>{const shape=new T.Shape();shape.moveTo(0,0);shape.quadraticCurveTo(-3,8,-11,22);shape.quadraticCurveTo(0,34,11,22);shape.quadraticCurveTo(3,8,0,0);const geo=new T.ExtrudeGeometry(shape,{depth:5,bevelEnabled:true,bevelSize:1,bevelThickness:1,bevelSegments:2});geo.translate(0,0,-2.5);add(geo,c);rounded(1.3,13,1,.5,'#38545a',0,15,3.9);ball(0,23,4.1,2.3,2.3,1,'#38545a');};
 if(l.shape==='quill'){
  nib(id==='phoenix'?'#edbc60':'#bd9b63');handle(24,25,8.5,l.b==='#3a3a3a'?'#557e8b':l.b);
  const feather=new T.Shape();feather.moveTo(0,32);feather.bezierCurveTo(-22,44,-39,62,-31,81);feather.lineTo(-22,78);feather.bezierCurveTo(-32,99,-24,119,-9,139);feather.quadraticCurveTo(22,133,32,115);feather.lineTo(18,117);feather.quadraticCurveTo(37,98,31,81);feather.lineTo(20,84);feather.quadraticCurveTo(28,57,0,32);
  const geo=new T.ExtrudeGeometry(feather,{depth:6,bevelEnabled:true,bevelSize:2,bevelThickness:2,bevelSegments:3,curveSegments:12});geo.translate(0,0,-3);add(geo,l.a,0,0,1,!!l.glow);
  const spine=add(new T.CapsuleGeometry(2.1,88,4,10),id==='phoenix'?'#ffcd66':id==='golden'?'#fff2bf':'#d7c9aa',0,86,6.7);spine.rotation.z=-.05;
  for(let side of [-1,1])for(let i=0;i<3;i++){const m=rounded(16,2,1,.8,new T.Color(l.a).lerp(new T.Color(l.b),.25).getStyle(),side*(9+i*1.4),66+i*18,6.7);m.rotation.z=side*.58;}
 }else if(l.shape==='brush'){
  lathe([[0,0],[8,3],[15,12],[20,27],[19,39],[14,48]],l.c);lathe([[0,-.2],[8,2.8],[15.2,11.7],[18.2,19]],l.p);lathe([[14,0],[16,3],[16,15],[13.5,18]],l.b,45);ring(48,16);ring(60,15);handle(63,77,14);
  // A large material emblem gives the family a recognizable silhouette.
  if(['reed','marsh','willow'].includes(id)){const leaf=ball(13,104,3,5,14,3,id==='marsh'?'#a7ba75':l.p);leaf.rotation.z=-.7;}
  if(id==='trail'){ring(91,14.8,'#9aa6a8');ring(115,13.8,'#9aa6a8');ball(0,103,13,6,7,2,l.p);}
 }else if(l.shape==='flat'){
  rounded(45,38,13,5,l.c,0,22);rounded(46,14,14,4,l.p,0,9);rounded(48,20,17,4,l.b,0,50);handle(60,78,13);for(let i=-2;i<=2;i++)rounded(1,20,1,.4,'#e2d2ae',i*7,29,8);
 }else if(l.shape==='pen'){
  nib(l.b);lathe([[10,0],[13,6],[14,23],[14,73],[12,92],[0,95]],l.a,25);ring(32,13,l.b);ring(107,13,l.b,2.5);const clip=rounded(5,44,4,2,l.b,16,89,6);clip.rotation.z=-.04;ball(16,66,6,4,4,3,l.b);ball(0,120,0,8,7,8,l.b);
 }else{
  lathe([[0,0],[7,5],[16,16],[17,29],[17,105],[14,116],[0,118]],l.a,0,8);lathe([[17.3,0],[18,2],[18,32],[17.2,35]],'#d4c9ae',62,8);ring(64,17.5,'#afa389',1.1);ring(94,17.5,'#afa389',1.1);ball(0,80,18,8,9,1.7,'#496b70');
 }
 // Small paint beads belong to the tip, not a halo of floating weapons.
 ball(11,4,4,4.3,5.8,4.1,l.p);if(['epic','legendary'].includes(spec.rarity)){ring(l.shape==='quill'?47:64,l.shape==='quill'?10:16,'#e9bf64',2.5);ball(-18,31,5,3.5,4.5,3.5,l.p);g.userData.splash=true;}
 const holder=new T.Group();holder.add(g);holder.userData.brush=id;holder.userData.inner=g;holder.userData.dispose=()=>disposeBrush(holder);return holder;
}
export function disposeBrush(g:T.Group){const geometry=new Set<T.BufferGeometry>(),materials=new Set<T.Material>();g.traverse(o=>{if(o instanceof T.Mesh){geometry.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m);}});geometry.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());}
let shot:{renderer:T.WebGLRenderer;scene:T.Scene;camera:T.OrthographicCamera}|null=null;const images=new Map<string,string>();
/** Auto-framed front view keeps feathers broad and every tip inside the portrait. */
export function brushImage(id:string){const cached=images.get(id);if(cached)return cached;try{if(!shot){const renderer=new T.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});renderer.setSize(384,384,false);renderer.setPixelRatio(1);renderer.setClearColor(0,0);const scene=new T.Scene();scene.add(new T.HemisphereLight(0xfff7df,0x6a8a91,2));const key=new T.DirectionalLight(0xffffff,2.6);key.position.set(-120,180,250);scene.add(key);const camera=new T.OrthographicCamera(-110,110,110,-110,1,1000);camera.position.set(0,0,400);camera.lookAt(0,0,0);shot={renderer,scene,camera};}const tool=makeBrush(id);tool.rotation.set(-.04,.13,-.58);tool.updateMatrixWorld(true);const bounds=new T.Box3().setFromObject(tool),size=bounds.getSize(new T.Vector3()),center=bounds.getCenter(new T.Vector3());tool.position.sub(center);const half=Math.max(size.x,size.y)*.59;shot.camera.left=shot.camera.bottom=-half;shot.camera.right=shot.camera.top=half;shot.camera.updateProjectionMatrix();shot.scene.add(tool);shot.renderer.render(shot.scene,shot.camera);const url=shot.renderer.domElement.toDataURL('image/png');shot.scene.remove(tool);disposeBrush(tool);images.set(id,url);return url;}catch{return '';}}
