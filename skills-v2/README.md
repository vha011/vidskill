# skills-v2 — bộ skill làm video cho Gemini Flash

Bản cũ (`SKILL.md`, `README_CAI_DAT_MAY_MOI.md`, `setup_all.bat`, `README.zip`) giữ nguyên ở thư mục gốc. Bộ mới nằm hoàn toàn trong thư mục này.

## Chọn skill

| Loại video | Skill | Trạng thái |
|---|---|---|
| Giải thích địa chính trị / quốc gia trên bản đồ | `explained-geo-map/` | Đầy đủ: thông số đo từ `singapore.mp4` + template chạy được |
| Phân tích tài chính / doanh nghiệp / số liệu | `explained-data-finance/` | Đầy đủ: thông số đo từ `pnj-tai-chinh.mp4` + template chạy được |
| Motion graphics ngắn | `motion-graphics/` | Khung hướng dẫn, chưa có demo |
| Phim ngắn / kể chuyện | `cinematic-movie/` | Khung hướng dẫn, chưa có demo |

Gemini đọc theo thứ tự: `_shared/PIPELINE.md` → `<skill>/SKILL.md` → mở `<skill>/template/index.html` và `<skill>/reference/*.png`. Làm theo template, không tự thiết kế lại.

## Cấu trúc

```
skills-v2/
  _shared/PIPELINE.md        8 bước, luật HyperFrames, bảng SFX, checklist QA, lỗi hay gặp
  _shared/scripts/new-project.sh   tạo dự án từ template (copy font, gsap, sfx)
  _shared/fonts, audio, gsap.min.js
  explained-geo-map/   SKILL.md, template/index.html, reference/
  explained-data-finance/ SKILL.md, template/index.html, reference/
  motion-graphics/SKILL.md
  cinematic-movie/SKILL.md
```

## Đã kiểm chứng
- Cả hai template: `hyperframes lint` 0 lỗi, `snapshot` đúng bố cục (ảnh trong `reference/template-snapshot.jpg`).
- `explained-data-finance` render thật: 1080×1920, 28 s, có audio, ~1m47s (HyperFrames 0.7.109).

## Về bộ preset cũ trong README.zip
- `fdi-explainer-preset/` có `index.html` + `DESIGN.md` đầy đủ, lint 0 lỗi → giữ làm thư viện 6 component motion.
- 4 thư mục `pnj-equity-preset`, `singapore-geopolitics-preset`, `vietjet-investigative-preset`, `gym-break-even-preset` **chỉ có `meta.json` + assets** (không có `index.html` hay `DESIGN.md`) nên Gemini không có gì để làm theo. Bảng màu trong `meta.json` còn lệch khỏi video mẫu thật (ví dụ PNJ khai `#F59E0B`/`#06B6D4`, video thật dùng lime `#ADF400`, đỏ `#E70A23`, vàng `#FEC73C`). Hai skill mới thay thế hai preset PNJ và Singapore; vietjet và gym chưa có video mẫu nên chưa làm lại.
