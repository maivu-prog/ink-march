import * as T from 'three';
import {BR} from './systems';
// Toon 3 mảng màu + viền đen kiểu "vỏ lộn ngược" để brush trông như hoạt hình
const ramp=(()=>{const data=new Uint8Array([90,90,90,255,175,175,175,255,255,255,255,255]);const t=new T.DataTexture(data,3,1,T.RGBAFormat);t.minFilter=t.magFilter=T.NearestFilter;t.needsUpdate=true;return t;})();
const ink=new T.MeshBasicMaterial({color:0x1b1d24,side:T.BackSide});
const toon=(c:string,glow?:string)=>new T.MeshToonMaterial({color:new T.Color(c),gradientMap:ramp,emissive:glow?new T.Color(glow):new T.Color(0),emissiveIntensity:glow?.35:0});
const lathe=(profile:number[][],seg=20)=>new T.LatheGeometry(profile.map(([r,y])=>new T.Vector2(r,y)),seg);
function part(g:T.Group,geo:T.BufferGeometry,color:string,pos:[number,number,number]=[0,0,0],outline=1.6,glow?:string){
 const m=new T.Mesh(geo,toon(color,glow));m.position.set(...pos);m.castShadow=true;g.add(m);
 if(outline){geo.computeBoundingSphere();const r=geo.boundingSphere!.radius||1,o=new T.Mesh(geo,ink),k=1+outline/Math.max(6,r*.55);o.scale.setScalar(k);o.position.copy(m.position);o.position.y+=geo.boundingSphere!.center.y*(1-k);g.add(o);}return m;}
function shine(g:T.Group,y:number,r:number){const s=new T.Mesh(new T.CapsuleGeometry(r*.12,r*1.6,4,8),new T.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.55}));s.position.set(-r*.55,y,r*.62);s.rotation.z=.12;g.add(s);}
// Gốc toạ độ là đầu lông/ngòi, cán hướng lên +Y
export function makeBrush(id:string):T.Group{const look=BR[id]?.look||BR.quill.look,g=new T.Group(),glow=look.glow;
 const handleRound=(y0:number,r0:number,len:number,wide:number)=>{part(g,lathe([[r0,0],[wide*.9,len*.18],[wide,len*.45],[wide*.85,len*.75],[wide*.45,len*.95],[0,len]]),look.a,[0,y0,0],1.8,glow);shine(g,y0+len*.45,wide);};
 const ferrule=(y0:number,r:number,h:number)=>{part(g,new T.CylinderGeometry(r,r*1.05,h,20),look.b,[0,y0+h/2,0],1.4);for(const k of [.28,.72]){let ring=new T.Mesh(new T.TorusGeometry(r*1.04,1.1,8,24),toon('#ffffff'));ring.rotation.x=Math.PI/2;ring.position.y=y0+h*k;ring.material.color.set(look.b).offsetHSL(0,0,.18);g.add(ring);}};
 const drip=(x:number)=>{part(g,new T.SphereGeometry(4.2,14,10),look.p,[x,-6,2],1.2);part(g,new T.CylinderGeometry(1.6,3,8,10),look.p,[x,-1,2],0);};
 if(look.shape==='brush'){const tuft=[[0,0],[6,3],[11,10],[14,22],[14.5,32],[12.5,42],[10,48]];part(g,lathe(tuft),look.c,[0,0,0],1.8,glow);part(g,lathe([[0,-.6],[6.6,2.6],[11.7,9.6],[13.8,16]]),look.p,[0,0,0],0,glow);drip(5);ferrule(47,10.5,15);handleRound(62,10,105,12.5);}
 else if(look.shape==='flat'){const bristle=part(g,new T.BoxGeometry(34,40,11,1,1,1),look.c,[0,22,0],1.6);bristle.geometry.translate(0,0,0);part(g,new T.BoxGeometry(35,12,12),look.p,[0,6,0],0);drip(-8);part(g,new T.BoxGeometry(36,16,14),look.b,[0,49,0],1.4);handleRound(57,7,105,10);}
 else if(look.shape==='pen'){part(g,lathe([[0,0],[3,6],[6.5,16],[7.5,22]]),look.b,[0,0,0],1.4);part(g,new T.CylinderGeometry(9,7.5,14,20),look.b,[0,29,0],1.4);part(g,lathe([[9,0],[10.5,30],[10.5,80],[9,96],[0,100]]),look.a,[0,36,0],1.8,glow);shine(g,80,10.5);part(g,new T.BoxGeometry(3,52,4),look.b,[11,96,0],1);drip(2);}
 else if(look.shape==='stick'){part(g,lathe([[0,0],[5,6],[10,18],[11,30],[12,90],[11,118],[8,124],[0,126]],7),look.a,[0,0,0],1.8);part(g,new T.CylinderGeometry(12.6,12.6,22,7),look.b,[0,100,0],1.4);shine(g,60,11);}
 else{part(g,lathe([[0,0],[2.5,6],[4.5,16]]),'#3a3a40',[0,0,0],1.2);part(g,new T.CylinderGeometry(2.6,3.2,150,10),'#f2ead6',[0,90,0],1.2);
  const vane=new T.Shape();vane.moveTo(0,0);vane.bezierCurveTo(30,22,28,96,6,132);vane.lineTo(0,128);vane.bezierCurveTo(-22,96,-26,22,0,0);
  const geo=new T.ExtrudeGeometry(vane,{depth:3,bevelEnabled:true,bevelThickness:1.5,bevelSize:1.5,bevelSegments:2});geo.translate(0,0,-1.5);
  const f=part(g,geo,look.a,[0,30,0],0,glow);f.rotation.y=Math.PI/2.4;const o=new T.Mesh(geo,ink);o.scale.set(1.05,1.03,1.6);o.position.set(0,28,0);o.rotation.y=Math.PI/2.4;g.add(o);
  for(let i=0;i<5;i++){let notch=new T.Mesh(new T.BoxGeometry(2,1.6,12),new T.MeshBasicMaterial({color:0x1b1d24}));notch.position.set(0,52+i*18,0);notch.rotation.set(0,Math.PI/2.4,.5);g.add(notch);}drip(3);}
 // brush hiếm: vệt sơn bay quanh như ảnh mẫu
 if(['epic','legendary'].includes(BR[id]?.rarity)){for(let i=0;i<(BR[id].rarity==='legendary'?3:2);i++){let blob=part(g,new T.CapsuleGeometry(4.5,26,6,12),i?look.p:(glow||look.p),[0,0,0],1.2);let a=i*2.3+.6;blob.position.set(Math.cos(a)*30,40+i*26,Math.sin(a)*30);blob.rotation.set(.4,a,1.1+i*.4);}g.userData.splash=true;}
 const holder=new T.Group();holder.add(g);holder.userData.brush=id;holder.userData.inner=g;return holder;}

// Ảnh chân dung brush cho UI: render model 3D ra ảnh, lưu cache theo id
let shot:{renderer:T.WebGLRenderer,scene:T.Scene,camera:T.PerspectiveCamera}|null=null;const images=new Map<string,string>();
export function brushImage(id:string){let url=images.get(id);if(url)return url;try{if(!shot){const renderer=new T.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});renderer.setSize(192,192,false);renderer.setClearColor(0,0);const scene=new T.Scene();scene.add(new T.AmbientLight(0xffffff,1.1));let key=new T.DirectionalLight(0xffffff,2.2);key.position.set(-80,160,180);scene.add(key);const camera=new T.PerspectiveCamera(30,1,1,2000);camera.position.set(0,82,300);camera.lookAt(0,82,0);shot={renderer,scene,camera};}
 const brush=makeBrush(id);brush.rotation.set(.15,.35,-.72);brush.position.set(-36,4,0);shot.scene.add(brush);shot.renderer.render(shot.scene,shot.camera);url=shot.renderer.domElement.toDataURL('image/png');shot.scene.remove(brush);images.set(id,url);}catch{url='';}return url;}
