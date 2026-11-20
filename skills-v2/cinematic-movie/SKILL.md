---
name: cinematic-movie
description: Video kể chuyện kiểu phim ngắn / phim tài liệu có thế giới hình ảnh xuyên suốt, máy quay ảo, cảnh chuyển có chủ đích. Dùng khi cần cảm xúc và mạch truyện hơn là số liệu.
---

# cinematic-movie  (CHƯA có video tham chiếu riêng)

Trạng thái: **khung hướng dẫn**. Chưa có video phim mẫu để đo nên chưa có template. Không viết thông số màu/font cho loại này cho tới khi có demo — tránh làm Gemini "đoán".

## Dựa vào gì
- Skill `video-storytelling` của herk-edit-kit: thiết kế hình ảnh như một thế giới xuyên suốt, ngữ pháp máy quay, "open loop" không gian, đồng bộ theo transcript.
- Skill `make-a-video`: quy trình 8 cổng (phỏng vấn brief → duyệt → dựng → xem trước → kiểm tra hình → render).
- Skill `hyperframes-video-beats` nếu có video người nói thật cần chèn overlay.
- Tái dùng `_shared` của repo này: font, gsap, SFX, `PIPELINE.md`, checklist QA.

## Khung làm việc tạm thời
1. Viết **logline 1 câu + 5 cảnh** (mở – đẩy – điểm ngoặt – cao trào – kết). Duyệt xong mới dựng.
2. Chọn **một** mô-típ hình xuyên suốt (một địa điểm, một vật thể, một tông màu). Mọi cảnh phải nối bằng mô-típ này.
3. Mỗi cảnh 4–10 s; chuyển cảnh bằng chuyển động camera liên tục (zoom/pan cùng hướng), không dùng hiệu ứng wipe ngẫu nhiên.
4. Chữ chỉ dùng cho tiêu đề cảnh và phụ đề; tối thiểu hóa chữ trên hình.
5. Làm theo `_shared/PIPELINE.md` từ bước 3 trở đi.

Khi có video phim mẫu: phân tích theo cách đã làm cho hai skill kia (cảnh cắt, khung contact-sheet, màu lấy mẫu, độ lớn âm thanh, khoảng lặng), rồi viết template + thông số vào skill này.
