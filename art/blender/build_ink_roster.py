"""Complete the approved Ink Sprite roster using real Blender geometry."""
from pathlib import Path
import sys,re
base=Path(__file__).parent
original=(base/'build_ink_sprite.py').read_text(encoding='utf-8')
pre=original.split('merge(root)')[0]
red=[(.34,.035,.035),(.62,.065,.045),(.82,.13,.075),(.025,.045,.06),(.82,.73,.55),(.96,.89,.72),(.63,.39,.13),(.91,.66,.25),(.19,.10,.055),(.37,.23,.11),(.43,.055,.045),(.79,.43,.19),(.52,.11,.075),(.23,.06,.055),(.075,.12,.14),(.94,.77,.43)]
roles=['archer','shield','spear','mage','healer','goblin','goblin_archer','orc','shaman']
manifest={}
for role in roles:
    code=pre.replace('ink-sprite-prototype','ink-roster-v1')
    if role in roles[5:]:code=re.sub(r'palette=\[.*?\]\nsource=re.sub',lambda m:'palette='+repr(red)+'\nsource=re.sub',code,flags=re.S)
    exec(compile(code,'ink_sprite_base','exec'))
    root.name=role
    # Remove the swordsman's weapon while retaining the same cloth, mask and rig.
    for obj in list(descendants(weapon))[::-1]:bpy.data.objects.remove(obj,do_unlink=True)
    def rod(name,parent,a,b,r,index=7):return tube(name,parent,[a,b],[r,r],index,10)
    def emblem(parent,y,z,index=7):
        pts=[]
        for i in range(10):
            a=math.pi/2+i*math.pi/5;r=.23 if i%2==0 else .10;pts.append((math.cos(a)*r,z+math.sin(a)*r))
        o=blade('Role star badge',parent,pts,index);o.location.y=y
    def bow(parent):
        w=empty('Curved inkwood longbow',parent,(-.07,-.25,-.20))
        pts=[(.22*math.sin(i/20*math.pi),0,-.63+i/20*1.60) for i in range(21)]
        tube('Gold sculpted bow limbs',w,pts,[.035+.03*math.sin(i/20*math.pi) for i in range(21)],7,10)
        rod('Bow string',w,pts[0],pts[-1],.012,5)
        rod('Nocked arrow',w,(-.32,-.035,.15),(.49,-.035,.15),.018,8)
        tip=blade('Arrow ink point',w,[(.47,.10),(.64,.15),(.47,.20)],3);tip.location.y=-.035
        q=empty('Back quiver',body,(.34,.43,.18));q.rotation_euler.y=-.25
        shape('Leather quiver','cylinder',q,(0,0,0),(.30,.30,.65),8)
        for x in [-.07,.02,.09]:
            rod('Arrow in quiver',q,(x,0,.15),(x,0,.70),.014,8)
            feather=blade('Cream arrow fletching',q,[(x-.04,.54),(x,.72),(x+.04,.65),(x+.04,.53)],5)
        return w
    if role in ['archer','goblin_archer']:
        bow(arms[0]);emblem(body,-.39,.24)
        tube('Long folded ranger hood',head,[(0,.10,.52),(.13,.16,.78),(.39,.20,.88),(.59,.20,.70)],[.27,.21,.13,.008],1,14)
    elif role=='shield':
        w=empty('Tower shield',arms[0],(-.09,-.34,-.22))
        pts=[(-.43,.55),(.43,.55),(.48,.18),(.35,-.48),(0,-.67),(-.35,-.48),(-.48,.18)]
        blade('Gold shield rim',w,pts,7)
        blade('Teal convex shield',w,[(x*.85,z*.85) for x,z in pts],0).location.y=-.09
        emblem(w,-.16,.02)
        shape('Round shoulder armor','ball',arms[1],(0,0,.08),(.57,.54,.40),4)
        tube('Helmet crest',head,[(0,.15,.58),(0,.08,.82),(0,-.09,.91),(0,-.22,.79)],[.10,.10,.09,.025],7,10)
        rod('Short guard baton',arms[1],(.12,-.1,-.52),(.12,-.1,.23),.065,3)
    elif role=='spear':
        w=empty('Long brush spear',arms[0],(-.09,-.19,-.20));w.rotation_euler.y=-.10
        rod('Long wooden shaft',w,(0,0,-.65),(0,0,1.53),.043,8)
        blade('Gold spear border',w,[(-.14,1.46),(0,1.99),(.14,1.46),(0,1.32)],7)
        blade('Dark ink spearhead',w,[(-.095,1.49),(0,1.87),(.095,1.49),(0,1.39)],3).location.y=-.06
        tube('Pennant',w,[(.02,.04,1.34),(.26,.06,1.27),(.36,.07,1.11)],[.08,.075,.008],2,10)
        emblem(body,-.40,.29)
    elif role in ['mage','healer','shaman']:
        w=empty('Casting staff',arms[0],(-.12,-.15,-.17))
        rod('Wooden staff',w,(0,0,-.65),(0,0,1.18),.05,8)
        if role=='mage':
            tube('Soft bent wizard hat',head,[(0,.06,.48),(0,.07,.73),(.04,.08,1.00),(.23,.10,1.24),(.43,.10,1.20)],[.46,.34,.22,.09,.008],0,20)
            ring('Gold hatband',head,(0,0,.65),.35,.11,.028,7)
            ring('Orb gold setting',w,(0,0,1.22),.19,.22,.035,7)
            shape('Ink magic orb','ball',w,(0,0,1.24),(.30,.30,.34),13)
            for x,z in [(-.22,1.51),(.21,1.37)]:shape('Orbiting ink beads','ball',w,(x,0,z),(.10,.10,.12),3)
        elif role=='healer':
            ring('Flower healer hoodband',head,(0,-.03,.49),.54,.14,.045,5)
            for i in range(5):
                a=i*math.tau/5
                shape('Cream healing petals','ball',w,(math.cos(a)*.19,-.02,1.25+math.sin(a)*.19),(.23,.13,.25),5)
            shape('Gold flower center','ball',w,(0,-.13,1.25),(.23,.12,.23),7)
            shape('Medicine satchel','box',body,(.41,-.22,-.22),(.35,.23,.38),4)
            shape('Medicine plus vertical','box',body,(.41,-.35,-.21),(.05,.04,.18),0)
            shape('Medicine plus horizontal','box',body,(.41,-.35,-.21),(.18,.04,.05),0)
        else:
            for side in [-1,1]:
                tube('Shaman branching antler',head,[(side*.38,.08,.45),(side*.63,.10,.73),(side*.72,.10,.98)],[.07,.055,.015],4,10)
                tube('Antler branch',head,[(side*.59,.10,.70),(side*.86,.10,.76)],[.055,.008],4,8)
            ring('Ritual staff hoop',w,(0,0,1.26),.22,.25,.047,7)
            shape('Hanging ink charm','ball',w,(0,0,1.24),(.20,.16,.29),3)
            for x in [-.20,.20]:rod('Talisman ribbon',w,(x,0,1.08),(x*.80,0,.83),.035,5)
    else:
        # Enemy light melee and bruiser keep the mask identity, red cloth and dark ink limbs.
        w=empty('Enemy weapon',arms[0],(-.10,-.20,-.18))
        if role=='orc':
            body.scale=(1.22,1.16,1.15);arms[0].location.x=-.64;arms[1].location.x=.64
            rod('Axe dark handle',w,(0,0,-.22),(0,0,1.04),.065,8)
            blade('Broad gold axe outline',w,[(-.05,.94),(-.40,1.08),(-.47,.56),(-.13,.60),(0,.73),(.16,.68),(.31,.59),(.42,.71),(.36,1.05),(.10,1.04)],7)
            blade('Black ink axe face',w,[(-.10,.91),(-.34,1.0),(-.39,.65),(-.15,.68),(.02,.83),(.27,.78),(.30,.96)],3).location.y=-.07
            for side in [-1,1]:tube('Short ivory horn',head,[(side*.41,.08,.49),(side*.58,.08,.72),(side*.64,.06,.85)],[.12,.08,.008],4,12)
            shape('Heavy shoulder pad','ball',arms[1],(0,0,.16),(.67,.61,.44),3)
        else:
            rod('Dagger handle',w,(0,0,-.05),(0,0,.24),.055,8)
            blade('Gold dagger edge',w,[(-.12,.20),(.12,.20),(.08,.62),(-.08,.91),(-.15,.58)],7)
            blade('Ink dagger',w,[(-.07,.24),(.07,.24),(.03,.60),(-.075,.80),(-.09,.55)],3).location.y=-.06
        ring('Crimson headband',head,(0,-.04,.40),.58,.20,.038,1)
    # Long cloth points on light enemies retain the approved sprite silhouette.
    if role in ['goblin','goblin_archer']:
        for side in [-1,1]:tube('Long goblin hood ears',head,[(side*.46,.05,.28),(side*.72,.08,.41),(side*.91,.10,.58)],[.12,.08,.008],0,12)
    merge(root)
    for o in descendants(root):
        if o.type=='MESH' and len(o.data.polygons)>250:
            bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Mobile silhouette budget','DECIMATE');mod.ratio=.60;bpy.ops.object.modifier_apply(modifier=mod.name)
    bind={o:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy()) for o in descendants(root)}
    animation((hip,body,head,arms,feet))
    # Each ranged role gets an actual draw/release or cast motion instead of a sword swing.
    if role in ['archer','goblin_archer','mage','healer','shaman','spear','shield']:
        for obj in [body]+arms:
            tr=obj.animation_data.nla_tracks.get('Attack')
            if tr:obj.animation_data.nla_tracks.remove(tr)
            loc=tuple(obj.location)
            if role in ['archer','goblin_archer']:
                turns=[(1,(0,0,0)),(7,(-.25,0,-.14 if obj==arms[0] else .42)),(13,(-.25,0,-.14 if obj==arms[0] else .42)),(16,(.05,0,0)),(28,(0,0,0))]
            elif role in ['mage','healer','shaman']:
                turns=[(1,(0,0,0)),(10,(-.55,0,-.16) if obj in arms else (.06,0,-.08)),(16,(.12,0,.15) if obj in arms else (-.06,0,.08)),(30,(0,0,0))]
            else:turns=[(1,(0,0,0)),(8,(.22,0,-.12)),(13,(-.45,0,.08)),(25,(0,0,0))]
            clip(obj,'Attack',{'rotation_euler':turns,'location':[(1,loc),(13,(loc[0],loc[1]-.19,loc[2])),(30,loc)]})
    bpy.context.scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for o in descendants(root):o.select_set(True)
    bpy.context.view_layer.objects.active=root
    path=Path(out)/(role+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_frame_range=False)
    data=path.read_bytes();n=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+n]);tris=sum(doc['accessors'][p['indices']]['count']//3 for m in doc['meshes'] for p in m['primitives'])
    assert tris<16000 and len(doc['materials'])==1,(role,tris)
    manifest[role]={'triangles':tris,'meshes':len(doc['meshes']),'materials':len(doc['materials']),'animations':[a['name'] for a in doc['animations']],'bytes':len(data)}
    # Save the animated editable source before resetting the evaluated channels for portraits.
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(art)/(role+'.blend')))
    for o,(loc,rot,scale) in bind.items():o.animation_data_clear();o.location=loc;o.rotation_euler=rot;o.scale=scale
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.world.color=(.24,.25,.22);scene.view_settings.view_transform='Standard';scene.render.film_transparent=True
    scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
    for loc,power,size in [((-3,-4,7),500,5),((4,-2,4),180,4),((0,4,6),250,4)]:
        bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;o.rotation_euler=(Vector((0,0,1.4))-o.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.camera_add(location=(3,-7,3.5));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=4.25;cam.rotation_euler=(Vector((0,0,1.5))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
    scene.render.filepath=str(Path(portraits)/(role+'.png'));bpy.ops.render.render(write_still=True)
    Path(art,'manifest.json').write_text(json.dumps(manifest,indent=2))
    print('ROSTER_ASSET',role,json.dumps(manifest[role]),flush=True)
print('ROSTER_COMPLETE',json.dumps(manifest),flush=True)
