---
name: explained-investigative
description: Video điều tra / giải thích một vụ việc tài chính-pháp lý có tiền, hợp đồng, tòa án (kiểu "Vietjet bị đòi 250 triệu USD"). Dọc 9:16, nền xám than có lưới, nhãn giấy kraft và lime xé mép, băng giấy rách, cutout (máy bay, tiền, ví, lịch, giấy tờ), dây lime nét đứt, dấu mộc. Dùng khi phải giải thích một cơ chế (thuê, vay, bảo lãnh, phạt) bằng hình ẩn dụ vật thể.
---

# explained-investigative

Trích từ `vietjet airline.mp4` (720×1280 → dựng lại 1080×1920, 30 fps, 208 s, −14,1 LUFS, AAC 44,1 kHz, không có khoảng lặng >0,25 s). Chỉ 7 lần đổi cảnh cứng trong 208 s → cảnh dài, mọi thay đổi diễn ra **bên trong** cảnh bằng chuyển động của vật thể.
Tham chiếu: `reference/vj-sheet_01..04.jpg` (1 khung / 5 s), `reference/vj52.jpg` (khung 2 cột chi tiết), `reference/vj112.jpg`, `reference/template-snapshot.jpg`.

## Cấu trúc câu chuyện (rút từ video mẫu)
1. **Hook (0–20 s)**: bản đồ vệ tinh tối + thẻ ảnh Polaroid ghi địa điểm/ngày ("TÒA ÁN LONDON · 15/10"), dây lime nét đứt thả xuống. Sau đó cột tiền "HƠN 250 TRIỆU USD" so với "8 TRIỆU USD" ("TRẢ CHẬM") → chênh lệch phi lý là móc câu.
2. **Giải thích thang đo**: cột đo bằng sọc ngang (xanh lime vs đỏ), có vạch 10/100 triệu USD; vật thể (máy bay) làm "con trỏ" trên thang.
3. **Cơ chế bằng ẩn dụ vật thể**: hai cột đối chiếu "HÃNG BAY | BÊN CHO THUÊ" trên băng giấy rách; ví, xấp tiền, lịch (KỲ 2, KỲ 3), giấy sở hữu; hàng máy bay trên đường băng có đèn vàng.
4. **Bản đồ dòng tiền**: cuộn bản đồ thế giới/Nhật/Việt Nam, đường lime nét đứt nối các thực thể (Vietjet → công ty Nhật → ngân hàng), icon ngân hàng/hợp đồng/virus.
5. **Bằng chứng thật**: ảnh bàn gỗ nhìn từ trên, hồ sơ, con dấu, hợp đồng "TERMINATED", nhãn đỏ "THÁNG 10/2021", bảng "PAYMENT SCHEDULE" có dấu "?".
6. **Hệ quả**: chồng phong bì tiền cao dần tới vạch "TÒA TUYÊN ~181 TRIỆU USD", rồi câu hỏi chốt "BỊ ĐÒI 2 LẦN?" với hai lựa chọn 1./2.
7. **Quay lại hiện tại**: tin báo chụp màn hình + hợp đồng có số lịch lớn "17" + dấu "QUÁ HẠN".

Nhịp: 1 vật thể mới mỗi 1–3 s; không có phụ đề đốt cứng (chữ trên hình là nhãn).

## Thông số (lấy mẫu pixel, ± vài đơn vị)

| Vai trò | Mã |
|---|---|
| Nền | `#252525`, lưới trắng 4,5% mỗi 90 px |
| Lime (nhãn, dây nét đứt, cột tốt) | `#CCF53C` (đo `#D6F152`…`#CBF73E`) |
| Giấy kraft (nhãn trung tính) | `#D8C8A9` |
| Băng giấy rách / đường băng | `#32323A` |
| Đỏ (nợ, hết hạn, cảnh báo) | `#E3202E` (ước lượng) |
| Dấu mộc | `#C21A1A` |

Font: **Inter** ExtraBold 800 in hoa. Nhãn 52 px (nhỏ 36 px), padding 14×26, xoay −2°…−3°, bóng cứng `0 6px 0 rgba(0,0,0,.35)`, **viền xé mép bằng `clip-path`** (đã có trong `.lab`). Nhãn kraft = đối tượng cố định; lime = bên mạnh/điểm cần nhớ; đỏ = rủi ro; trắng = đáp án lựa chọn.
Chuyển động: nhãn `back.out(2)` 0,35 s; cột tiền `power2.out` 1,6 s; dấu mộc `scale 2,4→1, 0,25 s, power4.in` + `sfx_hit`; băng giấy rách `y: +300→0, 0,6 s`; máy bay `x:-700→0, 0,9 s`.

## Quy trình
1. `_shared/PIPELINE.md` bước 1–3. Mỗi câu lời = 1 vật thể / 1 nhãn; ghi trước "ẩn dụ" cho từng ý (tiền = xấp phong bì; hợp đồng = tờ giấy…).
2. `bash skills-v2/_shared/scripts/new-project.sh explained-investigative <slug>`.
3. Sao chép khối `.beat`, đổi nội dung; thay ảnh `.card .ph`, `.doc` bằng ảnh thật nếu có (assets/*.jpg); chữ giữ ở HTML.
4. Căn thời gian bằng audio thật, SFX theo bảng.
5. Lint → snapshot → QA → render.

## Không được làm
- Không dùng quá 4 màu nhãn; không dùng chữ thường trong nhãn.
- Không để quá 6 vật thể trong một khung.
- Số tiền phải khớp nguồn, ghi đơn vị (triệu USD / tỷ đồng).
- Không dùng ảnh người/ảnh báo nếu chưa có quyền; ghi nguồn khi chụp tin.

## Hạn chế
Máy bay, ví, tiền, lịch trong video mẫu là ảnh cắt PNG chất lượng cao; template dùng hình khối SVG/CSS thay thế (xem snapshot). Anh nên chuẩn bị bộ PNG cutout và thay vào để giống mẫu hơn. Chưa trích được lời đọc và nhạc nền.
