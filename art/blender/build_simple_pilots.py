"""Build the two approved bean-style pilots; preserve the original character pack."""
import bpy, math, os, sys, json, struct
from mathutils import Vector, Euler, Quaternion
project=os.path.abspath(sys.argv[sys.argv.index('--')+1])
out=os.path.join(project,'public','assets','models','simple'); portraits=os.path.join(project,'public','assets','portraits','simple'); art=os.path.join(project,'art','simple-pilots')
for path in [out,portraits,art]:os.makedirs(path,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
COLORS=[(.16,.48,.88),(.055,.24,.55),(.82,.87,.91),(.34,.43,.52),(.97,.66,.40),(.35,.19,.12),(.98,.94,.78),(.035,.025,.035),(.43,.075,.13),(.56,.71,.16),(.87,.14,.10),(.17,.16,.18),(.88,.62,.24),(.90,.45,.23),(.42,.54,.10),(.94,.45,.25)]
atlas=bpy.data.images.new('Ink March Simple Palette 512',width=512,height=512,alpha=True)
pixels=[]
for y in range(512):
    for x in range(512):pixels.extend((*COLORS[(y//128)*4+x//128],1))
atlas.pixels.foreach_set(pixels);atlas.filepath_raw=os.path.join(art,'palette-512.png');atlas.file_format='PNG';atlas.save();atlas.pack()
material=bpy.data.materials.new('Single 512px Painted Palette');material.use_nodes=True
node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=atlas;node.interpolation='Closest';bs=material.node_tree.nodes.get('Principled BSDF');material.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.87
def empty(name,parent=None,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o.location=loc;return o
def color(o,index):
    o.data.materials.clear();o.data.materials.append(material);uv=o.data.uv_layers.get('UVMap') or o.data.uv_layers.new(name='UVMap');p=((index%4+.5)/4,(index//4+.5)/4)
    for loop in uv.data:loop.uv=p
    return o
def shape(name,kind,parent,loc,scale,index,rot=(0,0,0)):
    if kind=='ball':bpy.ops.mesh.primitive_uv_sphere_add(segments=12 if name in ['Round bean tunic','Big round face'] else 8,ring_count=8 if name in ['Round bean tunic','Big round face'] else 4,radius=.5)
    elif kind=='cone':bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=.5,radius2=0,depth=1)
    elif kind=='cylinder':bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.5,depth=1)
    else:bpy.ops.mesh.primitive_cube_add(size=1)
    o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=scale;o.rotation_euler=rot;color(o,index);return o
def poly(name,parent,verts,faces,index):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.parent=parent;return color(o,index)
def dome(name,parent,index,rx=.60,ry=.54,rz=.57):
    verts=[];segments=12;rings=5
    for j in range(rings+1):
        theta=j/rings*math.pi/2
        for i in range(segments):a=i/segments*math.tau;verts.append((rx*math.sin(theta)*math.cos(a),ry*math.sin(theta)*math.sin(a),rz*math.cos(theta)))
    faces=[]
    for j in range(rings):
        for i in range(segments):n=(i+1)%segments;faces.append((j*segments+i,(j+1)*segments+i,(j+1)*segments+n,j*segments+n))
    return poly(name,parent,verts,faces,index)
def blade(name,parent,points,index):
    n=len(points);verts=[(x,-.04,z) for x,z in points]+[(x,.04,z) for x,z in points];faces=[tuple(range(n)),tuple(range(n*2-1,n-1,-1))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return poly(name,parent,verts,faces,index)
def descendants(root):return [root]+list(root.children_recursive)
def merge(root):
    parents={}
    for o in descendants(root):
        if o.type=='MESH':parents.setdefault(o.parent,[]).append(o)
    for parent,objs in parents.items():
        bpy.ops.object.select_all(action='DESELECT')
        for o in objs:o.select_set(True)
        bpy.context.view_layer.objects.active=objs[0]
        if len(objs)>1:bpy.ops.object.join()
        obj=objs[0];obj.name=parent.name+'_Surface'
        for p in obj.data.polygons:p.use_smooth=False
def clip(obj,name,channels):
    base={prop:tuple(getattr(obj,prop)) for prop in channels};obj.animation_data_create();a=bpy.data.actions.new(obj.name+'_'+name);obj.animation_data.action=a
    for prop,keys in channels.items():
        for frame,value in keys:setattr(obj,prop,value);obj.keyframe_insert(data_path=prop,frame=frame)
    tr=obj.animation_data.nla_tracks.new();tr.name=name;strip=tr.strips.new(name,1,a);strip.name=name;tr.mute=True;obj.animation_data.action=None
    for prop,value in base.items():setattr(obj,prop,value)
def animation(joints):
    hip,body,head,arms,feet=joints
    allj=[hip,body,head]+arms+feet
    for j in allj:
        loc=tuple(j.location)
        idle=[(1,(0,0,0)),(16,(0,0,.025 if j==head else 0)),(32,(0,0,0))]
        clip(j,'Idle',{'rotation_euler':idle,'location':[(1,loc),(16,(loc[0],loc[1],loc[2]+(.025 if j==hip else 0))),(32,loc)]})
        if j in arms+feet:
            sign=1 if j in [arms[0],feet[1]] else -1;walk=[(1,(sign*.30,0,0)),(10,(-sign*.30,0,0)),(20,(sign*.30,0,0))]
        else:walk=[(1,(0,0,0)),(10,(0,0,.04 if j==body else 0)),(20,(0,0,0))]
        clip(j,'Walk',{'rotation_euler':walk,'location':[(1,loc),(5,(loc[0],loc[1],loc[2]+(.06 if j==hip else 0))),(10,loc),(15,(loc[0],loc[1],loc[2]+(.06 if j==hip else 0))),(20,loc)]})
        attack=[(1,(0,0,0)),(8,(-.7,0,-.25)),(13,(.6,0,.30)),(24,(0,0,0))] if j==arms[0] else [(1,(0,0,0)),(8,(0,0,-.08 if j==body else 0)),(13,(.08 if j==body else 0,0,.08 if j==body else 0)),(24,(0,0,0))]
        clip(j,'Attack',{'rotation_euler':attack,'location':[(1,loc),(24,loc)]})
        clip(j,'Death',{'rotation_euler':[(1,(0,0,0)),(12,(.6 if j==hip else .1,0,0)),(26,(math.pi/2 if j==hip else .18,0,.12 if j in arms else 0))],'location':[(1,loc),(26,(loc[0],loc[1],.18 if j==hip else loc[2]))]})
def make(kind):
    enemy=kind=='goblin';root=empty(kind);hip=empty(kind+'_Hips',root,(0,0,.32));body=empty(kind+'_Body',hip,(0,0,.64));head=empty(kind+'_Head',hip,(0,0,1.26));arms=[empty(kind+'_SwordArm',body,(-.60,-.02,.20)),empty(kind+'_OtherArm',body,(.60,-.02,.15))];feet=[empty(kind+'_FootL',hip,(-.30,-.07,-.16)),empty(kind+'_FootR',hip,(.30,-.07,-.16))]
    skin=9 if enemy else 4;cloth=10 if enemy else 0
    shape('Round bean tunic','ball',body,(0,0,-.06),(1.12,.86,1.22),cloth)
    shape('Big round face','ball',head,(0,-.03,0),(1.05,.95,1.03),skin)
    for arm in arms:shape('Stubby sleeve','ball',arm,(0,0,-.09),(.36,.36,.46),cloth);shape('Mitten','ball',arm,(-.05 if arm==arms[0] else .05,-.09,-.23),(.31,.29,.31),skin if enemy else 5)
    for foot in feet:shape('Tiny rounded boot','ball',foot,(0,-.045,.04),(.38,.49,.33),5)
    for side in [-1,1]:
        shape('Big eye white','ball',head,(side*.185,-.466,-.045),(.23,.045,.28),6)
        shape('Eye pupil','ball',head,(side*.185+(.035 if enemy else 0),-.49,-.04),(.115,.028,.18),7)
        shape('Eye sparkle','ball',head,(side*.185+.02,-.508,.015),(.027,.017,.043),6)
    shape('Goofy open smile','ball',head,(0,-.47,-.265),(.38,.04,.24),8);shape('Pink tongue','ball',head,(0,-.496,-.313),(.22,.015,.07),15)
    if enemy:
        shape('Button nose','ball',head,(0,-.52,-.12),(.19,.16,.16),13)
        for side in [-1,1]:
            ear=[(side*.38,.035,-.04),(side*1.05,.10,.40),(side*.59,-.075,.30),(side*.49,.20,.15)];poly('Big pointed ear',head,ear,[(0,2,1),(0,1,3),(0,3,2),(1,2,3)],9);poly('Ear inset',head,[(side*.51,-.01,.03),(side*.91,.065,.31),(side*.60,-.06,.22)],[(0,1,2)],13)
            shape('Funny fang','cone',head,(side*.14,-.51,-.22),(.09,.07,.18),6,rot=(0,side*.17,0))
            shape('Crooked eyebrow','box',head,(side*.19,-.46,.12),(.24,.04,.055),7,rot=(0,side*.20,0))
        dome('Red bandana cap',head,10,.59,.53,.58);shape('Bandana knot','ball',head,(.38,.31,.24),(.26,.23,.22),10);blade('Bandana flap',head,[(.29,.31),(.80,.36),(.69,.65),(.39,.56)],10).location.y=.22
        shape('One black shoulder pad','ball',arms[1],(0,0,.04),(.52,.47,.40),11);shape('One silly spike','cone',arms[1],(.07,0,.33),(.18,.18,.38),6,rot=(0,.22,0))
        w=empty('Goblin cleaver',arms[0],(-.05,-.09,-.24));shape('Wooden grip','cylinder',w,(0,0,.13),(.12,.12,.36),5);blade('Two-notched cleaver',w,[(-.23,.27),(.22,.27),(.22,1.24),(-.01,1.41),(-.30,1.24),(-.24,1.02),(-.08,.91),(-.24,.82),(-.24,.64),(-.09,.53),(-.24,.43)],11)
        blade('Cleaver broad bright edge',w,[(-.23,.27),(-.14,.27),(-.14,.46),(-.01,.53),(-.14,.64),(-.14,.83),(.00,.91),(-.14,1.02),(-.20,1.19),(-.01,1.41),(-.30,1.24),(-.24,1.02),(-.08,.91),(-.24,.82),(-.24,.64),(-.09,.53),(-.24,.43)],3).location.y=-.005
    else:
        dome('Plain silver helmet',head,2)
        for side in [-1,1]:shape('Helmet cheek','box',head,(side*.47,-.08,-.20),(.15,.46,.36),2);shape('Helmet side disc','cylinder',head,(side*.55,.02,-.04),(.24,.24,.10),3,rot=(0,math.pi/2,0))
        for x in [-.23,.0,.23]:shape('Helmet vent','box',head,(x,-.49,.17),(.075,.055,.17),3,rot=(-.3,0,0))
        plume=empty('Blue tuft',head,(0,.03,.54));shape('Plume base','ball',plume,(0,.02,.12),(.22,.24,.31),1);poly('Blue curved tuft',plume,[(-.10,.03,.10),(-.18,.03,.42),(.03,.03,.51),(.31,.03,.31),(.47,.03,.32),(.26,.03,.11),(0,.03,.04),(-.10,.15,.10),(-.18,.15,.42),(.03,.15,.51),(.31,.15,.31),(.47,.15,.32),(.26,.15,.11),(0,.15,.04)],[tuple(range(6,-1,-1)),tuple(range(7,14))]+[(i,(i+1)%7,(i+1)%7+7,i+7) for i in range(7)],0)
        w=empty('Toy sword',arms[0],(-.05,-.10,-.24));shape('Sword grip','cylinder',w,(0,0,.13),(.10,.10,.29),5);shape('Broad cross guard','box',w,(0,0,.30),(.48,.13,.105),12);blade('Oversized straight blade',w,[(-.135,.35),(.135,.35),(.135,1.13),(0,1.38),(-.135,1.13)],2);blade('Blade simple facet',w,[(0,.35),(.135,.35),(.135,1.13),(0,1.38)],3).location.y=-.006
        sh=empty('Round blue buckler',arms[1],(.07,-.24,-.18));shape('Shield silver rim','cylinder',sh,(0,0,0),(.72,.72,.12),2,rot=(math.pi/2,0,0));shape('Shield blue face','cylinder',sh,(0,-.076,0),(.60,.60,.07),0,rot=(math.pi/2,0,0));shape('Shield center','ball',sh,(0,-.14,0),(.24,.12,.24),3)
    merge(root);joints=(hip,body,head,arms,feet);animation(joints)
    return root,joints
roots={}
for kind in ['sword','goblin']:
    root,joints=make(kind);roots[kind]=root;bpy.context.scene.frame_set(1)
    bpy.ops.object.select_all(action='DESELECT')
    for o in descendants(root):o.select_set(True)
    bpy.context.view_layer.objects.active=root
    bpy.ops.export_scene.gltf(filepath=os.path.join(out,kind+'.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_frame_range=False)
    for o in descendants(root):o.hide_render=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.film_transparent=True;scene.world.color=(.30,.30,.30)
bpy.ops.object.camera_add(location=(3.3,-6,4.0));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=3.5;cam.rotation_euler=(Vector((0,0,1.2))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
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
    root.location.x=i*3.0
    for o in descendants(root):o.hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art,'ink-march-simple-pilots.blend'))
print('SIMPLE_PILOTS_COMPLETE')
