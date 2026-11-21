---
name: explained-history-dossier
description: Video giải thích lịch sử / chiến dịch theo phong cách "hồ sơ tư liệu" (kiểu "Kéo pháo ra", Điện Biên Phủ 1954). Ngang 16:9, nền xanh đen ấm, ảnh tư liệu đen trắng, panel kẻ viền, nhãn giấy kraft, mũi tên đỏ vẽ tay, thanh tiến trình ngày tháng. Dùng cho đề tài lịch sử, quân sự, chính trị cần mốc ngày và số liệu.
---

# explained-history-dossier

Trích từ `lichsu-vietnam.mp4` (1280×720 → dựng 1920×1080, 30 fps, 317,0 s, −14,2 LUFS, ~10 đoạn lặng >0,25 s ở chỗ chuyển ý). Khác bốn skill trước ở chỗ **ngang 16:9** và cảnh **tĩnh, ít chuyển động**: mỗi ý là một "trang hồ sơ" mà phần tử lần lượt hiện ra.
Tham chiếu: `reference/ls-sheet_01..06.jpg` (1 khung / 5 s), `ls012.jpg` (hook), `ls085.jpg` (lưới đơn vị + số lớn), `ls125.jpg` (điểm rẽ + giấy kraft), `ls215.jpg` (bản đồ + mốc ngày), `ls312.jpg` (chốt + câu hỏi), `template-snapshot.jpg` (template của skill này).

## Cấu trúc (rút từ video mẫu)
1. **Hook**: ảnh tư liệu đen trắng nghiêng nhẹ bên trái; panel bên phải gồm nhãn "HỒ SƠ 01 / …", ô ngày, câu hỏi cỡ lớn ("KÉO PHÁO RA?"), 1 dòng phụ; mũi tên đỏ vẽ tay nối ảnh với chữ.
2. **Tình hình bằng số**: tiêu đề 2 dòng, lưới "mỗi dấu = 1 đơn vị" (68 ô, 23 ô đỏ sáng lần lượt), dải số lớn "≈ 1/3" cùng chú thích nhỏ "dấu hiệu, không phải toàn bộ tương quan".
3. **Điểm rẽ**: nhãn giấy kraft "SƠ ĐỒ DIỄN GIẢI" + mũi tên đỏ ngược chiều; panel phải có ngày, "HOÃN TIẾN CÔNG KÉO PHÁO RA", phương châm vàng trong ngoặc kép, 3 thẻ mốc.
4. **Các đợt / giai đoạn**: mỗi đợt một trang: tiêu đề, nhãn ngày đỏ, 3 thẻ mốc (viền trên đỏ), ảnh nhỏ, bản đồ nền giấy kem bên phải; đợt sau thêm bảng chú thích "A1 / C1" nổi trên bản đồ.
5. **Nhân vật và kết cục**: ảnh chân dung nhỏ, hai dòng ngày kèm mô tả, một thẻ kem nổi bật giờ quyết định ("17:30 Sở chỉ huy bị chiếm").
6. **Chốt**: tiêu đề lớn, 1 câu phụ, gạch đỏ + mũi tên, vòng đếm ("56 NGÀY"), dải kem "CÂU HỎI DÀNH CHO BẠN" trượt vào.

## Thông số (đo từ khung hình)

| Vai trò | Mã |
|---|---|
| Nền | `#121411` → `#1D221C` (gradient chéo), quầng ấm `rgba(120,100,50,.16)` ở góc dưới phải |
| Panel | `#1C1E1B`, viền `#393B38` 1,5 px, đổ bóng sâu |
| Chữ tiêu đề | kem `#F2E6D2`, Roboto ExtraBold HOA, line-height 1.02 |
| Chữ phụ | `#DEE0D7`, Roboto Regular |
| Nhãn / mốc / nguồn | Courier Prime Bold HOA, giãn chữ 3–4 px; vàng `#E1BA74`, nâu nhạt `#B19064`, xám `#9A998F` |
| Đỏ (mũi tên, ô sáng, nhãn ngày, viền thẻ) | `#B4322C`, ô sáng `#A92C25`, số lớn `#D06955` |
| Giấy kraft / kem | `#E2D8C6`, chữ `#23201B`, nhãn đỏ `#A92C25` |

Khung cố định: viền mảnh cách mép 28 px; góc trái "HỒ SƠ CHIẾN DỊCH • 1954"; góc phải **ngày của trang hiện tại** (đổi theo cảnh); thanh tiến trình đỏ chạy đều từ đầu đến cuối với núm vàng; đường cong đứt đỏ ở đáy; **dòng nguồn riêng cho mỗi trang** (Courier HOA) ở góc trái dưới.

## Chuyển động
- Cảnh tĩnh: phần tử vào bằng `power3.out`, 0,4–0,7 s, trượt ≤ 80 px hoặc hiện mờ. Không zoom, không xoay trừ ảnh hook (−1,6°).
- Mũi tên / gạch đỏ vẽ bằng `stroke-dashoffset` (pathLength=1), 0,7 s `power2.out`, đầu mũi hiện sau cùng.
- Lưới đơn vị: từng ô scale 0,6 → 1, `stagger: 0.045`.
- Thẻ mốc ngày: `stagger: 0.45–0.6` bám theo lời đọc.
- Câu hỏi chốt trượt vào từ trái, `power3.out`.
- Chuyển trang ở khoảng lặng ~0,3 s: trang cũ tắt hẳn, trang mới dựng lại từ đầu (không cross-fade dài).

## Quy trình
1. Soạn kịch bản theo ngày: mỗi trang = 1 ý + 1 ngày + 1 nguồn, 8–15 s.
2. Chạy giọng đọc / timing theo `skills-v2/_shared/PIPELINE.md`; cắt khoảng lặng >0,25 s.
3. Copy `template/index.html` vào project mới (`_shared/new-project.sh`), đổi nội dung 5 trang, giữ nguyên khung, đổi 5 dòng `.dt` / `.src`.
4. Thay hộp `.photo .im` bằng ảnh thật, thay "BẢN ĐỒ" bằng bản đồ có nguồn rõ ràng.
5. `hyperframes lint` → `snapshot` giữa mỗi trang → render.

## Tư liệu
- Ảnh đen trắng có hạt: `filter: grayscale(1) contrast(1.1)`; cắt thẳng, không viền trắng; chỉ ảnh hook nghiêng.
- Bản đồ đặt trên nền giấy kem rộng hơn bản đồ để có lề.
- Ghi nguồn từng trang; nếu chưa xác minh quyền sử dụng thì ghi rõ "quyền khai thác công khai chưa xác nhận" như video mẫu.
- Template chỉ có hộp xám giữ chỗ cho ảnh và bản đồ — phải thay bằng tư liệu thật trước khi render.

## Không làm
- Không dùng emoji, icon hoạt hình hay màu ngoài bảng trên.
- Không để quá 2 mũi tên đỏ cùng lúc trên một trang.
- Không đưa số liệu khi chưa có nguồn; giữ dòng "dấu hiệu, không phải toàn bộ" cho tỷ lệ ước lượng.
- Không đổi sang dọc 9:16; skill dọc là `explained-fdi-timeline` và các skill khác.
- Không dùng ảnh cutout viền trắng như skill FDI / gym.

## Chưa có trong template
Trang "Đợt II / Đợt III" (bảng chú thích A1/C1, thẻ kem 17:30, chân dung) mới mô tả bằng chữ và ảnh tham chiếu; template có 5 trang: hook, lưới số, điểm rẽ, đợt I, chốt. Chưa trích lời đọc và nhạc nền của video.
