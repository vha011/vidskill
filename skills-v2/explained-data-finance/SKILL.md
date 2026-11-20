---
name: explained-data-finance
description: Video phân tích doanh nghiệp / tài chính / điều tra số liệu (kiểu "PNJ sa cơ như thế nào?"), dọc 9:16, nền tối, biểu đồ đường lime, cột vàng/đỏ, thẻ báo có khoanh đỏ, con dấu, sticker. Dùng khi nội dung chủ yếu là số liệu, biểu đồ, trích báo.
---

# explained-data-finance

Trích từ video tham chiếu `pnj-tai-chinh.mp4` (720×1280 → dựng lại 1080×1920, 30 fps, 225 s, −14,1 LUFS, không có khoảng lặng >0,4 s). Có 19 lần đổi cảnh cứng (ngưỡng cảnh 0,25) trong 225 s, mỗi chart giữ 6–12 s, giữa các chart xen b-roll và thẻ báo.
Ảnh tham chiếu: `reference/pnj-sheet-01..04.jpg` (1 khung / 5 s), `reference/pnj-frame-*.jpg` (khung chi tiết chart), `reference/template-snapshot.jpg`.

## Khi nào dùng
Phân tích cổ phiếu, báo cáo tài chính, vụ việc doanh nghiệp, so sánh số liệu theo thời gian. Không có phụ đề đốt cứng: chữ trên màn hình là tiêu đề chart, nhãn số liệu, trích báo.

## Cấu trúc (rút từ video mẫu)
1. **Hook** — chart/bản đồ tối làm nền + câu hỏi lớn ("PNJ SA CƠ NHƯ THẾ NÀO?"), từ khóa lime, dòng "Thực hiện bởi <kênh>" nhỏ phía trên.
2. **Dòng chảy bằng chứng** lặp lại: *(a) chart có số* → *(b) thẻ báo trích dẫn có khoanh đỏ/highlight* → *(c) b-roll tối + sticker minh họa* → *(d) chart tiếp theo*.
3. **Điểm nhấn pháp lý/sự kiện** — thanh giấy trắng/đen chữ lớn + con dấu đỏ xoay (−6°) đập xuống ("HẾT HIỆU LỰC").
4. **Chốt bằng số lớn** — huy hiệu viền lime + sticker + ô vàng ("700 TỶ").
5. **Kết** — nền đen, ảnh nhân vật cắt viền cùng tài liệu.

## Thông số (mã màu lấy mẫu pixel từ khung; ± vài đơn vị)

| Vai trò | Mã |
|---|---|
| Nền | `#080F0D` … `#090D0F` + b-roll/bản đồ vệ tinh làm tối (opacity 0,25–0,35) |
| Lime (tiêu đề chart, đường chính) | `#ADF400` |
| Đỏ (giảm, âm, khoanh, vòng đánh dấu) | `#E70A23` |
| Vàng (dương, số nổi bật, ô tổng) | `#FEC73C` |
| Highlight trên thẻ báo | `#D4F55A` |
| Chữ | trắng; phụ 72% trắng, nghiêng 500 |

Typography: tiêu đề chart ExtraBold 60 px (cụm chính lime, phần còn lại trắng); dòng phụ nghiêng "(đơn vị; nguồn: …)" 34 px; số trục 36 px / 500; nhãn số liệu 44–56 px / 800. Font: **Inter** (`_shared/fonts/Inter.ttf`, biến thiên 100–900).

Thành phần và chuyển động:
- **Chart đường**: path SVG stroke 8 px lime, vẽ bằng `stroke-dashoffset` trong 3 s (`power1.inOut`); trục trắng 2,5 px hiện trước (0,4 s); điểm cuối có vòng đỏ + đường đứt ngang. Dữ liệu ở `LINE.pts` (x 0–1, giá trị thực).
- **Chart cột dương/âm**: trục 0 trắng, cột vàng mọc lên, cột đỏ mọc xuống (`scaleY 0→1`, 0,7 s, `power3.out`), giá trị hiện sau (`stagger 1.2`). Dữ liệu ở `BARS`.
- **Thẻ báo**: nền trắng, xoay −2°, bóng mềm, vào `scale .9→1, y 40→0, 0,5 s`; khoanh đỏ bầu dục (viền 6 px) `scale .2→1, back.out(1.8)`; cụm quan trọng `<mark>` màu `#D4F55A`.
- **Con dấu**: viền 10 px `#C21A1A`, chữ 96 px, xoay −6°, `scale 2.2→1, 0,25 s, power4.in` + `sfx_hit.wav` đúng khung chạm.
- **Sticker**: emoji 150 px rơi `bounce.out` 0,5–0,6 s (thay bằng PNG 3D nếu có, như video mẫu).
- **Nền**: scale chậm 1 → 1.08 trong cả video (chống tĩnh). B-roll thật: `<video muted playsinline>`, phủ lớp tối `rgba(0,0,0,.35–.55)`.

## Quy trình
1. `_shared/PIPELINE.md` bước 1–3. Kịch bản: mỗi ý = 1 chart hoặc 1 thẻ báo; ghi sẵn đơn vị + nguồn của mọi số.
2. `bash skills-v2/_shared/scripts/new-project.sh explained-data-finance <slug>`.
3. Với mỗi chart: sao chép khối `#bN`, sửa `title`, `sub`, dữ liệu; chuẩn hóa trục (bắt đầu từ 0 trừ khi nêu rõ).
4. Thẻ báo: chụp màn hình bài thật → `assets/news-*.png`, thay `.card`; hoặc giữ HTML như template.
5. Căn thời gian từng beat với audio thật, chèn SFX theo bảng (`whoosh` tiêu đề, `ping` số, `hit` dấu, `click` huy hiệu).
6. Lint → snapshot → QA → render.

## Không được làm
- Không đổi màu lime/đỏ/vàng sang màu khác; đỏ chỉ cho giảm/âm/cảnh báo.
- Không chart nào thiếu đơn vị và nguồn.
- Không hiển thị >1 chart cùng lúc; mỗi chart ≥6 s để người xem đọc kịp.
- Không dùng ảnh người thật làm nhân vật phản diện nếu chưa có nguồn/giấy phép.

## Hạn chế đã biết
Phần nhân vật cắt viền, b-roll và ảnh 3D phải do người dùng cung cấp. Chưa trích xuất lời đọc/nhạc nền của video mẫu (không có công cụ nhận dạng lời trong môi trường phân tích).
