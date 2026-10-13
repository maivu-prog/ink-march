# Ink March

Demo game web màn dọc: chọn đội + brush → vẽ đường → tự chiến đấu → chọn bùa → sang màn tiếp theo.

## Chạy

```sh
npm install
npm run dev
```

Mở địa chỉ mà Vite hiển thị. Thêm `?debug=1` để có nút vẽ lời giải, thắng/thua, thêm Vàng/Ngọc, mở khoá hết, nhảy màn, tốc độ x4.

```sh
npm test
npm run build
```

## Luồng chơi

- **10 chương**, mỗi chương 3–5 màn chơi liên tiếp (kiểu Archero 2). Sân **nhỏ ở chương đầu rồi to dần** (70% → 100%), camera tự zoom theo sân.
- Mỗi màn có **3 trại địch**: phá được bao nhiêu trại thì bấy nhiêu sao. Thắng màn là hạ boss.
- Một số màn là **hai mặt trận**: hai cờ START, hai đội, dùng chung một bình mực. Có màn hai boss, mỗi đội phải nhắm một boss.
- Trước mỗi trận chọn **brush**. Shop/sự kiện là chặng nghỉ cố định giữa chương.

## Tutorial

- **Lần đầu chơi:** dẫn từng bước ở màn đầu. START → DRAW → vẽ theo **vệt sáng** có bàn tay kéo mẫu → MARCH → giải thích vòng ⚔/➶ → sao và Ngọc → chọn bùa. Có nút Skip.
- **Gợi ý theo ngữ cảnh**, mỗi loại hiện một lần: đạo địch và cướp bùa, địa hình, hai mặt trận, chìa/cổng, cầu vàng, đủ Ngọc để quay brush.
- Trạng thái lưu trong save (`tutorial`). Xoá save là xem lại từ đầu.

## Aggro

Mỗi lính dùng vùng aggro theo tầm đánh của mình: `tầm × aggroScale + aggroPadding` (0,5 và 12). Trên sân: **đĩa đặc ⚔** = vùng cận chiến, **vòng nét đứt ➶** = vùng tầm xa. Xanh là ta, đỏ là địch.

## Brush, lính và tiền

- **Brush** (gacha chính, trả bằng **Ngọc**): không đổi lượng mực, chỉ đổi **tốc độ đốt mực** (chung hoặc theo địa hình), bán kính nhặt bùa, tốc độ hành quân, hồi máu. Ra trùng thì lên sao (tối đa 5), hiệu ứng mạnh hơn. Model 3D kiểu hoạt hình, hiện ở đầu nét khi vẽ.
- **Ngọc** kiếm từ sao mới (+10/sao), lần đầu qua màn (+20), qua chương (+100).
- **Lính**: có sẵn 6 con (2 Kiếm sĩ, 2 Cung thủ, 2 Khiên). Gacha lính (phụ, trả bằng Vàng) thêm lính, tối đa 2 con mỗi loại; ra thừa thành thẻ để lên cấp ở Training.

## Địa hình

| Loại | Mực đốt | Tốc độ hành quân |
|---|---|---|
| Cát | ×1,6 | ×0,65 |
| Đầm lầy | ×2,2 | ×0,5 |
| Đường mòn | ×0,7 | ×1,3 |

Đoạn nét vẽ qua địa hình xấu đổi màu cam. Nhãn địa hình trên sân hiện hệ số mực đã tính theo brush đang cầm.

## Luật chiến đấu đáng chú ý

- Đạo địch tới được boss làm boss **ENRAGED** (+25% ATK, +20% HP).
- Boss có chiêu tầm xa nhắm hàng sau.
- Đạo địch đang hành quân đi ngang bùa thì **cướp** cho cả đạo. Đầu lâu bẫy cả địch. Bùa trên tuyến địch có dấu ⚠.

## Thiết kế màn

Màn sinh từ định nghĩa bố cục (vật cản, địa hình, trại, bùa, đạo địch). `tools/solve-map.ts` tự tính phần còn lại:

1. Scale boss cao nhất mà vẫn có tuyến phá đủ 3 trại và thắng với ≥20% quân, nhân hệ số dễ theo chương.
2. Mực gốc: tuyến thắng luôn vẽ được bằng Apprentice Quill. Tuyến 3 sao cần brush theo bậc: chương 1–3 Quill, 4–6 brush Rare, 7–10 brush Epic.
3. Đường mẫu (`referenceSolution`) là tuyến 3 sao.

```sh
npx tsx tools/solve-map.ts <mapId> --write   # tính lại một màn
npx tsx tools/check-maps.ts                  # tóm tắt thiết kế mọi màn
```

`tests/mapSolvable.test.ts` kiểm tra mọi màn: 3 trại, đường mẫu vẽ được với brush thiết kế và phá đủ trại mà thắng.

## Cấu trúc

- `src/systems.ts`: luật game headless (mực, trận, gacha, save).
- `src/render.ts`: Three.js. `src/brush3d.ts`: model brush.
- `src/main.ts`: UI và luồng màn hình. `src/game-ui.css`: bộ UI kiểu game.
- `src/data/`: map, lính, địch, boss, brush, địa hình, gacha.

## Còn lại

- Chưa đo FPS trên điện thoại thật.
- Thoát trình duyệt giữa trận rồi vào lại thì được vẽ lại màn đó.
- Cân bằng dựa trên mô phỏng với đội khởi đầu; cần playtest.
