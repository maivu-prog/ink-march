"""Original Ink March models. Run with Blender --background --python build_assets.py -- <project>."""
import bpy, math, os, sys, json
from mathutils import Vector
project = os.path.abspath(sys.argv[sys.argv.index('--')+1])
assets = os.path.join(project,'public','assets'); os.makedirs(assets,exist_ok=True)
models = os.path.join(assets,'models'); portraits = os.path.join(assets,'portraits')
os.makedirs(models,exist_ok=True); os.makedirs(portraits,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
mats={}
def mat(name,color,metal=0,rough=.7):
    if name in mats:return mats[name]
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;mats[name]=m;return m
steel=mat('Forged Steel',(.40,.55,.59),.5,.4);edge=mat('Blade Edges',(.77,.86,.81),.65,.28);gold=mat('Warm Brass',(.87,.55,.16),.6,.35)
skin=mat('Warm Skin',(.77,.48,.28));leather=mat('Dark Leather',(.10,.065,.05));eyes=mat('Eyes',(.014,.02,.027));white=mat('Ivory',(.95,.86,.63));wood=mat('Wood',(.28,.13,.05));red=mat('Enemy Cloth',(.55,.13,.09));green=mat('Goblin Skin',(.25,.44,.14))
def empty(name,parent=None,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o.location=loc;return o
def mesh_obj(name,geo,material,parent,loc=(0,0,0),scale=(1,1,1),rot=(0,0,0)):
    if geo=='box':bpy.ops.mesh.primitive_cube_add(size=1)
    elif geo=='sphere':bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.5)
    elif geo=='ico':bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.5)
    elif geo=='cone':bpy.ops.mesh.primitive_cone_add(vertices=10,radius1=.5,radius2=0,depth=1)
    elif geo=='cylinder':bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.5,depth=1)
    o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=scale;o.rotation_euler=rot;o.data.materials.append(material)
    if geo=='box':
        bevel=o.modifiers.new('Soft crafted edges','BEVEL');bevel.width=.06;bevel.segments=1
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bevel.name)
    return o
def rod(name,a,b,r,material,parent):
    a,b=Vector(a),Vector(b);o=mesh_obj(name,'cylinder',material,parent,tuple((a+b)/2),(r*2,r*2,(b-a).length));o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def ribbon(name,coords,material,parent):
    me=bpy.data.meshes.new(name);me.from_pydata(coords,[],[tuple(range(len(coords)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.parent=parent;me.materials.append(material);mod=o.modifiers.new('Cloth thickness','SOLIDIFY');mod.thickness=.025;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);return o
roots={};joints={}
def character(kind):
    enemy=kind in ['goblin','goblin_archer','orc','shaman','goblin_king','shadow_mage'];boss=kind in ['goblin_king','shadow_mage'];isgreen=kind in ['goblin','goblin_archer','orc','shaman','goblin_king'];caster=kind in ['mage','healer','shaman','shadow_mage'];bow=kind in ['archer','goblin_archer']
    pal={'sword':(.09,.28,.43),'archer':(.13,.39,.36),'shield':(.12,.24,.39),'spear':(.10,.36,.43),'mage':(.31,.16,.49),'healer':(.62,.65,.43),'shadow_mage':(.21,.075,.28)}
    cloth=mat(kind+' livery',pal.get(kind,(.43,.16,.095))); flesh=green if isgreen else skin
    root=empty(kind); hip=empty('Hips',root,(0,0,.82)); torso=empty('Torso',hip,(0,0,.18));head=empty('Head',torso,(0,0,.66));
    mesh_obj('Tunic','box',cloth,torso,(0,0,.02),(.68,.44,.66));mesh_obj('Breastplate','box',steel if not caster and not bow else cloth,torso,(0,-.23,.08),(.58,.11,.43));mesh_obj('Belt','box',leather,hip,(0,0,.12),(.73,.48,.11));mesh_obj('Buckle','box',gold,hip,(0,-.26,.12),(.13,.045,.10));
    for side in [-1,1]:
        mesh_obj('Tunic panel','box',cloth,hip,(side*.18,0,-.13),(.32,.44,.30),rot=(0,side*.12,0))
    mesh_obj('Face','sphere',flesh,head,(0,0,0),(.60,.55,.58));mesh_obj('Nose','ico',flesh,head,(0,-.29,-.02),(.16,.14,.13))
    for side in [-1,1]:
        mesh_obj('Eye white','box',white,head,(side*.13,-.258,.035),(.095,.018,.075));mesh_obj('Pupil','box',eyes,head,(side*.13,-.276,.038),(.035,.012,.047));mesh_obj('Brow','box',leather,head,(side*.13,-.25,.11),(.13,.035,.04),rot=(0,side*.16,side*-.1));
        if isgreen:mesh_obj('Pointed ear','cone',flesh,head,(side*.34,0,.05),(.20,.16,.33),rot=(0,side*math.pi/2,0))
    mesh_obj('Mouth','box',leather,head,(0,-.26,-.15),(.16,.018,.035))
    arms=[];legs=[]
    for side in [-1,1]:
        arm=empty('Arm_R' if side==1 else 'Arm_L',torso,(side*.43,0,.29));arms.append(arm)
        mesh_obj('Shoulder','sphere',cloth if caster or bow else steel,arm,(0,0,0),(.35,.38,.30));mesh_obj('Sleeve','box',cloth,arm,(side*.02,0,-.17),(.23,.25,.36));mesh_obj('Bracer','box',leather if bow or caster else steel,arm,(0,-.025,-.37),(.25,.29,.17));mesh_obj('Hand','sphere',flesh,arm,(0,-.025,-.47),(.22,.25,.22));
        leg=empty('Leg_R' if side==1 else 'Leg_L',hip,(side*.19,0,-.1));legs.append(leg);mesh_obj('Leg','box',cloth,leg,(0,0,-.23),(.25,.30,.42));mesh_obj('Boot','box',leather,leg,(0,-.07,-.53),(.29,.45,.29));mesh_obj('Knee guard','sphere',steel if not caster else gold,leg,(0,-.17,-.25),(.24,.09,.22))
    if caster:
        mesh_obj('Hat brim','cylinder',cloth,head,(0,0,.18),(.83,.83,.07));mesh_obj('Wizard hood','cone',cloth,head,(0,.035,.54),(.68,.63,.76),rot=(0,.08,0));mesh_obj('Hat band','cylinder',gold,head,(0,0,.27),(.56,.52,.08));
        ribbon('Cape',[(-.40,.25,.34),(.40,.25,.34),(.47,.40,-.47),(-.47,.40,-.47)],cloth,torso)
        ribbon('Robe front',[(-.28,-.25,0),(.28,-.25,0),(.39,-.26,-.77),(-.39,-.26,-.77)],cloth,torso)
        weapon=empty('Staff',arms[1],(0,-.04,-.44));rod('Staff shaft',(0,0,-.42),(0,0,1.10),.045,wood,weapon);mesh_obj('Staff crystal','ico',mat(kind+' crystal',(.28,.80,.71) if kind=='healer' else (.60,.32,.89)),weapon,(0,0,1.2),(.31,.31,.46));mesh_obj('Staff collar','cylinder',gold,weapon,(0,0,1.04),(.19,.19,.12))
        if kind=='healer':mesh_obj('Healer emblem vertical','box',white,torso,(0,-.28,.09),(.08,.02,.28));mesh_obj('Healer emblem horizontal','box',white,torso,(0,-.28,.09),(.25,.02,.07))
    elif bow:
        mesh_obj('Hood','sphere',cloth,head,(0,.05,.17),(.68,.61,.42));mesh_obj('Hood peak','cone',cloth,head,(0,.12,.41),(.50,.45,.45),rot=(.35,0,0));
        quiver=mesh_obj('Quiver','cylinder',leather,torso,(.13,.29,.12),(.24,.24,.68),rot=(0,.20,0))
        for i in range(3):rod('Arrow in quiver',(.09+i*.04,.3,.35),(.09+i*.04,.3,.72),.014,wood,torso);mesh_obj('Arrow feather','box',white,torso,(.09+i*.04,.3,.69),(.09,.022,.09))
        weapon=empty('Bow',arms[0],(0,-.09,-.34));arc=[(0,-.07,-.55),(0,-.27,-.32),(0,-.34,0),(0,-.27,.32),(0,-.07,.55)]
        for i in range(4):rod('Bow limb',arc[i],arc[i+1],.035,wood,weapon)
        rod('Bow string',arc[0],arc[-1],.008,white,weapon);rod('Nocked arrow',(-.07,-.14,0),(.58,-.14,0),.012,wood,weapon)
    else:
        mesh_obj('Helmet','sphere',steel,head,(0,.025,.17),(.72,.65,.46));mesh_obj('Helmet ridge','box',gold,head,(0,.015,.37),(.09,.49,.11));
        for side in [-1,1]:mesh_obj('Cheek guard','box',steel,head,(side*.25,-.03,-.05),(.16,.34,.25),rot=(0,side*.2,0))
        if kind in ['sword','shield','spear','goblin_king']:
            mesh_obj('Plume','cone',mat('Plume',(.77,.28,.12)),head,(0,.10,.58),(.17,.21,.47),rot=(.4,0,0));
        if kind in ['spear','goblin_king']:
            weapon=empty('Spear',arms[1],(0,-.10,-.43));rod('Spear haft',(0,0,-.40),(0,0,1.5),.035,wood,weapon);mesh_obj('Spear blade','cone',edge,weapon,(0,0,1.65),(.20,.09,.38));mesh_obj('Spear collar','cylinder',gold,weapon,(0,0,1.43),(.09,.09,.11))
        else:
            weapon=empty('Sword',arms[1],(0,-.07,-.4));mesh_obj('Sword grip','cylinder',leather,weapon,(0,0,.07),(.07,.07,.2));mesh_obj('Sword crossguard','box',gold,weapon,(0,0,.20),(.31,.095,.07));mesh_obj('Sword blade','box',edge,weapon,(0,0,.58),(.15,.045,.71));mesh_obj('Sword tip','cone',edge,weapon,(0,0,.99),(.15,.045,.17));
        if kind in ['shield','sword','orc','goblin_king']:
            shield=empty('Shield',arms[0],(0,-.19,-.30));mesh_obj('Shield rim','cylinder',gold,shield,(0,0,0),(.72,.72,.09),rot=(math.pi/2,0,0));mesh_obj('Shield face','cylinder',cloth,shield,(0,-.06,0),(.62,.62,.065),rot=(math.pi/2,0,0));mesh_obj('Shield boss','sphere',steel,shield,(0,-.12,0),(.18,.10,.18));
        if kind=='orc':
            for side in [-1,1]:mesh_obj('Tusk','cone',white,head,(side*.18,-.29,-.08),(.09,.09,.23),rot=(0,side*.3,0));
    if boss:
        mesh_obj('Crown band','cylinder',gold,head,(0,0,.38),(.83,.83,.12))
        for i in range(5):a=i*math.tau/5;mesh_obj('Crown point','cone',gold,head,(.31*math.cos(a),.31*math.sin(a),.57),(.11,.11,.30))
        ribbon('Royal cape',[(-.52,.25,.38),(.52,.25,.38),(.63,.48,-.73),(-.63,.48,-.73)],red if kind=='goblin_king' else cloth,torso)
    if kind=='orc':root.scale=(1.25,1.25,1.25)
    if boss:root.scale=(1.5,1.5,1.5)
    roots[kind]=root;joints[kind]=(hip,torso,head,arms,legs);return root
def action(obj,name,frames,prop='rotation_euler'):
    old=tuple(getattr(obj,prop))
    obj.animation_data_create();a=bpy.data.actions.new(name+'_'+obj.name);obj.animation_data.action=a
    for frame,value in frames:setattr(obj,prop,value);obj.keyframe_insert(data_path=prop,frame=frame)
    track=obj.animation_data.nla_tracks.new();track.name=name;strip=track.strips.new(name,int(a.frame_range[0]),a);strip.name=name;obj.animation_data.action=None;setattr(obj,prop,old)
    return a
def animate(kind):
    hip,body,head,arms,legs=joints[kind];hipbase=tuple(hip.location)
    action(body,'Idle',[(1,(0,0,-.025)),(20,(.025,0,.025)),(40,(0,0,-.025))]);action(hip,'Idle',[(1,hipbase),(20,(0,0,.84)),(40,hipbase)],'location')
    for j,o in enumerate(legs+arms):
        phase=1 if j in [0,3] else -1
        action(o,'Walk',[(1,(phase*.42,0,0)),(10,(-phase*.42,0,0)),(20,(phase*.42,0,0))])
    action(hip,'Walk',[(1,hipbase),(5,(0,0,.88)),(10,hipbase),(15,(0,0,.88)),(20,hipbase)],'location')
    bow=kind in ['archer','goblin_archer']; caster=kind in ['mage','healer','shaman','shadow_mage']
    action(arms[1],'Attack',[(1,(0,0,0)),(8,(-1.3 if not bow else -1.0,0,.2)),(13,(.5 if not caster else -.7,0,-.5)),(24,(0,0,0))]);action(arms[0],'Attack',[(1,(0,0,0)),(8,(-.8,0,-.15)),(13,(-.5,0,.05)),(24,(0,0,0))]);action(body,'Attack',[(1,(0,0,0)),(8,(0,0,-.18)),(13,(.16,0,.25)),(24,(0,0,0))])
    action(hip,'Death',[(1,hipbase),(12,(0,0,.45)),(25,(0,0,.18))],'location');action(hip,'Death',[(1,(0,0,0)),(12,(0,.2,.15)),(25,(math.pi/2,.1,.15))]);
    for o in arms+legs:action(o,'Death',[(1,(0,0,0)),(25,(.35,0,.4 if 'R' in o.name else -.4))])
def descendants(root):return [root]+list(root.children_recursive)
def optimize(root):
    material=mat('Character Vertex Palette',(1,1,1),0,.65)
    nodes=material.node_tree.nodes
    if not nodes.get('Model Colors'):
        attr=nodes.new('ShaderNodeVertexColor');attr.name='Model Colors';attr.layer_name='Color';material.node_tree.links.new(attr.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
    parents={}
    for o in descendants(root):
        if o.type!='MESH':continue
        colors=o.data.vertex_colors.new(name='Color')
        for poly in o.data.polygons:
            color=o.data.materials[poly.material_index].diffuse_color
            for i in poly.loop_indices:colors.data[i].color=color
            poly.material_index=0
        o.data.materials.clear();o.data.materials.append(material);parents.setdefault(o.parent,[]).append(o)
    for parent,parts in parents.items():
        bpy.ops.object.select_all(action='DESELECT')
        for o in parts:o.select_set(True)
        bpy.context.view_layer.objects.active=parts[0]
        if len(parts)>1:bpy.ops.object.join()
def export(root,path,anim=True):
    bpy.ops.object.select_all(action='DESELECT')
    for o in descendants(root):o.select_set(True)
    bpy.context.view_layer.objects.active=root
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=anim,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_materials='EXPORT',export_force_sampling=True,export_frame_range=False)
types=['sword','archer','shield','spear','mage','healer','goblin','goblin_archer','orc','shaman','goblin_king','shadow_mage']
for kind in types:
    root=character(kind);optimize(root);animate(kind)
    for o in descendants(root):
        if o.animation_data:
            for tr in o.animation_data.nla_tracks:tr.mute=True
    bpy.context.scene.frame_set(1);export(root,os.path.join(models,kind+'.glb'))
    root.hide_render=True;root.hide_viewport=True
    for o in descendants(root):o.hide_render=True
# Render original portraits, including locked units, for the squad cards.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=256;scene.render.resolution_y=320;scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene.world.color=(.25,.25,.25)
bpy.ops.object.camera_add(location=(3.6,-6,3.3));cam=bpy.context.object;cam.name='Portrait Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.8;cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
for loc,power,size in [((-3,-4,6),700,4),((3,0,5),900,3),((0,4,4),700,3)]:bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler()
for kind,root in roots.items():
    for o in descendants(root):o.hide_render=False
    for o in descendants(root):
        if o.animation_data:
            for tr in o.animation_data.nla_tracks:tr.mute=tr.name!='Idle'
    scene.frame_set(1)
    cam.data.ortho_scale=4 if kind in ['goblin_king','shadow_mage'] else 3.1 if kind=='orc' else 2.8
    scene.render.filepath=os.path.join(portraits,kind+'.png');bpy.ops.render.render(write_still=True)
    for o in descendants(root):o.hide_render=True
    for o in descendants(root):
        if o.animation_data:
            for tr in o.animation_data.nla_tracks:tr.mute=True
# Editable lineup with all original models and animation tracks retained.
for i,(kind,root) in enumerate(roots.items()):
    root.location=(i%6*3.5,i//6*4,0);root.hide_render=False;root.hide_viewport=False
    for o in descendants(root):o.hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(project,'art','ink-march-characters.blend'))
manifest={k:{'model':'/assets/models/'+k+'.glb','portrait':'/assets/portraits/'+k+'.png','animations':['Idle','Walk','Attack','Death']} for k in types}
with open(os.path.join(assets,'characters.json'),'w') as f:json.dump(manifest,f,indent=2)
print('INK_MARCH_ASSETS_COMPLETE')
