# Sinh THÊM màn (không đụng màn cũ). Màn mới chèn trước màn cuối (boss) của chương.
# Chạy: python tools/gen_extra.py .   rồi link-camps + solve-map cho các id in ra.
import json, os, sys
ROOT = sys.argv[1]
MAPS = os.path.join(ROOT, 'src', 'data', 'maps')
# Dùng lại helper và hàm co sân từ genmaps.py (chỉ phần định nghĩa, không chạy phần ghi file)
src = open(os.path.join(os.path.dirname(__file__), 'genmaps.py'), encoding='utf8').read()
ns = {'__name__': 'genmaps_defs'}
sys_argv = sys.argv
sys.argv = ['genmaps.py', '/nonexistent']
exec(src[:src.index("for f in glob.glob(os.path.join(MAPS, '*.json')): os.remove(f)")], ns)
sys.argv = sys_argv
g = type('G', (), ns)
R, W, Rk, camp, it, gate, sq, sand, swamp, road, boss, bosses2, TWO, ONE = g.R, g.W, g.Rk, g.camp, g.it, g.gate, g.sq, g.sand, g.swamp, g.road, g.boss, g.bosses2, g.TWO, g.ONE
CHIEF, KING, MAGE = 'goblin_chief', 'goblin_king', 'shadow_mage'
def CH(x, y, w, h): return R(x, y, w, h, 'chasm')
def hill(x, y, w, h): return {"kind": "hill", "points": g.rect_pts(x, y, w, h)}
def slope(x, y, w, h, up): return {"kind": "slope", "points": g.rect_pts(x, y, w, h), "up": list(up)}

EXTRA = [
 (1, dict(name="The Ravine", hint="A ravine splits the woods. Only the narrow gap lets you through.",
   bosses=[boss(CHIEF)], obstacles=[CH(0, 460, 180, 90), CH(280, 460, 440, 90)],
   camps=[camp(110, 720, g=1), camp(560, 300, g=1), camp(230, 290, g=2)], items=[it("hp_up", 560, 720), it("atk_up", 380, 300)],
   squads=[sq(2, [[230, 290], [300, 180], [340, 110]], g=4)], teach=["chasm"])),
 (2, dict(name="Windy Hills", hint="Hills burn a bit more ink and slow your march. The valley road is cheap.",
   bosses=[boss(CHIEF)], terrain=[hill(140, 250, 440, 480), road(60, 200, 70, 700)],
   camps=[camp(360, 480, g=2), camp(600, 760, g=2), camp(160, 260, g=1, ga=1)], items=[it("atk_up", 600, 400), it("shield", 95, 560)],
   squads=[sq(3, [[600, 760], [620, 300], [400, 110]], ga=4)], teach=["hill"])),
 (2, dict(name="Cliffside Pass", hint="Cliffs on both sides. The ledge road is safe but long.",
   bosses=[boss(CHIEF)], obstacles=[CH(120, 330, 480, 80), CH(0, 640, 260, 70)], terrain=[road(600, 180, 70, 700), sand(260, 560, 340, 180)],
   camps=[camp(400, 760, g=2, ga=1), camp(150, 230, g=2), camp(560, 230, g=2)], items=[it("hp_up", 80, 500), it("reinforce", 360, 220)],
   squads=[sq(4, [[150, 230], [60, 420], [80, 560]], g=5)], teach=[])),
 (3, dict(name="Mudslide", hint="Drawing uphill costs more ink. Downhill is cheap. Plan which way you climb.",
   bosses=[boss(CHIEF)], terrain=[slope(160, 240, 400, 420, (0, -1)), swamp(0, 520, 160, 200), road(560, 200, 70, 650)],
   camps=[camp(100, 300, g=2, sh=1), camp(620, 780, g=3), camp(360, 760, g=2)], items=[it("atk_up", 360, 400), it("hp_up", 600, 300)],
   squads=[sq(4, [[620, 780], [600, 450], [420, 110]], g=5)], teach=["slope"])),
 (4, dict(name="Twin Ravines", hint="A ravine splits the field. Each squad climbs its own hill.",
   starts=TWO, bosses=bosses2(CHIEF, CHIEF), obstacles=[CH(320, 120, 80, 760)], terrain=[hill(40, 300, 240, 300), hill(440, 300, 240, 300)],
   camps=[camp(120, 680, g=3), camp(600, 680, g=3), camp(360, 920, g=2, ga=1)], items=[it("atk_up", 160, 230), it("hp_up", 560, 230), it("reinforce", 250, 760), it("shield", 470, 760)],
   squads=[sq(5, [[120, 680], [60, 400], [180, 110]], g=5), sq(5, [[600, 680], [660, 400], [540, 110]], ga=4)], teach=[])),
 (5, dict(name="Canyon Steps", hint="Steps climb toward the gate. Grab the key on the way down.",
   bosses=[boss(CHIEF)], obstacles=[R(0, 420, 300, 50), R(400, 420, 320, 50)],
   terrain=[slope(0, 470, 720, 260, (0, -1)), slope(0, 150, 720, 270, (-1, 0))],
   camps=[camp(100, 800, g=3), camp(620, 260, g=3, ga=1), camp(120, 250, g=2, ga=1)],
   items=[it("key", 620, 820, color="red"), gate("red", 300, 420, 100, 50), it("atk_up", 360, 600), it("hp_up", 380, 260)],
   squads=[sq(5, [[620, 260], [500, 200], [400, 110]], ga=4)], teach=[])),
 (6, dict(name="Highland Fens", hint="Fens below, hills above. Shamans heal from the high ground.",
   bosses=[boss(CHIEF)], terrain=[swamp(0, 520, 720, 160), hill(100, 200, 220, 250), hill(400, 200, 220, 250)],
   camps=[camp(210, 320, sh=1, g=3), camp(510, 320, sh=1, g=2, ga=1), camp(360, 820, g=3)],
   items=[it("atk_up", 80, 700), it("hp_up", 640, 700), it("reinforce", 360, 450)],
   squads=[sq(4, [[510, 320], [600, 200], [400, 110]], speed=50, sh=1, g=3)], teach=[])),
]

chapters = json.load(open(os.path.join(ROOT, 'src', 'data', 'chapters.json'), encoding='utf8'))
index_path = os.path.join(MAPS, 'index.ts')
index = open(index_path, encoding='utf8').read()
made = []
for ci, s in EXTRA:
    stages = chapters[ci - 1]['stages']
    maps_in = [x for x in stages if not (x == 'shop' or x.startswith('event:'))]
    n = max(int(x.split('_s')[1]) for x in maps_in) + 1
    mid = f"c{ci}_s{n}"
    if any(json.load(open(os.path.join(MAPS, f), encoding='utf8')).get('name') == s['name'] for f in os.listdir(MAPS) if f.startswith(f"c{ci}_")) and os.path.exists(os.path.join(MAPS, mid)):
        continue
    starts = s.get('starts', ONE)
    m = {"id": mid, "name": s['name'], "chapter": ci, "baseInk": 2000, "starts": starts, "bosses": s['bosses'],
         "obstacles": s.get('obstacles', []), "items": s.get('items', []), "goldZones": [], "terrain": s.get('terrain', []), "camps": s['camps'],
         "enemySquads": [dict(q, id=f"s{i}") for i, q in enumerate(s.get('squads', []))], "bonusSquadRoute": [[20, 500], [300, 120]],
         "referenceSolution": [[[p["x"], p["y"]], [b["x"], b["y"]]] for p, b in zip(starts, s['bosses'] * 2)], "tutorialHint": s['hint'], "teach": s['teach']}
    m = g.shrink(json.loads(json.dumps(m)), g.SIZE[ci - 1])
    json.dump(m, open(os.path.join(MAPS, mid + '.json'), 'w', encoding='utf8'), indent=2, ensure_ascii=False)
    stages.insert(stages.index(maps_in[-1]), mid)
    index = f"import {mid} from './{mid}.json';\n" + index.replace("export default {", "export default {" + mid + ",")
    made.append(mid)
open(index_path, 'w', encoding='utf8').write(index)
json.dump(chapters, open(os.path.join(ROOT, 'src', 'data', 'chapters.json'), 'w', encoding='utf8'), indent=2, ensure_ascii=False)
print(' '.join(made))
