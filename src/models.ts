import * as T from 'three';
import {GLTFLoader,type GLTF} from 'three/addons/loaders/GLTFLoader.js';
import {clone} from 'three/addons/utils/SkeletonUtils.js';
export const modelTypes=['sword','archer','shield','spear','mage','healer','goblin','goblin_archer','orc','shaman','goblin_king','shadow_mage','tower','tree','rock'];
const library=new Map<string,GLTF>();
const beanV2=new Set(['sword','archer','shield','spear','mage','healer','goblin']);
const modelPaths:Record<string,string>=Object.fromEntries(modelTypes.map(id=>[id,(beanV2.has(id)?'bean-v2/':'bean-v3/')+id]));
export async function loadModels(progress:(n:number,total:number)=>void){const loader=new GLTFLoader();let count=0;await Promise.all(modelTypes.map(async type=>{const gltf=await loader.loadAsync(`./assets/models/${modelPaths[type]}.glb?v=bean-v3`);library.set(type,gltf);progress(++count,modelTypes.length);}));}
export function modelInstance(type:string,boss=false):T.Group{let asset=library.get(type);if(!asset)throw new Error(`Missing character model: ${type}`);let wrapper=new T.Group(),model=clone(asset.scene);model.traverse(o=>{if(o instanceof T.Mesh){o.castShadow=true;o.receiveShadow=true;}});model.scale.setScalar(boss?40:27);wrapper.add(model);wrapper.userData.assetInstance=true;wrapper.userData.model=model;let mixer=new T.AnimationMixer(model),actions:Record<string,T.AnimationAction>={};asset.animations.forEach(clip=>actions[clip.name]=mixer.clipAction(clip));wrapper.userData.mixer=mixer;wrapper.userData.actions=actions;wrapper.userData.state='';wrapper.userData.deadAt=0;wrapper.userData.facing=0;play(wrapper,'Idle');return wrapper;}
export function play(group:T.Group,state:string){if(group.userData.state===state)return;const actions=group.userData.actions as Record<string,T.AnimationAction>;const current=actions[group.userData.state],next=actions[state];if(!next)return;next.reset();next.setEffectiveTimeScale(state==='Walk'?1.15:1);next.setEffectiveWeight(1);if(state==='Death'){next.setLoop(T.LoopOnce,1);next.clampWhenFinished=true;}else next.setLoop(T.LoopRepeat,Infinity);next.play();if(current)next.crossFadeFrom(current,.12,true);group.userData.state=state;}
export function animateModel(group:T.Group,dt:number,state:string,dx=0,dz=0){play(group,state);if(Math.hypot(dx,dz)>.1){let target=Math.atan2(dx,dz),delta=Math.atan2(Math.sin(target-group.rotation.y),Math.cos(target-group.rotation.y));group.rotation.y+=delta*Math.min(1,dt*12);}group.userData.mixer?.update(dt);}


