"""Bean-world environment pack. Authoring unit = one bean soldier's height.
All new imagery is generated from geometry/periodic fields, with no external images.
"""
from pathlib import Path
source=Path(__file__).with_name('build_bean_squad_v2.py').read_text(encoding='utf-8-sig').split('\ndef make(kind):')[0]
source=source.replace("'bean-v2'","'env'").replace("'bean-squad-v2'","'environment-v4'")
source=source.replace('major_segments=16','major_segments=12')
exec(compile(source,str(Path(__file__).with_name('build_bean_squad_v2.py')),'exec'))
import numpy as np
budgets={'tower':1500,'rock':400,'rock_cluster':800,'tree':600,'tree_round':600,'wall':800,'gate_red':900,'gate_blue':900,'chest':600,'key_red':300,'key_blue':300,'flag_start':500,'flag_start_orange':500,'flag_clash':300,'pedestal':300,'bridge_gold':900,'hill':1200,'hill_large':1600,'slope_ramp':1000,'chasm':1500,'chasm_corner':1200,'cliff_edge':1200,'field_border':1500}

def rounded(name,parent,loc,size,c,bevel=.04):
    o=shape(name,'box',parent,loc,size,c);bpy.context.view_layer.objects.active=o
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    m=o.modifiers.new('Soft toy corners','BEVEL');m.width=bevel;m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name);color(o,c);return o

def ball(name,parent,loc,size,c):return shape(name,'ball',parent,loc,size,c)
def tube(name,parent,loc,size,c):return shape(name,'cylinder',parent,loc,size,c)
def face(name,parent,verts,c):return poly(name,parent,verts,[tuple(range(len(verts))),tuple(range(len(verts)-1,-1,-1))],c)

def stone(parent,loc=(0,0,0),s=1):
    g=empty('Mossy stone',parent,loc);g.scale=(s,s,s)
    o=ball('Round bean tunic',g,(0,0,.24),(1,.86,.60),3)
    for v in o.data.vertices:
        if v.co.z<-.40:v.co.z=-.40
    ball('Moss cap',g,(-.07,.04,.47),(.55,.48,.15),22);return g

def pine(parent):
    tube('Short chunky trunk',parent,(0,0,.29),(.24,.24,.58),5)
    for z,w,h,c in [(.64,1.0,.70,29),(1.01,.79,.68,22),(1.33,.53,.60,29)]:ball('Round bean tunic',parent,(0,0,z),(w,w*.93,h),c)

def goblin_emblem(parent,x,y,z,s=.15):
    ball('Green goblin emblem',parent,(x,y,z),(s*1.5,.03,s*1.3),9)
    for side in [-1,1]:
        face('Emblem ear',parent,[(x+side*s*.45,y-.02,z),(x+side*s*1.2,y-.02,z+s*.4),(x+side*s*.55,y-.02,z+s*.35)],9)
        ball('Emblem eye',parent,(x+side*s*.24,y-.025,z+s*.06),(s*.18,.02,s*.22),11)

def banner(parent,kind):
    clash=kind=='flag_clash';orange=kind=='flag_start_orange';c=13 if orange else 0
    if not clash:tube('Round rally pad',parent,(0,0,.04),(.87,.87,.08),c)
    h=.85 if clash else 1.70
    tube('Wooden pole',parent,(-.21,0,h/2),(.055,.055,h),5);ball('Gold pole tip',parent,(-.21,0,h+.03),(.11,.11,.11),12)
    verts=[]
    for i in range(5):
        x=-.20+i*.17;y=math.sin(i/4*math.pi)*.07
        verts.extend([(x,y,h-.10),(x,y,h-(.47 if not clash else .40))])
    poly('Waving cloth',parent,verts,[(i,i+1,i+3,i+2) for i in range(0,8,2)]+[(i+2,i+3,i+1,i) for i in range(0,8,2)],c)
    if clash:
        for side in [-1,1]:rod('Crossed sword emblem',parent,(.02-side*.11,-.035,h-.35),(.02+side*.11,-.035,h-.15),.018,6)
    else:face('White brush stroke',parent,[(-.02,-.035,h-.23),(.24,-.075,h-.20),(.29,-.075,h-.27),(.0,-.035,h-.31)],6)

def mound(parent,large=False):
    surface=empty('GrassSurface',parent)
    rx=2.5 if large else 1.5;rz=.3 if large else .2;segments=20;rings=6
    verts=[]
    for j in range(rings+1):
        r=j/rings;h=rz*(min(1,(1-r*r)*2.4) if large else 1-r*r)
        for i in range(segments):a=math.tau*i/segments;verts.append((rx*r*math.cos(a),rx*r*math.sin(a),h))
    poly('Low grassy mound',surface,verts,[(j*segments+i,(j+1)*segments+i,(j+1)*segments+(i+1)%segments,j*segments+(i+1)%segments) for j in range(rings) for i in range(segments)],22)
    if not large:
        stone(parent,(.72,.36,.075),.18)
        for x,y in [(-.55,.44),(.34,-.58)]:ball('Tiny pale flower',parent,(x,y,.16),(.09,.09,.025),6)

def ravine(parent,corner=False):
    # Open-topped, genuinely recessed meshes; unequal lips avoid a concrete-channel silhouette.
    base=[(-.5,-.5),(2,-.5),(2,.5),(.5,.5),(.5,2),(-.5,2)] if corner else [(-.5,-2),(.5,-2),(.5,2),(-.5,2)]
    caps=[1,4] if corner else [0,2];outline=[];wall_segments=[]
    for edge,a in enumerate(base):
        b=base[(edge+1)%len(base)];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);nx,ny=dy/length,-dx/length;count=max(1,round(length/.5));pts=[]
        for k in range(count+1):
            jitter=0 if k in [0,count] or edge in caps else math.sin(k*2.3+edge*1.7)*.065
            pts.append((a[0]+dx*k/count+nx*jitter,a[1]+dy*k/count+ny*jitter))
        outline.extend(pts[:-1])
        if edge not in caps:
            for k in range(count):wall_segments.append((pts[k],pts[k+1],nx,ny,k+edge))
    n=len(outline);verts=[(x,y,0) for x,y in outline]+[(x,y,-.6) for x,y in outline]
    poly('Deep open navy ravine',parent,verts,[tuple(range(n*2-1,n-1,-1))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],7)
    for a,b,nx,ny,k in wall_segments:
        v=[(a[0],a[1],.01),(b[0],b[1],.01),(b[0]+nx*.11,b[1]+ny*.11,.01),(a[0]+nx*.11,a[1]+ny*.11,.01)]
        v+=[(x,y,-.38) for x,y,z in v]
        poly('Uneven rock lip',parent,v,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],3)
        size=.20+(k%3)*.035;ball('Chunky lip stone',parent,((a[0]+b[0])/2+nx*.04,(a[1]+b[1])/2+ny*.04,.035),(size,size*.90,.13+(k%2)*.035),3)
    for a,b,nx,ny,k in wall_segments[::5]:face('Hanging root',parent,[(a[0],a[1],-.02),(a[0]+.02,a[1],-.02),(a[0]-nx*.04+.02,a[1]-ny*.04,-.34),(a[0]-nx*.04,a[1]-ny*.04,-.34)],5)

def make_asset(kind):
    root=empty(kind)
    if kind=='rock':stone(root)
    elif kind=='rock_cluster':
        for loc,s in [((-.28,.0,0),.75),((.31,.13,0),.60),((.08,-.30,0),.42)]:stone(root,loc,s)
    elif kind=='tree':pine(root)
    elif kind=='tree_round':
        tube('Chunky leafy trunk',root,(0,0,.36),(.26,.26,.72),5)
        for loc,size,c in [((0,0,1.0),(1.1,1.03,1.12),22),((-.32,.05,1.08),(.68,.71,.76),20),((.30,.05,1.2),(.70,.73,.74),29)]:ball('Round bean tunic',root,loc,size,c)
    elif kind=='tower':
        tube('Broad tower foot',root,(0,0,.07),(1.46,1.46,.14),3);ball('Round bean tunic',root,(0,0,.64),(1.22,1.22,1.20),24)
        tube('Stone roof collar',root,(0,0,1.08),(1.35,1.35,.15),24);ball('Bulgy red roof edge',root,(0,0,1.18),(1.52,1.52,.27),10)
        shape('Red pointed roof','cone',root,(0,0,1.38),(1.47,1.47,.46),10)
        rounded('Big wooden door',root,(0,-.56,.37),(.36,.13,.56),5,.08)
        for side in [-1,1]:ball('Dark window',root,(side*.34,-.49,.84),(.15,.06,.22),11)
        tube('War banner pole',root,(0,0,1.70),(.05,.05,.65),5)
        face('Red war banner',root,[(.02,0,1.97),(.56,0,1.94),(.45,0,1.78),(.56,0,1.62),(.02,0,1.65)],10);goblin_emblem(root,.25,-.025,1.81,.13)
        for i in range(8):
            a=math.tau*i/8;shape('Wooden spike fence','cone',root,(math.cos(a)*.77,math.sin(a)*.77,.24),(.14,.14,.48),5)
    elif kind=='wall':
        for z,xs in [(.12,[-.33,0,.33]),(.35,[-.25,.25])]:
            for x in xs:rounded('Rounded stone block',root,(x,0,z),(.32 if z<.2 else .48,.31,.23),3 if z<.2 else 24,.04)
        rounded('Mossy wall cap',root,(0,0,.48),(1,.32,.08),22,.03)
    elif kind.startswith('gate_'):
        c=10 if kind.endswith('red') else 0
        for x in [-.70,.70]:rounded('Rounded gate post',root,(x,0,.48),(.28,.32,.96),24,.055);ball('Stone post cap',root,(x,0,.98),(.36,.38,.22),3)
        hinge=empty(kind+'_GateHinge',root,(0,0,.90))
        for x in [-.4,-.2,0,.2,.4]:rounded('Painted gate plank',hinge,(x,0,-.38),(.19,.14,.75),c,.03)
        for z in [-.13,-.62]:rounded('Gold iron gate strap',hinge,(0,-.085,z),(1.05,.04,.08),12,.015)
        ball('Large keyhole ring',hinge,(0,-.10,-.38),(.19,.04,.19),12);ball('Dark keyhole',hinge,(0,-.13,-.37),(.07,.02,.08),11);rounded('Keyhole stem',hinge,(0,-.13,-.44),(.06,.02,.09),11,.008)
    elif kind=='chest':
        rounded('Wooden chest base',root,(0,0,.23),(.87,.56,.45),5,.055);ball('Rounded chest lid',root,(0,0,.47),(.88,.57,.35),23)
        for x in [-.31,.31]:
            band=torus('Gold band hugging lid',root,(x,0,.47),.285,.022,12,(.61,1,1.8));band.rotation_euler.y=math.pi/2
        rounded('Big gold chest lock',root,(0,-.32,.29),(.21,.08,.21),12,.03)
        for x in [-.17,.03,.20]:tube('Gold coin',root,(x,-.06,.63),(.17,.17,.04),12)
    elif kind.startswith('key_'):
        c=10 if kind.endswith('red') else 0
        torus('Gold key handle',root,(0,0,.72),.17,.045,12,scale=(1,1,1)).rotation_euler.x=math.pi/2
        ball('Colored handle gem',root,(0,-.01,.72),(.22,.08,.22),c);rounded('Thick key shaft',root,(0,0,.36),(.09,.10,.48),12,.015)
        for z in [.14,.27]:rounded('Chunky key tooth',root,(.10,0,z),(.22,.10,.08),12,.015)
    elif kind.startswith('flag_'):banner(root,kind)
    elif kind=='pedestal':
        tube('Cream pedestal base',root,(0,0,.035),(.94,.94,.07),24);ball('Soft cream pedestal top',root,(0,0,.07),(.96,.96,.12),6)
    elif kind=='bridge_gold':
        for i in range(7):rounded('Golden bridge plank',root,(0,-.45+i*.15,.065),(.92,.14,.10),12,.025)
        for x in [-.50,.50]:
            for y in [-.50,.50]:tube('Gold bridge post',root,(x,y,.20),(.07,.07,.40),12)
            rod('Warm rope rail',root,(x,-.50,.34),(x,.50,.34),.018,6)
    elif kind in ['hill','hill_large']:mound(root,kind=='hill_large')
    elif kind=='slope_ramp':
        surface=empty('RampSurface',root)
        poly('Low earthen ramp',surface,[(-1.5,-1.5,0),(1.5,-1.5,0),(1.5,1.5,0),(-1.5,1.5,0),(-1.5,-1.5,.3),(1.5,-1.5,.3)],[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(3,2,1,0)],23)
        for x in [-1.43,1.43]:rounded('Grassy ramp shoulder',root,(x,0,.12),(.12,3,.10),22,.03)
        for y in [-1.10,-.55,0,.55,1.10]:
            z=.15-y*.10+.007;face('Broad step groove',root,[(-1.25,y-.025,z+.003),(1.25,y-.025,z+.003),(1.25,y+.025,z-.003),(-1.25,y+.025,z-.003)],5)
        for y in [-.65,.65]:face('Pale uphill arrow',root,[(-.15,y+.20,.15-(y+.20)*.1+.012),(.15,y+.20,.15-(y+.20)*.1+.012),(.15,y-.03,.15-(y-.03)*.1+.012),(.31,y-.03,.15-(y-.03)*.1+.012),(0,y-.34,.15-(y-.34)*.1+.012),(-.31,y-.03,.15-(y-.03)*.1+.012),(-.15,y-.03,.15-(y-.03)*.1+.012)],6)
    elif kind in ['chasm','chasm_corner']:ravine(root,kind=='chasm_corner')
    elif kind=='cliff_edge':
        for z,c in [(-.18,23),(-.46,5),(-.70,3)]:rounded('Chunky cliff layer',root,(0,.03,z),(4,.42,.27),c,.07)
        rounded('Grass cliff lip',root,(0,0,.015),(4,.46,.09),22,.04)
    elif kind=='field_border':
        rounded('Chunky wooden field rail',root,(0,0,.08),(4,.22,.16),5,.05)
        rounded('Warm rail top',root,(0,0,.17),(3.98,.24,.06),23,.025)
        for x in [-1.84,0,1.84]:rounded('Stone rail bracket',root,(x,0,.12),(.24,.32,.24),24,.04)
    merge(root);return root

roots={};manifest={}
for kind,budget in budgets.items():
    root=make_asset(kind);roots[kind]=root
    bpy.context.view_layer.update()
    if kind not in ['chasm','chasm_corner','cliff_edge']:
        bottom=min((o.matrix_world@Vector(c)).z for o in descendants(root) if o.type=='MESH' for c in o.bound_box)
        for child in root.children:child.location.z-=bottom
    bpy.ops.object.select_all(action='DESELECT')
    for o in descendants(root):o.select_set(True)
    bpy.context.view_layer.objects.active=root;file=os.path.join(out,kind+'.glb')
    bpy.ops.export_scene.gltf(filepath=file,export_format='GLB',use_selection=True,export_animations=False)
    b=Path(file).read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);tris=sum(j['accessors'][p['indices']]['count']//3 for m in j['meshes'] for p in m['primitives']);assert tris<=budget,(kind,tris,budget)
    manifest[kind]={'triangles':tris,'budget':budget,'meshes':len(j['meshes']),'textureSize':[512,512],'units':'one bean soldier height'}
    for o in descendants(root):o.hide_render=True

texdir=os.path.join(project,'public','assets','textures');icondir=os.path.join(project,'public','assets','icons')
os.makedirs(texdir,exist_ok=True);os.makedirs(icondir,exist_ok=True)
def save_pixels(name,rgba,file):
    h,w=rgba.shape[:2];im=bpy.data.images.new(name,width=w,height=h,alpha=True);im.pixels.foreach_set(rgba.astype(np.float32).ravel());im.filepath_raw=file;im.file_format='PNG';im.save();return im

y,x=np.mgrid[0:512,0:512]/511.;tau=math.tau
specs={'grass':((.36,.55,.26),.055),'sand':((.76,.61,.33),.04),'swamp':((.27,.36,.23),.04),'road':((.64,.53,.36),.04),'water':((.27,.59,.68),.035),'hill':((.51,.65,.30),.045),'slope':((.51,.54,.30),.035),'chasm':((.045,.067,.11),.018)}
for name,(base,amp) in specs.items():
    field=(np.sin(tau*(x+y*2))+.6*np.cos(tau*(x*3-y))+.4*np.sin(tau*(x*5+y*3)))/2
    rgb=np.array(base)[None,None,:]+field[:,:,None]*amp
    if name in ['sand','water','slope']:
        ripple=np.cos(tau*(y*(12 if name=='sand' else 7)+np.sin(tau*x)*.16));rgb+=(np.maximum(0,ripple-.82)*(.10 if name=='water' else .07))[:,:,None]
    if name=='road':
        tracks=np.exp(-((np.sin(tau*(x-.18)))**2)/.004)+np.exp(-((np.sin(tau*(x-.44)))**2)/.004);rgb-=tracks[:,:,None]*.035
    if name in ['grass','hill','sand','road','swamp']:
        for k in range(13 if name!='swamp' else 7):
            cx=(k*.6180339+.16)%1;cy=(k*.4142135+.31)%1;dx=(x-cx+.5)%1-.5;dy=(y-cy+.5)%1-.5
            r=.008 if name in ['grass','hill'] else .013 if name in ['sand','road'] else .038;mask=dx*dx+(dy*1.3)**2<r*r
            rgb[mask]=np.array(base)+(np.array([.10,.12,.02]) if name!='hill' else np.array([.22,.19,.10]))
            if name=='swamp':rgb[mask]=(.40,.51,.25)
    rgba=np.dstack([np.clip(rgb,0,1),np.ones((512,512))]);save_pixels('Terrain '+name,rgba,os.path.join(texdir,'tex_'+name+'.png'))

# Deterministic badge drawings share the existing game's flat icon language.
yy,xx=np.mgrid[0:512,0:512]/4.;X=xx-64;Y=yy-64
def line_mask(points,width):
    mask=np.zeros_like(X,dtype=bool)
    for a,b in zip(points,points[1:]):
        ax,ay=a;bx,by=b;vx,vy=bx-ax,by-ay;t=np.clip(((xx-ax)*vx+(yy-ay)*vy)/(vx*vx+vy*vy),0,1);mask|=(xx-ax-t*vx)**2+(yy-ay-t*vy)**2<width*width
    return mask
for name in ['hill','slope','chasm','sand','swamp','road']:
    rgba=np.zeros((512,512,4));dist=np.sqrt(X*X+Y*Y);rgba[dist<59]=(.88,.92,.84,1);rgba[dist<54]=(.07,.13,.20,1)
    white=np.zeros_like(X,dtype=bool);green=np.zeros_like(X,dtype=bool)
    if name=='hill':
        white=((X/36)**2+((Y+12)/31)**2<1)&(Y>-14)&(Y<20);green=((X/30)**2+((Y+10)/25)**2<1)&(Y>-9)&(Y<18)
    elif name=='slope':
        white=(Y>-22)&(Y<.65*X+8)&(abs(X)<34);green=line_mask([(40,40),(83,82)],3)|line_mask([(68,82),(83,82),(83,66)],3)
    elif name=='chasm':white=line_mask([(52,98),(73,78),(57,64),(76,45),(66,30)],8);green=line_mask([(52,98),(73,78),(57,64),(76,45),(66,30)],3)
    elif name=='sand':
        for cy in [44,66,86]:white|=(abs(yy-(cy+5*np.sin((xx-25)/18)))<3)&(xx>29)&(xx<100)
    elif name=='swamp':
        white=line_mask([(33,38),(96,38)],3)
        for px,h in [(45,80),(64,97),(83,83)]:white|=line_mask([(px,40),(px,h)],2.5);green|=((xx-px)/5)**2+((yy-(h-8))/10)**2<1
    else:
        center=64+9*np.sin((yy-26)/26);white=(abs(xx-center)<17)&(yy>27)&(yy<101);green=(abs(xx-center)<3)&(yy>31)&(yy<99)&((yy.astype(int)//12)%2==0)
    rgba[white]=(.96,.95,.83,1);rgba[green]=(.42,.72,.32,1)
    small=rgba.reshape(128,4,128,4,4).mean(axis=(1,3));save_pixels('Terrain badge '+name,small,os.path.join(icondir,'icon_terrain_'+name+'.png'))

for i,(kind,root) in enumerate(roots.items()):
    root.location=(i%6*6,i//6*6,0)
    for o in descendants(root):o.hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art,'ink-march-environment-v4.blend'))
Path(os.path.join(art,'manifest.json')).write_text(json.dumps(manifest,indent=2))
print('ENVIRONMENT_V4_COMPLETE',json.dumps(manifest))
