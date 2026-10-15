"""Approved direction A: soft clay forest. Run with Blender --background --python ... -- output-root."""
import bpy, math, json, struct, sys
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1]); models=out/'models'; models.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
colors=['#5c906a','#6d9b63','#87ae71','#a2bd73','#867761','#a39d88','#b6b39d','#8a6245','#bc8b59','#dfb176','#bd4b37','#db6947','#ef8c59','#e7ce98','#f7e4b1','#41664b']
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
image=bpy.data.images.new('Clay palette',width=512,height=512,alpha=True)
pixels=[]
for y in range(512):
 for x in range(512):
  h=colors[(y//128)*4+x//128];pixels.extend([int(h[i:i+2],16)/255 for i in [1,3,5]]+[1])
image.pixels.foreach_set(pixels);image.filepath_raw=str(out/'palette.png');image.file_format='PNG';image.save();image.pack()
mat=bpy.data.materials.new('Matte clay');mat.use_nodes=True;n=mat.node_tree.nodes;tex=n.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Closest';bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.94;mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
def finish(o,name,loc,size,c,smooth=True):
 o.name=name;o.location=loc;o.scale=size;uv=o.data.uv_layers.active or o.data.uv_layers.new()
 for p in o.data.polygons:p.use_smooth=smooth
 for p in uv.data:p.uv=((c%4+.5)/4,(c//4+.5)/4)
 o.data.materials.clear();o.data.materials.append(mat);return o
def ball(name,loc,size,c):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10);return finish(bpy.context.object,name,loc,size,c)
def rod(name,a,b,r,c):
 a,b=Vector(a),Vector(b);bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=1,depth=2);o=finish(bpy.context.object,name,(a+b)/2,(r,r,(b-a).length/2),c);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def box(name,loc,size,c,bevel=.06):
 bpy.ops.mesh.primitive_cube_add(size=1);o=finish(bpy.context.object,name,loc,size,c,False);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);m=o.modifiers.new('Soft edges','BEVEL');m.width=bevel;m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name);finish(o,name,loc,(1,1,1),c,True);m=o.modifiers.new('Weighted toy normals','WEIGHTED_NORMAL');bpy.ops.object.modifier_apply(modifier=m.name);return o
def stone(x=0,y=0,s=1):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);o=bpy.context.object
 for v in o.data.vertices:
  v.co.x*=1+.08*math.sin(v.co.z*6+v.co.y*3);v.co.z=max(-.64,v.co.z)
 finish(o,'Soft river boulder',(x,y,.28*s),(.57*s,.47*s,.43*s),5)
 
 for dx,dy,r in [(-.18,.06,.22),(.02,.12,.24),(.15,.04,.17)]:ball('Soft moss lobe',(x+dx*s,y+dy*s,.61*s),(.22*s,r*s,.065*s),2)
def tree(round=False):
 rod('Squat trunk',(0,0,.03),(.04,.04,.74),.125,7)
 if round:
  for p,s,c in [((0,0,1.04),(.54,.48,.47),0),((-.30,-.03,.98),(.34,.36,.36),1),((.28,.04,1.14),(.38,.39,.39),1),((.0,-.13,1.34),(.35,.34,.31),2)]:ball('Cloud canopy',p,s,c)
 else:
  for p,s,c in [((0,0,.75),(.47,.43,.36),0),((.02,0,1.04),(.38,.35,.34),1),((-.02,0,1.30),(.27,.25,.31),1),((0,.015,1.52),(.15,.15,.24),2)]:ball('Soft pine crown',p,s,c)
def roof():
 # Lathed curved canvas roof, a low bell profile instead of a rigid cone.
 profile=[(.73,1.25),(.75,1.29),(.67,1.34),(.49,1.48),(.31,1.66),(.13,1.80),(.055,1.87),(0,1.90)];verts=[];N=24
 for r,z in profile:
  for i in range(N):
   a=i/N*math.tau;verts.append((math.cos(a)*r,math.sin(a)*r,z))
 faces=[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(profile)-1) for i in range(N)];mesh=bpy.data.meshes.new('Bell canopy');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Squishy red canopy',mesh);bpy.context.collection.objects.link(o);finish(o,o.name,(0,0,0),(1,1,1),11)
def tower():
 for x in [-.4,.4]:
  for y in [-.4,.4]:rod('Round timber leg',(x,y,0),(x*.94,y*.94,1.31),.085,7);ball('Wooden foot',(x,y,.06),(.13,.13,.08),8)
 for i in range(5):box('Deck plank',((i-2)*.20,0,.73),(.195,1.02,.12),8,.035)
 for y in [-.44,.44]:rod('Cross brace',(-.4,y,.1),(.4,y,.66),.04,9)
 for y in [-.5,.5]:rod('Broad rail',(-.51,y,1.06),(.51,y,1.06),.065,9)
 for x in [-.5,.5]:rod('Broad rail',(x,-.5,1.06),(x,.5,1.06),.065,9)
 roof();rod('Banner mast',(0,0,1.8),(0,0,2.18),.032,9);box('Red pennant',(.18,0,2.09),(.34,.035,.18),10,.035)
 # Oversized cloth on the front; the tower silhouette remains larger than a bean.
 box('Red front banner',(0,-.53,.86),(.36,.035,.38),10,.04);ball('Gold banner seal',(0,-.56,.87),(.09,.02,.09),14)
def bush():
 for x,y,z,s,c in [(-.18,0,.18,.26,0),(.18,.03,.22,.3,1),(0,-.11,.32,.29,2)]:ball('Round shrub',(x,y,z),(s,s*.85,s),c)
def mushroom():
 for x,y,s in [(-.14,0,1),(.19,.05,.7)]:
  rod('Cream stalk',(x,y,0),(x,y,.29*s),.07*s,14);ball('Red mushroom cap',(x,y,.30*s),(.25*s,.24*s,.13*s),11)
  for dx,dy in [(-.08,-.08),(.09,.03)]:ball('Cream spot',(x+dx*s,y+dy*s,.405*s),(.045*s,.045*s,.018*s),14)
def flower():
 rod('Short flower stalk',(0,0,0),(0,0,.12),.018,0)
 for i in range(5):a=i/5*math.tau;ball('Cream petal',(math.cos(a)*.08,math.sin(a)*.08,.14),(.055,.055,.025),14)
 ball('Gold flower heart',(0,0,.16),(.04,.04,.025),9)
assets=['tree','tree_round','rock','rock_cluster','tower','wall','bush','mushroom','flower']
manifest={}
for name in assets:
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 if name=='tree':tree()
 elif name=='tree_round':tree(True)
 elif name=='rock':stone()
 elif name=='rock_cluster':
  for x,y,s in [(-.25,.05,.9),(.31,.10,.65),(.05,-.27,.48)]:stone(x,y,s)
 elif name=='tower':tower()
 elif name=='wall':
  for z,xs in [(.13,[-.34,0,.34]),(.36,[-.25,.25])]:
   for x in xs:box('Soft stone brick',(x,0,z),(.32 if z<.2 else .49,.4,.24),5,.06)
  ball('Moss shoulder',(0,0,.5),(.46,.21,.055),2)
 elif name=='bush':bush()
 elif name=='mushroom':mushroom()
 elif name=='flower':flower()
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];bottom=min((o.matrix_world@Vector(v)).z for o in objects for v in o.bound_box) if False else 0
 bpy.context.view_layer.update();bottom=min((o.matrix_world@Vector(v)).z for o in objects for v in o.bound_box)
 for o in objects:o.location.z-=bottom
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();o=bpy.context.object;o.name=name;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 # Origin at ground zero and center horizontally, shared instancing contract.
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 bpy.ops.export_scene.gltf(filepath=str(models/(name+'.glb')),export_format='GLB',use_selection=True,export_animations=False)
 data=(models/(name+'.glb')).read_bytes();n=struct.unpack_from('<I',data,12)[0];j=json.loads(data[20:20+n]);tris=sum(j['accessors'][p['indices']]['count']//3 for m in j['meshes'] for p in m['primitives']);manifest[name]={'triangles':tris,'bytes':len(data)}
 bpy.ops.wm.save_as_mainfile(filepath=str(out/(name+'.blend')))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2));print('CLAY_V5_COMPLETE',manifest)
