---
name: explained-fdi-timeline
description: Video giải thích lịch sử kinh tế / chính sách theo dòng thời gian (kiểu "Hyundai được tạo ra thế nào", FDI Việt Nam). Dọc 9:16, thanh thời gian chạy trên đỉnh, bản đồ vệ tinh, thùng hàng xếp tầng, sơ đồ chính sách viền lime phát sáng, ảnh quảng cáo cũ, dấu "ĐÃ BÁN", donut. Dùng khi câu chuyện là chuỗi năm tháng + cơ chế chính sách.
---

# explained-fdi-timeline

Trích từ `fdi vn.mp4` (720×1280 → 1080×1920, 30 fps, 269,6 s, −14,1 LUFS, chỉ 5 lần đổi cảnh cứng; 1 khoảng lặng >0,25 s).
Tham chiếu: `reference/fdi-sheet_01..05.jpg` (1 khung / 5 s), `reference/fd120.jpg` (sơ đồ chính sách chi tiết), `reference/fd175.jpg` (ảnh xe + hàng xe nhỏ), `reference/template-snapshot.jpg`.

Bản đối chiếu có sẵn trong README.zip: `fdi-explainer-preset/` (Gemini dựng, dùng tông `#0A0D14` + lime `#A3E635`; đo thực tế từ video là nền gần đen ấm `#0D0B0C` và lime vàng hơn `#CBF73E`). Dùng **skill này** làm chuẩn.

## Cấu trúc (rút từ video mẫu)
1. **Hook**: ảnh vệ tinh tối + cờ, câu hỏi "HYUNDAI ĐƯỢC TẠO RA THẾ NÀO?" (trắng lớn + lime phụ).
2. **Mở đầu bằng thanh thời gian**: lịch đỏ-trắng trượt trên thước (1961 → 2026); dòng "QUAY VỀ ĐẦU THẬP NIÊN 60" (cam nhấn "ĐẦU THẬP NIÊN 60"), bản đồ nước đó nổi viền trắng, nhãn thành phố.
3. **Vấn đề bằng số**: chữ đỏ lớn ("9 THÁNG", "THIẾU ĐÔ LA"); cột lime lớn so với trục 0 ("205" triệu USD).
4. **Hệ quả vật thể**: két sắt mở, hòm tiền; **thùng hàng xếp tầng 1962 / 1963 / 1964**, đường đứt lime nối các đỉnh.
5. **Cơ chế chính sách** (sơ đồ): TỪNG BỘ → TỪNG NGÀNH → TỪNG DOANH NGHIỆP → HỌP MỖI THÁNG → [ĐẠT ✓ | VƯỠNG Ở ĐÂU? | TRƯỢT] → "Thưởng" → VỐN RẺ/VỐN ƯU ĐÃI → TÍN DỤNG XUẤT KHẨU. Hộp viền lime phát sáng; hộp đang nói sáng, hộp chưa tới mờ.
6. **Kết quả**: chart đường 1962–1977 ("10 TỶ ĐÔ", "×100 SAU 13 NĂM") + chân dung.
7. **Câu chuyện sản phẩm**: ảnh quảng cáo báo cũ xoay nghiêng, xe đỏ cutout viền trắng, dấu "ĐÃ BÁN", hàng xe nhỏ nhân bản, donut "GẦN 1/2".
8. **Liên hệ**: "VIỆT NAM LÀM LẠI Đ…", biển chỉ đường, biểu đồ bẫy thu nhập trung bình.

## Thông số

| Vai trò | Mã |
|---|---|
| Nền | `#0D0B0C` (khung xe: `#222021`), lưới trắng 3,5% mỗi 80 px |
| Lime (năm đang nói, viền hộp, đường, cột tốt) | `#CBF73E` (đo `#C3EF38`–`#CBF73E`) |
| Cam (nhấn năm/cụm quan trọng phụ) | `#F59A23` (ước lượng) |
| Đỏ (thiếu, trượt, dấu) | `#E5202E`; dấu mộc `#C21A1A` |
| Giấy ảnh | trắng `#F2F2F2` viền 14 px |

Font **Inter**. Tiêu đề 72/48 px 800; năm 36 px 800 **nghiêng**, năm đang nói màu lime còn lại trắng; nhãn chú thích 38 px nghiêng lime.
TimelineRunner: thước trắng 4 px, 4 vạch, năm đầu lime, năm cuối trắng, phần đã đi tô lime, icon lịch (đầu đỏ, thân trắng) trượt đều (`ease:'none'`) trong suốt video. Đổi mốc (ví dụ 1961 → 1964) thì đổi nhãn đầu/cuối và reset vị trí.
Thùng hàng: 230×92 px, gỗ `#caa26e`→`#b98a52`, viền `#8c6532`; rơi từ trên `y:-700…-1100 → 0`, `back.out(1.4)`, stagger 0,12 s, cột sau cách 0,35–1,4 s.
Sơ đồ: hộp 620×210 px, viền 7 px lime, bo 30 px, glow `0 0 40px rgba(203,247,62,.45)`; mũi tên lime 8 px; hộp vào `scale .8→1, back.out(1.6), 0,4 s`; mũi tên vẽ `scaleY 0→1, 0,3 s`; hộp cuối nhấp sáng 2 nhịp. `✓` tròn lime 76 px ở góc phải trên hộp "ĐẠT".
Donut: SVG r=70, stroke 34, nền `#3a3a3a`, cung lime; animate bằng `onUpdate` + `setAttribute('stroke-dashoffset')` (tween trực tiếp `strokeDashoffset` trên `<circle>` này không hiện khi em thử, nên dùng cách này).

## Quy trình
1. `_shared/PIPELINE.md` bước 1–3. Viết kịch bản theo mốc năm; mỗi mốc 1 vật thể (bản đồ / thùng / hộp / xe).
2. `bash skills-v2/_shared/scripts/new-project.sh explained-fdi-timeline <slug>`.
3. Chỉnh mốc thời gian đầu/cuối của thước, số thùng mỗi cột (tỉ lệ đúng với số liệu: thùng = đơn vị, ghi chú đơn vị), nội dung hộp sơ đồ.
4. Thay `.photo` bằng ảnh thật (`<img>` trong `.photo`, `object-fit:cover`).
5. Lint → snapshot → QA → render.

## Không được làm
- Không để thước thời gian đổi tốc độ giữa chừng; nếu cần nhảy mốc, tạo thước mới.
- Không dùng quá 7 hộp trong một sơ đồ; hộp chưa nói phải mờ (opacity .25).
- Thùng/cột phải tỉ lệ với số liệu thật, không vẽ cho đẹp.

## Hạn chế
Ảnh quảng cáo cũ, xe, chân dung phải do người dùng cung cấp; template dùng khung giữ chỗ. Chưa trích lời đọc và nhạc nền.
