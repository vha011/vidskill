# Mẫu kịch bản + danh sách shot cho video dài

Toàn bộ khung này là **ĐỀ XUẤT** dựa trên 68 s đầu của clip mẫu; chưa đo được từ bản đầy đủ.

## 1. Brief (điền trước)
| Mục | Điền |
|---|---|
| Logline 1 câu | "[Nhân vật chính] muốn [mục tiêu], nhưng [phản diện] đã [bẫy]; hậu quả là [điều lạ lùng]." |
| Tiêu đề = lời hứa | câu hỏi/gây tò mò, ví dụ "X tỉnh dậy HUGE… Y đã làm gì anh ấy?!" |
| Thời lượng | 10 phút = 12 chương × 50 s |
| Ngôn ngữ giọng đọc | Việt / Anh |
| Nhân vật (≤4) | điền khối prompt từ `characters-sample.md` |
| Địa điểm (≤6) | mỗi nơi 1 dòng mô tả cố định (như khối nhân vật) |

## 2. Khung chương (mỗi chương 40–60 s, ≈ 20–30 shot)
Mỗi chương ghi đủ 6 dòng:
1. **Mục tiêu nhỏ** của nhân vật chính.
2. **Cảnh phản diện/biến cố** (người xem biết trước nhân vật chính).
3. **Mồi/đạo cụ có nhãn** (nhãn 2–4 từ, in HOA).
4. **Sa bẫy hoặc xử lý sai**.
5. **Hậu quả** (phải lớn hơn chương trước, nhìn thấy được).
6. **Cliffhanger**: một câu hỏi hoặc một hình ảnh lạ cuối chương.

Gợi ý nhịp 12 chương: C1 mẫu 68 s (mục tiêu + bẫy) → C2–C3 hậu quả đầu tiên và che giấu → C4–C8 phản diện thêm mồi, hậu quả leo thang, nhân vật đối trọng cảnh báo → C9–C10 đỉnh điểm, mọi người phát hiện → C11 phản diện bị vạch → C12 trả lời đúng câu hỏi tiêu đề + cảnh kết hài.

## 3. Bảng shot (một bảng cho mỗi chương)
| # | Giây | Địa điểm | Cỡ cảnh | Góc | Hành động + cảm xúc | Nhãn chữ | Lời đọc | Prompt ảnh khóa | Prompt chuyển động | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0–2 | … | Wide | thấp | … | "GRAND RACE" | … | [STYLE]+[NV]+[bối cảnh]+… | Camera: … Giữ nguyên nhân vật… 2 giây | ☐ ảnh ☐ clip ☐ QA |

Quy tắc điền:
- Mỗi **cặp shot liền nhau đổi cỡ cảnh** (wide → medium → cận), tránh hai shot liên tiếp cùng cỡ và cùng nhân vật.
- 1 câu lời đọc = 2–4 shot; shot dài ≥ 3 s chỉ khi có hành động rõ.
- Ghi sẵn vị trí trái/phải của hai nhân vật trong từng địa điểm và giữ.
- Mỗi chương có ≥ 1 shot cận đạo cụ có nhãn và ≥ 1 shot "gáy tiền cảnh" khi phản diện hành động.

## 4. Danh sách kiểm QA mỗi clip
- [ ] Khuôn mặt, mũ, trang phục đúng khối nhân vật.
- [ ] Tay 5 ngón, không biến dạng.
- [ ] Chữ trên đạo cụ đúng; không có chữ lạ ở nền.
- [ ] Hướng nhìn nối được với shot trước và sau.
- [ ] Màu/đạo cụ liên tục (lọ, mũ đầu bếp).
- [ ] Không có logo/watermark không mong muốn.

## 5. Ghép
Copy `templates/assemble/index.html`, thêm một thẻ `<video>` cho mỗi shot (`data-start` nối tiếp), `data-track-index="0"` cho toàn bộ clip, giọng `5`, nhạc `6`, SFX `7+`. Mỗi chương 1 composition, rồi nối bằng FFmpeg.
