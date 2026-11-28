# Quy trình chung (mọi skill dùng)

Môi trường: `herk-edit-kit` (HyperFrames 0.7.x + GSAP 3.14). Mọi lệnh chạy trong thư mục dự án `video-projects/<slug>/`.
Đã kiểm chứng: template trong `skills-v2/` qua `hyperframes lint` (0 lỗi), `snapshot` và `render` (1080×1920, 28s, có audio, ~1m47s trên 1 worker).

## 9 bước — làm đúng thứ tự, không bỏ bước

1. **Brief (≤10 dòng)**: chủ đề, tỉ lệ (mặc định 9:16 1080×1920, 30fps), thời lượng mục tiêu, nguồn số liệu, CTA. Chọn skill theo `skills-v2/README.md`.
2. **Kịch bản**: chia câu ngắn 6–14 từ. Mỗi câu = 1 "beat" hình. Hook trong 3 giây đầu: một con số/câu hỏi gây sốc.
3. **Giọng đọc**: viết `script.json` (xem đầu `_shared/scripts/build_voiceover.py`) rồi chạy `<ROOT>/VieNeu-TTS/.venv/Scripts/python.exe skills-v2/_shared/scripts/build_voiceover.py <thư-mục-dự-án> script.json`. Script sinh từng câu, ghép `assets/vo.wav` và ghi `assets/timing.json` (start/end từng câu). **Thời gian beat = timing.json**, không đoán.
   **Nhịp nghỉ (bắt buộc, tránh đọc dồn):** nghỉ giữa câu cùng trang ≥ 0,7 s; câu cuối của trang (chuyển cảnh) ≥ 1,3 s; sau câu hỏi dẫn dắt ≥ 1,5 s; đầu bài 0,5 s; cuối bài giữ ≥ 1,5 s. Không rút ngắn các khoảng này để vừa thời lượng — bớt câu thay vì bớt nghỉ. Mỗi trang 1 ý, câu ≤ 14 từ. Cắt sang trang mới ở (end câu cuối + 0,5 s) để hình mới vào xong trước khi câu kế bắt đầu (≥ 0,6 s sau khi trang hiện).
4. **Dựng dự án**: Windows `skills-v2\_shared\scripts\new-project.bat <skill> <slug> [--theme=<màu>]`, macOS/Linux `bash skills-v2/_shared/scripts/new-project.sh <skill> <slug> [--theme=<màu>]` (copy template, gsap, font, sfx).
5. **Sửa template**: chỉ sửa các khối đánh dấu `DỮ LIỆU`, `CAPTIONS`, nội dung text trong `.beat`, và dòng `tl.` tương ứng. Giữ nguyên class, màu, cỡ chữ, easing trong SKILL.md.
5b. **Hình thật (bắt buộc, không để ô giữ chỗ)**: sửa `assets.json` của dự án (mỗi ô ảnh/bản đồ một mục: `query` tiếng Anh cụ thể có năm/địa danh, `caption`, hoặc `"file"` nếu người dùng có ảnh; bản đồ: mã ISO-3 `highlight`, `pins`, `route`) rồi chạy `python skills-v2/_shared/scripts/fetch_assets.py <thư-mục-dự-án> <thư-mục-dự-án>/assets.json`. Script tải ảnh tự do (Wikimedia Commons, NASA), vẽ bản đồ từ ranh giới thật (Natural Earth), gắn thẳng vào `index.html` qua marker `<!--asset:ID-->`, và xuất `ASSETS.md` (danh sách từng ô: nguồn, giấy phép, cách thay) sang `<ROOT>/output/`. Ô nào báo PLACEHOLDER: đổi query cụ thể hơn rồi chạy lại; vẫn không có thì để trong `ASSETS.md` cho người dùng thay và **nói rõ khi bàn giao**. Ô ảnh mới trong template: thêm `<!--asset:ID--><!--/asset:ID-->` trong `.im` hoặc `.mapbg`.
6. **Âm thanh**: chạy `python skills-v2/_shared/scripts/mix_audio.py <thư-mục-dự-án>` → `assets/mix.wav`: giọng + nhạc **theo 4 hồi** (hook căng → build có nhịp → climax → resolve), nhạc tự hạ ~15 dB dưới giọng khi có lời và nổi lên trong khoảng nghỉ, chuẩn −14 LUFS; ghi công nhạc vào `assets/music_credits.txt`. Dùng **một** thẻ `<audio id="mix" src="assets/mix.wav" data-start="0" data-duration="<tổng>" data-track-index="9" data-volume="1">` (không thêm thẻ vo/bg_music riêng). Đặt mốc hồi theo nội dung bằng `--acts hook:0,build:s4,climax:s18,resolve:s27` (s = số câu). Không dùng lại một vòng nhạc 30 s cho cả video. SFX dùng `_shared/audio/` (bảng ở dưới).
7. **Kiểm tra**: `npx hyperframes lint` → 0 error. Rồi `npx hyperframes snapshot --at <giây giữa mỗi beat>` và **mở contact-sheet.jpg xem từng khung**. Sửa tới khi qua hết checklist bên dưới.
7b. **(Tùy chọn, video ngang) Clip video AI**: nếu người dùng muốn thêm cảnh phim do video-AI tạo, làm theo `_shared/BROLL-VIDEO.md` (`broll.py plan` → viết file prompt → `broll.py check`) trước khi render.
7c. **Chuyển động (chống bỏ xem)**: không khung nào đứng yên > 3 s. Ảnh/bản đồ luôn trôi chậm (`kb()` trong template, scale 1→1,09 suốt trang); số lớn đếm lên (`countUp()`); mỗi câu đọc làm hiện thêm **một** thứ trên trang (nhãn, ghim, gạch chân, ô checklist) đúng `start` của câu trong `timing.json`; trang dài > 7 s phải có ≥ 2 nhịp hiện. Hook 0–3 s: ảnh thật mạnh nhất + con số/câu hỏi. Không trang nào chỉ có chữ nhỏ trên nền trống — tối thiểu một tiêu đề ≥ 96 px hoặc một ảnh/bản đồ.
8. **Render**: từ `<ROOT>/herk-edit-kit` chạy `npx hyperframes render video-projects/<slug> --output ../output/<slug>.mp4` (quality mặc định `standard`; thử nhanh dùng `-q draft`). **Mọi video, ảnh QA, `VERIFY.md` nằm trong `<ROOT>/output/`** (cùng cấp repo `vidskill`), không để trong `herk-edit-kit`. Ghi kết quả vào `output/<slug>-VERIFY.md` (lint, các khung đã xem, độ lớn file, LUFS).
9. **Kiểm tra thành phẩm (bắt buộc trước khi bàn giao)**: `python skills-v2/_shared/scripts/qa_video.py <ROOT>/output/<slug>.mp4 --project <thư-mục-dự-án>` phải ra **ĐẠT** (−14 LUFS, nghỉ đủ, không đoạn đứng yên > 3,5 s, không ô giữ chỗ). Chưa đạt thì sửa theo gợi ý rồi render lại. Bàn giao kèm `ASSETS.md`, `credits.txt`, `music_credits.txt`.

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
