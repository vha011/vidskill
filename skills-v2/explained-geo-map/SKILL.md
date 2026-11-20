---
name: explained-geo-map
description: Video giải thích địa chính trị / kinh tế quốc gia trên bản đồ (kiểu "Vì sao Singapore giàu"), dọc 9:16, bản đồ phẳng màu + ảnh vệ tinh, nhãn pop-up, vòng tròn vàng, phụ đề từ khóa vàng. Dùng khi chủ đề là một nơi/quốc gia/tuyến đường và câu chuyện đi theo không gian.
---

# explained-geo-map

Trích từ video tham chiếu `singapore.mp4` (720×1280 → dựng lại ở 1080×1920, 30 fps, 118,5 s, −14,1 LUFS, chỉ 3 khoảng lặng >0,4 s trong cả video → lời đọc liên tục, gần như không nghỉ).
Ảnh tham chiếu: `reference/singapore-sheet-*.jpg` (1 khung / 5 s), `reference/singapore-frame-45s.jpg` (khung chi tiết), `reference/template-snapshot.jpg` (template dựng lại).

## Khi nào dùng
Câu chuyện xoay quanh địa điểm: "vì sao X giàu/nghèo", tuyến thương mại, so sánh quốc gia, lịch sử một vùng. Không dùng cho số liệu dài (→ `explained-data-finance`).

## Cấu trúc câu chuyện (rút từ video mẫu)
1. **Hook 0–10 s** — ảnh vệ tinh zoom vào địa điểm + vòng tròn vàng + nhãn vàng so sánh gây bất ngờ ("Nhỏ hơn cả Sài Gòn", "Thu nhập ≈ Mỹ").
2. **Bối cảnh lịch sử** — bản đồ phẳng, số năm vàng cỡ lớn ("1965"), thẻ trắng có icon nhân vật/tivi.
3. **Nghịch lý** — 3 chip trắng xếp dọc với dấu ✕ đỏ (Đất: ít ✕ / Tài nguyên: không ✕ / Dân: nghèo ✕), vào lần lượt theo từng ý trong lời.
4. **Vị trí** — zoom ra khu vực (nền sa mạc/địa hình màu be), đường tàu vàng vẽ dần, nhãn tối xoay −24° ("Eo biển Malacca"), tàu nhỏ chạy theo đường.
5. **Chi tiết đặt chỗ** — quay lại ảnh vệ tinh: cảng, nhà máy lọc dầu, khu trung tâm; mỗi nơi 1 vòng vàng + 1 thẻ trắng ("Trung tâm lọc dầu lớn bậc nhất châu Á"); chip HQ đỏ/xanh/vàng.
6. **Tóm tắt "3 thứ"** — tiêu đề cố định trên cùng "X giàu nhờ 3 thứ", các mục đánh số 1, 2, 3 hiện dần dưới.
7. **CTA liên hệ khán giả** — zoom về Việt Nam, dấu "?" vàng, câu "Việt Nam mình có chỗ nào làm được vậy không?", chốt "VÌ SAO GIÀU?" + nút đỏ "+ Theo dõi" và "Comment cho tui biết nha".

Nhịp: có thay đổi trên hình ít nhất mỗi 2–4 s (nhãn mới / vòng vàng / camera). Mỗi câu lời 1 phụ đề, 4–8 từ.

## Thông số (đo từ khung hình; mã màu lấy mẫu pixel, ± vài đơn vị)

Màu — đã khai báo ở `:root` trong template:

| Vai trò | Mã |
|---|---|
| Nước biển (nền bản đồ phẳng) | `#6B9AA0` (ước lượng) |
| Quốc gia chủ đề (Malaysia) | `#C61F2E` |
| Quốc gia lân cận (Indonesia) | `#E0882F` |
| Vùng nền địa hình | `#E8D3A4` |
| Điểm nhấn (Singapore) | `#2B4EA8` |
| Vàng nhấn: vòng tròn, năm, nhãn, đường tàu | `#FFD708` |
| Từ khóa phụ đề | `#FADD0E` |
| Viền đất | `#111`, 5 px |
| Màu bổ sung theo nước: Thái `#4C9A3A`, Việt Nam `#2E9DB0`, Trung Quốc `#8B3FA8` (ước lượng) | |

Typography: **Be Vietnam Pro** (đã có trong `_shared/fonts`). Phụ đề ExtraBold 800, 56 px, viền đen 8 px (`paint-order:stroke fill`), vị trí `top:1180px`, căn giữa, tối đa 2 dòng. Thẻ trắng 54 px / 800, phụ 34 px / 700. Số năm 190 px / 800.

Thành phần:
- **Phụ đề**: từ khóa vàng, còn lại trắng. Mỗi câu hiện nguyên, vào 0,12 s (`y:14 → 0`, `power2.out`), không karaoke từng chữ.
- **Thẻ trắng** `.card`: bo 22 px, đổ bóng cứng `0 8px 0 rgba(0,0,0,.18)`; vào `y:60→0, 0,4 s, power3.out`.
- **Nhãn vàng** `.tag`: nền `#FFD708`, chữ đen 40 px; vào `scale .6→1, back.out(2), 0,35 s`.
- **Nhãn tối** `.dark`: `rgba(22,22,22,.88)`, chữ trắng 42 px, xoay theo hướng đường.
- **Vòng tròn vàng**: SVG `circle` r≈196, stroke 9 px, vẽ bằng `stroke-dashoffset 1→0` trong 0,6 s (`power2.out`).
- **Đường tuyến**: SVG `path` stroke 9 px vàng, vẽ 1,4 s `power1.inOut`.
- **Camera bản đồ**: `#map` scale 1.55 → 1.0 trong 13 s (`power1.inOut`), sau đó đổi tâm ở mỗi beat. Không để camera đứng yên >4 s.
- **Credit** góc trái trên: "Ảnh vệ tinh: Esri, Maxar, Earthstar Geographics", 20 px, nền đen 55%.

## Quy trình
1. Làm theo `_shared/PIPELINE.md` bước 1–3 (brief, kịch bản theo 7 phần ở trên, giọng đọc + đo thời lượng).
2. `bash skills-v2/_shared/scripts/new-project.sh explained-geo-map <slug>`.
3. Chuẩn bị ảnh nền: bản đồ phẳng (vẽ polygon SVG trong `#map` hoặc dùng ảnh PNG đặt vào `assets/` rồi thay khối `<svg>`) và ảnh vệ tinh (`assets/sat-*.jpg`). **Khi cần cảnh vệ tinh**: thêm `<img class="clip">` track 0 ở thời điểm đó và dùng `gsap.fromTo(scale 1.4→1.0)`. Ảnh phải có nguồn hợp pháp.
4. Sao chép khối `beat` trong `template/index.html` cho từng beat; đặt `data-start/duration` = thời lượng audio thật; đổi vị trí/nhãn.
5. Điền mảng `CAPTIONS = [bắt đầu, kết thúc, "câu", ["từ khóa"]]` bằng đúng thời gian từng câu.
6. Chèn audio, SFX (`whoosh` khi thẻ/nhãn vào, `click` khi chip vào, `ping` khi số lớn hiện).
7. Lint → snapshot → QA → render theo `PIPELINE.md`.

## Điều không được làm
- Không viết chữ trong ảnh nền; mọi chữ là HTML để đúng dấu tiếng Việt.
- Không dùng quá 3 màu quốc gia cùng lúc trên một khung ngoài bản đồ khu vực.
- Không để nhãn/thẻ đè lên vùng phụ đề (`y 1180–1420`).
- Không tự bịa số liệu: mọi con số ghi nguồn trong kịch bản.

## Hạn chế đã biết
Template chỉ có polygon minh họa; bản đồ thật phải thay bằng ảnh/SVG của bạn. Chưa phân tích kênh âm thanh (giọng đọc/nhạc nền) ngoài độ lớn và khoảng lặng, vì môi trường không có công cụ nhận dạng lời.
