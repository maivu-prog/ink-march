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
    if kind=='ball':bpy.ops.mesh.primitive_uv_sphere_add(segments=24 if name in ['Round bean tunic','Big round face'] else 12,ring_count=14 if name in ['Round bean tunic','Big round face'] else 8,radius=.5)
    elif kind=='cone':bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.5,radius2=0,depth=1)
    elif kind=='cylinder':bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.5,depth=1)
    else:bpy.ops.mesh.primitive_cube_add(size=1)
    o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=scale;o.rotation_euler=rot;color(o,index)
    if kind not in ['ball','cone','cylinder']:
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        mod=o.modifiers.new('Soft toy edges','BEVEL');mod.width=min(scale)*.24;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
        mod=o.modifiers.new('Weighted toy normals','WEIGHTED_NORMAL');mod.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    for face in o.data.polygons:face.use_smooth=kind=='ball' or (kind in ['cone','cylinder'] and abs(face.normal.z)<.95)
    return o
def poly(name,parent,verts,faces,index):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.parent=parent;return color(o,index)
def dome(name,parent,index,rx=.60,ry=.54,rz=.57):
    verts=[];segments=24;rings=8
    for j in range(rings+1):
        theta=j/rings*math.pi/2
        for i in range(segments):a=i/segments*math.tau;verts.append((rx*math.sin(theta)*math.cos(a),ry*math.sin(theta)*math.sin(a),rz*math.cos(theta)))
    faces=[]
    for j in range(rings):
        for i in range(segments):n=(i+1)%segments;faces.append((j*segments+i,(j+1)*segments+i,(j+1)*segments+n,j*segments+n))
    o=poly(name,parent,verts,faces,index)
    for face in o.data.polygons:face.use_smooth=True
    return o
def blade(name,parent,points,index):
    n=len(points);verts=[(x,-.04,z) for x,z in points]+[(x,.04,z) for x,z in points];faces=[tuple(range(n)),tuple(range(n*2-1,n-1,-1))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];o=poly(name,parent,verts,faces,index)
    bpy.context.view_layer.objects.active=o;o.select_set(True)
    mod=o.modifiers.new('Rounded blade edge','BEVEL');mod.width=.023;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=o.modifiers.new('Blade face normals','WEIGHTED_NORMAL');mod.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o
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
        # Preserve the smooth surfaces and flat weapon faces authored on each part.
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
