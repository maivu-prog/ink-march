import type {MapData} from './systems';
export type Page=string|[string,string];
export type LessonStep={id:string;pages:Page[];target?:string;ok?:boolean;guide?:boolean;hold?:boolean;top?:boolean;passive?:boolean;autoHide?:number};
export type FirstLessonState={screen:string;seen:Record<string,boolean>;preparing:boolean;hasPool:boolean;valid:boolean;battling:boolean};
/** Teach the action that is possible now. No acknowledgement gates in the first battle. */
export function firstLesson(s:FirstLessonState):LessonStep|null{
 if(s.screen!=='battle'||s.preparing)return null;
 if(s.battling)return s.seen.ftueBattle?null:{id:'ftueBattle',pages:['Your army fights on its own. Tap ×2 to speed up.'],passive:true,autoHide:4500};
 if(!s.hasPool)return null;
 if(s.valid)return s.seen['f-march']?null:{id:'f-march',pages:['Ready! Tap MARCH to send them in.'],target:'[data-action=start]',passive:true,autoHide:3000};
 return s.seen['f-draw']?null:{id:'f-draw',pages:['Drag from the blue flag to the boss.'],target:'#stage',guide:true,passive:true};
}
export const menuLessons:Record<string,string>={squad:'Tap a squad slot, then a recruit. FRONT takes hits; REAR supports.',upgrade:'Pick a soldier to level up with Gold and cards.',brushes:'Pick a brush to see its effect. Duplicates add stars.',summon:'Brushes cost gems. Troops cost Gold; extra troops become training cards.'};
const lessons:{id:string;text:string;has:(m:MapData)=>boolean}[]=[
 {id:'twofront',text:'Draw from both flags. Tap A / B to switch squads; they share your ink.',has:m=>m.starts.length>1},
 {id:'keys',text:'Draw through a key before its matching gate.',has:m=>m.items.some(o=>o.type==='key')},
 {id:'gold',text:'Golden ink builds bridges across the marked gaps.',has:m=>m.goldZones.length>0},
 {id:'muster',text:'Beat the camp before its timer ends. Escaping squads make the boss stronger.',has:m=>m.enemySquads.some(q=>q.camp!==undefined)},
 {id:'flags',text:'Cross the enemy route to plant a flag. It holds that squad for 10 seconds.',has:m=>m.enemySquads.length>0},
 {id:'chasm',text:'Ravines block your route. Find a way around, or use a golden bridge.',has:m=>m.obstacles.some(o=>o.kind==='chasm')},
 {id:'slope',text:'Ground arrows point uphill: ▲ costs more ink, ▼ costs less.',has:m=>m.terrain.some(t=>t.kind==='slope')},
 {id:'hill',text:'Marked hills use more ink and slow your march.',has:m=>m.terrain.some(t=>t.kind==='hill')},
 {id:'terrain',text:'Only marked terrain changes ink cost. Sand and swamp cost more; roads cost less.',has:m=>m.terrain.some(t=>['sand','swamp','road'].includes(t.kind))},
 {id:'thieves',text:'Enemies can steal charms marked ⚠. Reach them first; camps also drop loot.',has:m=>m.items.some(o=>o.type!=='ink_bottle')&&m.enemySquads.length>0},
 {id:'boss_sealbreaker',text:'Sealbreaker blocks most damage from the front (red fan). Draw your line around to its side or back.',has:m=>m.bosses.some(b=>b.type==='sealbreaker')},
 {id:'boss_inkpot_ogre',text:'Inkpot Ogre spills ink where your troops stand. End your line where the squad can spread out.',has:m=>m.bosses.some(b=>b.type==='inkpot_ogre')},
 {id:'boss_crimson_scribe',text:'Crimson Scribe jumps between rune circles and calls minions. Bring archers and mages.',has:m=>m.bosses.some(b=>b.type==='crimson_scribe')},
 {id:'layout',text:'The boss is not always at the top. Walls hide the real way in: trace it before you draw.',has:m=>!!(m as any).layout&&!['D','2S'].includes((m as any).layout)},
 {id:'choice',text:'Four camps here: destroy any three for all the stars.',has:m=>m.camps.length>3},
 {id:'loot',text:'Camps drop loot when destroyed. Every camp cleared earns a star.',has:m=>m.camps.some(c=>c.loot)}
];
export function contextLesson(map:MapData,seen:Record<string,boolean>):LessonStep|null{const teach=(map as MapData&{teach?:string[]}).teach,lesson=lessons.find(l=>!seen[l.id]&&(teach?teach.includes(l.id):l.has(map)));return lesson?{id:lesson.id,pages:[lesson.text],passive:true,ok:true,autoHide:8500}:null;}
