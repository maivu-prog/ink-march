import {BR,U} from './systems';
import {brushImage} from './brush3d';
import {bindBrushSwatch} from './brush-swatch';
const featured=['phoenix','golden','willow','trail','swift','atlas','broad','marsh','feather','charcoal','reed','quill'];
const effects:Record<string,string>={quill:'A clean, steady line',reed:'40% less ink on sand',charcoal:'8% less ink',feather:'Collect charms from farther away',marsh:'50% less ink in swamps',broad:'Extra reach for collecting charms',swift:'Troops march 15% faster',atlas:'60% less ink on roads',golden:'20% less ink',willow:'Heal 1.5% HP every second',trail:'Terrain penalties reduced by 50%',phoenix:'25% less ink · Heal 1% HP/s'};
const troops=['sword','archer','shield','spear','mage','healer'];
const troopEffects:Record<string,string>={sword:'Frontline fighter · Fast sword strikes',archer:'Ranged attacker · Fires from afar',shield:'Tank · Shields your frontline',spear:'Long reach · Strikes behind the front',mage:'Ranged attacker · Powerful spell strikes',healer:'Support · Heals nearby allies'};
let focus=0,troopFocus=0;

function slot(index:number){let d=(index-focus+featured.length)%featured.length;return d>featured.length/2?d-featured.length:d;}
export function summonBrushCarousel(){return '<section class="summon-carousel" aria-label="Brush showcase" aria-roledescription="carousel"><h2 class="summon-brush-name">'+BR[featured[focus]].name+'</h2><div class="summon-brush-track">'+featured.map((id,i)=>'<button type="button" class="summon-brush-slide" data-brush-index="'+i+'" style="--slot:'+slot(i)+';--scale:'+(i===focus?1:.62)+';opacity:'+(Math.abs(slot(i))<=1?1:0)+'" tabindex="'+(Math.abs(slot(i))<=1?0:-1)+'" aria-hidden="'+(Math.abs(slot(i))>1)+'" aria-label="Preview '+BR[id].name+'"><img draggable="false" src="'+brushImage(id)+'" alt=""></button>').join('')+'<canvas class="summon-ink-swatch" aria-hidden="true"></canvas></div><p class="summon-brush-effect">'+effects[featured[focus]]+'</p></section>';}
/** Keep animation local to the banner; dispose it whenever the menu is rebuilt. */
export function bindSummonCarousel(host:HTMLElement,blocked:()=>boolean){
 const root=host.querySelector<HTMLElement>('.summon-carousel');if(!root)return ()=>{};
 const troop=root.dataset.kind==='troop',items=troop?troops:featured;
 const current=()=>troop?troopFocus:focus;
 const distance=(i:number)=>{let d=(i-current()+items.length)%items.length;return d>items.length/2?d-items.length:d;};
 const controller=new AbortController(),signal=controller.signal,motion=matchMedia('(prefers-reduced-motion: reduce)');
 const swatchCanvas=root.querySelector<HTMLCanvasElement>('.summon-ink-swatch'),swatch=swatchCanvas?bindBrushSwatch(swatchCanvas,blocked,signal):null;
 const slides=Array.from(root.querySelectorAll<HTMLButtonElement>('.summon-brush-slide'));
 let nextAt=performance.now()+2800,startX:number|null=null,suppressClickUntil=0,captionTimer=0,initialized=false;
 const show=(index:number)=>{
  swatch?.clear();
  if(troop)troopFocus=(index+items.length)%items.length;else focus=(index+items.length)%items.length;
  slides.forEach((el,i)=>{const d=distance(i),visible=Math.abs(d)<=1;el.style.setProperty('--slot',String(d));el.style.setProperty('--scale',i===current()?'1':'.62');el.style.opacity=visible?'1':'0';el.style.zIndex=i===current()?'3':visible?'2':'0';el.tabIndex=visible?0:-1;el.setAttribute('aria-hidden',String(!visible));el.classList.toggle('is-center',i===current());});
  const captions=()=>{root.querySelector('.summon-brush-name')!.textContent=(troop?U:BR)[items[current()]].name;root.querySelector('.summon-brush-effect')!.textContent=(troop?troopEffects:effects)[items[current()]];root.classList.remove('is-sliding');swatch?.reveal(items[current()]);};
  window.clearTimeout(captionTimer);
  if(initialized&&!motion.matches){root.classList.add('is-sliding');captionTimer=window.setTimeout(captions,650);}else captions();initialized=true;
 };
 show(current());
 root.addEventListener('click',e=>{if(performance.now()<suppressClickUntil)return;const button=(e.target as Element).closest<HTMLButtonElement>('[data-brush-index]');if(!button)return;show(Number(button.dataset.brushIndex));nextAt=performance.now()+4500;},{signal});
 root.addEventListener('keydown',e=>{if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;e.preventDefault();show(current()+(e.key==='ArrowRight'?1:-1));nextAt=performance.now()+4500;},{signal});
 root.addEventListener('pointerdown',e=>{startX=e.clientX;},{signal});
 root.addEventListener('pointerup',e=>{if(startX!==null&&Math.abs(e.clientX-startX)>35){suppressClickUntil=performance.now()+400;show(current()+(e.clientX<startX?1:-1));nextAt=performance.now()+4500;}startX=null;},{signal});
 root.addEventListener('pointercancel',()=>{startX=null;},{signal});
 const timer=window.setInterval(()=>{if(!root.isConnected){window.clearInterval(timer);window.clearTimeout(captionTimer);controller.abort();return;}if(document.hidden||blocked()||motion.matches||startX!==null){nextAt=performance.now()+2800;return;}if(performance.now()>=nextAt){show(current()+1);nextAt=performance.now()+2800;}},200);
 return ()=>{window.clearInterval(timer);window.clearTimeout(captionTimer);controller.abort();};
}

export function summonTroopCarousel(portrait:(id:string)=>string){
 const offset=(i:number)=>{let d=(i-troopFocus+troops.length)%troops.length;return d>troops.length/2?d-troops.length:d;};
 return '<section class="summon-carousel summon-troop-carousel" data-kind="troop" aria-label="Troop showcase" aria-roledescription="carousel"><h2 class="summon-brush-name">'+U[troops[troopFocus]].name+'</h2><div class="summon-brush-track">'+troops.map((id,i)=>'<button type="button" class="summon-brush-slide" data-brush-index="'+i+'" style="--slot:'+offset(i)+';--scale:'+(i===troopFocus?1:.62)+';opacity:'+(Math.abs(offset(i))<=1?1:0)+'" tabindex="'+(Math.abs(offset(i))<=1?0:-1)+'" aria-hidden="'+(Math.abs(offset(i))>1)+'" aria-label="Preview '+U[id].name+'"><img draggable="false" src="'+portrait(id)+'" alt=""></button>').join('')+'</div><p class="summon-brush-effect">'+troopEffects[troops[troopFocus]]+'</p></section>';
}
