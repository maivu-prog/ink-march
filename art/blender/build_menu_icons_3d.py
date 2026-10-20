"""Actual Blender toy props for the game's five menu destinations."""
from pathlib import Path
common=Path(__file__).with_name('build_ink_sprite.py').read_text(encoding='utf-8').split("root=empty('Ink_Sprite_Swordsman')")[0].replace('ink-sprite-prototype','menu-toys-v3')
exec(compile(common,'menu_helpers','exec'))
bs.inputs['Roughness'].default_value=.52
def ball(name,parent,loc,size,index):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,radius=.5)
    o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc;o.scale=size;color(o,index)
    for p in o.data.polygons:p.use_smooth=True
    return o
def torus(parent,loc,r,thick,index,rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=12,major_radius=r,minor_radius=thick)
    o=bpy.context.object;o.parent=parent;o.location=loc;o.rotation_euler=rot;color(o,index)
    for p in o.data.polygons:p.use_smooth=True
    return o
def star(parent,loc,r,index=7):
    pts=[]
    for i in range(10):a=math.pi/2+i*math.pi/5;d=r if i%2==0 else r*.46;pts.append((math.cos(a)*d,math.sin(a)*d))
    o=blade('Thick star',parent,pts,index);o.location=loc
    return o
def chest():
    root=empty('summon')
    shape('Rounded wooden treasure chest','box',root,(0,0,.48),(1.75,1.10,.87),9)
    shape('Golden front plate','box',root,(0,-.55,.45),(1.76,.10,.61),6)
    shape('Front walnut inset','box',root,(0,-.62,.45),(1.46,.05,.43),9)
    for x in [-.69,.69]:shape('Broad gold band','box',root,(x,-.65,.50),(.18,.08,.72),7)
    shape('Deep open interior','box',root,(0,0,.90),(1.48,.89,.10),3)
    lid=empty('Open curved lid',root,(0,.46,.89));lid.rotation_euler.x=-.65
    shape('Round chest lid','box',lid,(0,-.49,.16),(1.85,1.10,.40),6)
    shape('Caramel lid panel','box',lid,(0,-.49,.38),(1.56,.78,.10),9)
    for x in [-.69,.69]:shape('Lid gold strap','box',lid,(x,-.49,.40),(.18,1.00,.13),7)
    shape('Gold latch','box',root,(0,-.73,.57),(.39,.13,.42),7)
    ball('Teal lock jewel',root,(0,-.82,.60),(.14,.09,.17),1)
    star(root,(.53,-.80,1.68),.23,5);star(root,(-.65,-.50,1.48),.12,7)
    return root,1.02,2.70
def brush():
    root=empty('brushes');w=empty('Brush body',root,(0,0,.12));w.rotation_euler.y=.45
    shape('Warm wooden handle','cylinder',w,(0,0,1.54),(.34,.34,1.08),6)
    ball('Rounded brush end',w,(0,0,2.08),(.34,.34,.34),6)
    shape('Gold ferrule','cylinder',w,(0,0,.91),(.57,.57,.47),7)
    for z in [.75,1.08]:torus(w,(0,0,z),.285,.045,6)
    tube('Sculpted ink bristles',w,[(0,0,.72),(-.01,-.015,.48),(-.11,-.04,.23),(-.26,-.08,.09)],[.285,.31,.22,.008],1,24)
    tube('Bristle highlight',w,[(-.17,-.25,.62),(-.20,-.28,.45),(-.28,-.20,.25)],[.018,.025,.008],13,10)
    tube('Wet ink stroke',root,[(-.82,-.23,.02),(-.61,-.20,.11),(-.28,-.18,.12),(.10,-.16,.04),(.48,-.12,.12),(.79,-.08,.23)],[.04,.075,.09,.085,.06,.008],1,16)
    ball('Ink bead',root,(-.82,-.23,.02),(.14,.14,.10),1)
    return root,1.04,2.75
def swords():
    root=empty('battle')
    for side in [-1,1]:
        w=empty('Crossed sword',root,(side*.24,side*.10,.92));w.rotation_euler.y=side*.67
        shape('Leather grip','cylinder',w,(0,0,-.63),(.20,.20,.52),8)
        ball('Gold pommel',w,(0,0,-.94),(.32,.30,.27),7)
        for z in [-.76,-.63,-.50]:torus(w,(0,0,z),.105,.018,6)
        tube('Swept crossguard',w,[(-.36,0,-.25),(-.18,-.01,-.32),(0,-.02,-.30),(.18,-.01,-.32),(.36,0,-.25)],[.065,.07,.08,.07,.065],7,14)
        pts=[(-.23,-.23),(.23,-.23),(.24,.79),(0,1.15),(-.24,.79)]
        blade('Broad gold blade rim',w,pts,6)
        for depth in [-.07,.07]:
            o=blade('Ivory blade face',w,[(x*.78,(z+.23)*.96-.20) for x,z in pts],5);o.location.y=depth
        tube('Blade center ridge',w,[(0,-.13,-.14),(0,-.13,.72),(0,-.08,1.04)],[.018,.018,.001],4,8)
    return root,.99,2.92
def squad():
    root=empty('squad')
    # Use the actual approved troop head, rather than drawing a substitute face.
    old=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath='D:/Bagelcode/GameJam/ink-march/public/assets/models/ink-sprite-prototype/sword.glb')
    imported=set(bpy.data.objects)-old
    head=next(o for o in imported if o.name.startswith('Sprite_Head') and o.type=='EMPTY')
    source=[head]+list(head.children_recursive)
    for obj in imported:obj.hide_render=True
    for i,(x,y,z) in enumerate([(-.47,.15,.98),(.43,-.23,.88)]):
        copies={}
        for obj in source:
            cp=obj.copy()
            if obj.data:cp.data=obj.data.copy()
            bpy.context.collection.objects.link(cp);copies[obj]=cp;cp.hide_render=False
        for obj,cp in copies.items():cp.parent=copies.get(obj.parent,root)
        h=copies[head];h.location=(x,y,z);h.scale=(1,1,1);h.rotation_euler=(0,0,.08 if i==0 else -.10)
        ball('Rounded teal shoulder',root,(x,y,z-.58),(1.09,.66,.47),1)
        shape('Gold scarf clasp','cylinder',root,(x,y-.36,z-.54),(.22,.22,.09),7,rot=(math.pi/2,0,0))
    return root,.92,2.82
def training():
    root=empty('training')
    shape('Wood post','box',root,(0,.18,.49),(.17,.22,.92),8)
    for x in [-.29,.29]:shape('Sturdy wooden foot','box',root,(x,.10,.09),(.67,.39,.16),9,rot=(0,0,-.20 if x<0 else .20))
    shape('Thick round target','cylinder',root,(0,.07,1.20),(1.73,1.73,.28),8,rot=(math.pi/2,0,0))
    shape('Cream target face','cylinder',root,(0,-.10,1.20),(1.55,1.55,.07),5,rot=(math.pi/2,0,0))
    torus(root,(0,-.17,1.20),.58,.075,6,rot=(math.pi/2,0,0))
    shape('Teal bullseye','cylinder',root,(0,-.18,1.20),(.52,.52,.07),1,rot=(math.pi/2,0,0))
    w=empty('Practice sword',root,(.43,-.38,.82));w.rotation_euler.y=.65
    shape('Wooden practice blade','box',w,(0,0,.35),(.19,.13,1.26),9)
    ball('Rounded practice blade tip',w,(0,0,.98),(.19,.13,.18),9)
    shape('Wooden blade bevel','box',w,(-.04,-.08,.37),(.05,.03,1.10),6)
    shape('Gold wrapped grip','cylinder',w,(0,0,-.54),(.17,.17,.38),6)
    shape('Cream crossguard','box',w,(0,0,-.28),(.59,.21,.15),7)
    ball('Practice sword pommel',w,(0,0,-.76),(.25,.22,.20),7)
    return root,1.01,2.86
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True;scene.world.color=(.25,.26,.25);scene.view_settings.view_transform='Standard';scene.render.film_transparent=True;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
bpy.ops.object.camera_add(location=(3,-9,4.2));cam=bpy.context.object;cam.data.type='ORTHO';scene.camera=cam
for loc,power,size in [((-3,-4,7),440,4),((4,-2,4),160,4),((0,3,5),220,4)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
for build in [chest,brush,swords,squad,training]:
    if 'battle-only' in sys.argv and build!=swords:continue
    for obj in bpy.data.objects:
        if obj.type in ['MESH','EMPTY']:obj.hide_render=True
    root,center,scale=build()
    for obj in descendants(root):obj.hide_render=False
    cam.location=(2.3,-9,3.5) if build==squad else (3,-9,4.2);cam.rotation_euler=(Vector((0,0,center))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    bpy.context.view_layer.update();scene.render.filepath=os.path.join(portraits,root.name+'.png');bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art,root.name+'.blend'))
    print('MENU_RENDER',root.name,flush=True)
