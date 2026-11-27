# 🎬 HƯỚNG DẪN ĐIỀU PHỐI HỆ THỐNG EXPLAINED VIDEO (AGENTS.MD)

> **Dành cho mọi AI Agent (Antigravity, Gemini, Claude Code, Cursor)**:
> Đây là bản đồ kiến trúc và quy chuẩn sản xuất video giải thích tự động (Explained Video Engine) chạy **100% Offline Local** trên máy tính. Bắt buộc đọc kỹ file này khi bắt đầu bất kỳ tác vụ tạo video hoặc preset mới.

---

## 🗺️ 1. BẢN ĐỒ CẤU TRÚC THƯ MỤC HỆ THỐNG

Thư mục làm việc chính của người dùng là `vidskill`. Hai hệ sinh thái phụ trợ (`herk-edit-kit` và `VieNeu-TTS`) nằm ở thư mục cha cùng cấp:

```
F:\2.sources\d.explainedvideo\
├── vidskill\                           <-- [WORKSHOP & KHO PRESETS] Thư mục làm việc hiện tại
│   ├── AGENTS.md                       <-- File này (Chỉ dẫn AI)
│   ├── skills-v2\                      <-- Kho Preset Templates chuẩn hóa
│   │   ├── explained-fdi-timeline\     (Dọc 9:16 · Lịch sử kinh tế / chính sách theo năm)
│   │   ├── explained-history-dossier\  (Ngang 16:9 · Hồ sơ tư liệu lịch sử / chiến dịch)
│   │   ├── explained-history-chronicle\ (Ngang 16:9 · Lịch sử dài, nền giấy sáng, bản đồ + Polaroid)
│   │   ├── explained-data-finance\     (Dọc 9:16 · Báo cáo tài chính / cổ phiếu PNJ)
│   │   ├── explained-geo-map\          (Dọc 9:16 · Địa chính trị / bản đồ Singapore)
│   │   ├── explained-gym-business\     (Dọc 9:16 · Mô hình kinh doanh / hòa vốn Gym)
│   │   ├── explained-investigative\    (Dọc 9:16 · Phóng sự điều tra nợ / tòa án Vietjet)
│   │   ├── motion-graphics\            (Chuyển động đồ họa ngắn)
│   │   ├── cinematic-movie\            (Phim ngắn kể chuyện)
│   │   └── _shared\                    (Fonts Việt hóa, Audio SFX, gsap.min.js)
│   └── video-reference\                <-- Kho video gốc .mp4 & ảnh bóc tách từng khung hình
│
├── herk-edit-kit\                      <-- [RENDER ENGINE] Hệ thống dựng & xuất video HyperFrames
│   ├── video-projects\                 <-- Nơi khởi tạo mã nguồn dự án mới (index.html, assets/)
│   ├── renders\                        <-- Nơi chứa video MP4 hoàn thiện sau khi render
│   ├── node_modules\                   <-- Thư viện HyperFrames, GSAP
│   └── package.json
│
└── VieNeu-TTS\                         <-- [AI VOICE ENGINE] Thuyết minh tiếng Việt Offline
    ├── .venv\Scripts\python.exe        <-- Trình thông dịch Python chứa PyTorch & VieNeu-TTS
    └── src\vieneu\                     <-- Thư viện sinh giọng đọc (25 giọng chuẩn 3 miền)
```

---

## ⚡ 2. CÚ PHÁP RA LỆNH CỦA NGƯỜI DÙNG & BẢNG ÁNH XẠ PRESET

Khi người dùng yêu cầu làm video mới theo cấu trúc:
> *"Dùng preset [Tên Preset] làm video giải thích về [Chủ đề], [thời lượng], [giọng đọc]..."*

Agent tra cứu bảng ánh xạ sau để chọn đúng template gốc trong `skills-v2/`:

| Tên gọi người dùng | Thư mục Template trong `skills-v2/` | Tỉ lệ | Video mẫu tham chiếu | Màu sắc / Visual nhận diện |
|---|---|---|---|---|
| **FDI Timeline** / Kinh tế vĩ mô | `explained-fdi-timeline` | **9:16** (1080×1920) | `video-reference/fdi vn.mp4` | Nền `#0D0B0C`, Lime `#CBF73E`, Thước TimelineRunner đỉnh, Thùng hàng xếp tầng, Sơ đồ phát sáng, Mộc đỏ |
| **History Dossier** / Lịch sử | `explained-history-dossier` | **16:9** (1920×1080) | `video-reference/lichsu-vietnam.mp4` | Nền rêu `#121411`, Kem `#F2E6D2`, Đỏ `#B4322C`, Giấy kraft, Mũi tên vẽ tay, Thẻ mốc ngày, Lưới đơn vị |
| **History Chronicle** / Lịch sử dài (Triều Tiên) | `explained-history-chronicle` | **16:9** (1920×1080) | Video mẫu 30:39 (Google Drive, chưa nằm trong `video-reference/`) | Nền giấy sáng `#E1E1DB`, nhấn vàng `#F3C31B`, mực `#0F0F0F`, chữ Barlow Condensed, nhãn mono gõ từng chữ, Polaroid + băng keo, Bản đồ vệ tinh đen trắng + vùng đỏ + ghim xanh |
| **Data Finance** / PNJ Tài chính | `explained-data-finance` | **9:16** (1080×1920) | `video-reference/pnj-tai-chinh.mp4` | Nền tối `#080F0D`, Lime `#ADF400`, Vàng `#FEC73C`, Đỏ `#E70A23`, Biểu đồ đường/cột, Thẻ báo khoanh đỏ, Con dấu |
| **Geo Map** / Singapore / Bản đồ | `explained-geo-map` | **9:16** (1080×1920) | `video-reference/singapore.mp4` | Bản đồ phẳng màu + ảnh vệ tinh, Vàng nhấn `#FFD708` (vòng tròn, năm, nhãn, đường tàu), Nhãn pop-up, Phụ đề từ khóa vàng |
| **Gym Business** / Điểm hòa vốn | `explained-gym-business` | **9:16** (1080×1920) | `video-reference/gym center.mp4` | Nền ảnh vệ tinh tối (`#0E1114`), Lime `#CBF73E`, Đỏ `#C5202B`, Bảng giá viền trắng, Thẻ báo highlight lime, Biểu đồ cột, Chú giải bản đồ |
| **Investigative** / Vietjet Điều tra | `explained-investigative` | **9:16** (1080×1920) | `video-reference/vietjet airline.mp4` | Nền xám than `#252525` có lưới, Lime `#CCF53C`, Đỏ `#E3202E`, Nhãn giấy kraft + lime xé mép, Băng giấy rách, Dây lime nét đứt, Dấu mộc |
| **Juno UGC** / Thời trang quảng cáo | `../juno-ugc-toolkit` | **9:16** (1080×1920) | Tham khảo UGC 30s | Sáng thời trang, PIP cận cảnh vải, Phụ đề Liquid-Glass, CTA giỏ hàng |

---

## 🛠️ 3. QUY TRÌNH THỰC THI 4 BƯỚC (STANDARD OPERATING PROCEDURE)

Mọi video đều phải thực hiện tuần tự qua 4 bước khép kín sau:

### Bước 1: Khởi tạo dự án & Soạn kịch bản (Script Breakdown)
1. Tạo thư mục dự án mới trong:
   `F:\2.sources\d.explainedvideo\herk-edit-kit\video-projects\<ten-du-an>\`
2. Tạo thư mục `assets/` bên trong và copy tài nguyên dùng chung từ `vidskill/skills-v2/_shared/`:
   - `assets/gsap.min.js`
   - `assets/*.wav` (SFX: whoosh, click, ping, hit)
   - `assets/fonts/` (Inter.ttf, BeVietnamPro-*.ttf, Roboto.ttf, IBMPlexMono-*.ttf, BarlowCondensed-*.ttf)
   - Nhạc nền `assets/bg_music.wav`
3. Phân chia kịch bản thành các phân đoạn (Beats/Scenes) tương ứng với từng mốc nội dung (mỗi phân đoạn từ 5 – 8 giây).

### Bước 2: Sinh giọng đọc AI & Đo thời lượng thực tế (Audio Sync)
Chạy script Python bằng trình thông dịch của VieNeu-TTS:
- **Executable**: `F:\2.sources\d.explainedvideo\VieNeu-TTS\.venv\Scripts\python.exe`
- **Cách gọi model**:
  ```python
  import sys, wave, os
  sys.path.insert(0, r"F:\2.sources\d.explainedvideo\VieNeu-TTS\src")
  from vieneu import Vieneu

  vieneu = Vieneu()
  # Các giọng chuẩn: "Thùy Dung" (Nữ miền Nam tin tức), "Minh Đức" (Nam tin tức), "Trúc Ly" (Nữ miền Nam trẻ trung)
  audio = vieneu.infer(text, voice="Thùy Dung")
  vieneu.save(audio, r"assets/vo_s1.wav")
  vieneu.close()
  ```
- **Bắt buộc đo thời lượng chính xác** từng file `.wav` bằng `wave.open()` để làm căn cứ thiết lập keyframes và duration trên timeline GSAP.

### Bước 3: Dựng mã HTML/GSAP (`index.html`) & Phụ đề Karaoke
1. Lấy khung mẫu từ `vidskill/skills-v2/<preset>/template/index.html`.
2. Tạo file cấu hình `hyperframes.json` (ghi rõ `width`, `height`, `fps: 30`, `duration`).
3. **Quy tắc Audio**:
   - Nhạc nền `bg_music.wav` **bắt buộc giảm âm lượng (ducking)**: `data-volume="0.08"` đến `0.10` để giọng nói luôn nổi bật.
   - Voiceover gán `data-volume="1.0"`.
   - Mỗi clip âm thanh / hình ảnh chồng lớp **phải có `data-track-index` riêng biệt**, không được trùng nhau.
4. **Quy tắc Phụ đề chân trang (Captions)**:
   - Đối với video dọc (9:16): Triển khai dạng **Karaoke Word-by-Word Runner**. Từng từ `<span class="w">` nhảy sáng màu Lime `#CBF73E` kết hợp phóng to `scale: 1.18x` theo đúng thời gian nói thực tế; không hiển thị huy hiệu model thừa.
   - Đối với video ngang (16:9): không dùng Karaoke; theo từng skill (dossier: nhãn ngày + dòng nguồn mỗi trang; chronicle: nhãn mono gõ từng chữ + cụm nhấn nền vàng).

### Bước 4: Kiểm tra Linter & Render Video
1. **Kiểm tra chuẩn HyperFrames** (phải đạt 0 errors):
   ```bash
   cd "F:\2.sources\d.explainedvideo\herk-edit-kit"
   npx hyperframes lint video-projects/<ten-du-an>
   ```
2. **Kết xuất video hoàn thiện**:
   ```bash
   cd "F:\2.sources\d.explainedvideo\herk-edit-kit"
   npx hyperframes render video-projects/<ten-du-an> --output renders/<ten-video>.mp4
   ```
3. **Trích xuất ảnh kiểm tra**: Dùng FFmpeg trích xuất lưới 2×2 (4 phân cảnh) để đối soát chất lượng trước khi bàn giao.

---

## 🚫 4. NGUYÊN TẮC CỐT LÕI (DO'S & DON'TS)

- **TUÂN THỦ PRESET GỐC**: Làm theo template có sẵn trong `skills-v2/` và đối chiếu ảnh trong `reference/`. Không tự ý vẽ lại layout, không đổi bảng màu hoặc font chữ ngoài quy định.
- **TỈ LỆ KHUNG HÌNH BẤT DI BẤT DỊCH**:
  + `explained-history-dossier`, `explained-history-chronicle`: Bắt buộc ngang **16:9** (1920×1080).
  + Tất cả các preset kinh tế, tài chính, bản đồ, UGC khác: Bắt buộc dọc **9:16** (1080×1920).
- **KHÔNG CHÈN TẠP ÂM / BADGE THỪA**: Không hiển thị các nhãn kỹ thuật như "VieNeu-TTS :: Thùy Dung" lên khung hình trừ khi người dùng yêu cầu rõ ràng.
- **FONT CHỮ NỘI BỘ**: Chỉ sử dụng font local đã nhúng trong `assets/fonts/` (Inter, BeVietnamPro, Roboto, IBM Plex Mono, Barlow Condensed) để chống lỗi vỡ chữ có dấu tiếng Việt khi render headless.
