# explained-vox-cards — video giải thích dựng từ thư viện card của herk-edit-kit

Ngang 16:9. Phong cách cắt dán tài liệu kiểu Vox: giấy báo, ảnh đen trắng thật, chữ Fraunces đậm nhạt tương phản, khối nhấn xanh, chuyển động giật kiểu stop-motion. **Không tự vẽ layout**: mỗi cảnh là một card có sẵn trong `herk-edit-kit/style-library/01-vox-explainer` (106 card: 41 card con số, 18 card mở chương, 21 card tổng quan, 26 card chú thích). AI chỉ chọn card, điền chữ, ảnh và canh thời gian.

Ảnh mẫu: `reference/demo-fixes.jpg`. Storyboard mẫu 6 cảnh: `template/storyboard.json` (Hưng Nam 1950), ảnh của nó: `template/assets.json`.

## Dựng lại video demo (42 s) để kiểm tra máy
Chạy từ thư mục repo (Windows dùng `new-project.bat`):
```
bash skills-v2/_shared/scripts/new-project.sh explained-vox-cards demo-vox
python skills-v2/_shared/scripts/fetch_assets.py ../herk-edit-kit/video-projects/demo-vox ../herk-edit-kit/video-projects/demo-vox/assets.json
python skills-v2/_shared/scripts/mix_audio.py ../herk-edit-kit/video-projects/demo-vox --duration 42 --acts hook:0,build:15,climax:64,resolve:83
python skills-v2/_shared/scripts/cards.py build ../herk-edit-kit/video-projects/demo-vox ../herk-edit-kit/video-projects/demo-vox/storyboard.json
cd ../herk-edit-kit && npx hyperframes lint video-projects/demo-vox && npx hyperframes render video-projects/demo-vox --output ../output/demo-vox.mp4
```
Demo không có giọng đọc (`--duration 42` = chỉ nhạc). Video thật: làm giọng bằng `build_voiceover.py` trước, bỏ `--duration`, và dùng `from`/`to` (số câu) thay `duration` trong storyboard.

## Vì sao đẹp hơn template HTML tự vẽ
Card của herk do người thiết kế làm từng cái, có hệ màu, font, nhịp chuyển động thống nhất (`tokens.css`, `DESIGN.md` của style). Các preset cũ trong `skills-v2` không dùng thư viện này mà vẽ lại một template đơn, nên ít bố cục và đứng yên nhiều.

## Quy trình
1. Kịch bản → `build_voiceover.py` → `assets/timing.json` (giọng VieNeu-TTS, nghỉ 0,7/1,3/1,5 s).
2. Chọn card cho từng nhóm câu: `python skills-v2/_shared/scripts/cards.py list --purpose stat` (hoặc `section`, `overview`, `label`, `lower-third`). Mỗi dòng in tên card, thời lượng thiết kế, slot và số ký tự tối đa.
   - Con số → `stat.*` (có ảnh nền: `stat.over-photo`; số chạy: `stat.odometer`; so sánh: `stat.versus`).
   - Mở chương / ý chính → `section.*` (ảnh toàn khung: `section.fullbleed`; câu có cụm nhấn: `section.highlight`; hồ sơ mật: `section.classified`).
   - Mốc thời gian / nhiều ảnh → `overview.*` (`overview.filmstrip`, `overview.vtimeline`).
   - Đổi card liên tục; không dùng một card quá 2 lần trong 1 phút.
3. Viết `storyboard.json` trong thư mục dự án (định dạng ở đầu `cards.py`): mỗi beat `card`, `from`/`to` (số câu trong timing.json), `slots` (chữ tiếng Việt, `<em>` cho cụm nhấn), `images` (ảnh thật, tải bằng `fetch_assets.py` hoặc ảnh tạo bằng Muse).
4. Nhạc + giọng: `mix_audio.py` → `assets/mix.wav`.
5. Ghép: `python skills-v2/_shared/scripts/cards.py build <thư-mục-dự-án> <thư-mục-dự-án>/storyboard.json` → `index.html` + `compositions/bNN.html`. Đọc các dòng cảnh báo `!` (chữ quá dài, beat dài hơn card).
6. `npx hyperframes lint` (0 lỗi) → `snapshot` giữa mỗi beat, **xem contact sheet** → render vào `<ROOT>/output/` → `qa_video.py` ĐẠT.

## Luật
- Không sửa CSS/JS của card. Chỉ điền slot. Muốn đổi màu cả video: sửa `tokens.css` của style trong herk.
- Tôn trọng `maxChars`: số dài (14.000) đặt vào card số có khung rộng (`stat.over-photo`, `stat.odometer`), không vào `stat.torn`.
- Slot nối tiếp nhau (`key` rồi `post`): `post` bắt đầu bằng dấu cách (" lên tàu.").
- Font viết tay Caveat không có dấu tiếng Việt; `cards.py` tự đổi sang Patrick Hand. Không đưa lại Caveat.
- Mỗi beat theo thời lượng thiết kế của card (thường 5–8 s). Câu dài hơn → tách 2 card. `cards.py` báo khi beat dài hơn card 2 s.
- Ảnh trong card tự chuyển đen trắng. Ảnh AI phải ghi "ẢNH MINH HOẠ · TẠO BẰNG AI" trong slot `source`.

## `cards.py` tự sửa khi ghép
- Đổi id từng card (dùng một card nhiều lần không đụng nhau).
- Bỏ `@import` Google Fonts (HyperFrames tự nhúng font khi render).
- 18 card dùng `transform: scaleX(0)` trong CSS bị lint báo lỗi; chuyển sang `gsap.set` (hình không đổi).
- Card giữ khung cuối khi beat dài: khung chứa card trôi chậm (scale 1→1,035) để không đứng yên.
