"""Complete the enemy bean set and camp tower, using the approved v2 geometry/palette."""
from pathlib import Path
source=Path(__file__).with_name('build_bean_squad_v2.py').read_text(encoding='utf-8-sig').split('roots={}')[0]
source=source.replace("'bean-v2'","'bean-v3'").replace("'bean-squad-v2'","'bean-enemies-v3'")
source=source.replace('(.29,.62,.27)','(.12,.42,.20)').replace('(.82,.34,.38)','(.76,.25,1.0)')
exec(compile(source,str(Path(__file__).with_name('build_bean_squad_v2.py')),'exec'))
TYPES=['goblin_king','goblin_archer','orc','shaman','shadow_mage','tower','tree','rock']

def ear_pair(head,skin=9):
    for side in [-1,1]:
        verts=[(side*.48,-.03,-.13),(side*1.40,-.10,.40),(side*.81,-.25,.32),(side*.67,.18,.08)]
        poly('Long broad bean goblin ear',head,verts,[(0,2,1),(0,1,3),(0,3,2),(1,2,3)],skin)
        poly('Warm ear inset',head,[(side*.62,-.12,0),(side*1.23,-.14,.32),(side*.82,-.27,.25)],[(0,1,2)],13)

def skull(parent,loc,scale=1):
    g=empty('Big readable toy skull',parent,loc);g.scale=(scale,scale,scale)
    shape('Skull dome','ball',g,(0,0,0),(.55,.18,.48),6)
    for side in [-1,1]:shape('Skull eye socket','ball',g,(side*.13,-.10,.035),(.13,.035,.16),11)
    shape('Skull square jaw','box',g,(0,-.02,-.19),(.30,.15,.14),6)
    return g

def make_enemy(kind):
    root=empty(kind);hip=empty(kind+'_Hips',root,(0,0,.32));body=empty(kind+'_Body',hip,(0,-.08,.70));head=empty(kind+'_Head',hip,(0,.10,1.27))
    arms=[empty(kind+'_WeaponArm',body,(-.80,-.02,.16)),empty(kind+'_OffArm',body,(.78,-.02,.12))];feet=[empty(kind+'_FootL',hip,(-.34,-.12,-.195)),empty(kind+'_FootR',hip,(.34,-.12,-.195))]
    king=kind=='goblin_king';shadow=kind=='shadow_mage';orc=kind=='orc';skin=29 if orc else 9;cloth=19 if shadow else 11 if kind in ['goblin_archer','orc'] else 10
    shape('Round bean tunic','ball',body,(0,0,-.06),(1.65 if king or orc else 1.42,1.18 if king else 1.06,1.30),cloth)
    shape('Big round face','ball',head,(0,-.03,0),(1.42,1.20,1.26),11 if shadow else skin)
    for arm in arms:
        shape('Stubby sleeve','ball',arm,(0,0,-.09),(.43,.43,.44),cloth);shape('Bean mitten','ball',arm,(0,-.10,-.23),(.35,.33,.35),19 if shadow else skin)
    for foot in feet:shape('Tiny rounded boot','ball',foot,(0,-.045,.04),(.43,.53,.33),11 if shadow else 5)
    if not shadow:
        ear_pair(head,skin)
        for side in [-1,1]:
            shape('Big eye white','ball',head,(side*.24,-.615,-.045),(.29,.055,.34),6);shape('Eye pupil','ball',head,(side*.24+.035,-.652,-.04),(.13,.025,.19),7)
            shape('Crooked eyebrow','box',head,(side*.24,-.60,.15),(.30,.045,.07),7,rot=(0,side*.24,0))
            shape('Large goofy tusk','cone',head,(side*.20,-.635,-.23),(.15 if orc else .11,.095,.34 if orc else .23),6,rot=(0,side*.2,0))
        shape('Open grin','ball',head,(0,-.58,-.275),(.47,.04,.25),8);shape('Button nose','ball',head,(0,-.68,-.12),(.20,.14,.16),skin)
    if kind=='goblin_archer':
        torus('Thin red bandana',head,(0,0,.30),.585,.055,10,(1.10,.91,1));shape('Bandana knot','ball',head,(.48,.42,.28),(.19,.19,.16),10)
        poly('Bandana tail',head,[(.44,.43,.29),(.90,.43,.23),(.74,.44,.04),(.45,.43,.19)],[(0,1,2,3)],10)
        for x in [-.32,.32]:shape('Broad orange leather strap','box',body,(x,-.52,.02),(.13,.09,.98),13,rot=(0,x*.7,0))
        bow=empty('Crude oversized bone bow',arms[0],(-.13,-.18,.07));arc=[(0,0,-.94),(-.34,-.03,-.66),(-.46,-.03,0),(-.34,-.03,.66),(0,0,1.03)]
        for a,b in zip(arc,arc[1:]):rod('Chunky bone bow',bow,a,b,.075,6)
        rod('Black bow string',bow,arc[0],arc[-1],.013,11);rod('Ready red arrow',bow,(0,-.02,0),(.78,-.02,0),.023,10)
        shape('Red quiver','cylinder',body,(.30,.50,.25),(.37,.37,.80),10,rot=(0,.18,0))
        for i in range(3):rod('Red arrow shaft',body,(.23+i*.08,.51,.48),(.23+i*.08,.51,1.00),.016,10);shape('Red fletching','box',body,(.23+i*.08,.51,.94),(.13,.03,.18),10)
    elif orc:
        for side,arm in zip([-1,1],arms):
            shape('Big black shoulder pad','ball',arm,(0,0,.10),(.68,.55,.45),11)
            for x in [-.17,.17]:shape('Shoulder ivory spike','cone',arm,(x,0,.42),(.20,.20,.40),6,rot=(0,x,0))
            shape('Red cheek warpaint','box',head,(side*.44,-.54,-.07),(.15,.055,.38),10,rot=(0,side*-.30,0))
        shape('Red brow paint','box',head,(0,-.54,.31),(.16,.06,.39),10)
        club=empty('Huge spiked club',arms[0],(-.13,-.12,-.25));club.rotation_euler.y=-.30;rod('Club long grip',club,(0,0,-.20),(0,0,1.03),.09,5)
        shape('Chunky black club head','ball',club,(0,0,1.14),(.66,.64,.96),11)
        for x,z,a in [(-.36,1.0,-1.15),(-.36,1.35,-1.15),(.36,1.0,1.15),(.36,1.35,1.15),(0,1.72,0)]:shape('Large club spike','cone',club,(x,0,z),(.23,.23,.40),6,rot=(0,a,0))
        root.scale=(1.40,1.40,1.40)
    elif kind=='shaman':
        skull(head,(0,-.54,.38),1.1)
        for side in [-1,1]:
            shape('Red cloak collar','ball',body,(side*.37,.30,.43),(.57,.38,.30),10)
            poly('Large orange feather',head,[(side*.48,.16,.35),(side*.92,.16,.95),(side*.92,.16,.48),(side*.60,.16,.18)],[(0,1,2,3)],13)
        poly('Ragged red cloak',body,[(-.74,.38,.49),(.74,.38,.49),(.76,.59,-.70),(.30,.61,-.48),(0,.63,-.72),(-.30,.61,-.48),(-.76,.59,-.70)],[(0,1,2,3,4,5,6)],10)
        staff=empty('Crooked flame staff',arms[0],(-.14,-.11,-.25));arc=[(0,0,-.60),(0,0,1.10),(-.25,0,1.40),(-.13,0,1.66)]
        for a,b in zip(arc,arc[1:]):rod('Crooked wood',staff,a,b,.065,5)
        shape('Orange magic flame','ball',staff,(-.13,0,1.78),(.48,.43,.62),13);shape('Golden flame tip','cone',staff,(-.17,0,2.10),(.38,.34,.52),12,rot=(0,-.22,0));shape('Yellow flame core','ball',staff,(-.13,-.21,1.78),(.22,.06,.33),6)
    elif king:
        torus('Open golden crown band',head,(0,0,.40),.59,.09,12,(1.10,.95,1))
        for i in range(7):
            a=i*math.tau/7;shape('Big crown point','cone',head,(math.cos(a)*.59,math.sin(a)*.51,.66),(.23,.23,.54),12)
        shape('One red crown jewel','ball',head,(0,-.61,.43),(.21,.07,.23),10)
        shape('Royal red cape','ball',body,(0,.39,-.03),(1.80,.63,1.42),10)
        for x in [-.57,-.28,0,.28,.57]:shape('Black fur cape collar','ball',body,(x,.23,.49),(.39,.40,.34),11)
        shape('Wide black belt','box',body,(0,-.53,-.25),(1.35,.14,.18),11);shape('Gold buckle','box',body,(0,-.62,-.25),(.24,.07,.23),12)
        axe=empty('Big royal war axe',arms[0],(-.19,-.12,-.25));axe.rotation_euler.y=-.23;rod('Axe shaft',axe,(0,0,-.25),(0,0,1.65),.065,5)
        blade('Broad crescent axe head',axe,[(-.12,1.13),(-.74,1.02),(-.82,1.70),(-.16,1.55),(.16,1.55),(.66,1.78),(.78,1.14),(.16,1.12)],3)
        rod('Gold axe binding',axe,(0,0,1.12),(0,0,1.56),.10,12)
        shield=empty('Royal spiked shield',arms[1],(.15,-.25,-.08));shape('Gold shield rim','cylinder',shield,(0,0,0),(1.23,1.23,.17),12,rot=(math.pi/2,0,0));shape('Black shield face','cylinder',shield,(0,-.11,0),(1.06,1.06,.11),11,rot=(math.pi/2,0,0));skull(shield,(0,-.21,.05),.9)
        for x,z in [(-.53,0),(.53,0),(0,.53)]:shape('Big shield spike','cone',shield,(x,-.04,z),(.19,.19,.35),6,rot=(math.pi/2,0,0))
        # The runtime already enlarges bosses (40 vs 27). Keep the crown below the HUD.
        root.scale=(1.12,1.12,1.12)
    elif shadow:
        shape('Deep purple hood','ball',head,(0,.10,.07),(1.59,1.27,1.46),19)
        shape('Dark face opening','ball',head,(0,-.63,.03),(1.10,.20,.95),11)
        for side in [-1,1]:shape('Glowing violet eye','ball',head,(side*.21,-.765,.12),(.25,.04,.16),30)
        shape('Dark hood peak','cone',head,(0,.24,.68),(.79,.72,.80),19,rot=(.25,0,-.12))
        shape('Black bean robe','ball',body,(0,-.01,-.12),(1.61,1.13,1.58),11)
        for side in [-1,1]:
            poly('Broad purple robe trim',body,[(side*.13,-.55,.49),(side*.39,-.57,.42),(side*.53,-.49,-.66),(side*.28,-.53,-.67)],[(0,1,2,3)],19)
            orb=empty('Floating dark magic orb',arms[0 if side<0 else 1],(side*.15,-.17,.44));shape('Dark violet orb','ball',orb,(0,0,0),(.61,.61,.61),19);torus('Bright violet orbit',orb,(0,0,0),.35,.035,30,scale=(1,1,.7));shape('Orb highlight','ball',orb,(-.13,-.23,.14),(.16,.08,.16),30)
        for z in [-.40,-.04,.30]:
            poly('One large glowing rune',body,[(0,-.59,z+.12),(.10,-.59,z),(0,-.59,z-.12),(-.10,-.59,z)],[(0,1,2,3)],30)
        root.scale=(1.10,1.10,1.10)
    merge(root);animation((hip,body,head,arms,feet));return root

def make_scenery(kind):
    root=empty(kind)
    if kind=='tree':
        shape('Chunky trunk','cylinder',root,(0,0,.65),(.44,.44,1.30),5)
        for z,w,h,c in [(1.20,2.05,1.40,29),(1.94,1.61,1.35,22),(2.57,1.09,1.20,29)]:
            shape('Round bean tunic','ball',root,(0,0,z),(w,w*.92,h),c)
    else:
        o=shape('Round bean tunic','ball',root,(0,0,.52),(2.1,1.8,1.30),3)
        for v in o.data.vertices:
            if v.co.z<-.40:v.co.z=-.40
        shape('Broad moss cap','ball',root,(-.12,.10,1.00),(1.24,1.03,.35),22)
    merge(root);return root

def make_tower():
    root=empty('tower')
    shape('Rounded broad stone foot','cylinder',root,(0,0,.18),(2.65,2.65,.36),3)
    shape('Round toy stone tower','ball',root,(0,0,1.42),(2.08,2.08,2.85),24)
    shape('Upper stone collar','cylinder',root,(0,0,2.40),(2.30,2.30,.28),24)
    # Large rounded door and windows; no micro masonry at phone scale.
    shape('Dark arched door','ball',root,(0,-.94,.69),(.69,.16,1.16),5)
    shape('Iron door band','box',root,(0,-1.04,.52),(.59,.05,.13),11)
    for side in [-1,1]:shape('Dark window','ball',root,(side*.58,-.84,1.75),(.29,.12,.43),11)
    shape('Red padded roof lip','ball',root,(0,0,2.66),(2.53,2.53,.42),10)
    shape('Chunky red pointed roof','cone',root,(0,0,3.11),(2.47,2.47,1.04),10)
    shape('Wooden banner pole','cylinder',root,(0,0,3.90),(.10,.10,1.35),5)
    poly('Large red swallowtail banner',root,[(.02,0,4.46),(1.00,0,4.40),(.78,0,4.11),(1.00,0,3.86),(.02,0,3.91)],[(0,1,2,3,4),(4,3,2,1,0)],10)
    skull(root,(.42,-.035,4.19),.65)
    for i in range(7):
        a=math.tau*i/7;shape('Short wooden base stake','cone',root,(math.cos(a)*1.23,math.sin(a)*1.23,.48),(.25,.25,.90),5,rot=(math.sin(a)*.22,-math.cos(a)*.22,0))
    merge(root);return root

roots={};manifest={}
for kind in TYPES:
    root=make_tower() if kind=='tower' else make_scenery(kind) if kind in ['tree','rock'] else make_enemy(kind);roots[kind]=root;bpy.context.scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for o in descendants(root):o.select_set(True)
    bpy.context.view_layer.objects.active=root;path=os.path.join(out,kind+'.glb')
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_frame_range=False)
    b=Path(path).read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);tris=sum(j['accessors'][p['indices']]['count']//3 for m in j['meshes'] for p in m['primitives']);assert tris<3000,(kind,tris)
    manifest[kind]={'triangles':tris,'meshes':len(j['meshes']),'materialCount':len(j['materials']),'textureSize':[512,512],'animations':[a['name'] for a in j.get('animations',[])]}
    for o in descendants(root):o.hide_render=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.film_transparent=True;scene.world.color=(.30,.30,.30)
bpy.ops.object.camera_add(location=(3.1,-6,4.3));cam=bpy.context.object;cam.data.type='ORTHO';cam.rotation_euler=(Vector((0,0,1.70))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
for loc,power,size in [((-3,-4,6),650,4),((3,-1,5),450,4),((0,4,5),550,3)]:
    bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.size=size;light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
for kind,root in roots.items():
    cam.data.ortho_scale=6.5 if kind=='goblin_king' else 5.7 if kind in ['shadow_mage','tower','orc'] else 4.1
    for o in descendants(root):
        o.hide_render=False
        if o.animation_data:
            for tr in o.animation_data.nla_tracks:tr.mute=tr.name!='Idle'
    scene.frame_set(1);scene.render.filepath=os.path.join(portraits,kind+'.png');bpy.ops.render.render(write_still=True)
    for o in descendants(root):
        o.hide_render=True
        if o.animation_data:
            for tr in o.animation_data.nla_tracks:tr.mute=True
for i,(kind,root) in enumerate(roots.items()):
    root.location=(i%3*5.5,i//3*6,0)
    for o in descendants(root):o.hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art,'ink-march-bean-enemies-v3.blend'))
Path(os.path.join(art,'manifest.json')).write_text(json.dumps(manifest,indent=2))
print('BEAN_ENEMIES_V3_COMPLETE',json.dumps(manifest))

