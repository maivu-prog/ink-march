# Ink March — Prompt gen asset (GPT Astra 6)

## ELI5

Game nhìn sân từ trên xuống, nghiêng khoảng 40°. Lính rất nhỏ trên màn hình điện thoại, nên asset phải **đọc được ở cỡ ngón tay**: nhìn một cái là biết ai phe mình, ai phe địch, ai bắn xa, ai đánh gần. Mọi prompt dưới đây dùng chung một "luật nhìn" (mục 1), sau đó là prompt riêng cho từng asset (mục 3).

Copy nguyên khối **STYLE BLOCK** vào đầu mọi prompt để các asset cùng một phong cách.

---

## 1. Luật nhìn (bắt buộc cho mọi asset)

| Luật | Cơ bản | Edge case |
|---|---|---|
| Góc nhìn | Dựng để xem từ trên xuống, nghiêng ~40° | Đầu, vai, vũ khí phải thấy rõ từ trên. Chân gần như không thấy nên không cần chi tiết |
| Tỉ lệ | Chibi: đầu ~40% chiều cao, vũ khí to quá khổ | Boss to gấp ~2,5 lính thường |
| Phe | **Ta = xanh dương + trắng + vàng kim**, mũ tròn, khiên tròn | **Địch = đỏ + cam + đen**, tai nhọn, gai, răng nanh |
| Vai trò | Mỗi vai một hình dáng nhìn từ trên: khiên to (tank), kiếm (cận chiến), giáo dài (cận chiến tầm trung), cung (bắn xa), gậy phép có ngọc sáng (pháp sư), vương miện lá + bình thuốc (hồi máu) | Không dựa vào màu để phân biệt vai trò. Màu chỉ để phân biệt phe |
| Độ chi tiết | Ít chi tiết nhỏ, mảng màu lớn, viền tối dày | Tránh hoa văn mảnh, chữ, logo |
| Nền | Asset không có nền, không bóng đổ nướng sẵn | Game tự đổ bóng |

### STYLE BLOCK (dán vào đầu mọi prompt)

```
Stylized low-poly toy miniature for a mobile strategy game, viewed from a high top-down camera at about 40 degrees.
Chibi proportions: big head (40% of height), oversized weapon, short stubby legs.
Flat cel-shaded colors with a thick dark outline, large readable color blocks, no tiny details, no text, no logos.
Soft studio lighting, isolated on a plain transparent/neutral background, no ground shadow baked in.
Silhouette must read clearly at 48 pixels tall.
```

---

## 2. Thông số kỹ thuật để đưa vào game

| Mục | Yêu cầu |
|---|---|
| Định dạng | **GLB** (glTF binary). Nếu tool chỉ ra ảnh: PNG nền trong suốt, 512×512, nhìn chéo từ trên |
| Hướng | Nhân vật nhìn về **+Z**, chân đặt ở gốc toạ độ (y = 0) |
| Kích thước | Lính cao ~1 đơn vị, boss ~2,5, tháp trại ~3 |
| Poly | Lính ≤ 3k tam giác, boss ≤ 8k, prop ≤ 1k |
| Texture | 1 texture 512×512 hoặc vertex color. Không dùng normal map |
| Animation | 4 clip tên đúng: **Idle, Walk, Attack, Death** (vòng lặp trừ Death). Nếu tool không làm animation được thì xuất mesh có tách bộ phận đầu/thân/tay/vũ khí, mình rig bằng code |
| Tên file | Đúng tên trong cột "File" ở mục 3, bỏ vào `public/assets/models/` |

---

## 3. Prompt từng asset

### 3.1 Lính phe ta (xanh)

| File | Prompt (thêm sau STYLE BLOCK) |
|---|---|
| `shield.glb` | `Friendly knight shieldbearer. Blue and white armor with gold trim, round helmet, a huge round blue shield with a gold star covering half the body, short mace. Sturdy and wide stance.` |
| `sword.glb` | `Friendly swordsman. Blue tunic over light silver armor, round helmet with a small blue plume, oversized straight sword held high, small round buckler.` |
| `spear.glb` | `Friendly spearman. Blue and white padded armor, conical helmet, a very long spear with a blue pennant, held diagonally so the spear reads clearly from above.` |
| `archer.glb` | `Friendly archer. Teal-blue hooded cloak, light leather armor, a big curved longbow taller than the body, quiver of white-feathered arrows on the back.` |
| `mage.glb` | `Friendly battle mage. Deep blue robe with gold stars, tall pointed hat, wooden staff topped with a glowing cyan crystal orb.` |
| `healer.glb` | `Friendly field healer. White and light-blue robe, green leaf circlet, a satchel with a red cross, holding a glowing green potion flask.` |

### 3.2 Lính địch (đỏ/cam)

| File | Prompt |
|---|---|
| `goblin.glb` | `Enemy goblin raider. Green skin, long pointy ears, red and black scrap armor with spikes, jagged cleaver, angry grin with fangs.` |
| `goblin_archer.glb` | `Enemy goblin archer. Green skin, pointy ears, red bandana, black leather with orange straps, crude bone bow, quiver of red arrows.` |
| `orc.glb` | `Enemy orc brute. Big dark-green orc, 1.5x the size of a goblin, red war paint, spiked black shoulder pads, huge two-handed spiked club, tusks.` |
| `shaman.glb` | `Enemy goblin shaman. Green skin, skull mask on the forehead, ragged red cloak with feathers, crooked staff with a glowing orange flame.` |

### 3.3 Boss

| File | Prompt |
|---|---|
| `goblin_king.glb` | `Enemy boss: Goblin King. Large and fat goblin, 2.5x the height of a soldier, golden spiked crown, red royal cape with black fur, huge spiked shield and war axe, menacing pose.` (dùng chung cho Goblin Chief, game tự thu nhỏ) |
| `shadow_mage.glb` | `Enemy boss: Shadow Mage. Tall hooded sorcerer, 2.5x soldier height, black and deep purple robes with glowing violet runes, floating dark orbs around the hands, face hidden in shadow with two glowing eyes.` |

### 3.4 Trại địch và đạo cụ

| File | Prompt |
|---|---|
| `tower.glb` | `Enemy watchtower camp. Short round stone tower with a red pointed roof, a red goblin war banner on top, wooden spikes around the base. 3x soldier height. Reads as an enemy target from above.` |
| `rock.glb` | `Large grey boulder, faceted low-poly, flat on the bottom, mossy top.` |
| `tree.glb` | `Stylized pine tree, three stacked cone layers, dark green, chunky trunk.` |
| `flag_start.glb` | `Tall blue rally flag on a wooden pole with a gold tip, banner with a white brush-stroke emblem.` |
| `flag_clash.glb` | `Small blue battle flag stuck in the ground, crossed swords emblem, slightly waving.` |

### 3.5 Brush (gacha chính)

Hướng nghệ thuật theo ảnh mẫu Mai gửi: cọ hoạt hình, viền đen dày, cán bóng, có vệt sơn.

```
[STYLE BLOCK]
Cartoon paintbrush as a collectible game item, thick black outline, glossy handle with a highlight stroke, metal ferrule with two bands,
bristles shaped like a teardrop flame, a few paint splashes floating around it. Single object, centered, diagonal pose.
```

Thêm phần riêng cho từng brush (độ hiếm càng cao càng nhiều vệt sơn và có phát sáng):

| File | Độ hiếm | Phần thêm |
|---|---|---|
| `brush_quill.glb` | Common | `simple white feather quill with a black metal nib, no splashes` |
| `brush_reed.glb` | Common | `green bamboo reed handle, cream bristles dipped in sand-yellow paint` |
| `brush_charcoal.glb` | Common | `stubby black charcoal stick wrapped in grey cloth` |
| `brush_feather.glb` | Common | `teal feather quill, light blue ink drop on the tip` |
| `brush_marsh.glb` | Rare | `mossy dark-green handle, brown bristles dripping swamp-green paint, small lily pad charm` |
| `brush_broad.glb` | Rare | `wide flat house-painter brush, coral handle, white bristles dipped in red` |
| `brush_swift.glb` | Rare | `sleek blue fountain pen with silver clip, motion streaks` |
| `brush_atlas.glb` | Rare | `brown leather-wrapped cartographer's pen with a gold compass on the cap` |
| `brush_golden.glb` | Epic | `golden quill with a warm glow, gold paint splashes` |
| `brush_willow.glb` | Epic | `cream willow-wood handle with leaves, mint-green glowing paint, healing sparkles` |
| `brush_trail.glb` | Epic | `dark slate handle, bright orange flame-shaped bristles, orange and blue paint splashes` (gần ảnh mẫu 1 nhất) |
| `brush_phoenix.glb` | Legendary | `phoenix feather brush, red-orange fiery bristles, golden handle, flame and ember splashes, strong glow` |

### 3.6 Icon bùa trên sân (2D, PNG 256×256 nền trong suốt)

```
Round game pickup icon, glossy coin-like disc with a thick dark outline, bold white symbol in the center, flat cartoon style, no text.
```

| File | Màu đĩa | Biểu tượng |
|---|---|---|
| `icon_atk.png` | cam | hai thanh kiếm bắt chéo |
| `icon_hp.png` | xanh ngọc | trái tim |
| `icon_shield.png` | vàng | khiên |
| `icon_range.png` | tím nhạt | ống nhòm / tâm ngắm |
| `icon_haste.png` | xanh lá nhạt | đôi giày có cánh |
| `icon_reinforce.png` | xanh dương | lá cờ có dấu + |
| `icon_ink.png` | xanh cyan | lọ mực |
| `icon_skull.png` | đỏ sẫm | đầu lâu |

### 3.7 Địa hình (texture lặp, PNG 512×512 tileable, nhìn thẳng từ trên)

| File | Prompt |
|---|---|
| `tex_grass.png` | `Seamless top-down stylized grass texture, soft painted look, gentle light-green variation, no flowers.` |
| `tex_sand.png` | `Seamless top-down stylized desert sand texture, warm yellow, soft ripples and a few pebbles.` |
| `tex_swamp.png` | `Seamless top-down stylized swamp texture, murky green water with mud patches and reeds.` |
| `tex_road.png` | `Seamless top-down stylized dirt road texture, light brown packed earth with cart tracks.` |
| `tex_water.png` | `Seamless top-down stylized river water texture, clear blue with soft white foam streaks.` |

---

## 4. Thứ tự gen đề xuất

1. **2 lính mẫu** (`sword`, `goblin`) → mình đưa vào game kiểm tra độ đọc trên điện thoại.
2. Chốt phong cách rồi gen phần còn lại của lính, boss, tháp.
3. Brush và icon bùa.
4. Địa hình.

## 5. Nghiệm thu

1. Trên điện thoại, nhìn sân 1 giây phân biệt được ta/địch và lính bắn xa/đánh gần.
2. Lính đứng cạnh tháp trại vẫn thấy tháp to hơn rõ ràng.
3. Brush hiện ở đầu nét vẽ không che mất đường vẽ (đầu cọ là điểm chạm).
4. Mỗi model có đủ 4 clip, hoặc tách bộ phận để rig bằng code.
