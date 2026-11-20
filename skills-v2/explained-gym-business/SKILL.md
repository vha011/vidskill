---
name: explained-gym-business
description: Video điều tra kinh doanh một chuỗi/doanh nghiệp (kiểu "California Fitness: chuyện gì đã xảy ra"). Dọc 9:16, nền ảnh vệ tinh tối, bảng giá viền trắng, thẻ báo trích dẫn có highlight lime, biểu đồ cột trắng/lime/đỏ có vạch mốc, chú giải bản đồ chấm đỏ/lime, thẻ giá đen. Dùng khi nội dung là thị trường + số liệu + trích dẫn báo.
---

# explained-gym-business

Trích từ `gym center.mp4` (720×1280 → 1080×1920, 30 fps, 225,4 s, −14,1 LUFS, không khoảng lặng >0,25 s). 32 lần đổi cảnh (ngưỡng 0,25), nhiều cụm cắt nhanh ở 91 s và 105 s (tường thumbnail).
Tham chiếu: `reference/gym-sheet_01..04.jpg` (1 khung / 5 s), `reference/gy150.jpg` (chú giải + ảnh), `reference/gy190.jpg` (thẻ tin có ảnh), `reference/template-snapshot.jpg`.
Bản Gemini cũ `gym-break-even-preset` (README.zip) dùng chế độ khác hẳn (thẻ "tiệm cầm đồ vs hội viên gym" kiểu hộp bo) — không khớp video mẫu; dùng skill này.

## Cấu trúc (rút từ video mẫu)
1. **Hook (0–25 s)**: ảnh vệ tinh tối + cung lime quét; bảng "Bảng giá các hạng" (Hạng | Giá | Nguồn) hiện dần từng hàng; số "10/2026" trắng lớn; thẻ tin báo nền ảnh.
2. **Tiêu đề điều tra**: nền thương hiệu (biển hiệu đỏ), "Thực hiện bởi ⚡ <Kênh>" nhỏ, "RỐT CUỘC" trắng 800 lớn + "CHUYỆN GÌ ĐÃ XẢY RA" lime.
3. **Tính toán nhanh**: "MỖI HỘI VIÊN = 10 TRIỆU ĐỒNG × 500.000" chạy trên bản đồ; hiệu ứng tia vàng; đường vàng nét đứt.
4. **Quy mô**: bản đồ Việt Nam viền lime, ghim trắng + đường cong trắng nối 2 thành phố + khối tiền.
5. **Tường thumbnail** (lưới 5×7 ảnh chi nhánh) với bộ đếm "THÁNG 3/2026 — 34" rồi "20": ảnh dần tối/mất.
6. **Bằng chứng**: tiêu đề báo (nền trắng, chữ đen 800), thông báo nội bộ, chấm đỏ trên bản đồ (chi nhánh còn mở) + chấm lime có vầng sáng (gym nhỏ gần nhà), chú giải.
7. **Biểu đồ**: "Người tiêu dùng Việt Nam THẮT CHẶT CHI TIÊU (% người được hỏi; nguồn: NielsenIQ)" cột trắng 57% (2024) so với lime ~8% (2025); biểu đồ "Tiền thuê mặt bằng so với doanh thu tháng" có vạch đỏ "MỐC 50%", cột đỏ 35–45% vs cột lime dưới 20%.
8. **Thẻ giá đối thủ**: nền đen, tiêu đề lime "PHÒNG GYM GẦN NHÀ", các dòng gói/giá, gạch dưới lime.

## Thông số (lấy mẫu pixel, ± vài đơn vị)

| Vai trò | Mã |
|---|---|
| Nền | ảnh vệ tinh làm tối (overlay `rgba(0,0,0,.45)`), cơ sở `#0E1114` |
| Lime (tiêu đề phụ, cột 2025, vòng sáng, highlight) | `#CBF73E` |
| Đỏ chú giải "California" | `#951A22` (trên nền mờ), đỏ cột `#C5202B` |
| Xanh chú giải "gym nhỏ" | `#7E9434` (lime nhạt do trong suốt) |
| Chữ thẻ tin | đen `#111` trên trắng |

Font **Inter**: tiêu đề 60 px 800 (cụm chính lime); dòng nguồn nghiêng 34 px 500 màu 72% trắng; số trục 30 px 600; nhãn giá trị 34 px 700; bảng 34 px, viền trắng 2 px (không có nền); tiêu đề bảng nghiêng lime 44 px 800.
Chuyển động: bảng hiện hàng cách 0,9 s; cột trắng mọc 1,0 s `power3.out`, cột lime mọc 0,8 s sau khoảng nghỉ 1,2 s (tạo bất ngờ); chấm lime có vầng sáng nhấp 2 nhịp; thẻ tin `y: +120→0, 0,5 s`.
Nền: trôi chậm `scale 1→1.15` cả video; cắt nhanh bằng "zoom ảnh vệ tinh" khi chuyển chủ đề.

## Quy trình
1. `_shared/PIPELINE.md` bước 1–3. Kịch bản bám cấu trúc 8 phần; mỗi con số ghi nguồn.
2. `bash skills-v2/_shared/scripts/new-project.sh explained-gym-business <slug>`.
3. **Thay nền**: ảnh vệ tinh thật (`assets/sat.jpg`) vào `#sat` bằng `background:url(assets/sat.jpg) center/cover`, giữ lớp `#dim`.
4. Biểu đồ: sửa mảng `BARS`, `MAX`, trục; thêm vạch ngưỡng bằng `el(s,'path',...)` màu đỏ `#E5202E` + nhãn "MỐC 50%".
5. Thẻ tin: chụp màn hình bài thật (có tên báo + ngày), dán `<img>` thay `.news` nếu muốn như mẫu.
6. Lint → snapshot → QA → render.

## Không được làm
- Không thêm phụ đề đốt cứng (video mẫu không có); chữ trên hình là nhãn/số.
- Không vẽ cột sai tỉ lệ: cột lime 8% phải thấp hơn cột 57% đúng tỉ lệ 8/57.
- Không dùng tên người/ảnh người thật nếu chưa có nguồn hợp pháp.

## Hạn chế
Template dùng nền giả lập vệ tinh, ảnh thương hiệu/người là khung giữ chỗ. Tường thumbnail + bộ đếm "34→20" chưa có template (cần ảnh thật; dựng bằng lưới `.thumb` và `gsap.to(obj,{n:20,onUpdate})`). Chưa trích lời đọc và nhạc nền.
