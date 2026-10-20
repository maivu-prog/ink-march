"""One actual Blender/GLB Ink Sprite prototype; no production asset replacement."""
from pathlib import Path
import re
source=Path('D:/Bagelcode/GameJam/ink-march/art/blender/bean_soft_helpers.py').read_text(encoding='utf-8')
source=source.replace("'models','simple'","'models','ink-sprite-prototype'").replace("'portraits','simple'","'portraits','ink-sprite-prototype'").replace("'art','simple-pilots'","'art','ink-sprite-prototype'")
palette=[(.035,.24,.27),(.055,.37,.41),(.10,.46,.48),(.025,.075,.10),(.91,.84,.65),(.97,.91,.74),(.76,.49,.16),(.94,.71,.31),(.20,.12,.07),(.38,.25,.12),(.14,.29,.30),(.48,.62,.52),(.15,.43,.38),(.31,.62,.63),(.07,.16,.20),(.55,.73,.73)]
source=re.sub(r'COLORS=\[.*?\]\natlas=',lambda m:'COLORS='+repr(palette)+'\natlas=',source,flags=re.S)
exec(compile(source,'bean_soft_helpers.py','exec'))

def tube(name,parent,points,radii,index,sides=12):
    vs=[]
    for k,p in enumerate(points):
        tangent=Vector(points[min(k+1,len(points)-1)])-Vector(points[max(0,k-1)])
        tangent.normalize();normal=tangent.cross(Vector((0,1,0)))
        if normal.length<.01:normal=tangent.cross(Vector((1,0,0)))
        normal.normalize();other=tangent.cross(normal).normalized()
        for j in range(sides):vs.append(tuple(Vector(p)+(normal*math.cos(j/sides*math.tau)+other*math.sin(j/sides*math.tau))*radii[k]))
    faces=[]
    for k in range(len(points)-1):
        for j in range(sides):n=(j+1)%sides;faces.append((k*sides+j,k*sides+n,(k+1)*sides+n,(k+1)*sides+j))
    faces.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))])
    o=poly(name,parent,vs,faces,index)
    for f in o.data.polygons:f.use_smooth=True
    return o

def ring(name,parent,loc,rx,rz,r,index):
    p=[(loc[0]+rx*math.cos(i/32*math.tau),loc[1],loc[2]+rz*math.sin(i/32*math.tau)) for i in range(33)]
    return tube(name,parent,p,[r]*33,index,8)

root=empty('Ink_Sprite_Swordsman')
hip=empty('Sprite_Hips',root,(0,0,.30));body=empty('Sprite_Body',hip,(0,0,.65));head=empty('Sprite_Head',hip,(0,-.015,1.55))
arms=[empty('Sprite_SwordArm',body,(-.57,-.005,.24)),empty('Sprite_OffArm',body,(.55,-.01,.22))]
feet=[empty('Sprite_FootL',hip,(-.25,-.07,-.13)),empty('Sprite_FootR',hip,(.25,-.07,-.13))]

shape('Round bean tunic','ball',body,(0,.015,-.01),(1.02,.72,1.04),1)
shape('Dark inner tunic','ball',body,(0,-.04,-.13),(.86,.65,.90),0)
# A cloth bell hem with a subtly uneven edge, rather than a primitive cone.
vs=[];faces=[]
for j,(z,rx,ry) in enumerate([(-.54,.54,.37),(-.36,.54,.38),(-.10,.46,.34),(.17,.43,.32)]):
    for i in range(24):
        a=i/24*math.tau;vs.append((rx*math.cos(a),ry*math.sin(a),z+(.035*math.cos(3*a) if j==0 else 0)))
for j in range(3):
    for i in range(24):n=(i+1)%24;faces.append((j*24+i,j*24+n,(j+1)*24+n,(j+1)*24+i))
tunic=poly('Flared cloth tunic',body,vs,faces,1)
for f in tunic.data.polygons:f.use_smooth=True
solid=tunic.modifiers.new('Cloth thickness','SOLIDIFY');solid.thickness=.026
bpy.context.view_layer.objects.active=tunic;bpy.ops.object.modifier_apply(modifier=solid.name)

for n,foot in enumerate(feet):
    shape('Ink boot','ball',foot,(0,-.08,.01),(.39,.57,.34),3)
    shape('Boot cuff','ball',foot,(0,.015,.14),(.31,.33,.35),14)
for arm in arms:
    shape('Cream rolled sleeve','ball',arm,(0,0,-.06),(.40,.40,.45),4)
    shape('Teal shoulder wrap','ball',arm,(0,.015,.12),(.46,.40,.31),0)
    shape('Ink mitten','ball',arm,(-.055 if arm==arms[0] else .055,-.06,-.25),(.32,.34,.37),3)
    shape('Cream cuff','cylinder',arm,(0,-.015,-.15),(.34,.34,.13),5)

# Tailored cape: broad folds, thick edge, its silhouette flares behind the feet.
vs=[];faces=[]
for j in range(7):
    t=j/6
    for i in range(11):
        u=i/10*2-1;vs.append((u*(.35+t*.42)+.12*t*t,.29+t*.34+.055*math.cos(u*math.pi*3)*t,.47-t*1.02+.065*math.cos(u*math.pi*2)*t))
for j in range(6):
    for i in range(10):a=j*11+i;faces.append((a,a+11,a+12,a+1))
cape=poly('Sculpted short cape',body,vs,faces,0)
for f in cape.data.polygons:f.use_smooth=True
for typ in ['SOLIDIFY','SUBSURF']:
    mod=cape.modifiers.new('Soft cape '+typ,typ)
    if typ=='SOLIDIFY':mod.thickness=.035
    else:mod.levels=1
    bpy.context.view_layer.objects.active=cape;bpy.ops.object.modifier_apply(modifier=mod.name)
for k in [-.65,0,.65]:
    tube('Cape fold',body,[(k*.33,.32,.43),(k*.45+.02,.48,-.02),(k*.64+.09,.63,-.48)],[.025,.035,.014],1,8)

# A hollow, continuous hood shell with a real face opening.
vs=[];faces=[];segments=32;rings=13
for j in range(rings+1):
    theta=.98+(math.pi-.98)*j/rings
    for i in range(segments):
        a=i/segments*math.tau;sn=math.sin(theta);x=.70*sn*math.cos(a);z=.66*sn*math.sin(a)
        z+=max(0,math.sin(a))*.085*sn;x-=.065*max(0,math.sin(a))*sn
        vs.append((x,-.55*math.cos(theta),z+.035))
for j in range(rings):
    for i in range(segments):n=(i+1)%segments;faces.append((j*segments+i,(j+1)*segments+i,(j+1)*segments+n,j*segments+n))
hood=poly('Hollow teal cloth hood',head,vs,faces,1)
for f in hood.data.polygons:f.use_smooth=True
mod=hood.modifiers.new('Hood lining thickness','SOLIDIFY');mod.thickness=.034
bpy.context.view_layer.objects.active=hood;bpy.ops.object.modifier_apply(modifier=mod.name)
opening=vs[:segments]+[vs[0]];tube('Rolled hood opening',head,opening,[.043]*len(opening),0,8)
shape('Dark face recess','ball',head,(0,-.275,.025),(1.15,.28,1.22),3)
shape('Big round face','ball',head,(0,-.365,.035),(1.01,.235,1.11),5)
for side in [-1,1]:
    eye=shape('Brushstroke eye','ball',head,(side*.185,-.489,.105),(.097,.026,.255),3,rot=(0,side*.14,0))
    # Distinct droplet tips remain visible from the game camera.
    tube('Ink drop hood tip',head,[(side*.42,.04,.49),(side*.51,.065,.67),(side*.58,.085,.83),(side*.59,.085,.96)],[.14,.125,.072,.008],3,12)
    tube('Hood shoulder fold',head,[(side*.43,-.27,-.25),(side*.56,-.12,-.36),(side*.49,.05,-.45)],[.04,.05,.015],0,8)
tube('Crown seam',head,[(-.03,-.27,.63),(-.05,.02,.73),(-.04,.29,.61),(0,.46,.30)],[.018,.022,.02,.008],2,8)

# Scarf and belt physically sit above the tunic.
scarf=shape('Wide soft scarf','ball',body,(0,-.005,.43),(1.02,.79,.30),0)
blade('Scarf front fold',body,[(-.46,.45),(.47,.48),(.20,.22),(-.12,.21)],1).location.y=-.39
points=[(.49*math.cos(i/32*math.tau),.345*math.sin(i/32*math.tau),-.07) for i in range(33)]
tube('Leather waist belt',body,points,[.054]*33,8,8)
ring('Gold ring buckle',body,(.08,-.388,-.07),.105,.112,.027,7)
shape('Buckle tongue','box',body,(.08,-.414,-.07),(.16,.025,.025),7)

# Broad asymmetric ink blade: genuine bevels, two-sided gold border, not a flat sprite.
weapon=empty('Ink blade',arms[0],(-.10,-.16,-.14));weapon.rotation_euler.y=-.30
shape('Leather sword handle','cylinder',weapon,(0,0,.10),(.13,.13,.31),8)
for z in [-.015,.09,.19]:ring('Grip wrap',weapon,(0,-.005,z),.064,.015,.012,9)
shape('Gold pommel','ball',weapon,(0,0,-.09),(.19,.18,.16),7)
tube('Swept gold guard',weapon,[(-.30,0,.29),(-.17,-.015,.235),(0,-.02,.25),(.17,-.015,.235),(.30,0,.29)],[.04,.055,.058,.055,.035],7,10)
outline=[(-.17,.31),(.17,.31),(.185,.53),(.09,.63),(.205,.76),(.17,.91),(.06,.99),(.18,1.12),(.10,1.34),(-.06,1.58),(-.22,1.36),(-.15,1.17),(-.23,1.05),(-.19,.87),(-.12,.77),(-.22,.64),(-.19,.47)]
blade('Warm gold blade border',weapon,outline,7)
inner=[(x*.80,(z-.31)*.94+.34) for x,z in outline]
for side in [-1,1]:
    o=blade('Black liquid ink blade',weapon,inner,3);o.location.y=side*.057
# Quiet inset glints describe the dark blade without emissive effects.
blade('Ink blade reflection',weapon,[(-.115,.65),(-.035,.73),(-.08,1.10),(-.13,1.21),(-.12,1.02)],14).location.y=-.105

merge(root)
for o in descendants(root):
    if o.type=='MESH' and len(o.data.polygons)>200:
        bpy.context.view_layer.objects.active=o
        mod=o.modifiers.new('Mobile silhouette budget','DECIMATE');mod.ratio=.64
        bpy.ops.object.modifier_apply(modifier=mod.name)
bind_pose={o:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy()) for o in descendants(root)}
animation((hip,body,head,arms,feet));bpy.context.scene.frame_set(1)
bpy.ops.object.select_all(action='DESELECT')
for o in descendants(root):o.select_set(True)
bpy.context.view_layer.objects.active=root
glb=os.path.join(out,'sword.glb')
bpy.ops.export_scene.gltf(filepath=glb,export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_frame_range=False)
b=Path(glb).read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);triangles=sum(j['accessors'][p['indices']]['count']//3 for m in j['meshes'] for p in m['primitives'])
manifest={'triangles':triangles,'meshes':len(j['meshes']),'materials':len(j['materials']),'animations':[a['name'] for a in j.get('animations',[])],'glbBytes':len(b)}
Path(art,'manifest.json').write_text(json.dumps(manifest,indent=2))
assert triangles<14000,triangles

# glTF sampling leaves evaluated channels at the last clip's frame on Blender 4.5.
# The GLB bind nodes are correct; reset the authoring scene for still previews.
for o,(loc,rot,scale) in bind_pose.items():
    o.animation_data_clear();o.location=loc;o.rotation_euler=rot;o.scale=scale
bpy.context.view_layer.update()

# Actual Blender renders are included as model evidence, never AI concept renders.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True;scene.world.color=(.24,.27,.24)
scene.render.resolution_x=900;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard'
for loc,power,size in [((-3,-4,7),500,5),((4,-2,4),140,4),((0,4,6),250,4)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3,-7,3.3));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=3.9;scene.camera=cam
def camera_at(loc,target,scale):cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
scene.render.film_transparent=True
camera_at((3,-7,3.4),(0,0,1.38),3.8);scene.render.filepath=os.path.join(portraits,'sword.png');bpy.ops.render.render(write_still=True)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.02));ground=bpy.context.object;ground.name='Preview ground';mat=bpy.data.materials.new('Preview sage ground');mat.diffuse_color=(.43,.56,.37,1);ground.data.materials.append(mat)
scene.render.film_transparent=False
camera_at((3,-7,3.4),(0,0,1.38),3.9);scene.render.filepath=os.path.join(art,'close-front.png');bpy.ops.render.render(write_still=True)
camera_at((0,-7.5,9),(0,0,1.25),4.2);scene.render.filepath=os.path.join(art,'game-angle-front.png');bpy.ops.render.render(write_still=True)
camera_at((0,7.5,9),(0,0,1.25),4.2);scene.render.filepath=os.path.join(art,'game-angle-back.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art,'ink-sprite-swordsman.blend'))
print('INK_SPRITE_RESULT',json.dumps(manifest))
