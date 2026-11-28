# skills-v2 — bộ skill làm video cho Gemini Flash

Bản cũ (`SKILL.md`, `setup_all.bat`, `README.zip`) giữ nguyên ở thư mục gốc. Bộ mới nằm hoàn toàn trong thư mục này.

## Chọn skill

| Loại video | Skill | Video mẫu | Trạng thái |
|---|---|---|---|
| Địa chính trị / quốc gia trên bản đồ | `explained-geo-map/` | singapore.mp4 | Đầy đủ |
| Phân tích số liệu tài chính doanh nghiệp | `explained-data-finance/` | pnj-tai-chinh.mp4 | Đầy đủ |
| Điều tra vụ việc có hợp đồng/tiền/tòa án | `explained-investigative/` | vietjet airline.mp4 | Đầy đủ |
| Lịch sử kinh tế / chính sách theo năm | `explained-fdi-timeline/` | fdi vn.mp4 | Đầy đủ |
| Điều tra kinh doanh một chuỗi/thị trường | `explained-gym-business/` | gym center.mp4 | Đầy đủ (thiếu tường thumbnail) |
| Lịch sử / chiến dịch, ngang 16:9, nền TỐI, hồ sơ tư liệu (5–6 trang) | `explained-history-dossier/` | lichsu-vietnam.mp4 | Đầy đủ 5 trang (thiếu đợt II–III) |
| Lịch sử dài, ngang 16:9, nền GIẤY SÁNG, nhịp 4–6 s/trang, bản đồ vệ tinh + polaroid | `explained-history-chronicle/` | trieu-tien-chronicle.mp4 (30:39) | 7 trang mẫu; thiếu đồng hồ, biểu đồ nhỏ, bản đồ thế giới |
| Motion graphics ngắn | `motion-graphics/` | chưa có | Khung hướng dẫn |
| Phim ngắn / kể chuyện (khung chung) | `cinematic-movie/` | chưa có | Khung hướng dẫn |
| Hoạt hình 3D kể chuyện dài, nhân vật do AI tạo | `animated-story-ai/` | mario-animation-ai.mp4 (68 s mở đầu) | Quy trình + sổ nhân vật + kịch bản/shot; ghép bằng HyperFrames đã kiểm |

Gemini đọc theo thứ tự: `_shared/PIPELINE.md` → `<skill>/SKILL.md` → mở `<skill>/template/index.html` và `<skill>/reference/*.jpg`. Làm theo template, không tự thiết kế lại.

## Cấu trúc

```
skills-v2/
  _shared/PIPELINE.md         8 bước, luật HyperFrames, bảng SFX, checklist QA, lỗi hay gặp
  _shared/scripts/new-project.sh   tạo dự án từ template
  _shared/fonts, audio, gsap.min.js
  _shared/gemini-preset-review/    đánh giá 4 preset Gemini dựng (REVIEW.md + ảnh snapshot)
  <skill>/SKILL.md, template/index.html, reference/
```

## Đã kiểm chứng
- 5 template: `hyperframes lint` 0 lỗi (1 cảnh báo `timeline_track_too_dense`, chấp nhận được), `snapshot` đã xem từng khung (`reference/template-snapshot.jpg`).
- Render thật: `explained-data-finance` (28 s) và `explained-fdi-timeline` (30 s), 1080×1920, có audio.
- 4 preset Gemini trong README.zip (bản cập nhật): lint sạch nhưng lệch phong cách so với video mẫu → xem `_shared/gemini-preset-review/REVIEW.md`.
