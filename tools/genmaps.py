# Sinh 10 chương Ink March. Chạy: python genmaps2.py <ink-march root>
# Scale boss, mực gốc và đường mẫu do tools/solve-map.ts điền sau.
import json, os, sys, glob
ROOT = sys.argv[1]
MAPS = os.path.join(ROOT, 'src', 'data', 'maps')

def R(x, y, w, h, kind=None):
    o = {"type": "rect", "x": x, "y": y, "w": w, "h": h}
    if kind: o["kind"] = kind
    return o
def W(x, y, w, h): return R(x, y, w, h, "water")
def Rk(x, y, r): return {"type": "circle", "x": x, "y": y, "r": r}
def rect_pts(x, y, w, h): return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
def sand(x, y, w, h): return {"kind": "sand", "points": rect_pts(x, y, w, h)}
def swamp(x, y, w, h): return {"kind": "swamp", "points": rect_pts(x, y, w, h)}
def road(x, y, w, h): return {"kind": "road", "points": rect_pts(x, y, w, h)}
U = {"g": "goblin", "ga": "goblin_archer", "o": "orc", "sh": "shaman"}
def units(spec): return [{"type": U[k], "count": n} for k, n in spec.items()]
def camp(x, y, **spec): return {"x": x, "y": y, "units": units(spec)}
def it(t, x, y, **kw): return {"type": t, "x": x, "y": y, **kw}
def gate(color, x, y, w, h): return {"type": "gate", "color": color, "rect": {"x": x, "y": y, "w": w, "h": h}}
def sq(delay, route, speed=55, **spec): return {"spawnDelay": delay, "speed": speed, "units": units(spec), "route": route}
ONE = [{"x": 360, "y": 940}]
TWO = [{"x": 180, "y": 940}, {"x": 540, "y": 940}]
def boss(t, x=360, y=80): return {"type": t, "x": x, "y": y, "scale": 1}
def bosses2(a, b): return [boss(a, 180), boss(b, 540)]

CH = []
def chapter(name, stages, interlude):
    CH.append((name, stages, interlude))
def st(name, hint, starts=ONE, bosses=None, obstacles=(), terrain=(), camps=(), items=(), squads=(), gold=(), bonus=None, teach=None):
    return dict(name=name, hint=hint, starts=starts, bosses=bosses, obstacles=list(obstacles), terrain=list(terrain), camps=list(camps), items=list(items), squads=list(squads), gold=list(gold), bonus=bonus, teach=teach)

KING, CHIEF, MAGE = "goblin_king", "goblin_chief", "shadow_mage"

chapter("The Waking Woods", [
  st("First Lines", "Draw from START to the boss. Pass close to a camp to attack it: every camp destroyed is a star.",
     bosses=[boss(CHIEF)], obstacles=[Rk(360, 520, 60)],
     camps=[camp(150, 620, g=1), camp(570, 430, g=1), camp(210, 260, g=1)], items=[it("atk_up", 480, 720)], teach=[]),
  st("Camp Muster", "The left camp sends a squad when its timer ends. Destroy it first and the boss stays weak.",
     bosses=[boss(CHIEF)], obstacles=[Rk(380, 470, 70)],
     camps=[camp(220, 640, g=3), camp(540, 360, g=1), camp(210, 260, g=1)],
     items=[it("atk_up", 540, 720)],
     squads=[sq(2, [[220, 640], [250, 300], [340, 110]], g=5)], teach=["muster"]),
  st("The Crossing", "That camp is too far. Cross its squad's route instead: a flag holds them until you arrive.",
     bosses=[boss(CHIEF)], obstacles=[R(80, 640, 170, 40), R(250, 640, 40, 360), W(290, 500, 430, 60)],
     camps=[camp(110, 840, g=1), camp(600, 300, g=1), camp(560, 760, g=1)],
     items=[it("hp_up", 470, 620), it("atk_up", 200, 300)],
     squads=[sq(2, [[110, 840], [60, 600], [200, 420], [360, 360], [360, 110]], g=4)], teach=["flags"]),
  st("Goblin King's Gate", "Two warbands march on the King. They steal charms on the way. Check the forecast before you march.",
     bosses=[boss(KING)], obstacles=[R(170, 30, 40, 190), R(510, 30, 40, 190), R(170, 190, 120, 40), R(430, 190, 120, 40), R(140, 470, 440, 60)],
     camps=[camp(70, 330, g=2, ga=1), camp(650, 330, g=2, ga=1), camp(360, 700, g=2)],
     items=[it("reinforce", 70, 640), it("atk_up", 650, 640), it("hp_up", 360, 330)],
     squads=[sq(4, [[20, 720], [70, 400], [250, 280], [360, 260], [360, 130]], g=5), sq(8, [[700, 720], [650, 400], [470, 280], [360, 260], [360, 130]], ga=4)], teach=["thieves", "loot", "forecast"]),
], "shop")

chapter("Dusty Trail", [
  st("Dune Sea", "Sand burns ink fast and slows your march. The road on the east is cheap but long.",
     bosses=[boss(CHIEF)], terrain=[sand(0, 300, 560, 400), road(560, 300, 80, 400)],
     camps=[camp(120, 520, g=2), camp(360, 200, g=2), camp(620, 780, g=1, ga=1)],
     items=[it("atk_up", 360, 520), it("shield", 600, 300)],
     squads=[sq(5, [[20, 250], [300, 150], [360, 100]], ga=4)]),
  st("Sun-baked Road", "Follow the road around the dunes, or cut across the sand and pay in ink.",
     bosses=[boss(CHIEF)], obstacles=[Rk(300, 600, 50), Rk(450, 400, 50)], terrain=[sand(150, 210, 570, 640), road(80, 150, 70, 700), road(80, 150, 560, 60)],
     camps=[camp(600, 800, g=2), camp(600, 450, g=2, ga=1), camp(250, 330, g=2)],
     items=[it("hp_up", 600, 620), it("reinforce", 360, 790), it("ink_bottle", 110, 600, value=250)],
     squads=[sq(3, [[700, 300], [450, 200], [360, 100]], g=6)]),
  st("Bandit King's Oasis", "The oasis blocks the middle. Roads north and south of it save ink.",
     bosses=[boss(KING)], obstacles=[W(280, 420, 160, 140)], terrain=[sand(80, 250, 560, 480), road(330, 250, 60, 170), road(330, 560, 60, 170)],
     camps=[camp(110, 330, g=3, ga=1), camp(610, 330, g=3, ga=1), camp(610, 790, g=2, ga=2)],
     items=[it("atk_up", 150, 700), it("hp_up", 570, 600), it("shield", 360, 200)],
     squads=[sq(4, [[20, 600], [150, 400], [300, 200], [360, 120]], g=6), sq(8, [[700, 600], [560, 400], [420, 200], [360, 120]], ga=5)]),
], "event:ev_shrine")

chapter("Mirelands", [
  st("Bog Crossing", "The causeway is the only cheap way over the bog, and a camp watches it.",
     bosses=[boss(CHIEF)], terrain=[swamp(0, 400, 470, 220), swamp(550, 400, 170, 220), road(470, 400, 80, 220)],
     camps=[camp(510, 320, g=2, ga=1), camp(100, 720, g=2), camp(200, 250, g=3)],
     items=[it("hp_up", 110, 500), it("atk_up", 640, 520)],
     squads=[sq(5, [[700, 720], [510, 660], [510, 380], [380, 110]], g=5)]),
  st("Reed Maze", "The shaman's band loops through the maze and will steal what it passes.",
     bosses=[boss(CHIEF)], obstacles=[R(0, 620, 500, 40), R(220, 380, 500, 40)], terrain=[swamp(0, 420, 220, 200), swamp(500, 660, 220, 200)],
     camps=[camp(600, 520, g=3), camp(120, 520, g=2, sh=1), camp(600, 250, g=2, ga=1)],
     items=[it("shield", 110, 780), it("atk_up", 360, 520), it("reinforce", 110, 250)],
     squads=[sq(4, [[700, 460], [400, 520], [150, 500], [150, 250], [330, 110]], speed=50, sh=1, g=3)]),
  st("Sunken Shrine", "Roads ring the drowned shrine. Its camp sits deep in the swamp.",
     bosses=[boss(CHIEF)], terrain=[swamp(150, 250, 420, 450), road(80, 150, 60, 700), road(580, 150, 60, 700)],
     camps=[camp(360, 480, g=3, sh=1), camp(110, 520, g=2, ga=1), camp(610, 300, g=3)],
     items=[it("atk_up", 360, 300), it("hp_up", 110, 250), it("ink_bottle", 610, 700, value=300)],
     squads=[sq(3, [[700, 850], [610, 600], [610, 200], [400, 100]], g=5), sq(9, [[20, 850], [110, 600], [110, 200], [320, 100]], ga=4)]),
  st("Mire Chieftain", "Two causeways cross the mire. The island camp can only be reached through the swamp.",
     bosses=[boss(KING)], terrain=[swamp(0, 300, 150, 400), swamp(220, 300, 280, 400), swamp(570, 300, 150, 400), road(150, 300, 70, 400), road(500, 300, 70, 400)],
     camps=[camp(185, 220, g=3, ga=2), camp(535, 220, g=3, ga=2), camp(360, 500, sh=1, g=3)],
     items=[it("reinforce", 185, 780), it("atk_up", 535, 780), it("hp_up", 360, 800)],
     squads=[sq(5, [[20, 500], [185, 450], [185, 200], [330, 110]], g=6), sq(7, [[700, 500], [535, 450], [535, 200], [390, 110]], speed=50, sh=1, g=3)]),
], "shop")

chapter("Twin Rivers", [
  st("Two Banks", "Two squads, one ink pot. Each squad must reach its own boss.",
     starts=TWO, bosses=bosses2(CHIEF, CHIEF), obstacles=[W(330, 150, 60, 700)], terrain=[sand(110, 380, 160, 220), sand(450, 380, 160, 220)],
     camps=[camp(80, 500, g=3), camp(640, 500, g=3), camp(360, 100, g=2, ga=1)],
     items=[it("atk_up", 80, 760), it("hp_up", 640, 760), it("shield", 80, 250), it("range_up", 640, 250)],
     squads=[sq(4, [[20, 300], [180, 150]], g=4), sq(6, [[700, 300], [540, 150]], g=4)]),
  st("Crossing Fords", "The river has two fords. Sand guards the western one.",
     bosses=[boss(CHIEF)], obstacles=[W(0, 450, 100, 90), W(160, 450, 400, 90), W(620, 450, 100, 90)], terrain=[sand(60, 360, 140, 270)],
     camps=[camp(130, 300, g=3, ga=1), camp(590, 300, g=3, ga=1), camp(360, 720, g=2, ga=1)],
     items=[it("atk_up", 360, 250), it("hp_up", 130, 720), it("reinforce", 590, 720)],
     squads=[sq(4, [[700, 250], [360, 200], [360, 100]], ga=5)]),
  st("Split Assault", "A ridge splits the field. Sand on the west, swamp on the east, one boss for both squads.",
     starts=TWO, bosses=[boss(CHIEF)], obstacles=[R(300, 300, 120, 500)], terrain=[sand(30, 300, 240, 400), swamp(450, 300, 240, 400)],
     camps=[camp(150, 230, g=3), camp(570, 230, g=3), camp(360, 860, g=2, ga=1)],
     items=[it("atk_up", 150, 760), it("hp_up", 570, 760)],
     squads=[sq(6, [[20, 500], [150, 300], [330, 110]], g=5), sq(6, [[700, 500], [570, 300], [390, 110]], ga=4)]),
  st("Twin Fortress", "Two kings, two squads. Share the ink wisely between the fronts.",
     starts=TWO, bosses=bosses2(KING, KING), obstacles=[W(330, 0, 60, 820), R(60, 350, 200, 40), R(460, 350, 200, 40)],
     camps=[camp(60, 620, g=3, ga=2), camp(660, 620, g=3, ga=2), camp(360, 900, g=4)],
     items=[it("reinforce", 250, 500), it("reinforce", 470, 500), it("atk_up", 100, 220), it("hp_up", 620, 220)],
     squads=[sq(8, [[20, 220], [180, 120]], g=6), sq(8, [[700, 220], [540, 120]], g=6)]),
], "event:ev_mercenary")

chapter("Red Canyon", [
  st("Canyon Gate", "The wall is sealed. The red key lies in the sand.",
     bosses=[boss(CHIEF)], obstacles=[R(0, 450, 310, 50), R(410, 450, 310, 50)], terrain=[sand(0, 600, 260, 300)],
     camps=[camp(620, 780, g=3, ga=1), camp(110, 250, g=3, ga=1), camp(610, 250, g=3, ga=1)],
     items=[it("key", 110, 760, color="red"), gate("red", 310, 450, 100, 50), it("atk_up", 600, 600), it("hp_up", 360, 300)],
     squads=[sq(6, [[20, 350], [360, 250], [360, 110]], ga=5)]),
  st("Twin Locks", "Red key, red gate, blue key, blue gate. The orc band steals on its way.",
     bosses=[boss(CHIEF)], obstacles=[R(0, 640, 520, 50), R(620, 640, 100, 50), R(0, 330, 100, 50), R(200, 330, 520, 50)], terrain=[sand(200, 690, 520, 200)],
     camps=[camp(360, 500, g=3, ga=2), camp(600, 200, g=3, ga=1), camp(600, 820, g=2, ga=1)],
     items=[it("key", 90, 820, color="red"), gate("red", 520, 640, 100, 50), it("key", 640, 480, color="blue"), gate("blue", 100, 330, 100, 50), it("atk_up", 90, 500), it("hp_up", 360, 200)],
     squads=[sq(5, [[700, 560], [150, 520], [150, 250], [330, 110]], speed=45, o=1, g=3)]),
  st("Dust Devils", "A crossroads of roads in a sea of sand. A war party crosses the middle.",
     bosses=[boss(CHIEF)], terrain=[sand(0, 120, 720, 780), road(100, 120, 60, 780), road(560, 120, 60, 780), road(100, 480, 520, 60)],
     camps=[camp(360, 300, g=3, ga=2), camp(130, 300, g=3), camp(590, 760, g=3, ga=1)],
     items=[it("atk_up", 360, 700), it("reinforce", 590, 300)],
     squads=[sq(4, [[700, 450], [360, 450], [20, 450]], g=6), sq(0, [[20, 150], [330, 110]], ga=4)]),
  st("Warlord's Keep", "The keep has one gate. Its key is out on the eastern sands.",
     bosses=[boss(KING)], obstacles=[R(150, 250, 170, 50), R(400, 250, 170, 50), R(150, 40, 40, 210), R(530, 40, 40, 210)], terrain=[sand(500, 550, 220, 350)],
     camps=[camp(70, 250, g=4, ga=2), camp(650, 250, g=4, ga=2), camp(360, 600, o=1, g=2)],
     items=[it("key", 650, 720, color="red"), gate("red", 320, 250, 80, 50), it("atk_up", 100, 720), it("hp_up", 360, 820), it("reinforce", 70, 450)],
     squads=[sq(5, [[20, 500], [100, 350], [360, 340]], speed=45, o=1, g=3), sq(8, [[700, 500], [620, 360], [360, 340]], ga=5)]),
], "shop")

chapter("Shaman Fens", [
  st("Fen Paths", "Two squads cross the fen on wooden paths. The healer camp sits in the middle.",
     starts=TWO, bosses=[boss(CHIEF)], terrain=[swamp(0, 350, 150, 350), swamp(210, 350, 300, 350), swamp(570, 350, 150, 350), road(150, 350, 60, 350), road(510, 350, 60, 350)],
     camps=[camp(360, 520, sh=1, g=3), camp(60, 200, g=3, ga=1), camp(660, 200, g=3, ga=1)],
     items=[it("atk_up", 70, 700), it("hp_up", 650, 700)],
     squads=[sq(6, [[20, 250], [360, 250], [360, 110]], speed=50, sh=1, g=3)]),
  st("Healers' Hollow", "A shaman patrol loops the hollow. Meet it head-on or let it reach the boss.",
     bosses=[boss(CHIEF)], obstacles=[R(235, 230, 40, 520), R(485, 230, 40, 520), R(275, 440, 210, 60)], terrain=[swamp(0, 230, 235, 520)],
     camps=[camp(117, 500, sh=1, g=2), camp(620, 500, g=2, ga=1), camp(380, 330, g=2)],
     items=[it("atk_up", 620, 330), it("hp_up", 620, 680), it("reinforce", 117, 800)],
     squads=[sq(0, [[620, 300], [620, 800], [380, 860], [117, 800], [117, 250], [330, 110]], speed=50, sh=1, g=4)]),
  st("Mirror Marsh", "Two bosses mirror each other across the marsh.",
     starts=TWO, bosses=bosses2(CHIEF, CHIEF), terrain=[swamp(250, 200, 220, 600)], obstacles=[R(0, 500, 235, 40), R(485, 500, 235, 40)],
     camps=[camp(80, 300, g=3, ga=2), camp(640, 300, g=3, ga=2), camp(360, 870, sh=1, g=3)],
     items=[it("atk_up", 200, 650), it("hp_up", 520, 650), it("range_up", 80, 760), it("shield", 640, 760)],
     squads=[sq(5, [[360, 160], [180, 120]], g=5), sq(5, [[360, 170], [540, 120]], g=5)]),
  st("Shadow of the Fens", "The Shadow Mage waits beyond the fen. One causeway, two flanks.",
     bosses=[boss(MAGE)], obstacles=[R(150, 600, 420, 40)], terrain=[swamp(0, 250, 330, 250), swamp(390, 250, 330, 250), road(330, 250, 60, 250)],
     camps=[camp(100, 380, sh=1, g=3, ga=1), camp(620, 380, sh=1, g=3, ga=1), camp(360, 780, o=1, g=3)],
     items=[it("reinforce", 100, 780), it("atk_up", 620, 780), it("hp_up", 360, 520)],
     squads=[sq(4, [[20, 550], [180, 450], [330, 150]], speed=50, sh=2, g=3), sq(7, [[700, 550], [540, 450], [390, 150]], speed=45, o=1, g=3)]),
], "event:ev_mystery_chest")

chapter("Iron Pass", [
  st("Orc Outpost", "Orcs march up the eastern road. Meet them with Attack, or slip through the western sands.",
     bosses=[boss(CHIEF)], obstacles=[Rk(300, 520, 150)], terrain=[road(560, 150, 70, 700), sand(0, 300, 160, 500)],
     camps=[camp(80, 520, o=1, g=2), camp(620, 250, o=1, g=2), camp(520, 800, g=4)],
     items=[it("atk_up", 470, 700), it("reinforce", 90, 820), it("hp_up", 640, 520)],
     squads=[sq(4, [[700, 760], [600, 450], [430, 110]], speed=45, o=2, g=3)]),
  st("Iron Switchback", "Enemy archers hold the sandy corridor between the walls.",
     bosses=[boss(CHIEF)], obstacles=[R(0, 650, 480, 60), R(240, 350, 480, 60)], terrain=[sand(0, 410, 720, 240)],
     camps=[camp(100, 520, o=1, g=3), camp(620, 800, g=3, ga=2), camp(120, 200, o=1, g=2)],
     items=[it("range_up", 80, 790), it("shield", 610, 520), it("hp_up", 620, 240)],
     squads=[sq(0, [[690, 480], [120, 480], [110, 280], [330, 110]], speed=45, ga=6)]),
  st("Hammer and Anvil", "A ridge splits the pass. Road on the west, swamp on the east.",
     starts=TWO, bosses=[boss(CHIEF)], obstacles=[R(320, 250, 80, 600)], terrain=[road(60, 200, 80, 700), swamp(450, 250, 250, 500)],
     camps=[camp(200, 300, o=1, g=3), camp(560, 300, o=1, g=3), camp(360, 920, g=4)],
     items=[it("atk_up", 100, 520), it("hp_up", 600, 800), it("reinforce", 600, 450)],
     squads=[sq(6, [[20, 150], [330, 110]], speed=45, o=2), sq(3, [[700, 150], [390, 110]], g=6)]),
  st("Gatehouse", "Two gates, three keys. The second red key opens the treasure.",
     bosses=[boss(CHIEF)], obstacles=[R(0, 640, 310, 50), R(410, 640, 310, 50), R(0, 300, 560, 50), R(660, 300, 60, 50)], terrain=[sand(410, 690, 310, 220)],
     camps=[camp(360, 480, o=1, g=3), camp(640, 170, o=1, ga=2), camp(620, 820, g=3, ga=2)],
     items=[it("key", 80, 800, color="red"), gate("red", 310, 640, 100, 50), it("key", 90, 470, color="blue"), gate("blue", 560, 300, 100, 50), it("key", 640, 520, color="red"), it("chest", 120, 200, color="red"), it("atk_up", 220, 820), it("hp_up", 220, 150)],
     squads=[sq(0, [[700, 470], [610, 260], [430, 110]], speed=45, ga=3), sq(6, [[20, 470], [180, 470], [610, 420], [610, 250], [430, 110]], speed=45, o=1, g=3)]),
  st("Iron Warlord", "A royal road runs straight to the warlord. Everything else is sand.",
     bosses=[boss(KING)], obstacles=[R(250, 300, 60, 400), R(410, 300, 60, 400)], terrain=[sand(0, 100, 720, 800), road(330, 100, 60, 800)],
     camps=[camp(100, 250, o=2, g=2), camp(620, 250, o=2, g=2), camp(600, 720, o=1, g=3, ga=2)],
     items=[it("reinforce", 100, 720), it("atk_up", 620, 500), it("hp_up", 100, 470)],
     squads=[sq(4, [[20, 600], [190, 600], [190, 250], [330, 120]], speed=45, o=2, g=3), sq(5, [[700, 600], [530, 600], [530, 250], [390, 120]], speed=45, o=2)]),
], "shop")

chapter("Golden Bridge", [
  st("River Run", "The river only has a ford on the far east, behind the sand.",
     bosses=[boss(MAGE)], obstacles=[W(0, 500, 640, 90)], terrain=[sand(560, 420, 160, 260)],
     camps=[camp(100, 300, g=3, ga=2), camp(360, 760, o=1, g=2), camp(620, 250, g=3, ga=2)],
     items=[it("atk_up", 100, 760), it("hp_up", 360, 300)],
     squads=[sq(3, [[20, 350], [330, 110]], ga=5)]),
  st("Ferry Point", "Two squads, two mages, one river between them.",
     starts=TWO, bosses=bosses2(MAGE, MAGE), obstacles=[W(330, 100, 60, 700)], terrain=[sand(0, 380, 330, 180), sand(390, 380, 330, 180)],
     camps=[camp(80, 470, o=1, g=3), camp(640, 470, o=1, g=3), camp(360, 880, g=4, ga=1)],
     items=[it("atk_up", 250, 250), it("hp_up", 470, 250), it("reinforce", 80, 800), it("range_up", 640, 800)],
     squads=[sq(5, [[20, 200], [180, 110]], speed=45, o=1, g=3), sq(5, [[700, 200], [540, 110]], speed=45, o=1, g=3)]),
  st("The Golden Bridge", "Golden ink builds a bridge straight to the chest. Without it, take the long ford.",
     bosses=[boss(MAGE)], obstacles=[W(0, 450, 640, 100)], gold=[{"points": [[310, 445], [410, 445], [410, 555], [310, 555]]}],
     camps=[camp(100, 250, o=1, g=3), camp(620, 250, o=1, g=3), camp(100, 760, g=3, ga=2)],
     items=[it("key", 360, 700, color="red"), it("chest", 360, 330, color="red"), it("atk_up", 600, 650), it("hp_up", 600, 300)],
     squads=[sq(0, [[20, 330], [200, 220], [330, 110]], ga=4), sq(5, [[700, 360], [560, 250], [410, 110]], speed=45, o=2)]),
  st("Marsh Ferry", "The ferry gap is narrow. Shamans heal their friends on the far bank.",
     bosses=[boss(MAGE)], obstacles=[W(0, 550, 280, 80), W(440, 550, 280, 80)], terrain=[swamp(0, 200, 720, 300)],
     camps=[camp(100, 350, sh=1, g=3), camp(620, 350, sh=1, g=3), camp(360, 800, o=1, g=3)],
     items=[it("atk_up", 150, 800), it("hp_up", 570, 800), it("reinforce", 360, 300)],
     squads=[sq(6, [[20, 400], [360, 420], [360, 110]], speed=50, sh=2, g=3)]),
  st("The Drowned King", "Three rivers, three crossings. The island camp waits in the middle.",
     bosses=[boss(KING)], obstacles=[W(0, 300, 330, 60), W(390, 300, 330, 60), W(0, 650, 100, 60), W(160, 650, 400, 60), W(620, 650, 100, 60)],
     camps=[camp(360, 500, o=2, g=3), camp(100, 180, o=1, ga=3), camp(620, 180, o=1, ga=3)],
     items=[it("reinforce", 360, 820), it("atk_up", 100, 500), it("hp_up", 620, 500)],
     squads=[sq(5, [[20, 500], [360, 420], [360, 280], [360, 120]], g=6), sq(10, [[700, 500], [360, 430], [360, 120]], speed=45, o=2, ga=3)]),
], "event:ev_ink_forge")

chapter("Shadow Wood", [
  st("Thorn Lanes", "Three lanes. The middle one is a swamp with a healer camp.",
     bosses=[boss(MAGE)], obstacles=[R(170, 200, 40, 600), R(510, 200, 40, 600)], terrain=[swamp(210, 200, 300, 600)],
     camps=[camp(90, 400, o=1, g=3, ga=1), camp(630, 400, o=1, g=3, ga=1), camp(360, 500, sh=1, g=3)],
     items=[it("atk_up", 90, 790), it("hp_up", 630, 790), it("reinforce", 360, 250)],
     squads=[sq(4, [[20, 150], [330, 110]], ga=5), sq(8, [[700, 150], [390, 110]], speed=45, o=2)]),
  st("Twin Shadows", "Sand on the west, swamp on the east, a mage at the end of each.",
     starts=TWO, bosses=bosses2(MAGE, MAGE), obstacles=[R(330, 150, 60, 650)], terrain=[sand(30, 250, 280, 500), swamp(410, 250, 280, 500)],
     camps=[camp(180, 500, o=1, g=3), camp(540, 500, sh=1, g=3), camp(360, 900, g=4, ga=2)],
     items=[it("atk_up", 80, 800), it("hp_up", 640, 800), it("reinforce", 80, 200), it("shield", 640, 200)],
     squads=[sq(5, [[20, 110], [180, 110]], g=6), sq(5, [[700, 110], [540, 110]], speed=50, sh=2, g=3)]),
  st("Cursed Crossroads", "A cursed stone blocks the crossroads. Every way around costs something.",
     bosses=[boss(MAGE)], obstacles=[Rk(360, 500, 75)], terrain=[road(330, 100, 60, 800), road(60, 470, 600, 60), sand(60, 100, 270, 370), swamp(390, 100, 270, 370), swamp(60, 530, 270, 330), sand(390, 530, 270, 330)],
     camps=[camp(195, 285, o=1, g=3), camp(525, 285, sh=1, g=3), camp(195, 700, g=3, ga=2)],
     items=[it("atk_up", 525, 700), it("hp_up", 360, 200)],
     squads=[sq(4, [[20, 500], [250, 420], [330, 110]], g=6), sq(8, [[700, 500], [470, 420], [390, 110]], speed=45, o=2)]),
  st("Witch Hunt", "Two squads hunt one mage. Healer camps guard both flanks.",
     starts=TWO, bosses=[boss(MAGE)], obstacles=[R(150, 350, 180, 40), R(390, 350, 180, 40), R(250, 600, 220, 40)],
     camps=[camp(90, 500, sh=2, g=3), camp(630, 500, sh=2, g=3), camp(360, 250, o=1, ga=3)],
     items=[it("atk_up", 90, 800), it("hp_up", 630, 800), it("reinforce", 360, 480)],
     squads=[sq(5, [[20, 250], [330, 110]], speed=50, sh=2, o=1), sq(5, [[700, 250], [390, 110]], speed=50, sh=2, o=1)]),
  st("Heart of Shadow", "A goblin king and the Shadow Mage. Two fronts, one ink pot.",
     starts=TWO, bosses=bosses2(KING, MAGE), obstacles=[R(330, 0, 60, 700)], terrain=[sand(0, 200, 330, 500), swamp(390, 200, 330, 500)],
     camps=[camp(100, 420, o=2, g=3), camp(620, 420, sh=2, o=1, g=2), camp(360, 860, g=4, ga=2)],
     items=[it("reinforce", 250, 620), it("reinforce", 470, 620), it("atk_up", 100, 760), it("hp_up", 620, 760)],
     squads=[sq(6, [[20, 250], [180, 110]], speed=45, o=2, g=3), sq(6, [[700, 250], [540, 110]], speed=50, sh=2, g=4)]),
], "shop")

chapter("The Ink Citadel", [
  st("Citadel Approach", "The red key waits in the swamp. The road through the sand is the only cheap way.",
     bosses=[boss(MAGE)], obstacles=[R(0, 500, 310, 50), R(410, 500, 310, 50)], terrain=[swamp(520, 650, 200, 300), sand(0, 150, 330, 350), sand(390, 150, 330, 350), road(330, 150, 60, 350)],
     camps=[camp(100, 800, o=1, g=3, ga=1), camp(100, 250, o=2, ga=2), camp(620, 250, o=2, ga=2)],
     items=[it("key", 650, 820, color="red"), gate("red", 310, 500, 100, 50), it("atk_up", 360, 750), it("hp_up", 620, 400)],
     squads=[sq(4, [[20, 330], [330, 110]], ga=6), sq(8, [[700, 330], [390, 110]], speed=45, o=2, g=3)]),
  st("Ink Moat", "A moat with two bridges guards both mages.",
     starts=TWO, bosses=bosses2(MAGE, MAGE), obstacles=[W(0, 350, 100, 60), W(160, 350, 400, 60), W(620, 350, 100, 60)], terrain=[swamp(0, 410, 720, 200)],
     camps=[camp(360, 230, o=2, sh=1, g=2), camp(80, 720, o=1, g=3, ga=1), camp(640, 720, o=1, g=3, ga=1)],
     items=[it("atk_up", 260, 800), it("hp_up", 460, 800), it("reinforce", 130, 250), it("shield", 590, 250)],
     squads=[sq(3, [[20, 200], [180, 110]], g=6), sq(3, [[700, 200], [540, 110]], g=6)]),
  st("Hall of Gates", "Two gates over sand and swamp. Orcs patrol the halls.",
     bosses=[boss(MAGE)], obstacles=[R(0, 640, 520, 50), R(620, 640, 100, 50), R(0, 330, 100, 50), R(200, 330, 520, 50)], terrain=[sand(0, 690, 520, 220), swamp(200, 380, 520, 260)],
     camps=[camp(360, 500, o=2, g=2), camp(600, 180, o=2, ga=2), camp(620, 830, o=1, g=3, ga=1)],
     items=[it("key", 90, 820, color="red"), gate("red", 520, 640, 100, 50), it("key", 640, 480, color="blue"), gate("blue", 100, 330, 100, 50), it("atk_up", 90, 500), it("hp_up", 360, 180), it("reinforce", 430, 800)],
     squads=[sq(5, [[700, 560], [150, 520], [150, 250], [330, 110]], speed=45, o=1, g=4), sq(0, [[700, 250], [390, 110]], ga=5)]),
  st("Last Stand", "Roads hug the walls. Sand and swamp fill everything between.",
     starts=TWO, bosses=[boss(MAGE)], obstacles=[R(330, 300, 60, 500)], terrain=[sand(90, 300, 240, 500), swamp(390, 300, 240, 500), road(30, 100, 60, 800), road(630, 100, 60, 800)],
     camps=[camp(200, 250, o=2, ga=2), camp(520, 250, o=2, sh=1, ga=1), camp(360, 900, o=1, g=4)],
     items=[it("atk_up", 200, 600), it("hp_up", 520, 600), it("reinforce", 60, 820), it("shield", 660, 820)],
     squads=[sq(5, [[20, 150], [330, 110]], speed=45, o=2, g=3), sq(5, [[700, 150], [390, 110]], speed=50, sh=2, o=1)]),
  st("The Ink Citadel", "The king and the mage defend the citadel together. Everything you learned, all at once.",
     starts=TWO, bosses=bosses2(KING, MAGE), obstacles=[R(100, 250, 200, 40), R(420, 250, 200, 40), R(330, 300, 60, 500)], terrain=[sand(0, 300, 330, 500), swamp(390, 300, 330, 500)],
     camps=[camp(60, 160, o=2, ga=2), camp(660, 160, sh=2, o=1, ga=1), camp(360, 880, o=2, g=3)],
     items=[it("reinforce", 200, 700), it("reinforce", 520, 700), it("atk_up", 100, 450), it("hp_up", 620, 450)],
     squads=[sq(6, [[20, 500], [60, 320], [180, 110]], speed=45, o=2, g=4), sq(6, [[700, 500], [660, 320], [540, 110]], speed=50, sh=2, o=1, g=3)]),
], None)

# Sân nhỏ ở chương đầu rồi to dần: co mọi toạ độ quanh tâm (360,500)
SIZE = [.7, .75, .8, .85, .88, .92, .96, 1, 1, 1]
def shrink(m, k):
    cx, cy = 360, 500
    P = lambda x, y: [round(cx + (x - cx) * k), round(cy + (y - cy) * k)]
    def pt(o):
        o["x"], o["y"] = P(o["x"], o["y"])
    def poly(ps): return [P(x, y) for x, y in ps]
    for o in m["starts"] + m["bosses"] + m["camps"]: pt(o)
    for o in m["obstacles"]:
        if o["type"] == "circle": pt(o); o["r"] = round(o["r"] * k)
        else:
            o["x"], o["y"] = P(o["x"], o["y"]); o["w"] = round(o["w"] * k); o["h"] = round(o["h"] * k)
    for o in m["items"]:
        if o["type"] == "gate":
            r = o["rect"]; r["x"], r["y"] = P(r["x"], r["y"]); r["w"] = round(r["w"] * k); r["h"] = round(r["h"] * k)
        else: pt(o)
    for t in m["terrain"] + m["goldZones"]: t["points"] = poly(t["points"])
    for q in m["enemySquads"]: q["route"] = poly(q["route"])
    m["bonusSquadRoute"] = poly(m["bonusSquadRoute"])
    m["referenceSolution"] = [poly(r) for r in m["referenceSolution"]]
    m["field"] = {"x": round(cx - 360 * k), "y": round(cy - 500 * k), "w": round(720 * k), "h": round(1000 * k)}
    return m

for f in glob.glob(os.path.join(MAPS, '*.json')): os.remove(f)
ids = []; chapters_json = []
for ci, (name, stages, interlude) in enumerate(CH, 1):
    stage_ids = []
    for si, s in enumerate(stages, 1):
        mid = f"c{ci}_s{si}"; ids.append(mid); stage_ids.append(mid)
        bonus = s["bonus"] or [[20, 500], [300, 120]]
        m = {"id": mid, "name": s["name"], "chapter": ci, "baseInk": 2000, "starts": s["starts"], "bosses": s["bosses"],
             "obstacles": s["obstacles"], "items": s["items"], "goldZones": s["gold"], "terrain": s["terrain"], "camps": s["camps"],
             "enemySquads": [dict(q, id=f"s{i}") for i, q in enumerate(s["squads"])], "bonusSquadRoute": bonus,
             "referenceSolution": [[[p["x"], p["y"]], [b["x"], b["y"]]] for p, b in zip(s["starts"], s["bosses"] * 2)], "tutorialHint": s["hint"]}
        if s["teach"] is not None: m["teach"] = s["teach"]
        m = shrink(json.loads(json.dumps(m)), SIZE[ci - 1])
        json.dump(m, open(os.path.join(MAPS, mid + ".json"), "w", encoding="utf8"), indent=2, ensure_ascii=False)
    if interlude and len(stage_ids) >= 3: stage_ids.insert(2, interlude)
    chapters_json.append({"name": name, "stages": stage_ids})
open(os.path.join(MAPS, 'index.ts'), 'w').write("".join(f"import {i} from './{i}.json';\n" for i in ids) + "export default {" + ",".join(ids) + "};\n")
json.dump(chapters_json, open(os.path.join(ROOT, 'src', 'data', 'chapters.json'), 'w', encoding='utf8'), indent=2, ensure_ascii=False)
print("wrote", len(ids), "stages in", len(CH), "chapters")
