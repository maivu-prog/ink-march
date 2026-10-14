"""Seven matched bean characters, tuned for the actual high-angle game camera."""
from pathlib import Path
# Reuse the palette/geometry/export helpers; route all output into versioned folders.
common=Path(__file__).with_name('build_simple_pilots.py').read_text(encoding='utf-8').split('def make(kind):')[0]
common=common.replace("'models','simple'","'models','bean-v2'").replace("'portraits','simple'","'portraits','bean-v2'").replace("'art','simple-pilots'","'art','bean-squad-v2'")
common=common.replace("atlas=bpy.data.images.new", "COLORS += [(.06,.56,.51),(.12,.25,.66),(.12,.86,.94),(.39,.19,.65),(.25,.83,.36),(.92,.96,.96),(.45,.67,.29),(.60,.43,.25),(.84,.75,.48),(.63,.91,.82),(.23,.36,.48),(.72,.49,.29),(.90,.90,.63),(.29,.62,.27),(.82,.34,.38),(.16,.62,.75)]\natlas=bpy.data.images.new")
common=common.replace('(y//128)*4+x//128','(y//64)*4+x//128').replace('(index//4+.5)/4','(index//4+.5)/8')
exec(compile(common,str(Path(__file__).with_name('build_simple_pilots.py')),'exec'))
TYPES=['sword','archer','shield','spear','mage','healer','goblin']
def torus(name,parent,loc,major,minor,index,scale=(1,1,1)):
    bpy.ops.mesh.primitive_torus_add(major_segments=16,minor_segments=4,major_radius=major,minor_radius=minor);o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=scale;return color(o,index)
def rod(name,parent,a,b,r,index):
    a,b=Vector(a),Vector(b);o=shape(name,'cylinder',parent,tuple((a+b)/2),(r*2,r*2,(b-a).length),index);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def star(parent,loc,r=.32):
    pts=[(0,0,0)]+[(math.sin(i*math.pi/5)*(r if i%2==0 else r*.46),0,math.cos(i*math.pi/5)*(r if i%2==0 else r*.46)) for i in range(10)];o=poly('One broad star',parent,pts,[(0,i+1,(i+1)%10+1) for i in range(10)],6);o.location=loc;return o
def helmet(head,blue=False):
    dome('Compact blue helmet' if blue else 'Compact silver helmet',head,0 if blue else 2,.55,.51,.49).location.z=.04
    torus('Helmet thin rim',head,(0,0,.04),.50,.035,12 if blue else 3,(1,.9,1))
    for side in [-1,1]:shape('Small cheek guard','box',head,(side*.46,-.02,-.17),(.10,.28,.25),2)
    if not blue:
        verts=[]
        for y in [-.43,-.25,0,.25,.43]:
            z=.04+.49*math.sqrt(max(0,1-(y/.51)**2))+.022;verts.extend([(-.20,y,z),(.20,y,z)])
        poly('Wide blue crown stripe',head,verts,[(i,i+1,i+3,i+2) for i in range(0,8,2)],0)
    tuft=empty('One blue tuft',head,(0,.08,.52));shape('Tuft','ball',tuft,(0,.05,.12),(.20,.34,.27),0)
def buckler(parent,huge=False):
    sh=empty('Huge round shield' if huge else 'Round buckler',parent,(.10,-.28,-.12));d=1.25 if huge else .64
    shape('Shield rim','cylinder',sh,(0,0,0),(d,d,.13),12 if huge else 2,rot=(math.pi/2,0,0));shape('Shield blue face','cylinder',sh,(0,-.08,0),(d-.13,d-.13,.07),0,rot=(math.pi/2,0,0))
    if huge:star(sh,(0,-.125,0),.37)
    else:shape('Small shield boss','ball',sh,(0,-.14,0),(.20,.10,.20),3)
def make(kind):
    enemy=kind=='goblin';root=empty(kind);hip=empty(kind+'_Hips',root,(0,0,.32));body=empty(kind+'_Body',hip,(0,-.08,.70));head=empty(kind+'_Head',hip,(0,.10,1.27));arms=[empty(kind+'_WeaponArm',body,(-.80 if kind in ['sword','goblin'] else -.68,-.02,.16)),empty(kind+'_OffArm',body,(.70,-.02,.12))];feet=[empty(kind+'_FootL',hip,(-.32,-.12,-.195)),empty(kind+'_FootR',hip,(.32,-.12,-.195))]
    skin=9 if enemy else 4;cloth={'sword':0,'archer':16,'shield':0,'spear':15,'mage':17,'healer':21,'goblin':10}[kind]
    shape('Round bean tunic','ball',body,(0,0,-.06),(1.38,1.06,1.30),cloth)
    shape('Big round face','ball',head,(0,-.03,0),(1.42,1.20,1.26) if enemy else (1.06,.98,1.00),skin)
    for arm in arms:shape('Stubby sleeve','ball',arm,(0,0,-.09),(.39,.39,.44),cloth);shape('Mitten','ball',arm,(-.04 if arm==arms[0] else .04,-.10,-.23),(.33,.31,.33),skin if enemy else 5)
    for foot in feet:shape('Tiny rounded boot','ball',foot,(0,-.045,.04),(.40,.50,.33),5)
    eyeY=-.615 if enemy else -.51;ex=.24 if enemy else .185
    for side in [-1,1]:
        shape('Big eye white','ball',head,(side*ex,eyeY,-.045),(.29,.055,.34) if enemy else (.25,.055,.30),6)
        shape('Eye pupil','ball',head,(side*ex+(.035 if enemy else 0),eyeY-.037,-.04),(.13,.025,.19),7)
        shape('Eye sparkle','ball',head,(side*ex+.02,eyeY-.055,.015),(.028,.014,.042),6)
    mouthY=-.58 if enemy else -.48;shape('Goofy smile','ball',head,(0,mouthY,-.275),(.45,.04,.25) if enemy else (.37,.04,.23),8);shape('Tongue','ball',head,(0,mouthY-.025,-.33),(.24,.015,.07),15)
    if enemy:
        shape('Small button nose','ball',head,(0,-.68,-.12),(.18,.14,.16),13)
        for side in [-1,1]:
            ear=[(side*.48,-.03,-.13),(side*1.40,-.10,.40),(side*.81,-.25,.32),(side*.67,.18,.08)]
            poly('Long broad green ear',head,ear,[(0,2,1),(0,1,3),(0,3,2),(1,2,3)],9)
            poly('Broad ear inset',head,[(side*.62,-.12,.0),(side*1.23,-.14,.32),(side*.82,-.27,.25)],[(0,1,2)],13)
            shape('Big funny fang','cone',head,(side*.17,-.635,-.23),(.105,.075,.20),6,rot=(0,side*.18,0));shape('Crooked eyebrow','box',head,(side*.24,-.60,.15),(.28,.04,.055),7,rot=(0,side*.18,0))
        torus('Thin red headband — no cap',head,(0,0,.30),.585,.055,10,(1.10,.91,1))
        shape('Small band knot','ball',head,(.48,.42,.28),(.19,.19,.16),10);poly('Short band tie',head,[(.44,.43,.29),(.84,.43,.23),(.72,.44,.06),(.45,.43,.19)],[(0,1,2,3)],10)
        shape('One dark shoulder pad','ball',arms[1],(0,0,.04),(.50,.46,.36),11);shape('One big shoulder spike','cone',arms[1],(.06,0,.31),(.18,.18,.36),6)
        w=empty('Notched toy cleaver',arms[0],(-.10,-.10,-.23));w.rotation_euler.y=-.25;shape('Cleaver grip','cylinder',w,(0,0,.13),(.13,.13,.36),5)
        blade('Big cleaver',w,[(-.25,.29),(.25,.29),(.25,1.34),(-.01,1.55),(-.34,1.30),(-.28,1.08),(-.10,.97),(-.28,.86),(-.28,.68),(-.10,.57),(-.28,.46)],11)
    elif kind=='sword':
        helmet(head);w=empty('Oversized visible sword',arms[0],(-.10,-.13,-.23));w.rotation_euler.y=-.25
        shape('Sword grip','cylinder',w,(0,0,.14),(.12,.12,.29),5);shape('Large cross guard','box',w,(0,0,.32),(.62,.15,.13),12)
        blade('Wide long silver blade',w,[(-.23,.39),(.23,.39),(.23,1.48),(0,1.75),(-.23,1.48)],2);blade('Broad blade facet',w,[(0,.39),(.23,.39),(.23,1.48),(0,1.75)],3).location.y=-.006;buckler(arms[1])
    elif kind=='archer':
        dome('Teal hood',head,16,.57,.53,.56);shape('Hood peak','cone',head,(0,.17,.56),(.40,.39,.38),16,rot=(.45,0,0))
        for side in [-1,1]:shape('Hood side','ball',head,(side*.43,.08,-.17),(.23,.42,.40),16)
        w=empty('Tall curved longbow',arms[0],(-.12,-.18,.10));arc=[(0,0,-1.00),(-.26,-.03,-.70),(-.42,-.03,0),(-.26,-.03,.70),(0,0,1.00)]
        for a,b in zip(arc,arc[1:]):rod('Thick wooden bow',w,a,b,.06,12)
        rod('Bowstring',w,arc[0],arc[-1],.012,6);rod('Nocked arrow',w,(0,-.02,0),(.72,-.02,0),.018,5)
        shape('Back quiver','cylinder',body,(.26,.51,.23),(.32,.32,.76),5,rot=(0,.15,0))
        for i in range(3):rod('Arrow',body,(.19+i*.07,.51,.45),(.19+i*.07,.51,.95),.012,5);shape('White arrow feather','box',body,(.19+i*.07,.51,.90),(.11,.025,.15),6)
    elif kind=='shield':
        helmet(head,True);buckler(arms[1],True);w=empty('Short toy mace',arms[0],(-.06,-.10,-.22));rod('Mace handle',w,(0,0,.02),(0,0,.64),.055,5);shape('Round mace head','ball',w,(0,0,.81),(.44,.44,.44),3)
        for x,y in [(-.24,0),(.24,0),(0,-.24)]:shape('Mace stud','cone',w,(x,y,.84),(.15,.15,.23),2,rot=(0,math.copysign(.7,x) if x else 0,0))
    elif kind=='spear':
        dome('Blue helmet base',head,0,.60,.56,.57);shape('Blue conical helmet','cone',head,(0,.04,.46),(1.10,.99,.74),0);torus('Helmet silver band',head,(0,.04,.02),.50,.035,2,(1,.9,1))
        w=empty('Long spear with pennant',arms[0],(-.07,-.10,-.22));w.rotation_euler.y=-.18;rod('Spear shaft',w,(0,0,-.62),(0,0,1.86),.04,5);blade('Big spear point',w,[(-.16,1.86),(.16,1.86),(0,2.27)],2);poly('Large blue pennant',w,[(.06,-.01,1.80),(.72,-.01,1.66),(.08,-.01,1.46)],[(0,1,2)],0)
    elif kind=='mage':
        dome('Wizard hat base',head,17,.60,.56,.57);shape('Blue wizard brim','cylinder',head,(0,0,.08),(1.23,1.10,.09),17);shape('Tall pointed wizard hat','cone',head,(0,.08,.59),(.99,.92,1.00),17,rot=(.12,0,.08));star(head,(0,-.41,.43),.12)
        w=empty('Cyan crystal staff',arms[0],(-.08,-.09,-.25));rod('Staff',w,(0,0,-.55),(0,0,1.44),.05,5);shape('Glowing crystal','ball',w,(0,0,1.57),(.43,.43,.48),18);torus('Crystal gold collar',w,(0,0,1.36),.16,.035,12)
        star(body,(0,-.55,.06),.15)
    elif kind=='healer':
        torus('Green leaf circlet',head,(0,0,.22),.48,.045,20,(1,.9,1))
        for side in [-1,1]:shape('One big leaf','ball',head,(side*.32,-.25,.27),(.27,.11,.14),20,rot=(0,side*-.4,0))
        shape('Blue collar','ball',body,(0,-.45,.30),(.78,.20,.15),18);bag=empty('Simple healer satchel',body,(.40,-.43,-.25));shape('White bag','box',bag,(0,0,0),(.39,.16,.34),21);shape('Red cross vertical','box',bag,(0,-.09,0),(.07,.025,.23),10);shape('Red cross horizontal','box',bag,(0,-.09,0),(.23,.025,.07),10)
        bottle=empty('Large green potion',arms[0],(-.08,-.10,-.08));shape('Round green flask','ball',bottle,(0,0,.12),(.45,.40,.50),20);shape('Flask neck','cylinder',bottle,(0,0,.40),(.18,.18,.19),18);shape('Bottle cork','cylinder',bottle,(0,0,.52),(.20,.20,.09),5)
    merge(root);joints=(hip,body,head,arms,feet);animation(joints);return root,joints

roots={};manifest={}
for kind in TYPES:
    root,joints=make(kind);roots[kind]=root;bpy.context.scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for o in descendants(root):o.select_set(True)
    bpy.context.view_layer.objects.active=root;path=os.path.join(out,kind+'.glb')
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_frame_range=False)
    b=Path(path).read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);tris=sum(j['accessors'][p['indices']]['count']//3 for m in j['meshes'] for p in m['primitives']);assert tris<3000,(kind,tris)
    manifest[kind]={'triangles':tris,'meshes':len(j['meshes']),'materialCount':len(j['materials']),'textureSize':[512,512],'animations':[a['name'] for a in j['animations']]}
    for o in descendants(root):o.hide_render=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.film_transparent=True;scene.world.color=(.30,.30,.30)
bpy.ops.object.camera_add(location=(3.1,-6,4.3));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=4;cam.rotation_euler=(Vector((0,0,1.35))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
for loc,power,size in [((-3,-4,6),650,4),((3,-1,5),450,4),((0,4,5),550,3)]:
    bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.size=size;light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
for kind,root in roots.items():
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
    root.location=(i%4*3.5,i//4*4,0)
    for o in descendants(root):o.hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art,'ink-march-bean-squad-v2.blend'))
Path(os.path.join(art,'manifest.json')).write_text(json.dumps(manifest,indent=2))
print('BEAN_SQUAD_V2_COMPLETE',json.dumps(manifest))

