---
name: explained-video-maker
description: Quy trình sản xuất video giải thích đa thể loại (Explained Videos) chuyên nghiệp 100% Local bằng HyperFrames + GSAP (herk-edit-kit) và giọng đọc AI VieNeu-TTS Trúc Ly. Hỗ trợ 4 Preset chuẩn (Biocodex Y tế, Greenland Phóng sự/Bản đồ, Juno Thời trang UGC, FDI / Finpath Kinh tế vĩ mô) và khả năng Reverse-Engineering phân tích video mẫu bất kỳ để nhân bản thành Style Preset.
---

# 🎬 EXPLAINED VIDEO MAKER SKILL

Hệ thống sản xuất video giải thích chuyên nghiệp sử dụng chuyển động đồ họa HTML5/GSAP (HyperFrames) kết hợp giọng đọc thuyết minh tiếng Việt tự nhiên (VieNeu-TTS) chạy 100% offline nội bộ.

---

## 1. BỐN PRESET CỐT LÕI

### Preset 1: Medical / Pharma / Science Explainer (Phong cách Biocodex)
- **Mục tiêu**: Giải thích cơ chế bệnh học, cơ chế vi sinh vật, tác dụng dược lý, phân tích số liệu y khoa.
- **Visual**: Infographics y tế sạch sẽ, sơ đồ vi khuẩn/tế bào chuyển động (animated diagrams), biểu đồ số liệu lâm sàng, tone màu xanh navy y tế + trắng ngọc trai.
- **Tỉ lệ**: 16:9 (YouTube) hoặc 9:16 (Shorts/Reels).
- **Tone giọng**: Trầm tĩnh, chuyên gia, chuẩn mực, đáng tin cậy.

### Preset 2: Geopolitics / Documentary / Storytelling (Phong cách Greenland - Trump)
- **Mục tiêu**: Kể chuyện phóng sự, phân tích chiến lược, địa chính trị, xâu chuỗi sự kiện lịch sử (phong cách Vox, Johnny Harris).
- **Visual**: Bản đồ động phóng to/thu nhỏ (Map zoom & territory highlight), tư liệu báo chí, timeline chạy mốc thời gian, camera kinetic zoom.
- **Tỉ lệ**: 16:9 hoặc 9:16 dọc.
- **Tone giọng**: Hùng biện, lôi cuốn, nhịp điệu dồn dập, gợi mở tò mò.

### Preset 3: Commercial / Fashion / Product UGC (Phong cách Juno)
- **Mục tiêu**: Video quảng cáo chuyển đổi cao theo UGC framework 30s.
- **Visual**: Hook 0-7s chống nuốt dáng, PIP cận cảnh chất liệu, đường gióng 1px tôn đường cong, dải phụ đề Liquid-Glass chân trang, CTA giỏ hàng TikTok Shop.
- **Tỉ lệ**: 9:16 dọc (1080x1920, 30fps).
- **Tone giọng**: Nữ trẻ trung (Trúc Ly), tươi tắn, gần gũi, thuyết phục.

### Preset 4: Macroeconomics / Geopolitics / Tech Policy (Phong cách Finpath / FDI VN)
- **Mục tiêu**: Video phân tích kinh tế vĩ mô, chuỗi cung ứng FDI, câu chuyện tự chủ công nghệ, địa chính trị tài chính.
- **Visual**: Dark Tech Slate (#0A0E17) + Technical Graph Grid 60px; Neon Lime (#A3E635) + Golden (#FACC15); Timeline Runner đỉnh khung hình; bản đồ tuyến vận tải phát sáng; biểu đồ thùng hàng xếp tầng (Bounce Physics); sơ đồ cây quyết định chính sách (Policy Tree Glow); cắt dán tư liệu báo chí viền trắng + con dấu đỏ "ĐÃ BÁN" đập mạnh (Hit SFX).
- **Tỉ lệ**: 9:16 dọc (1080x1920, 30fps).
- **Tone giọng**: Trầm hùng, khách quan, sắc bén, nhịp điệu cuốn hút.

---

## 2. QUY TRÌNH REVERSE-ENGINEERING VIDEO MẪU THÀNH STYLE PRESET

Khi người dùng cung cấp một video mẫu (link hoặc file mp4), thực hiện quy trình 4 bước để nhân bản thành Preset:

```
[Video Mẫu] ──> [Bóc Tách 5 Lớp] ──> [Tái Tạo GSAP/CSS] ──> [Đóng Gói Preset]
```

### Bước 1: Bóc tách 5 lớp cấu trúc (Deconstruction)
1. **Lớp 1: Cấu trúc kịch bản (Narrative Beats)**:
   - Trích xuất lời thoại qua audio.
   - Xác định cấu trúc: Hook (Mở đầu) ➔ Pain point (Nỗi đau) ➔ Mechanism (Cơ chế giải thích) ➔ Climax ➔ Resolution / CTA.
2. **Lớp 2: Diễn hoạt chuyển động (Motion & Animation)**:
   - Các hiệu ứng chữ: Kinetic typography, highlight từng từ theo voice, typewriter, slide up/fade.
   - Các chuyển cảnh: Whip pan, push in, smooth zoom, paper tear, match cut.
3. **Lớp 3: Bố cục & Visual Design (Layout / Palette)**:
   - Tỉ lệ khung hình (16:9 hay 9:16).
   - Màu sắc nhận diện (Primary, Secondary, Background, Glass/Shadow).
   - Vị trí safe-zones (tránh nút like/share của TikTok hoặc thanh điều khiển YouTube).
4. **Lớp 4: Âm thanh & Nhịp điệu (Audio Bed & Sound Design)**:
   - Đo BPM của nhạc nền (thường 110-128 BPM).
   - Đánh dấu vị trí SFX khớp với keyframe chuyển động (whoosh, hit, ping, click).
5. **Lớp 5: Voiceover**: Tone giọng, tốc độ đọc (WPM - Words Per Minute).

### Bước 2: Mã hóa thành Style Component trong herk-edit-kit
- Tạo thư mục project mới trong `herk-edit-kit/video-projects/<tên_dự_án>`.
- Viết file `index.html` mô phỏng chính xác layout, font chữ, màu sắc và diễn hoạt bằng GSAP Timeline.
- Sử dụng font Việt hóa nhúng nội bộ (`BeVietnamPro-Bold.ttf`, `Montserrat-Bold.ttf`) để chống méo chữ có dấu tiếng Việt.

### Bước 3: Đồng bộ Multitrack & Khớp nhịp (Beat-Sync)
- Sinh voiceover tiếng Việt qua VieNeu-TTS Trúc Ly:
  ```python
  from vieneu import Vieneu
  vieneu = Vieneu()
  audio = vieneu.infer(script_text, voice="Trúc Ly")
  vieneu.save(audio, "voice.wav")
  ```
- Đo thời lượng chính xác của từng câu bằng `wave.open()`.
- Cân chỉnh nhịp chuyển cảnh `T1`, `T2`, `T3` trên timeline GSAP dựa trên độ dài audio thực tế.

### Bước 4: Kiểm tra Preflight & Render
- Chạy kiểm tra quy chuẩn:
  ```bash
  npx hyperframes lint
  ```
- Render video hoàn thiện:
  ```bash
  npx hyperframes render --output renders/<ten_video>.mp4
  ```
- Trích xuất ảnh lưới đối soát 2x2 bằng FFmpeg để kiểm tra chất lượng trước khi bàn giao.
