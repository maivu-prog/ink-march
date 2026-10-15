import {along,length,type P} from './systems';
import {brushImageTip} from './brush3d';
import {brushStrokeStyle,drawBrushInk} from './brush-ink';
/** A cosmetic sample anchored to the actual nib in the centered brush portrait. */
export function bindBrushSwatch(canvas:HTMLCanvasElement,blocked:()=>boolean,signal:AbortSignal){
 const ctx=canvas.getContext('2d')!,motion=matchMedia('(prefers-reduced-motion: reduce)');
 let id='quill',born=0,frame=0,active=false,w=0,h=0,ratio=1,points:P[]=[];
 const route=()=>{
  const nib=brushImageTip(id),size=Math.min(w*.52,h),sx=w*.5+(nib.x-.5)*size,sy=Math.min(h-9,h*.5+(nib.y-.5)*size+2),span=Math.min(180,w*.42),amp=Math.min(30,Math.max(5,h-sy-8));
  const out:P[]=[],bezier=(a:P,b:P,c:P,d:P)=>{for(let i=0;i<=30;i++){const t=i/30,u=1-t;out.push({x:u*u*u*a.x+3*u*u*t*b.x+3*u*t*t*c.x+t*t*t*d.x,y:u*u*u*a.y+3*u*u*t*b.y+3*u*t*t*c.y+t*t*t*d.y});}};
  const bend={x:sx-span*.3,y:sy+amp*.85};
  bezier({x:sx,y:sy},{x:sx-span*.32,y:sy-amp*.1},{x:sx-span*.62,y:sy+amp*.75},bend);
  bezier(bend,{x:sx-span*.06,y:sy+amp*1.1},{x:sx+span*.3,y:sy-amp*.2},{x:sx+span*.65,y:sy+amp*.5});
  points=out;
 };
 const measure=()=>{const r=canvas.getBoundingClientRect();w=r.width;h=r.height;ratio=Math.min(devicePixelRatio,2);canvas.width=Math.round(w*ratio);canvas.height=Math.round(h*ratio);route();};
 const paint=(ms:number)=>{
  frame=0;if(!active||!canvas.isConnected||signal.aborted||document.hidden||blocked())return;
  ctx.setTransform(ratio,0,0,ratio,0,0);ctx.clearRect(0,0,w,h);
  const progress=motion.matches?1:Math.min(1,Math.max(0,(ms-born)/600)),distance=length(points)*progress;
  let walked=0;const visible:P[]=[];
  for(let i=0;i<points.length;i++){if(i)walked+=Math.hypot(points[i].x-points[i-1].x,points[i].y-points[i-1].y);if(walked>distance)break;visible.push(points[i]);}
  if(progress<1)visible.push(along(points,distance));
  drawBrushInk(ctx,id,visible,Math.max(7,Math.min(10,w*.023)),ms/1000,motion.matches);
  canvas.dataset.inkState=progress===1?'ready':'drawing';
  if(!motion.matches&&(progress<1||brushStrokeStyle(id).animated))frame=requestAnimationFrame(paint);
 };
 const request=()=>{if(!frame&&active&&!signal.aborted)frame=requestAnimationFrame(paint);};
 const clear=()=>{cancelAnimationFrame(frame);frame=0;active=false;canvas.dataset.inkState='empty';ctx.clearRect(0,0,canvas.width,canvas.height);};
 const observer=new ResizeObserver(()=>{measure();request();});observer.observe(canvas);
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)request();},{signal});
 signal.addEventListener('abort',()=>{clear();observer.disconnect();},{once:true});
 return {clear,reveal:(brush:string)=>{clear();id=brush;born=performance.now();active=true;measure();request();}};
}
