/** Chunky toy emblems: one grid, rounded ink outlines, a shaded edge and painted highlights. */
const svg=(name:string,body:string)=>`<svg class="g-ico ico-${name}" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><g stroke="#25464b" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">${body}</g></svg>`;
const path=(d:string,fill:string)=>`<path d="${d}" fill="${fill}"/>`;
const shine=(d:string)=>`<path d="${d}" fill="none" stroke="#fff6d9" stroke-width="2" opacity=".85"/>`;
const star=(fill:string)=>path('M16 3 20 11 29 12.5 22.5 19 24 28 16 23.5 8 28 9.5 19 3 12.5 12 11Z',fill);
const drop=(fill:string)=>path('M16 3C12 9 6 14 6 20a10 10 0 0 0 20 0c0-6-6-11-10-17Z',fill)+shine('M12 15q-4 5-1 8');
const sword=path('m8 3 6 2 11 15-5 4L8 9Z','#e4f0df')+shine('m11 7 11 14')+path('m17 22 8-6 3 4-8 6Z','#f3c65f')+path('m21 25 4-3 4 5-4 3Z','#d97c56');
export const icon:Record<string,string>={
 gold:svg('gold','<ellipse cx="16" cy="18" rx="12" ry="12" fill="#ba8736"/><circle cx="16" cy="15" r="12" fill="#f4c65e"/><circle cx="16" cy="15" r="7.5" fill="#e8a73c"/>'+path('m16 9 4 6-4 6-4-6Z','#fff1b1')+shine('M8 11q2-5 8-5')),
 coin:svg('coin','<ellipse cx="16" cy="18" rx="12" ry="11" fill="#799b98"/><circle cx="16" cy="15" r="12" fill="#c6dfd6"/><circle cx="16" cy="15" r="7" fill="#8cbbb5"/>'+path('m16 10 4 5-4 5-4-5Z','#f2f3d8')+shine('M8 11q2-5 8-5')),
 star:svg('star',star('#f3c553')+shine('m8 14 6-1 2-5')),
 starOff:svg('star-off',star('#6f8e82')),
 gem:svg('gem',path('M8 4h16l6 9-14 17L2 13Z','#e568a4')+path('M2 13h28L16 30Z','#b34f91')+path('m8 4 5 9h6l5-9Z','#f7b2cb')+path('m13 13 3 17 3-17Z','#eb7bb4')+shine('M6 11 9 7h5')),
 ink:svg('ink',drop('#4bade0')),
 goldInk:svg('gold-ink',drop('#efbf44')),
 xp:svg('xp',path('m19 2-14 17h9l-2 11 15-18h-9Z','#9aca6c')+shine('m17 8-6 8')),
 card:svg('card',path('M5 6h19v23H5Z','#7194b7')+'<rect x="8" y="3" width="19" height="23" rx="4" fill="#a5d6d7"/>'+path('m18 8 2 4 5 1-4 3 1 5-4-2-4 2 1-5-4-3 5-1Z','#fff0b8')),
 brush:svg('brush',path('M24 2q5 0 4 5L17 21l-6-5Z','#e7b777')+shine('m24 6-9 11')+path('m12 15 6 5-4 5-6-5Z','#a7c9c1')+path('M9 20q-7 0-6 6l-1 3q12 1 12-6Z','#6bbdb1')+shine('M7 24h3')),
 pause:svg('pause','<rect x="6" y="5" width="7" height="22" rx="2.5" fill="#fff0c6"/><rect x="19" y="5" width="7" height="22" rx="2.5" fill="#fff0c6"/>'),
 undo:svg('undo',path('M13 3 2 13l11 9v-7h6q7 0 6 10l4-1q3-16-10-16h-6Z','#fff0c6')),
 reset:svg('reset',path('M25 7a13 13 0 1 0 3 15l-5-2a8 8 0 1 1-3-9l-4 3h14V2Z','#fff0c6')),
 close:svg('close',path('m8 4 8 8 8-8 4 4-8 8 8 8-4 4-8-8-8 8-4-4 8-8-8-8Z','#fff0d1')),
 left:svg('left',path('m21 3-13 13 13 13 5-6-8-7 8-7Z','#fff0c6')),
 right:svg('right',path('m11 3 13 13-13 13-5-6 8-7-8-7Z','#fff0c6')),
 down:svg('down',path('m3 11 13 13 13-13-6-5-7 8-7-8Z','#fff0c6')),
 check:svg('check',path('m3 16 6-5 6 7L25 4l5 5-15 21Z','#93ce79')),
 lock:svg('lock', '<path d="M9 14V9a7 7 0 0 1 14 0v5" fill="none" stroke="#b6c9bb" stroke-width="5"/><rect x="5" y="13" width="22" height="16" rx="4" fill="#b8aa84"/><circle cx="16" cy="20" r="2.5" fill="#25464b"/><path d="M16 21v3"/>'),
 skull:svg('skull',path('M16 3C0 3 0 23 9 24v5h14v-5C32 23 32 3 16 3Z','#f1e8cb')+'<ellipse cx="10" cy="16" rx="3" ry="4" fill="#25464b"/><ellipse cx="22" cy="16" rx="3" ry="4" fill="#25464b"/><path d="M13 29v-4m6 4v-4"/>'),
 boss:svg('boss',path('M3 9 10 15 16 4 22 15 29 9 26 28H6Z','#f1be53')+path('M6 23h20v5H6Z','#d98948')+'<circle cx="16" cy="18" r="3" fill="#dd6c62"/>'+shine('m8 18-2-5')),
 tabBattle:svg('battle',sword+'<g transform="translate(32 0) scale(-1 1)">'+sword+'</g>'),
 tabSquad:svg('squad',path('M16 2 29 7v10c-1 7-7 11-13 14C10 28 4 24 3 17V7Z','#69adb8')+path('m16 6 8 4v7q-1 5-8 9Z','#418490')+star('#efc761').replace('M16 3 20 11 29 12.5 22.5 19 24 28 16 23.5 8 28 9.5 19 3 12.5 12 11Z','m16 9 2 4 5 1-4 3 1 5-4-2-4 2 1-5-4-3 5-1Z')),
 tabTraining:svg('training',path('M6 16h20v14H6Z','#b17c50')+path('m5 17 11-11 11 11-5 5-6-6-6 6Z','#a7d07c')+path('M4 3h7v7H4Zm17 0h7v7h-7Z','#f2cc74')+'<path d="M11 6h10" fill="none" stroke-width="4"/>'),
 tabRecruit:svg('recruit',path('M4 15q0-10 12-10t12 10v14H4Z','#c28c55')+path('M4 16h24v13H4Z','#8e6650')+'<path d="M9 8v20m14-20v20" stroke="#efd38a" stroke-width="4"/>'+path('M12 16h8v7h-8Z','#efc961')+shine('M8 12q1-4 6-4')),
 heart:svg('heart',path('M16 28 4 17C-4 7 10-1 16 8 22-1 36 7 28 17Z','#e87581')+shine('M6 12q0-4 5-4')),
 bow:svg('bow','<path d="M7 3q30 13 0 26l7-13Z" fill="#e8bd70"/><path d="M4 16h24m-6-5 6 5-6 5" fill="none" stroke="#f1eed8" stroke-width="3"/>'),
 target:svg('target','<circle cx="16" cy="16" r="13" fill="#b499d0"/><circle cx="16" cy="16" r="8" fill="#e7d9ea"/><circle cx="16" cy="16" r="3" fill="#8465a4"/>'),
 plus:svg('plus',path('M11 3h10v8h8v10h-8v8H11v-8H3V11h8Z','#a6d683')),
 flag:svg('flag','<path d="M6 30V3" stroke="#e1c997" stroke-width="4"/>'+path('M8 3h21l-5 8 5 8H8Z','#6aafc9')+shine('M12 7h9')),
 spark:svg('spark',path('m16 2 5 10 9 4-9 5-5 9-5-9-9-5 9-4Z','#efd07b')),
 fang:svg('fang',path('M5 4q11 5 22 0l-4 22-7-9-7 9Z','#eddbd3')),
 warning:svg('warning',path('m16 2 14 27H2Z','#efac69')+'<path d="M16 10v9" stroke-width="3"/><circle cx="16" cy="24" r="1" fill="#25464b"/>'),
 shrine:svg('shrine',path('M4 6h24v5H4Zm5 5h5v18H9Zm10 0h5v18h-5Z','#d58467')+'<path d="M2 3q14 6 28 0" stroke="#6eb0a6" stroke-width="5"/>'),
};
const buffEmblems:Record<string,[string,string]>={
 rb_atk:['tabBattle','#d87665'],rb_hp:['heart','#7ba56a'],rb_volley:['bow','#699db6'],rb_eagle:['target','#9a7cba'],rb_vamp:['fang','#b36886'],rb_pickup_heal:['plus','#68a88d'],rb_extra_unit:['flag','#6598b0'],rb_boss_slayer:['boss','#c89b4f'],rb_first_strike:['spark','#d89157'],rb_frugal:['ink','#67a8b7'],rb_golden_touch:['goldInk','#bf9c4e'],rb_skull_ward:['skull','#8e809c']};
export const buffIcon=(id:string)=>{const [name,color]=buffEmblems[id]||['spark','#699db6'];return `<span class="g-buff-ico" style="--c:${color}">${icon[name]}</span>`;};

/** Shared by on-field charm tokens and camp rewards. */
export function pickupIcon(type:string){return icon[({atk_up:'tabBattle',hp_up:'heart',shield:'tabSquad',reinforce:'flag',range_up:'target',haste:'xp',ink_bottle:'ink',skull:'skull'} as Record<string,string>)[type]||'spark'];}
