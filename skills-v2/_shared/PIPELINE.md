# Quy trình chung (mọi skill dùng)

Môi trường: `herk-edit-kit` (HyperFrames 0.7.x + GSAP 3.14). Mọi lệnh chạy trong thư mục dự án `video-projects/<slug>/`.
Đã kiểm chứng: template trong `skills-v2/` qua `hyperframes lint` (0 lỗi), `snapshot` và `render` (1080×1920, 28s, có audio, ~1m47s trên 1 worker).

## 8 bước — làm đúng thứ tự, không bỏ bước

1. **Brief (≤10 dòng)**: chủ đề, tỉ lệ (mặc định 9:16 1080×1920, 30fps), thời lượng mục tiêu, nguồn số liệu, CTA. Chọn skill theo `skills-v2/README.md`.
2. **Kịch bản**: chia câu ngắn 6–14 từ. Mỗi câu = 1 "beat" hình. Hook trong 3 giây đầu: một con số/câu hỏi gây sốc.
3. **Giọng đọc**: tạo mỗi câu 1 file WAV bằng VieNeu-TTS; đo `ffprobe -v error -show_entries format=duration -of csv=p=0 cau_01.wav`. Ghép lại bằng ffmpeg `concat` thành `assets/vo.wav`, giữ khoảng nghỉ 0,15 s giữa câu. **Thời gian beat = thời lượng audio thật**, không đoán.
4. **Dựng dự án**: `bash skills-v2/_shared/scripts/new-project.sh <skill> <slug>` (copy template, gsap, font, sfx).
5. **Sửa template**: chỉ sửa các khối đánh dấu `DỮ LIỆU`, `CAPTIONS`, nội dung text trong `.beat`, và dòng `tl.` tương ứng. Giữ nguyên class, màu, cỡ chữ, easing trong SKILL.md.
6. **Âm thanh**: thêm `<audio id="vo" src="assets/vo.wav" data-start="0" data-duration="<tổng giây>" data-track-index="9" data-volume="1">`. SFX dùng `_shared/audio/` (bảng ở dưới). Nhạc nền nếu cần: `ugc_bg_music_30s.wav` trong `README.zip` của repo, volume 0.12.
7. **Kiểm tra**: `npx hyperframes lint` → 0 error. Rồi `npx hyperframes snapshot --at <giây giữa mỗi beat>` và **mở contact-sheet.jpg xem từng khung**. Sửa tới khi qua hết checklist bên dưới.
8. **Render**: `npx hyperframes render --output renders/<slug>.mp4` (quality mặc định `standard`; thử nhanh dùng `-q draft`). Ghi kết quả vào `VERIFY.md` (lint, các khung đã xem, độ lớn file, LUFS).

## Quy tắc HyperFrames bắt buộc (lint sẽ bắt)

- Root: `data-composition-id`, `data-start="0"`, `data-duration`, `data-width="1080"`, `data-height="1920"`.
- Mỗi clip có `id` duy nhất, `data-start`, `data-duration`, `data-track-index`. Cùng track không được chồng thời gian.
- Timeline GSAP: `gsap.timeline({paused:true})`, dựng đồng bộ, đăng ký `window.__timelines['<composition-id>']`. Không `repeat:-1`, không `Math.random`, không `setTimeout`.
- Font phải có `@font-face` với **đúng tên family** ("Be Vietnam Pro", "Inter"); nếu không lint báo `font_family_without_font_face`.
- Cảnh báo `timeline_track_too_dense` (>5 clip cùng track) chấp nhận được trong 1 file; nếu >10 beat thì tách file con trong `compositions/` (`data-composition-src`).
- Video chèn vào phải `muted playsinline`; tiếng đi qua `<audio>` riêng.

## Bảng SFX (đã có trong `_shared/audio/`)

| Sự kiện trên hình | File | Volume | Ghi chú |
|---|---|---|---|
| Tiêu đề / thẻ trượt vào | `sfx_whoosh.wav` (0,8s) | 0.5 | đặt tại thời điểm bắt đầu chuyển động |
| Con số / giá trị bật lên | `sfx_ping.wav` (0,6s) | 0.5 | |
| Con dấu, đập xuống | `sfx_hit.wav` (1,5s) | 0.7 | căn đỉnh tiếng đập với khung dấu chạm |
| Chip / nút bật | `sfx_click.wav` (0,2s) | 0.4 | |

Tối đa 1 SFX / 2 giây; không đặt SFX chồng lên giọng đọc ở những từ khóa.

## Checklist QA (xem ảnh snapshot, không chỉ dựa vào lint)

- [ ] Hook xuất hiện trong ≤3 s; có chữ hoặc số trên màn hình ở khung 0–1 s.
- [ ] Mọi chữ nằm trong vùng an toàn: cách mép trái/phải ≥ 60 px, cách mép trên ≥ 150 px, mép dưới ≥ 250 px (UI TikTok/Reels che).
- [ ] Không chữ nào bị cắt, tràn khung, hoặc đè lên phụ đề (phụ đề ở y≈1180–1420 cho skill geo-map).
- [ ] Chữ tiếng Việt đủ dấu (ế, ợ, ỷ…), không rơi về font mặc định.
- [ ] Cỡ chữ tối thiểu: nhãn 34 px, số trục 36 px, phụ đề 56 px (khung 1080 rộng).
- [ ] Mỗi ≤3 s có ít nhất 1 thay đổi trên hình (nhãn mới, camera, chart, cắt cảnh).
- [ ] Số liệu trên chart khớp nguồn đã ghi trong phụ đề nhỏ `(đơn vị; nguồn: …)`.
- [ ] Beat cuối có CTA/câu hỏi chốt; không dừng đột ngột (còn ≥0,5 s hình tĩnh).
- [ ] Âm lượng tổng ≈ −14 LUFS: `ffmpeg -i out.mp4 -af ebur128 -f null - 2>&1 | grep "I:"` (cả 2 video tham chiếu đều đo −14,1 LUFS).
- [ ] Render xong: `ffprobe` đúng 1080×1920, 30 fps, có audio, thời lượng = audio ±0,1 s.

## Lỗi hay gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Chữ không có dấu đúng / font lạ | thiếu `@font-face` hoặc sai tên family | copy `_shared/fonts` vào `assets/fonts/`, dùng đúng tên family |
| Phần tử đứng yên, không animate | quên đăng ký `window.__timelines['root']` | đúng ID composition |
| Chart vẽ ra ngoài khung | tọa độ `T,B,L,R` / hệ số `K` sai | chỉnh trong khối IIFE dựng SVG; xem lại snapshot |
| Render chậm | 1 worker | dùng `-q draft` khi thử, `standard` khi chốt |
