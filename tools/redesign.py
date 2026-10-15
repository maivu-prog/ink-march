# Vòng thiết kế lại 15/10: mỗi chương một cơ chế chủ đề, đa dạng số trại và buff.
# Sửa trực tiếp JSON đang có (toạ độ viết theo sân gốc 720x1000, script tự co theo chương).
# Chạy: python tools/redesign.py .   rồi link-camps + solve-map cho các id in ra.
import json, os, sys
ROOT = sys.argv[1]
MAPS = os.path.join(ROOT, 'src', 'data', 'maps')
src = open(os.path.join(os.path.dirname(__file__), 'genmaps.py'), encoding='utf8').read()
ns = {'__name__': 'genmaps_defs'}
argv = sys.argv; sys.argv = ['genmaps.py', '/nonexistent']
exec(src[:src.index("for f in glob.glob(os.path.join(MAPS, '*.json')): os.remove(f)")], ns)
sys.argv = argv
g = type('G', (), ns)
R, W, camp, it, sand, swamp, road = g.R, g.W, g.camp, g.it, g.sand, g.swamp, g.road
def CH(x, y, w, h): return R(x, y, w, h, 'chasm')
def hill(x, y, w, h): return {"kind": "hill", "points": g.rect_pts(x, y, w, h)}
def slope(x, y, w, h, up=(0, -1)): return {"kind": "slope", "points": g.rect_pts(x, y, w, h), "up": list(up)}
def gold(x, y, w, h): return {"points": g.rect_pts(x, y, w, h)}

# Mỗi patch: terrain (chèn lên đầu để thắng vùng cũ), obstacles, gold, camps thêm, drop_camps (chỉ số), items thêm,
# swap_items {cũ: mới}, hint mới.
P = {
 # --- Biến thể số trại ở chương đầu ---
 'c3_s2': dict(camps=[camp(360, 820, g=3)], hint="Four camps in the maze. Any three earn every star."),
 # --- Chương 4: hai mặt trận + sông. Thêm lựa chọn trại ---
 'c4_s2': dict(camps=[camp(640, 860, g=2, ga=1)], hint="Four camps guard the fords. Pick the three on your way."),
 # --- Chương 5 Red Canyon: chìa khoá + dốc hẻm núi ---
 'c5_s1': dict(terrain=[slope(260, 500, 460, 400)], hint="The canyon floor climbs toward the gate. Fetch the key on the cheap low ground first."),
 'c5_s2': dict(terrain=[slope(100, 380, 620, 260, (1, 0))], swap={'atk_up': 'haste'}, hint="The middle terrace rises to the east. Keys, gates, and a thief band."),
 'c5_s3': dict(obstacles=[CH(200, 240, 320, 50)], camps=[camp(130, 760, g=3, ga=1)], swap={'reinforce': 'haste'}, hint="A ravine cuts the crossroads. Four camps: any three earn every star."),
 'c5_s4': dict(terrain=[slope(0, 300, 720, 160)], hint="The keep sits on high ground. Every climb costs ink."),
 # --- Chương 6 Shaman Fens: đầm + đồi (shaman đứng trên cao) ---
 'c6_s1': dict(terrain=[hill(0, 120, 140, 170), hill(580, 120, 140, 170)], hint="Two squads cross the fen. The flank camps hold the hills."),
 'c6_s2': dict(drop_camps=[2], hint="Only two camps, but the shaman patrol never stops. Clear both for every star."),
 'c6_s3': dict(terrain=[hill(270, 800, 180, 140)], hint="Two bosses mirror each other. The healer camp holds the southern hill."),
 'c6_s4': dict(terrain=[hill(260, 700, 200, 170)], items=[it('skull', 360, 640)], hint="The Shadow Mage waits beyond the fen. A trap sits on the short way."),
 # --- Chương 7 Iron Pass: vực + dốc đèo ---
 'c7_s1': dict(obstacles=[CH(160, 680, 260, 50)], terrain=[slope(160, 140, 400, 220)], hint="A ravine splits the west. The last climb to the outpost is steep."),
 'c7_s2': dict(terrain=[slope(0, 710, 720, 200), slope(0, 140, 720, 210)], hint="Switchbacks: climb, cross the archers' corridor, climb again."),
 'c7_s3': dict(obstacles=[CH(140, 580, 180, 40), CH(400, 520, 50, 40)], hint="Ravines narrow both lanes. The road on the west is the safe way."),
 'c7_s4': dict(terrain=[slope(0, 690, 310, 220)], hint="Two gates, three keys, and a steep western yard."),
 'c7_s5': dict(obstacles=[CH(0, 460, 250, 50), CH(470, 460, 250, 50)], camps=[camp(360, 820, o=1, g=2)], hint="Ravines cut the flanks. Take the royal road, then branch out. Four camps: any three earn every star."),
 # --- Chương 8 Golden Bridge: mực vàng bắc cầu ---
 'c8_s1': dict(gold=[gold(150, 495, 110, 100)], drop_camps=[1], hint="Two camps. Golden ink can bridge the river in the west; otherwise take the far ford."),
 'c8_s2': dict(gold=[gold(325, 560, 70, 90)], hint="Two squads, one river. A golden crossing joins the banks."),
 'c8_s4': dict(gold=[gold(80, 545, 120, 90), gold(520, 545, 120, 90)], swap={'reinforce': 'range_up'}, hint="The ferry gap is narrow. Golden ink opens two more crossings."),
 'c8_s5': dict(obstacles=[CH(0, 480, 230, 40), CH(490, 480, 230, 40)], gold=[gold(160, 645, 100, 70), gold(0, 475, 230, 50)], hint="Rivers and a ravine ring the island. Golden ink shortens every crossing."),
 # --- Chương 9 Shadow Wood: dốc/đồi + trại hồi máu, nhiều lựa chọn ---
 'c9_s1': dict(terrain=[slope(0, 200, 170, 600), slope(550, 200, 170, 600)], swap={'reinforce': 'haste'}, hint="Three lanes. The outer lanes climb; the middle swamp hides a healer camp."),
 'c9_s3': dict(camps=[camp(560, 760, o=1, g=2)], items=[it('skull', 250, 500)], hint="Four camps around the cursed stone. Any three earn every star. Mind the trap."),
 'c9_s4': dict(terrain=[hill(20, 410, 150, 180), hill(550, 410, 150, 180)], hint="Two squads hunt one mage. Healer camps hold the flank hills."),
 'c9_s5': dict(terrain=[slope(0, 700, 330, 120), slope(390, 700, 330, 120)], hint="A king and the Shadow Mage. Both fronts start with a climb."),
 # --- Chương 10 Ink Citadel: trộn mọi thứ ---
 'c10_s1': dict(terrain=[slope(0, 550, 310, 330)], hint="Climb the western yard or wade the eastern swamp for the red key."),
 'c10_s2': dict(gold=[gold(300, 345, 120, 70)], hint="A moat with two bridges. Golden ink can make a third."),
 'c10_s3': dict(items=[it('skull', 360, 760)], swap={'reinforce': 'haste'}, hint="Two gates over sand and swamp. Orcs patrol the halls, and a trap guards the short cut."),
 'c10_s4': dict(terrain=[hill(270, 820, 180, 120)], obstacles=[CH(150, 180, 120, 40), CH(450, 180, 120, 40)], hint="Roads hug the walls. Ravines guard the mage's door."),
 'c10_s5': dict(terrain=[hill(0, 120, 140, 120), hill(580, 120, 140, 120)], obstacles=[CH(0, 820, 120, 40), CH(600, 820, 120, 40)], hint="The king and the mage, on their hills. Everything you learned, all at once."),
}

SIZE = g.SIZE
changed = []
for mid, p in P.items():
    path = os.path.join(MAPS, mid + '.json')
    m = json.load(open(path, encoding='utf8'))
    if m.get('redesign') == '1015':
        continue
    k = SIZE[m['chapter'] - 1]
    add = {"starts": [], "bosses": [], "camps": p.get('camps', []), "obstacles": p.get('obstacles', []), "items": p.get('items', []),
           "terrain": p.get('terrain', []), "goldZones": p.get('gold', []), "enemySquads": [], "bonusSquadRoute": [], "referenceSolution": []}
    add = g.shrink(json.loads(json.dumps(add)), k)
    for i in sorted(p.get('drop_camps', []), reverse=True):
        m['camps'].pop(i)
    m['terrain'] = add['terrain'] + m['terrain']
    m['obstacles'] += add['obstacles']
    m['goldZones'] += add['goldZones']
    m['camps'] += add['camps']
    m['items'] += add['items']
    for o in m['items']:
        if o['type'] in p.get('swap', {}):
            o['type'] = p['swap'][o['type']]
    if 'hint' in p:
        m['tutorialHint'] = p['hint']
    m['redesign'] = '1015'
    json.dump(m, open(path, 'w', encoding='utf8'), indent=2, ensure_ascii=False)
    changed.append(mid)
print(' '.join(changed))
