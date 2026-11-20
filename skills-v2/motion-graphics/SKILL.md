---
name: motion-graphics
description: Video motion graphics ngắn (10–30 s) không lời đọc hoặc lời đọc tối thiểu — brand reel, giới thiệu sản phẩm, hiệu ứng chữ/số. Dùng khi mục tiêu là chuyển động đẹp theo nhạc, không phải giải thích dài.
---

# motion-graphics  (CHƯA có video tham chiếu riêng)

Trạng thái: **khung hướng dẫn**, chưa trích từ video demo nào (hai video demo đều là video giải thích). Phần thông số bên dưới lấy từ hai skill đã đo được và từ `fdi-explainer-preset` có sẵn trong `README.zip`. Khi anh có video motion mẫu, gửi lên để em đo lại và thay các giá trị mang dấu (*).

## Dùng gì có sẵn
- **Dựng nhanh một reel theo nhạc**: dùng skill `motion-showreel` của herk-edit-kit (10–30 s, một motif biến hình xuyên suốt, chương có nhãn, HUD cố định, cắt theo beat nhạc, logo lockup cuối). Lệnh dò nhịp: `npx hyperframes beats <audio>` → ghi `beats/<audio>.json`.
- **Thành phần motion tái dùng**: 6 component trong `fdi-explainer-preset/DESIGN.md` (TimelineRunner, SatelliteMapGlow, CrateStackingChart, CoinRatioComparison, PolicyDecisionTree, CutoutPaperStamp) — `README.zip`.
- **Thẻ phong cách có sẵn**: `style-library/registry.json` (406 thẻ); chọn qua skill `style-library`.
- **Nền động không cần footage**: `dark-graph-paper-template` (README.zip).

## Quy tắc nhịp (*chưa kiểm chứng bằng demo riêng)
- Dùng nền, màu, font của `explained-data-finance` (nền `#080F0D`, lime `#ADF400`, Inter 800) làm mặc định để đồng bộ thương hiệu.
- Một chuyển động chính mỗi 1–2 s; cắt tại beat nhạc (±1 khung ở 30 fps).
- Vào cảnh `power3.out` 0,35–0,6 s; chữ lớn `back.out(2)`; không dùng easing `linear` ngoài nền trôi.
- Mỗi cảnh một ý, chữ ≤7 từ, cỡ ≥96 px cho tiêu đề, ≥40 px cho nhãn.
- SFX: whoosh khi chuyển cảnh, hit khi chốt logo (xem `_shared/PIPELINE.md`).

## Quy trình
`_shared/PIPELINE.md` (bỏ bước 3 nếu không có lời), tạo dự án bằng `new-project.sh explained-data-finance <slug>` làm khung rồi thay beat theo storyboard, hoặc `npm run new-video -- <slug>` của herk-edit-kit rồi load skill `motion-showreel`.
