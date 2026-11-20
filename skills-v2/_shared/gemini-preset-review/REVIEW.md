# Đánh giá 4 preset do Gemini dựng (README.zip, bản cập nhật)

Cách làm: giải nén `README.zip` mới, chạy `hyperframes lint` + `snapshot` ở 1 s, 4 s, 7 s, 10 s, 13 s, 14,55 s cho từng preset, rồi so với video mẫu tương ứng. Ảnh nằm cạnh file này (`*.jpg`).

## Kết quả kiểm tra tự động
| Preset | lint | Thời lượng | Audio |
|---|---|---|---|
| pnj-equity | 0 lỗi, 0 cảnh báo | 15 s | 4 SFX |
| singapore-geopolitics | 0 lỗi, 0 cảnh báo | 15 s | 4 SFX |
| vietjet-investigative | 0 lỗi, 0 cảnh báo | 15 s | 4 SFX |
| gym-break-even | 0 lỗi, 0 cảnh báo | 15 s | 5 SFX |

Cả 4 chạy được và sạch lỗi cú pháp. Nhưng lint chỉ chứng minh chạy được, không chứng minh đúng phong cách.

## Lệch so với video mẫu (đối chiếu từng khung)
1. **Cùng một khuôn cho cả 4 loại.** Mỗi preset: thanh tiêu đề "HỒ SƠ …" ở đỉnh, nền xanh navy gần đen, một khối nội dung, **hộp phụ đề bo góc ở đáy**. Video mẫu không có hộp phụ đề (trừ Singapore là chữ viền đen, không hộp) và mỗi video có ngôn ngữ hình ảnh riêng.
2. **Thiếu hẳn lớp nền.** Video mẫu dùng ảnh vệ tinh tối (Singapore, gym, FDI), bàn gỗ nhìn từ trên (Vietjet), nền xám than có lưới + băng giấy rách (Vietjet). Preset Gemini chỉ có gradient navy phẳng.
3. **Màu lệch.** PNJ preset dùng xanh lục `#10B981`/cam `#F59E0B`; video thực dùng lime `#ADF400`, đỏ `#E70A23`, vàng `#FEC73C`. Vietjet preset dùng đỏ đậm/xanh lục; video thực dùng lime `#CCF53C` + kraft `#D8C8A9`. Gym preset dùng lime `#84CC16`; video thực `#CBF73E`.
4. **Hình ẩn dụ bị thay bằng emoji và thẻ chữ.** Video mẫu dùng cutout (máy bay, xấp tiền, ví, lịch, thùng gỗ, két), nhãn giấy xé mép, dây nét đứt. Preset Gemini dùng emoji ✈️ 💵 🗄️ và hộp bo.
5. **Thời lượng 15 s** so với 118–270 s: không có cấu trúc dài (hook → bối cảnh → nghịch lý → bằng chứng → chốt).
6. **Lỗi hiển thị ở khung 1 s của Vietjet**: dấu "TÀI LIỆU KÝ KẾT" và "ĐÃ KÝ" chồng lên tiêu đề thẻ hợp đồng, chữ "BÊN CHO THUÊ" bị cắt mép phải (ảnh `vietjet-investigative.jpg`).
7. Biểu đồ cột PNJ dùng gradient xanh/đỏ có bóng; video mẫu dùng cột phẳng lime/đỏ/vàng, nền tối.

## Điểm tốt nên giữ
- Cấu trúc `index.html` + `assets/` + `meta.json` đúng chuẩn HyperFrames, nhúng font Việt, đã có SFX và nhạc nền 30 s.
- Thanh ticker giá (PNJ) và tọa độ (Singapore) là chi tiết đẹp nếu muốn làm phiên bản "terminal".
- Có sẵn cả 4 file `index.html` để Gemini copy làm điểm xuất phát (lint sạch).

## Kết luận
Giữ 4 preset làm khuôn kỹ thuật, nhưng **làm theo skill mới** (`explained-geo-map`, `explained-data-finance`, `explained-investigative`, `explained-fdi-timeline`, `explained-gym-business`) cho phong cách. Mỗi skill có mã màu, cỡ chữ, easing và template khớp với video thật.
