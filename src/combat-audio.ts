/** Small synthesized toy sounds; no downloads and no sound before a user gesture. */
export class CombatAudio {
 private context:AudioContext|null=null;private last=new Map<string,number>();private voices=0;
 enabled=true;
 constructor(){try{this.enabled=localStorage.getItem('ink-march-sound')!=='off';}catch{}}
 unlock(){try{this.context??=new AudioContext();if(this.context.state==='suspended')void this.context.resume().catch(()=>{});}catch{}}
 toggle(){this.enabled=!this.enabled;try{localStorage.setItem('ink-march-sound',this.enabled?'on':'off');}catch{}if(this.enabled)this.unlock();}
 play(kind:'slash'|'bow'|'magic'|'hit'|'slam'|'throw'|'heal'|'win'|'down'){
  const ctx=this.context;if(!this.enabled||!ctx||ctx.state!=='running'||this.voices>12)return;const now=ctx.currentTime,gap=kind==='hit'?.065:.035;if(now-(this.last.get(kind)??-10)<gap)return;this.last.set(kind,now);
  const params={slash:[460,130,.09,.025],bow:[740,280,.1,.022],magic:[440,920,.19,.025],hit:[165,65,.085,.035],slam:[100,32,.3,.065],throw:[170,95,.16,.035],heal:[540,820,.22,.025],win:[660,1320,.42,.04],down:[180,55,.3,.04]}[kind],osc=ctx.createOscillator(),gain=ctx.createGain();osc.type=kind==='magic'||kind==='heal'||kind==='win'?'sine':'triangle';osc.frequency.setValueAtTime(params[0],now);osc.frequency.exponentialRampToValueAtTime(params[1],now+params[2]);gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(params[3],now+.008);gain.gain.exponentialRampToValueAtTime(.0001,now+params[2]);osc.connect(gain);gain.connect(ctx.destination);this.voices++;osc.onended=()=>{this.voices--;osc.disconnect();gain.disconnect();};osc.start(now);osc.stop(now+params[2]+.02);
 }
}
