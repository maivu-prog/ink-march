# Ink March — Spec demo (HTML, màn dọc)

> Tài liệu cho coding agent (Codex) dựng bản demo chơi được 15–30 phút.
> Ngôn ngữ spec: tiếng Việt. Tên biến/file/config: tiếng Anh.

---

## Thay đổi sau review (12/10)

Các mục dưới đây **ghi đè** phần tương ứng trong spec:

| Mục | Thay đổi |
|---|---|
| 6.1 Bản đồ nút | **Bỏ chọn nhánh.** Mỗi chương là chuỗi màn cố định, thắng tự sang màn sau. Shop và sự kiện là chặng nghỉ cố định (`chapters.json` → `stages`). Cả 7 map của mỗi chương đều được chơi |
| 5.7 Boss | Boss có chiêu tầm xa nhắm hàng sau. Mỗi đạo địch tới được boss: boss +25% ATK, +20% HP |
| 5.4 Giao tranh | Lính bị tách khỏi đội hình đi men theo đường vẽ để quay về |
| 6.5 Thoát giữa trận | Pause khi trận đã bắt đầu chỉ còn Retreat, tính là thua |
| 10.2 Map | 14 map làm lại, mỗi map một câu hỏi. Luật thiết kế kiểm tra tự động: xem README |
| 9 Tuần tra idle | **Bỏ.** Thay bằng gacha lính (màn Recruit): mở khoá loại lính và nhận thẻ để lên cấp. Lính không còn mở theo tiến độ màn |
| 8.2 Nâng cấp | Cần Vàng + thẻ lính (cấp n cần n thẻ) |
| 12 Đường vẽ | Dày hơn (`inkWidth` 16), viền tối + lõi sáng, mũi tên chỉ hướng, chuyển xanh lá khi hợp lệ |
| 4.5 Buff trên sân | Địch đi ngang buff thì cướp cho cả đạo (buff mất). Đầu lâu bẫy cả địch. Lọ mực/chìa/rương không bị cướp |
| Chương/màn (13/10) | 10 chương × 3–5 màn, sân nhỏ dần to. Mỗi màn 3 trại địch = 3 sao. Có màn hai mặt trận dùng chung bình mực |
| Brush (13/10) | Gacha chính bằng Ngọc. Brush đổi tốc độ đốt mực/hiệu ứng, không đổi lượng mực. Model 3D hoạt hình hiện khi vẽ |
| Địa hình (13/10) | Cát, đầm lầy, đường mòn: đổi mực đốt và tốc độ hành quân |
| Lính (13/10) | Có sẵn 6 con. Gacha lính bằng Vàng là phụ |
| 13 Tham số | `starInkRatio` 0.1, `runLevelXp` [40…160], bỏ `cameraTiltDeg`/`cameraFov` (camera orthographic cố định) |

---

## 0. ELI5

Bạn có một đạo quân nhỏ ở dưới màn hình và một con boss ở trên cùng. Bạn **cầm bút vẽ một con đường** từ quân mình tới boss, nhưng **mực có hạn**. Trên đường có bùa tăng sức mạnh, chìa khoá, rương, và cả những đạo quân địch cũng đang đi về phía boss. Vẽ xong bấm **Start**, quân bạn tự đi theo đường, gặp ai thì tự đánh, tới boss thì tự đánh boss. Bạn chỉ ngồi xem.

Vẽ khéo, **tiết kiệm mực** thì mực thừa thành **điểm kinh nghiệm của chuyến đi**, đủ điểm được chọn thêm sức mạnh. Một chuyến đi (run) gồm nhiều trận nối nhau trên một bản đồ có nhiều ngã rẽ. Thua thì làm lại chuyến mới, nhưng vàng đã kiếm vẫn giữ để nâng cấp lính.

Mỗi màn đã thắng, **con đường bạn vẽ được lưu lại thành tuyến tuần tra**: quân bạn đi đi lại lại trên đó để kiếm vàng kể cả khi tắt game. Đường càng xịn (ăn nhiều bùa, mở rương, chặn được địch) thì kiếm càng nhiều.

---

## 1. Tổng quan

| Mục | Giá trị |
|---|---|
| Tên tạm | Ink March |
| Thể loại | Puzzle vẽ đường + auto battle + roguelite run + idle tuần tra |
| Nền tảng | Web (HTML5), ưu tiên mobile browser, màn **dọc** |
| Đồ hoạ | **3D**, camera **nhìn từ trên xuống** (top-down). Gameplay là 2D trên mặt đất, chỉ phần hiển thị là 3D |
| Độ dài demo | 2 chương, khoảng 15–30 phút |
| Người chơi tương tác | **Chỉ trước trận** (chọn đội, vẽ đường) và giữa các trận (chọn nút, chọn buff, nâng cấp). **Trong trận không có thao tác nào** ngoài nút tốc độ x1/x2 |

### 1.1 Ba trụ, ba tầng

| Tầng | Thời lượng | Sở hữu | Không được đụng tới |
|---|---|---|---|
| **Trận** | 1–2 phút | Đường vẽ, mực, buff trên sân, chìa/cổng/rương, aggro, combat | |
| **Run (chương)** | 10–15 phút | Bản đồ nút, XP run, buff run (chọn 1 trong 3), Xu run, mực vàng | Cấp lính vĩnh viễn |
| **Vĩnh viễn** | Xuyên suốt | Vàng, cấp loại lính, mở khoá loại lính, tuần tra idle | **Mực thường** (không bao giờ được nâng mực bằng meta) |

### 1.2 Nguyên tắc thiết kế bất biến (Codex phải giữ)

1. **Mực gốc của mỗi map luôn đủ giải đường chính.** Không có nguồn nào ngoài map (meta, run) được cộng vào mực thường của trận.
2. Mực mang sang giữa các trận **không cộng vào bình mực**. Mực dư chuyển thành **XP run** (mục 6.2).
3. **Mực vàng** chỉ dùng được trên **vùng vàng** designer đặt sẵn. Trong demo chỉ có **1 map** có vùng vàng (mục 4.9).
4. Meta chỉ tăng **HP/ATK**. Không có nâng cấp vĩnh viễn nào cho tầm đánh, tốc độ hay mực.

---

## 2. Công nghệ & cấu trúc

| Mục | Yêu cầu |
|---|---|
| Stack | Vite + TypeScript + **Three.js** (render 3D). UI (HUD, menu, thẻ buff) làm bằng **HTML/CSS overlay** đè lên canvas, không vẽ UI trong 3D |
| Độ phân giải logic | Khung dọc tỉ lệ 9:16 (logic 720 × 1280), co giãn vừa màn hình, căn giữa. Desktop hiển thị khung dọc ở giữa |
| Input | Pointer (chuột và cảm ứng như nhau), **một ngón** |
| Art | Placeholder bằng khối 3D cơ bản và màu (mục 12). Không chặn tiến độ vì art |

### 2.0 3D và camera nhìn từ trên xuống

| Cơ bản | Edge case |
|---|---|
| **Toàn bộ logic (đường vẽ, va chạm, aggro, combat, map json) chạy trên mặt phẳng 2D**, toạ độ `(x, y)` trong sân 720 × 1000 | Không dùng physics 3D. Test chạy headless, không cần WebGL |
| Hiển thị: mặt đất là mặt phẳng XZ của Three.js. Ánh xạ `worldX = x`, `worldZ = y`, đơn vị 1 px = 1 unit (hoặc scale chung `worldScale`) | Trục `y` của map tăng từ trên xuống, nên điểm xuất phát (y lớn) nằm gần phía dưới màn hình |
| Camera **nhìn từ trên xuống, hơi nghiêng** để thấy khối 3D: mặc định `PerspectiveCamera`, góc nghiêng `cameraTiltDeg` (mặc định 15° so với phương thẳng đứng), FOV `cameraFov` | Đặt `cameraTiltDeg = 0` thì thành nhìn thẳng từ trên xuống. Camera phải **thấy trọn sân** 720 × 1000 ở mọi tỉ lệ màn hình dọc |
| Camera **cố định** trong giai đoạn vẽ (không pan, không zoom) để vẽ không bị trôi | Giai đoạn hành quân: cho phép camera hơi lắc khi boss dùng kỹ năng. Không bám theo đạo quân |
| Vẽ đường: **raycast** từ điểm chạm xuống mặt phẳng đất để lấy `(x, y)` logic | Chạm trúng vật thể 3D cao (đá, boss) thì vẫn lấy giao điểm với **mặt đất**, bỏ qua mesh |
| Đường mực hiển thị là dải mesh phẳng (ribbon) nằm sát mặt đất (nâng `y = 0.5` để không z-fighting), dày 8 unit | Đoạn trong vùng vàng đổi màu vàng |
| Toạ độ của HUD/bong bóng gợi ý gắn với vật thể: chiếu từ 3D ra màn hình (`Vector3.project`) | |
| Đổ bóng đơn giản (1 directional light có shadow) | Mobile yếu: tắt shadow qua `config.shadows = false` |
| Lưu | `localStorage`, key `inkmarch_save_v1`, bọc try/catch. Lỗi đọc thì tạo save mới |
| Data | Toàn bộ số liệu nằm trong `src/data/*.json`, **không hard-code** trong logic |
| Build | `npm run dev`, `npm run build` ra static folder chạy được khi mở bằng server tĩnh |

### 2.1 Cấu trúc thư mục đề xuất

```
ink-march/
  src/
    main.ts
    scenes/        Boot, Home, Squad, Upgrade, Patrol, RunMap, Battle, Result, BuffPick, Event, Shop, RunEnd
                   (Battle và Patrol dùng Three.js; các màn còn lại là HTML/CSS overlay)
    render/        Stage3D.ts (scene, camera, light), MapView.ts, UnitView.ts, InkRibbon.ts, Picking.ts
    systems/       InkPath.ts, PathValidator.ts, Army.ts, Combat.ts, EnemySquad.ts, Boss.ts,
                   RunState.ts, MetaState.ts, Patrol.ts, Save.ts
    data/          config.json, units.json, enemies.json, bosses.json, fieldBuffs.json,
                   runBuffs.json, events.json, chapters.json, maps/*.json
    debug/         DebugPanel.ts
  tests/           pathValidator.test.ts, mapSolvable.test.ts, combat.test.ts
```

---

## 3. Vòng lặp chơi

```
Home ─► Chọn đội (3 slot) ─► Bản đồ run ─► [Nút trận] ─► Vẽ đường ─► Start ─► Xem trận
  ▲                              ▲                                              │
  │                              └──── Chọn buff (nếu lên cấp) ◄── Kết quả ◄────┘
  │                              [Nút sự kiện / shop]
  └── Kết thúc run (thắng boss / thua) ─► nhận Vàng ─► Nâng cấp / Tuần tra
```

---

## 4. Trận đấu: giai đoạn VẼ (Plan)

### 4.1 Bố cục màn hình

| Vùng | Kích thước | Nội dung |
|---|---|---|
| HUD trên | 720 × 120 | Thanh mực (số + thanh), mực vàng (nếu > 0), nút Pause |
| Sân | 720 × 1000 | Map. Điểm xuất phát ở **dưới**, boss ở **trên** |
| Thanh dưới | 720 × 160 | Nút **Reset**, **Undo**, **Start** (chỉ sáng khi đường hợp lệ), chân dung 3 slot |

### 4.2 Thông tin hiện ra khi vẽ

- Đường đi của **mọi đạo địch** hiện dạng nét đứt, mũi tên theo chiều đi, kèm số giây xuất phát.
- **Bóng ma thời gian:** trong lúc vẽ, ở đầu bút hiện con số `t = x.x s`, là thời điểm quân mình (đi tốc độ chuẩn, không tính dừng đánh) sẽ tới điểm đó. Đồng thời các đạo địch hiện **bóng mờ** ở vị trí của chúng tại thời điểm `t`. Nhờ vậy người chơi tính được chỗ chặn.
- Vòng aggro của đạo địch và của quân mình hiện mờ.

### 4.3 Luật vẽ

| Cơ bản | Edge case |
|---|---|
| Bắt đầu nét bằng cách chạm trong bán kính `startSnapRadius` quanh điểm xuất phát | Chạm ngoài vùng đó: không vẽ, điểm xuất phát nhấp nháy gợi ý |
| Kéo tay để vẽ. Đường là polyline, lấy mẫu mỗi `sampleStep` px | Kéo nhanh: nội suy thêm điểm sao cho không đoạn nào dài hơn `sampleStep` |
| Mỗi px đường tiêu 1 mực | Hết mực: đường dừng ở điểm cuối cùng, thanh mực rung đỏ, ngón tay kéo tiếp không vẽ thêm |
| Đường không được đi xuyên vật cản | Đoạn mới cắt vật cản: **không thêm điểm**. Đường đứng ở mép, khi ngón tay ra khỏi vật cản mà đoạn thẳng từ điểm cuối tới ngón tay không cắt vật cản thì vẽ tiếp |
| Đường được **cắt ngang đường địch** | Không có luật cấm. Cắt ngang chỉ có ý nghĩa khi khớp thời gian (aggro) |
| Đường được tự cắt chính nó | Cho phép. Ink vẫn tính theo độ dài |
| Chạm vào vùng boss (bán kính `bossSnapRadius`) thì đường **tự hoàn thành**, nét kết thúc, đường **hợp lệ** | Đi qua boss rồi kéo tiếp: phần thừa bỏ đi, không tốn mực |
| Nhấc tay khi chưa tới boss: đường vào trạng thái **chờ** (nhấp nháy đỏ) trong `liftGraceSec` giây. Chạm lại trong bán kính `resumeRadius` quanh đầu mút thì vẽ tiếp | Hết thời gian chờ mà không nối: **fail**, đường xoá, hoàn toàn bộ mực, mọi vật phẩm đã đánh dấu trả lại trạng thái ban đầu |
| Nút **Undo**: xoá ngược `undoLength` px cuối, hoàn mực tương ứng | Undo lùi qua lọ mực, chìa khoá: trả lại vật phẩm, trừ lại mực của lọ. Nếu mực âm thì tiếp tục lùi cho tới khi mực ≥ 0 |
| Nút **Reset**: xoá cả đường | |
| Nút **Start** chỉ bấm được khi đường hợp lệ | Đường hợp lệ vẫn được Undo để sửa. Sau Undo thì thành chưa hợp lệ |

### 4.4 Vật phẩm trên sân: đánh dấu khi vẽ, nhận khi đi qua

- Khi **đường vẽ** đi trong bán kính `pickupRadius` của vật phẩm, vật phẩm được **đánh dấu** (viền sáng, kèm icon ✓ nhỏ).
- **Lọ mực** là ngoại lệ: cộng mực **ngay lúc vẽ** (để mở puzzle "đi vòng lấy mực rồi mới đủ mực đi tiếp").
- Mọi vật phẩm khác chỉ **có hiệu lực khi quân đi tới** điểm gần nhất trên đường. Nếu quân chết hết trước đó thì không nhận.
- Mỗi vật phẩm chỉ nhận một lần.

### 4.5 Buff trên sân (`fieldBuffs.json`), chỉ hiệu lực trong trận

| id | Tên | Hiệu ứng |
|---|---|---|
| `atk_up` | Kiếm đỏ | +20% ATK cả đạo, cộng dồn |
| `hp_up` | Tim xanh | +25% HP tối đa và hồi lượng máu tương ứng |
| `reinforce` | Cờ tiếp viện | +2 lính vào slot có ít lính nhất |
| `range_up` | Ống nhòm | +20% tầm đánh của lính ranged |
| `shield` | Khiên vàng | Mỗi lính nhận khiên 40 điểm, chặn sát thương trước HP |
| `haste` | Giày gió | +25% tốc độ hành quân |
| `ink_bottle` | Lọ mực | +`value` mực ngay khi vẽ qua |
| `skull` | Đầu lâu (bẫy) | Mỗi slot mất 1 lính. Khi vẽ qua thì cảnh báo đỏ |

### 4.6 Chìa, cổng, rương

| Cơ bản | Edge case |
|---|---|
| Chìa có màu (`red`/`blue`). Đường đi qua chìa thì "cầm" chìa màu đó | Cầm nhiều chìa cùng màu thì đếm số lượng |
| **Cổng** cùng màu là vật cản, nhưng đường được đi xuyên qua nếu **trước đó trên cùng nét** đã cầm chìa đúng màu. Đi qua thì tiêu 1 chìa | Vẽ tới cổng mà chưa có chìa: cổng là vật cản bình thường, hiện icon ổ khoá đỏ |
| **Rương** cùng màu: đi qua khi có chìa thì mở, tiêu 1 chìa | Đi qua rương mà không có chìa: không đánh dấu, rương hiện ổ khoá |
| Rương mở: sau trận người chơi được **chọn thêm 1 buff run** (trong 3) | Thắng trận mới nhận. Thua thì mất |
| Undo lùi qua cổng hay rương: trả lại chìa | Undo lùi qua chìa mà phía sau đã dùng chìa đó: lùi tiếp tới trước cổng/rương đã dùng nó |

### 4.7 Vật cản

- Dạng `rect`, `circle`, `polygon`. Có thuộc tính `blocksUnits` (mặc định true). Lính không đi xuyên vật cản khi rời đường để đánh nhau (mục 5.4).
- Loại `water` (sông): chặn vẽ, chặn lính, dùng cho map mực vàng.

### 4.8 Mực

| Cơ bản | Edge case |
|---|---|
| Mực của trận = `map.baseInk` | **Không** cộng từ meta, từ run hay từ trận trước |
| Lọ mực cộng thêm khi vẽ qua | Thanh mực có thể vượt `baseInk` (hiện phần vượt màu khác) |
| Mực dư = mực còn lại lúc bấm Start | Dùng để tính XP run (mục 6.2) và ⭐ |

### 4.9 Mực vàng (gia vị, chỉ 1 map: `c2_m4`)

| Cơ bản | Edge case |
|---|---|
| Mực vàng là tài nguyên **của run** (`run.goldInk`, đơn vị px) | Hết run thì mất |
| Map có **vùng vàng** (`goldZones`, polygon). Vẽ trong vùng vàng thì tiêu **mực vàng** thay vì mực thường, 1 px = 1 mực vàng | `run.goldInk = 0`: vùng vàng là vật cản, hiện icon ổ khoá vàng kèm tooltip "Cần mực vàng" |
| Mực vàng hết khi đang vẽ trong vùng: đường dừng ở đó như hết mực | Undo trong vùng thì hoàn mực vàng |
| Nguồn mực vàng: sự kiện **Lò luyện mực**, shop (mục 7) | Chỉ xuất hiện ở các nút **trước** `c2_m4` trong chương 2 |
| Map `c2_m4` vẫn **giải được không cần mực vàng**. Vùng vàng là lối tắt tới rương lớn và điểm chặn một đạo địch | Mực vàng thừa sau `c2_m4` đổi thành XP run theo `goldInkToXp` |

---

## 5. Trận đấu: giai đoạn HÀNH QUÂN (auto)

### 5.1 Đạo quân người chơi

- Một đạo, **3 slot**, đi chung một đường. Mỗi slot = một loại lính với số lượng lính theo `units.json`.
- **Thứ tự slot:** slot 1 đi đầu, slot 3 đi cuối. Mỗi slot cách nhau `slotSpacing` px dọc theo đường. Lính trong slot xếp thành cụm nhỏ quanh tâm slot.
- Tốc độ đạo = `armySpeed` px/s (nhân buff haste). Cả đạo đi cùng tốc độ.
- Được trùng loại lính giữa các slot.

### 5.2 Loại lính (`units.json`), chỉ số cấp 1

| id | Tên | Vai | Số lính/slot | HP | ATK | Nhịp đánh (s) | Tầm (px) | Đặc tính | Mở khoá |
|---|---|---|---|---|---|---|---|---|---|
| `sword` | Kiếm sĩ | melee | 4 | 120 | 12 | 0.8 | 30 | | Có sẵn |
| `archer` | Cung thủ | ranged | 4 | 70 | 10 | 1.0 | 140 | Đạn bay `projectileSpeed` | Có sẵn |
| `shield` | Khiên binh | tank | 3 | 260 | 6 | 1.0 | 30 | Giảm 30% sát thương nhận. Địch melee ưu tiên đánh khiên binh trong tầm | Qua nút L3 chương 1 |
| `spear` | Thương binh | melee | 3 | 100 | 14 | 0.9 | 60 | Đánh xuyên 2 mục tiêu thẳng hàng | Qua elite chương 1 |
| `mage` | Pháp sư | ranged | 2 | 60 | 18 | 1.6 | 120 | Sát thương lan bán kính 40 | Thắng boss chương 1 |
| `healer` | Trị liệu | support | 2 | 70 | 4 | 1.2 | 110 | Thay vì đánh: hồi 10 HP cho đồng minh thấp máu nhất trong tầm. Không ai mất máu thì đánh thường | Qua nút L3 chương 2 |

### 5.3 Synergy đội hình (tính lúc vào trận)

| Điều kiện | Thưởng |
|---|---|
| 2 slot cùng loại | +15% ATK cho loại đó |
| 3 slot cùng loại | +30% ATK cho loại đó |
| Slot 1 là melee/tank **và** slot 3 là ranged/support | +10% HP cả đạo ("Tiền tuyến") |

Màn chọn đội phải hiện synergy đang kích hoạt.

### 5.4 Aggro & giao tranh (cả hai phía dùng chung luật)

| Cơ bản | Edge case |
|---|---|
| Mỗi đạo (của mình hoặc địch) có `aggroRadius` = tầm xa nhất trong các lính còn sống của đạo, cộng `aggroPadding` | Lính ranged chết hết thì aggro co lại theo tầm của lính còn sống |
| Khi có lính phe A lọt vào aggro của đạo phe B (hoặc ngược lại), **cả hai đạo dừng hành quân** và vào trạng thái giao tranh | Khoảng cách tính từ lính gần nhất của mỗi bên |
| Trong giao tranh, từng lính chọn mục tiêu **gần nhất** (trừ luật khiêu khích của khiên binh). Trong tầm thì đánh. Ngoài tầm thì **rời đường**, di chuyển tới mục tiêu (né vật cản bằng steering đơn giản hoặc lưới A*) | Lính không được đi quá `leashRadius` tính từ vị trí slot trên đường. Quá thì quay về |
| Lính ranged đứng yên bắn khi mục tiêu đã trong tầm | Vì aggro = tầm xa nhất, đạo có ranged thường **bắn trước** khi melee hai bên chạm nhau. Đây là hành vi mong muốn |
| Hết địch trong aggro: lính **quay về vị trí đội hình** trên đường (tối đa `regroupSec` giây), rồi đạo đi tiếp | Lính chưa kịp về sau `regroupSec` thì dịch chuyển nhẹ (lerp nhanh) về chỗ |
| Hai đạo địch cùng lọt aggro thì cả hai nhập trận | Đạo địch thứ ba tới sau thì nhập trận khi lọt aggro |
| Đạo địch đang giao tranh thì **không đi tiếp về boss** | Đánh xong mà còn sống thì đi tiếp |
| Cắt ngang đường địch nhưng lệch thời gian, không ai lọt aggro: **không có giao tranh** | Đây là một phần của puzzle, không phải lỗi |

### 5.5 Đạo địch (`maps/*.json` → `enemySquads`)

- Mỗi đạo có: `route` (polyline), `spawnDelay` (giây kể từ Start), `speed`, `units` (loại và số lượng).
- Đạo địch xuất phát tại điểm đầu `route`, đi về boss. Tới boss thì vào trạng thái **hộ vệ**: đứng quanh boss, đánh mọi lính người chơi trong tầm.
- Trước khi bấm Start, đạo địch đứng ở điểm xuất phát (hiện số giây đếm ngược `spawnDelay`).

### 5.6 Loại lính địch (`enemies.json`)

| id | Tên | Vai | HP | ATK | Nhịp (s) | Tầm | Tốc độ | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| `goblin` | Goblin | melee | 60 | 8 | 0.9 | 30 | 55 | |
| `goblin_archer` | Goblin cung | ranged | 40 | 7 | 1.1 | 130 | 55 | |
| `orc` | Orc | melee | 220 | 18 | 1.2 | 35 | 45 | |
| `shaman` | Pháp sư goblin | support | 50 | 4 | 1.4 | 110 | 50 | Hồi 8 HP cho đồng minh thấp máu nhất |

### 5.7 Boss (`bosses.json`)

- Boss đứng yên ở điểm cuối. Có HP, ATK, tầm, nhịp đánh và 1–2 kỹ năng tự động.
- Khi quân mình tới vùng boss: đạo **dừng hẳn**, mọi lính vào giao tranh với boss và hộ vệ.

| id | Chương | HP | ATK | Tầm | Nhịp | Kỹ năng |
|---|---|---|---|---|---|---|
| `goblin_king` | 1 (boss thường của map dùng `goblin_chief`, 40% chỉ số) | 1500 | 25 | 50 | 1.5 | **Dậm đất:** mỗi 6 s, sát thương 30 lên mọi lính trong bán kính 90 |
| `shadow_mage` | 2 | 3000 | 22 | 150 | 1.8 | **Triệu hồi:** mỗi 12 s gọi 3 `goblin` cạnh boss. **Khiên bóng tối:** khi HP < 50% lần đầu, nhận khiên 600 trong 8 s |

Map thường (không phải boss chương) dùng boss nhỏ theo `map.boss` với chỉ số scale `bossScale`.

### 5.8 Thắng / thua

| Cơ bản | Edge case |
|---|---|
| Boss về 0 HP: **thắng** | Hộ vệ còn sống thì tự biến mất (hiệu ứng tan) |
| Mọi lính người chơi chết: **thua** | |
| Vượt `battleTimeoutSec`: **thua** | Hiện lý do "Hết giờ" |
| Nút tốc độ x1/x2 trong trận | Lưu lựa chọn x2 cho các trận sau (localStorage) |

### 5.8b Sao (⭐) mỗi map

| ⭐ | Điều kiện |
|---|---|
| 1 | Thắng |
| 2 | Thắng và mực dư ≥ `starInkRatio` × `baseInk` |
| 3 | Thắng, đạt ⭐2, và mở hết rương của map (map không có rương thì chặn được hết các đạo địch trước khi chúng tới boss) |

Lưu sao tốt nhất của từng map vào save.

---

## 6. Run (chương)

### 6.1 Bản đồ nút (`chapters.json`)

- Mỗi chương có 7 tầng. Người chơi đi từ dưới lên, mỗi tầng chọn 1 trong các nút nối với nút vừa qua.
- **Map gắn cố định với nút** (không random). Phần roguelite nằm ở: nhánh đi, buff được đưa ra, sự kiện, hàng trong shop.

| Tầng | Lựa chọn | Dạy gì (chương 1) |
|---|---|---|
| L1 | Trận `c1_m1` | Vẽ, mực, Start |
| L2 | Trận `c1_m2` **hoặc** Sự kiện | Buff trên sân, lọ mực |
| L3 | Trận `c1_m3` **hoặc** Shop | Đạo địch đầu tiên, chặn đường |
| L4 | Elite `c1_e1` **hoặc** Sự kiện | Chìa → cổng |
| L5 | Trận `c1_m5a` **hoặc** Trận `c1_m5b` | Chìa → rương, đầu lâu |
| L6 | Shop **hoặc** Sự kiện | |
| L7 | Boss chương `c1_boss` | Tổng hợp |

Chương 2 cùng khung, map `c2_*` khó hơn: nhiều đạo địch trên nhiều tuyến, có Orc và Shaman. Nút L4 của chương 2 là trận `c2_m4` (**map mực vàng**). Mọi nguồn mực vàng (sự kiện Lò luyện mực, ô mực vàng trong shop) chỉ xuất hiện ở L2–L3 chương 2.

Chương 2 chỉ mở sau khi thắng boss chương 1.

### 6.2 XP run & lên cấp

| Cơ bản | Edge case |
|---|---|
| Thắng trận: `XP += leftoverInk × inkToXp + battleXp[nodeType]` | Thua trận: kết thúc run, không cộng XP |
| Đủ ngưỡng `runLevelXp[level]`: lên cấp, mở màn **Chọn buff** (1 trong 3 buff run, random theo trọng số) | Lên nhiều cấp một lúc thì chọn lần lượt |
| Rương mở trong trận: thêm 1 lượt chọn buff sau trận | Cộng với lượt lên cấp nếu có |
| Thanh XP run luôn hiện trên màn bản đồ run và màn kết quả | Màn kết quả hiện rõ "Mực dư 340 → +34 XP" để người chơi hiểu vì sao nên tiết kiệm |

### 6.3 Buff run (`runBuffs.json`), kéo dài hết run

| id | Tên | Hiệu ứng | Trọng số |
|---|---|---|---|
| `rb_atk` | Lưỡi sắc | +12% ATK cả đạo (cộng dồn) | 10 |
| `rb_hp` | Giáp dày | +15% HP cả đạo (cộng dồn) | 10 |
| `rb_volley` | Bắn loạt | Cung thủ bắn thêm 1 mũi tên vào mục tiêu thứ hai | 6 |
| `rb_eagle` | Mắt ưng | +15% tầm đánh cho ranged | 6 |
| `rb_vamp` | Hút máu | Melee hồi 10% sát thương gây ra | 6 |
| `rb_pickup_heal` | Bùa hồi | Mỗi lần nhận buff trên sân: hồi 10% HP cả đạo | 6 |
| `rb_extra_unit` | Tân binh | +1 lính cho mỗi slot | 5 |
| `rb_boss_slayer` | Diệt đầu lĩnh | +25% sát thương lên boss | 6 |
| `rb_first_strike` | Đánh phủ đầu | 5 s đầu mỗi giao tranh: +40% ATK | 6 |
| `rb_frugal` | Keo kiệt | `inkToXp` +50% | 5 |
| `rb_golden_touch` | Bàn tay vàng | +20% Xu run mỗi trận | 5 |
| `rb_skull_ward` | Bùa trừ tà | Miễn hiệu ứng đầu lâu | 4 |

Buff đã cộng dồn tối đa (`maxStack` trong json) thì không xuất hiện nữa.

### 6.4 Tiền tệ

| Tiền | Phạm vi | Nguồn | Dùng |
|---|---|---|---|
| **Xu** | Run | Thắng trận | Shop trong run |
| **Mực vàng** | Run | Sự kiện, shop (chương 2) | Vùng vàng ở `c2_m4` |
| **Vàng** | Vĩnh viễn | Thắng trận, kết thúc run, tuần tra | Nâng cấp lính |

### 6.5 Kết thúc run

| Cơ bản | Edge case |
|---|---|
| Thắng boss chương: run thắng, thưởng Vàng `runClearGold[chapter]`, mở chương sau, mở lính theo bảng 5.2 | |
| Thua bất kỳ trận nào: run thua. **Giữ toàn bộ Vàng đã kiếm trong run**, mất buff run, Xu, mực vàng | Không được để người chơi thua trắng tay |
| Thoát game giữa run: lưu `runState`, vào lại thì tiếp tục từ màn bản đồ run | Thoát giữa trận: trận đó tính lại từ giai đoạn vẽ |

---

## 7. Sự kiện & Shop

### 7.1 Sự kiện (`events.json`), mỗi sự kiện có 2 lựa chọn

| id | Tên | Lựa chọn A | Lựa chọn B | Ghi chú |
|---|---|---|---|---|
| `ev_ink_forge` | Lò luyện mực | Đổi 40 XP run lấy 250 mực vàng | Bỏ qua | **Chỉ ở chương 2, L2–L3** |
| `ev_shrine` | Đền cầu nguyện | Nhận 1 buff run ngẫu nhiên, trận sau lính bắt đầu với 80% HP | Bỏ qua | |
| `ev_mercenary` | Lính đánh thuê | Trả 60 Xu: +2 lính cho slot chọn, hết run | Bỏ qua | |
| `ev_mystery_chest` | Rương bí ẩn | 60%: chọn 1 trong 3 buff run. 40%: trận sau có thêm 1 đạo `goblin` ×4 | Bỏ qua | Đạo thêm đi một tuyến định sẵn trong map (`bonusSquadRoute`) |

### 7.2 Shop

- 3 buff run ngẫu nhiên, giá 60–100 Xu (theo `shopPrice` trong json).
- Chương 2 trước L4: ô **mực vàng** 150 px giá 50 Xu.
- Nút đổi hàng: 20 Xu, giá tăng thêm 10 Xu sau mỗi lần đổi.

---

## 8. Meta (vĩnh viễn)

### 8.1 Chọn đội

- Màn chọn đội trước mỗi run: kéo loại lính vào 3 slot, đổi được thứ tự. Hiện synergy (5.3).
- Chỉ dùng loại lính đã mở khoá.

### 8.2 Nâng cấp lính

| Cơ bản | Edge case |
|---|---|
| Mỗi loại lính có cấp 1–10 | Cấp 10 thì nút nâng cấp chuyển thành "Tối đa" |
| Mỗi cấp: +`levelStatPct`% HP và ATK (tính theo chỉ số cấp 1, cộng tuyến tính) | **Không** tăng tầm, tốc độ, nhịp đánh |
| Giá: `round(upgradeBaseCost × upgradeCostGrowth^(level-1))` Vàng | Không đủ Vàng: nút xám, hiện số còn thiếu |

### 8.3 Nguồn Vàng

| Nguồn | Mặc định |
|---|---|
| Thắng trận thường / elite / boss chương | 20 / 45 / 120 |
| Mỗi ⭐ đạt được **lần đầu** ở một map | +10 |
| Kết thúc run thắng | `runClearGold`: chương 1 = 150, chương 2 = 300 |
| Tuần tra | Mục 9 |

---

## 9. Tuần tra idle

### 9.1 Lưu tuyến

| Cơ bản | Edge case |
|---|---|
| Mỗi lần **thắng** một map: tính `patrolScore` của đường vừa đi (dựa trên những gì **thực sự nhận được** trong trận) | Thua: không lưu |
| Nếu `patrolScore` mới > điểm đang lưu của map đó: thay đường lưu, hiện thông báo "Tuyến tuần tra mới tốt hơn! +x%" | Bằng hoặc thấp hơn: giữ đường cũ |
| Lưu: polyline đường, `patrolScore`, số buff, số rương, số đạo địch đã chặn | |

`patrolScore = 1 + buffWeight × buffsCollected + chestWeight × chestsOpened + interceptWeight × squadsIntercepted`

(Đầu lâu không tính là buff. Đạo "đã chặn" = đạo bị tiêu diệt trước khi tới boss.)

### 9.2 Kiếm Vàng

| Cơ bản | Edge case |
|---|---|
| Người chơi chọn **1 map đã lưu** làm tuyến tuần tra đang chạy | Chưa có map nào: màn tuần tra hiện "Thắng một màn để mở tuần tra" |
| Vàng/phút = `map.patrolBaseGold × patrolScore` | |
| Thời gian thực nhân `patrolTimeScale` (để demo 15–30 phút vẫn thấy tiền chảy) | |
| Cộng dồn kể cả khi tắt game, theo `lastPatrolTimestamp` | Tối đa `patrolCapMinutes` phút tuần tra. Đầy thì hiện "Kho đầy" |
| Nút **Thu** trên Home và màn tuần tra | Đổi tuyến tuần tra: tự thu số đang có trước khi đổi |
| Màn tuần tra hiện mini-map: đạo quân chạy vòng trên đường đã lưu (chạy tới boss rồi quay về đầu, lặp lại), hiện buff/rương đã ăn trên tuyến | Chỉ là hoạt cảnh, không có combat |

---

## 10. Nội dung map

### 10.1 Định dạng map (`src/data/maps/<id>.json`)

```jsonc
{
  "id": "c1_m3",
  "name": "Ngã ba rừng",
  "baseInk": 1600,
  "start": { "x": 360, "y": 940 },          // toạ độ trong sân 720×1000
  "boss": { "type": "goblin_chief", "x": 360, "y": 80, "scale": 0.4 },
  "obstacles": [
    { "type": "rect", "x": 100, "y": 500, "w": 220, "h": 60 },
    { "type": "circle", "x": 520, "y": 380, "r": 50 },
    { "type": "polygon", "points": [[0,0],[50,0],[25,40]], "kind": "rock" },
    { "type": "polygon", "points": [...], "kind": "water" }
  ],
  "items": [
    { "type": "atk_up", "x": 600, "y": 700 },
    { "type": "ink_bottle", "x": 80, "y": 650, "value": 300 },
    { "type": "key", "color": "red", "x": 640, "y": 260 },
    { "type": "gate", "color": "red", "rect": { "x": 300, "y": 180, "w": 120, "h": 20 } },
    { "type": "chest", "color": "red", "x": 120, "y": 140 }
  ],
  "goldZones": [ { "points": [[...]] } ],     // chỉ c2_m4
  "enemySquads": [
    { "id": "s1", "spawnDelay": 0, "speed": 55,
      "units": [{ "type": "goblin", "count": 4 }],
      "route": [[700, 600], [400, 450], [360, 120]] }
  ],
  "bonusSquadRoute": [[20, 500], [360, 120]],
  "patrolBaseGold": 2,
  "referenceSolution": [[360, 940], [ ... ], [360, 110]],
  "tutorialHint": "Kéo từ lá cờ tới boss. Mực có hạn!"
}
```

### 10.2 Danh sách map cần dựng

| id | Chương/tầng | Ý đồ thiết kế | Mực gốc gợi ý |
|---|---|---|---|
| `c1_m1` | C1 L1 | Đường gần thẳng, vài tảng đá. Dạy vẽ | 1400 |
| `c1_m2` | C1 L2 | 1 buff dễ trên đường thẳng, 1 buff khó phía sau tường. Lọ mực ở góc giúp đủ mực lấy buff khó | 1300 |
| `c1_m3` | C1 L3 | 1 đạo goblin đi chéo. Chặn đúng giờ thì boss yếu hơn hẳn | 1500 |
| `c1_e1` | C1 L4 | Elite: chìa đỏ bên trái, cổng đỏ chắn lối tắt. 2 đạo địch | 1600 |
| `c1_m5a` | C1 L5 | Rương đỏ, chìa ở xa, đầu lâu nằm giữa đường ngắn nhất | 1500 |
| `c1_m5b` | C1 L5 | Nhiều buff rải rác, không rương, 2 đạo địch | 1700 |
| `c1_boss` | C1 L7 | Boss Vua Goblin, 3 đạo địch, chìa + rương, lọ mực | 1900 |
| `c2_m1` | C2 L1 | 2 đạo có goblin cung, đạo có ranged nên aggro lớn | 1600 |
| `c2_m2` | C2 L2 | Orc đi một mình, chậm. Nên né hay nên chặn | 1600 |
| `c2_m3` | C2 L3 | Shaman hồi máu cho đạo đi kèm | 1700 |
| `c2_m4` | C2 L4 | **Map mực vàng:** sông cắt ngang. Đường vòng giải được bằng mực gốc. Vùng vàng (khoảng 200 px) là cầu tắt tới rương lớn và điểm chặn đạo Orc | 1800 |
| `c2_m5a` / `c2_m5b` | C2 L5 | Hai biến thể: nhiều cổng hai màu, hoặc nhiều đạo địch | 1800 |
| `c2_boss` | C2 L7 | Pháp sư Bóng Tối, 4 đạo địch, chìa đỏ + xanh | 2100 |

Elite và L5 chương 2 nếu cần thêm thì Codex tự dựng theo cùng khung (`c2_e1`).

### 10.3 Kiểm tra giải được (bắt buộc)

- Mỗi map phải có `referenceSolution`: một đường chạy được do người dựng map vẽ sẵn.
- Test `mapSolvable.test.ts` chạy cho **mọi map**:
  1. `referenceSolution` qua được `PathValidator` (không xuyên vật cản, bắt đầu và kết thúc đúng chỗ).
  2. Độ dài ≤ `baseInk` + mực từ các lọ mà đường đó đi qua (không dùng mực vàng).
  3. Mô phỏng trận headless với đội mặc định (`sword`, `archer`, `archer`, cấp 1, không buff run) phải **thắng** cho các map chương 1. Chương 2 thắng với cấp 3.

---

## 11. Màn hình

| Màn | Nội dung chính |
|---|---|
| Home | Nút Chơi (chọn chương đã mở), Đội hình, Nâng cấp, Tuần tra (kèm số Vàng chờ thu), số Vàng |
| Chọn đội | 3 slot, danh sách lính đã mở, synergy đang bật, nút Bắt đầu run |
| Bản đồ run | Cây nút 7 tầng, nút có thể chọn thì sáng. HUD: XP run, Xu, mực vàng, buff run đã có (bấm xem) |
| Trận (vẽ) | Mục 4.1 |
| Trận (hành quân) | Sân, thanh máu boss ở trên, thanh máu tổng mỗi slot ở dưới, nút x1/x2 |
| Kết quả | Thắng/thua, ⭐, mực dư → XP, Xu, Vàng, thông báo tuyến tuần tra mới |
| Chọn buff | 3 thẻ buff, chọn 1 |
| Sự kiện | Ảnh placeholder, mô tả, 2 nút |
| Shop | 3 ô buff, ô mực vàng (nếu có), nút đổi hàng |
| Kết thúc run | Tổng Vàng nhận, map đã qua, nút về Home |
| Nâng cấp | Danh sách loại lính, cấp, chỉ số hiện tại → cấp sau, giá |
| Tuần tra | Danh sách map đã lưu (điểm, vàng/phút), chọn tuyến, mini-map hoạt cảnh, nút Thu |

Hướng dẫn: map chương 1 có `tutorialHint`, hiện dạng bong bóng ở giai đoạn vẽ lần đầu chơi map đó.

---

## 12. Hình ảnh placeholder (khối 3D cơ bản)

| Thứ | Hình |
|---|---|
| Mặt đất | Plane màu cỏ nhạt, có lưới mờ để dễ ước khoảng cách |
| Đường vẽ | Ribbon phẳng sát đất, xanh đen, dày 8 unit, đầu bút là đĩa tròn. Chờ nối: nhấp nháy đỏ |
| Đoạn trong vùng vàng | Ribbon vàng |
| Tuyến địch | Ribbon nét đứt đỏ nhạt sát đất, kèm mũi tên |
| Lính mình | Capsule xanh dương cao khoảng 16 unit. Mỗi loại một màu đậm nhạt khác nhau + đỉnh đầu có khối nhỏ phân biệt (kiếm: hộp, cung: nón, khiên: đĩa dẹt...) |
| Lính địch | Capsule đỏ. Orc to gấp rưỡi |
| Boss | Khối lục giác tím cao, thanh máu dạng HTML overlay bám theo vị trí chiếu |
| Vật cản | Đá: khối xám (box/dodecahedron) cao 20–40 unit. Nước: plane xanh nhạt thấp hơn mặt đất, có sóng nhẹ bằng shader hoặc dịch UV |
| Cổng | Hai cột + thanh ngang màu theo `color`. Mở thì thanh ngang hạ xuống đất |
| Chìa / rương | Chìa: khối nhỏ xoay tại chỗ. Rương: hộp màu theo `color` |
| Buff | Khối bát diện lơ lửng, xoay chậm, màu theo loại. Đầu lâu: khối đỏ sẫm có gai |
| Vùng vàng | Plane vàng mờ phát sáng nhẹ |
| Vòng aggro | Vòng tròn mờ trên mặt đất |
| Sát thương | Số bay lên (HTML overlay hoặc sprite). Chí mạng không có trong demo |

---

## 13. Tham số mặc định (`config.json`)

| Key | Giá trị | Ghi chú |
|---|---|---|
| `sampleStep` | 8 | px |
| `startSnapRadius` | 50 | px |
| `bossSnapRadius` | 70 | px |
| `pickupRadius` | 36 | px, khoảng cách từ đường tới tâm vật phẩm |
| `liftGraceSec` | 1.0 | s |
| `resumeRadius` | 45 | px |
| `undoLength` | 120 | px |
| `armySpeed` | 60 | px/s |
| `slotSpacing` | 34 | px |
| `aggroPadding` | 20 | px |
| `leashRadius` | 160 | px |
| `regroupSec` | 1.5 | s |
| `projectileSpeed` | 500 | px/s |
| `battleTimeoutSec` | 180 | s |
| `bossScale` | 0.4 | Boss nhỏ của map thường so với boss chương |
| `starInkRatio` | 0.2 | |
| `inkToXp` | 0.1 | XP mỗi px mực dư |
| `goldInkToXp` | 0.05 | |
| `battleXp` | `{ "battle": 30, "elite": 50, "boss": 80 }` | |
| `runLevelXp` | `[60, 100, 140, 180, 220, 260, 300]` | XP cần để lên từng cấp |
| `battleCoins` | `{ "battle": 30, "elite": 50, "boss": 0 }` | Xu |
| `levelStatPct` | 8 | % mỗi cấp |
| `upgradeBaseCost` | 40 | Vàng |
| `upgradeCostGrowth` | 1.45 | |
| `buffWeight` / `chestWeight` / `interceptWeight` | 0.15 / 0.3 / 0.2 | Tuần tra |
| `patrolTimeScale` | 10 | 1 phút thật = 10 phút tuần tra |
| `patrolCapMinutes` | 480 | |
| `cameraTiltDeg` | 15 | Độ nghiêng camera so với phương thẳng đứng. 0 = nhìn thẳng xuống |
| `cameraFov` | 40 | độ |
| `worldScale` | 1 | unit 3D trên mỗi px logic |
| `shadows` | true | Tắt cho máy yếu |

---

## 14. Debug (`?debug=1`)

- Hiện vòng aggro, tầm đánh, `pickupRadius`, polyline tuyến địch, số mực dạng số.
- Nút: thắng ngay, thua ngay, +500 Vàng, +100 XP run, +300 mực vàng, tốc độ x4, nhảy tới nút bất kỳ trong run, mở hết chương và lính, xoá save.
- Nút "Vẽ `referenceSolution`" để kiểm tra map nhanh.

---

## 15. Thứ tự làm (milestone)

| # | Nội dung | Xong khi |
|---|---|---|
| M0 | Dựng khung Three.js: sân 3D, camera nhìn từ trên xuống, raycast điểm chạm xuống mặt đất, HTML overlay cho HUD | Chạm đâu thì đĩa đánh dấu hiện đúng chỗ đó trên mặt đất |
| M1 | Vẽ đường: mực, vật cản, snap đầu/cuối, chờ nối, undo/reset, lọ mực, chìa/cổng | Vẽ được `c1_m1`–`c1_e1`, test `PathValidator` qua |
| M2 | Hành quân + combat: đạo 3 slot, aggro hai phía, đạo địch, boss, thắng/thua, x2 | Chơi trọn `c1_m3` từ vẽ tới thắng |
| M3 | Toàn bộ map chương 1 + ⭐ + test giải được | `mapSolvable` qua cho chương 1 |
| M4 | Run: bản đồ nút, XP run từ mực dư, chọn buff, sự kiện, shop, kết thúc run | Chơi hết chương 1 như một run |
| M5 | Meta: chọn đội, synergy, nâng cấp, mở lính, tuần tra idle | Thua run vẫn giữ Vàng, nâng cấp được, tuần tra ra Vàng |
| M6 | Chương 2 + mực vàng `c2_m4` + polish (số bay, rung, âm thanh placeholder nếu kịp) | Chơi trọn 2 chương |

---

## 16. Nghiệm thu

1. Vẽ: không thể vẽ xuyên vật cản, cổng thiếu chìa, hoặc vùng vàng khi không có mực vàng.
2. Nhấc tay giữa chừng: có 1 giây để nối tiếp, quá thì đường xoá, mực hoàn đủ.
3. Lọ mực cộng mực ngay khi vẽ qua. Undo qua lọ thì trừ lại.
4. Buff chỉ có hiệu lực khi quân thực sự đi tới. Quân chết trước đó thì không nhận.
5. Cắt ngang đường địch nhưng lệch giờ thì không giao tranh. Khớp giờ thì cả hai dừng lại đánh.
6. Đạo có cung thủ bắt đầu bắn trước khi melee hai bên chạm nhau.
7. Đạo địch sống sót tới boss thì đứng hộ vệ và đánh quân mình.
8. Mực dư hiện rõ trên màn kết quả và cộng đúng `leftoverInk × inkToXp` vào XP run.
9. **Không có đường nào** (meta, run, sự kiện) cộng mực thường vào trận. Kiểm tra bằng cách nâng max mọi thứ: `baseInk` hiển thị không đổi.
10. Map `c2_m4` thắng được khi không có mực vàng. Có mực vàng thì đi được cầu tắt.
11. Thua run: Vàng đã nhận trong run vẫn còn ở Home.
12. Tuần tra: tắt tab 2 phút, mở lại thì Vàng chờ thu ≈ `2 × patrolTimeScale × vàng/phút`.
13. Test `mapSolvable` qua cho mọi map.
14. Chạy được trên Chrome mobile (màn dọc) và desktop. Không cuộn trang, không zoom khi vẽ (chặn gesture mặc định của trình duyệt).
15. Camera thấy trọn sân ở các tỉ lệ dọc phổ biến (9:16, 9:19.5, 3:4). Điểm vẽ trùng khớp vị trí ngón tay trên mặt đất (sai lệch dưới 4 unit), kể cả khi `cameraTiltDeg` khác 0.
16. Mobile tầm trung giữ khoảng 60 fps trong trận đông nhất (`c2_boss`). Không đạt thì tắt shadow trước.

---

## 17. Ngoài phạm vi demo

- Art và âm thanh thật, animation nhân vật.
- Nợ mực (vay mực trận sau): để sau, vì xung đột với nguyên tắc 1.2.1.
- Tướng có kỹ năng chủ động, gacha, trang bị.
- Backend, tài khoản, IAP, quảng cáo.
- Map sinh ngẫu nhiên.
