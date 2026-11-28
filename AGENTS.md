# 🎬 HƯỚNG DẪN ĐIỀU PHỐI HỆ THỐNG EXPLAINED VIDEO (AGENTS.MD)

> **Dành cho mọi AI Agent (Antigravity, Gemini, Claude Code, Cursor)**:
> Đây là bản đồ kiến trúc và quy chuẩn sản xuất video giải thích tự động (Explained Video Engine) chạy **100% Offline Local** trên máy tính. Bắt buộc đọc kỹ file này khi bắt đầu bất kỳ tác vụ tạo video hoặc preset mới.

---

## 🚀 0. KHỞI ĐỘNG TRÊN MÁY MỚI (AI ĐỌC TRƯỚC KHI LÀM BẤT CỨ GÌ)

`<ROOT>` = **thư mục cha của repo này** (nơi chứa `vidskill/`). Không có đường dẫn cố định; tự xác định bằng `cd ..` từ thư mục repo.

1. Kiểm tra môi trường: tồn tại `<ROOT>/herk-edit-kit/node_modules` và `<ROOT>/VieNeu-TTS/.venv`?
2. Nếu **thiếu** → chạy `setup_all.bat` ở gốc repo (Windows). Script tự cài Git/Node/Python/FFmpeg qua winget nếu thiếu, clone `herk-edit-kit` + `VieNeu-TTS` vào `<ROOT>`, `npm install`, tạo `.venv`, cài PyTorch + VieNeu-TTS, đăng ký skill. Lần đầu có thể mất 10–20 phút và tải model giọng đọc. Nếu vừa cài công cụ mới mà lệnh chưa nhận, mở lại terminal rồi chạy lại script (chạy lại an toàn).
3. Tạo dự án từ preset. **Windows (mặc định, không cần Git Bash):** `skills-v2\_shared\scripts\new-project.bat <preset> <slug> [--theme=<màu>]`. macOS/Linux/Git Bash: lệnh `bash` dưới đây. Cả hai làm giống nhau:
   `bash skills-v2/_shared/scripts/new-project.sh <preset> <slug> [--theme=<màu>]` (mặc định tìm `herk-edit-kit` ở `<ROOT>`; video xuất ra `<ROOT>/output/`)
   Script copy template, font, SFX, `gsap.min.js` và `meta.json`/`hyperframes.json` mẫu vào `video-projects/<slug>`.
4. Giọng đọc: dùng `<ROOT>/VieNeu-TTS/.venv/Scripts/python.exe` (Linux/macOS: `.venv/bin/python`).
5. **Chọn giọng**: chạy `preview_voices.bat` (hoặc `<ROOT>/VieNeu-TTS/.venv/Scripts/python.exe preview_voices.py`) để liệt kê các giọng, gõ số để nghe thử, `c <số>` để chọn. Giọng chọn lưu ở `voice_choice.txt`. Nếu người dùng chưa nêu giọng, AI phải đọc `voice_choice.txt` nếu có; nếu không thì hướng dẫn người dùng chạy script này (hoặc `--list`) trước khi sinh giọng. Tên giọng dùng trong `infer(voice=...)` phải đúng ID mà script liệt kê.

### Bước 0 — HỎI NHANH TRƯỚC KHI LÀM (bắt buộc)

Khi người dùng yêu cầu làm video (hoặc mở repo và nói "bắt đầu", "làm video", "xin chào"…), AI **không được tự chọn hộ**. Gửi **đúng một tin nhắn** theo mẫu dưới, chỉ giữ lại các mục người dùng **chưa** nêu, rồi chờ trả lời. Người dùng đã nêu đủ thì bỏ qua bước này. Mục nào họ không trả lời thì dùng mặc định ghi trong ngoặc và nói rõ đã dùng mặc định.

> Em làm video theo các lựa chọn sau, anh chọn giúp (trả lời kiểu "A, chronicle, sepia-archive, Thùy Dung, 3 phút"):
>
> **1. Cách làm hình** (mặc định A)
> - **A — Đồ họa động + ảnh/bản đồ thật:** dựng từ template; em tự tìm ảnh tư liệu tự do (Wikimedia, NASA), vẽ bản đồ từ ranh giới thật, trộn nhạc theo hồi (mở – cao trào – kết), ra video luôn kèm danh sách asset (`ASSETS.md`) để anh thay ảnh nào muốn.
> - **B — Đồ họa + cảnh phim AI:** như A, thêm khoảng cứ 25–30 giây một clip 5–8 giây do video-AI tạo (có SFX, không nhạc, không giọng). Em giao file prompt đánh số 1. 2. 3. để anh chạy batch; anh lưu clip vào một thư mục (tên bắt đầu bằng số thứ tự) và đưa đường dẫn thư mục đó, em tự ghép đúng vị trí, chuẩn hóa clip và render bản cuối. Em render bản A trước để xem nhịp. Chỉ dùng cho preset ngang 16:9.
>
> **2. Preset** (xem danh sách ở mục 2; gợi ý theo chủ đề: lịch sử dài → `explained-history-chronicle`, hồ sơ tư liệu → `explained-history-dossier`, kinh tế vĩ mô → `explained-fdi-timeline`, tài chính doanh nghiệp → `explained-data-finance`, bản đồ/địa chính trị → `explained-geo-map`, điều tra → `explained-investigative`, kinh doanh → `explained-gym-business`)
>
> **3. Màu** (chỉ preset có `themes/`; hiện là `explained-history-chronicle`, mặc định `paper`): `paper` giấy xám như video mẫu · `sepia-archive` ố vàng hoài cổ · `ocean-chart` xanh lạnh hải đồ. Preset khác dùng màu cố định của preset.
>
> **4. Giọng đọc** (mặc định giọng trong `voice_choice.txt`, chưa có thì chạy `preview_voices.bat` để nghe thử)
>
> **5. Thời lượng và nguồn kịch bản** (anh dán kịch bản, hoặc em tự viết từ nguồn anh đưa)

Sau khi có câu trả lời: nhắc lại một dòng tóm tắt lựa chọn, rồi làm đủ các bước ở mục 3. Chọn **B** thì thêm bước clip AI (`skills-v2/_shared/BROLL-VIDEO.md`) và giao bảng slot kèm file prompt trong `<ROOT>/output/`. Chỉ hỏi lại khi thiếu thông tin không có mặc định (chủ đề, kịch bản).

### Mẫu câu lệnh người dùng (copy/paste)

> Đọc `AGENTS.md`. Cách làm **<A hoặc B>**. Dùng preset **<tên preset>** làm video giải thích về **<chủ đề>**, thời lượng **<~N giây/phút>**, giọng **<tên giọng>**, màu **<tên bảng màu, nếu preset có>**. Kịch bản: <dán kịch bản hoặc "tự viết từ nguồn …">. Xuất ra `<ROOT>/output/<ten-video>.mp4`.

AI phải: (a) tra bảng ở mục 2 để chọn preset và tỉ lệ khung; (b) đọc `skills-v2/<preset>/SKILL.md` + `template/index.html` + ảnh trong thư mục reference của preset; (c) chạy đủ 4 bước ở mục 3; (d) lint 0 errors trước khi render; (e) bàn giao đường dẫn MP4 + ảnh lưới kiểm tra 2×2. Nếu người dùng muốn thêm clip phim do video-AI tạo (khoảng 25–30 s một clip 5–8 s, preset ngang): làm theo `skills-v2/_shared/BROLL-VIDEO.md`, giao file `<ROOT>/output/<ten-video>-broll-prompts.txt` (mỗi prompt một đoạn, đánh số 1. 2. …) cùng bảng slot (số, giây bắt đầu, độ dài). Preset có thư mục `themes/` (hiện: `explained-history-chronicle` với `paper`, `sepia-archive`, `ocean-chart`) thì cho người dùng chọn màu và tạo dự án bằng `--theme=<tên>`. Kết quả luôn nằm ở `<ROOT>/output/`, không để trong `herk-edit-kit`. Nếu thiếu thông tin (chủ đề, thời lượng, giọng, màu), chỉ hỏi những mục đó rồi làm tiếp.

---

## 🗺️ 1. BẢN ĐỒ CẤU TRÚC THƯ MỤC HỆ THỐNG

Thư mục làm việc chính của người dùng là `vidskill`. Hai hệ sinh thái phụ trợ (`herk-edit-kit` và `VieNeu-TTS`) nằm ở thư mục cha cùng cấp:

```
<ROOT>/   (thư mục CHA của repo vidskill)
├── vidskill\                           <-- [WORKSHOP & KHO PRESETS] Thư mục làm việc hiện tại
│   ├── AGENTS.md                       <-- File này (Chỉ dẫn AI)
│   ├── skills-v2\                      <-- Kho Preset Templates chuẩn hóa
│   │   ├── explained-fdi-timeline\     (Dọc 9:16 · Lịch sử kinh tế / chính sách theo năm)
│   │   ├── explained-history-dossier\  (Ngang 16:9 · Hồ sơ tư liệu lịch sử / chiến dịch)
│   │   ├── explained-history-chronicle\ (Ngang 16:9 · Lịch sử dài, nền giấy sáng, bản đồ + Polaroid)
│   │   ├── animated-story-ai\         (Ngang 16:9 · Hoạt hình 3D nhân vật AI, truyện dài: sổ nhân vật, kịch bản, shot list)
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
│   ├── node_modules\                   <-- Thư viện HyperFrames, GSAP
│   └── package.json
│
├── output\                             <-- [KẾT QUẢ] Toàn bộ MP4, ảnh QA, VERIFY.md (cùng cấp vidskill)
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
| **History Chronicle** / Lịch sử dài (Triều Tiên) | `explained-history-chronicle` | **16:9** (1920×1080) | `video-reference/trieu-tien-chronicle.mp4` (bản nén 1280×720 của video 30:39) | Nền giấy sáng `#E1E1DB`, nhấn vàng `#F3C31B`, mực `#0F0F0F`, chữ Barlow Condensed, nhãn mono gõ từng chữ, Polaroid + băng keo, Bản đồ vệ tinh đen trắng + vùng đỏ + ghim xanh |
| **Data Finance** / PNJ Tài chính | `explained-data-finance` | **9:16** (1080×1920) | `video-reference/pnj-tai-chinh.mp4` | Nền tối `#080F0D`, Lime `#ADF400`, Vàng `#FEC73C`, Đỏ `#E70A23`, Biểu đồ đường/cột, Thẻ báo khoanh đỏ, Con dấu |
| **Geo Map** / Singapore / Bản đồ | `explained-geo-map` | **9:16** (1080×1920) | `video-reference/singapore.mp4` | Bản đồ phẳng màu + ảnh vệ tinh, Vàng nhấn `#FFD708` (vòng tròn, năm, nhãn, đường tàu), Nhãn pop-up, Phụ đề từ khóa vàng |
| **Gym Business** / Điểm hòa vốn | `explained-gym-business` | **9:16** (1080×1920) | `video-reference/gym center.mp4` | Nền ảnh vệ tinh tối (`#0E1114`), Lime `#CBF73E`, Đỏ `#C5202B`, Bảng giá viền trắng, Thẻ báo highlight lime, Biểu đồ cột, Chú giải bản đồ |
| **Investigative** / Vietjet Điều tra | `explained-investigative` | **9:16** (1080×1920) | `video-reference/vietjet airline.mp4` | Nền xám than `#252525` có lưới, Lime `#CCF53C`, Đỏ `#E3202E`, Nhãn giấy kraft + lime xé mép, Băng giấy rách, Dây lime nét đứt, Dấu mộc |
| **Animated Story AI** / Hoạt hình nhân vật AI dài | `animated-story-ai` | **16:9** (1920×1080) | `video-reference/mario-animation-ai.mp4` (68 s mở đầu) | Hình do AI tạo (ảnh khóa → clip 2 s), KHÔNG dùng template HTML để vẽ hình; HyperFrames chỉ ghép clip + giọng + nhạc; đọc `SKILL.md` của skill trước khi làm |

---

## 🛠️ 3. QUY TRÌNH THỰC THI 4 BƯỚC (STANDARD OPERATING PROCEDURE)

Mọi video đều phải thực hiện tuần tự qua 4 bước khép kín sau:

### Bước 1: Khởi tạo dự án & Soạn kịch bản (Script Breakdown)
1. Tạo thư mục dự án mới trong:
   `<ROOT>/herk-edit-kit/video-projects/<ten-du-an>/`
2. Tạo thư mục `assets/` bên trong và copy tài nguyên dùng chung từ `vidskill/skills-v2/_shared/`:
   - `assets/gsap.min.js`
   - `assets/*.wav` (SFX: whoosh, click, ping, hit)
   - `assets/fonts/` (Inter.ttf, BeVietnamPro-*.ttf, Roboto.ttf, IBMPlexMono-*.ttf, BarlowCondensed-*.ttf)
   - Nhạc: không copy; `mix_audio.py` tự tải nhạc CC BY theo hồi (xem `skills-v2/_shared/music-library.json`) hoặc dùng file nhạc của người dùng (`--music build=đường/dẫn.mp3`)
   - Ảnh/bản đồ: `fetch_assets.py` theo `assets.json` (xem `skills-v2/_shared/PIPELINE.md` bước 5b)
3. Phân chia kịch bản thành các phân đoạn (Beats/Scenes) tương ứng với từng mốc nội dung (mỗi phân đoạn từ 5 – 8 giây).

### Bước 2: Sinh giọng đọc AI & Đo thời lượng thực tế (Audio Sync)
Chạy script Python bằng trình thông dịch của VieNeu-TTS:
- **Executable**: `<ROOT>/VieNeu-TTS/.venv/Scripts/python.exe`
- **Cách gọi model**:
  ```python
  import sys, wave, os
  sys.path.insert(0, r"<ROOT>/VieNeu-TTS/src")
  from vieneu import Vieneu

  vieneu = Vieneu()
  # Các giọng chuẩn: "Thùy Dung" (Nữ miền Nam tin tức), "Minh Đức" (Nam tin tức), "Trúc Ly" (Nữ miền Nam trẻ trung)
  audio = vieneu.infer(text, voice="Thùy Dung")
  vieneu.save(audio, r"assets/vo_s1.wav")
  vieneu.close()
  ```
- **Dùng `skills-v2/_shared/scripts/build_voiceover.py`** thay vì tự ghép: nó sinh từng câu, ghép `vo.wav` với khoảng nghỉ chuẩn và ghi `assets/timing.json` (thời điểm từng câu) làm căn cứ keyframes/duration trên timeline GSAP. Chi tiết `script.json` ở đầu file script.
- **NHỊP NGHỈ (bắt buộc, không đọc dồn):** giữa câu cùng trang ≥ 0,7 s; câu cuối của trang/chuyển cảnh ≥ 1,3 s; sau câu hỏi dẫn dắt ≥ 1,5 s; đầu bài 0,5 s; cuối bài giữ ≥ 1,5 s. Muốn ngắn hơn thì bớt câu, không bớt nghỉ. Hình mới phải vào xong trước khi câu kế bắt đầu.

### Bước 3: Dựng mã HTML/GSAP (`index.html`) & Phụ đề Karaoke
1. Lấy khung mẫu từ `vidskill/skills-v2/<preset>/template/index.html`.
2. Tạo file cấu hình `hyperframes.json` (ghi rõ `width`, `height`, `fps: 30`, `duration`).
3. **Quy tắc Audio**:
   - **Giọng + nhạc trộn sẵn bằng `skills-v2/_shared/scripts/mix_audio.py`** → một file `assets/mix.wav` (nhạc theo 4 hồi, tự hạ dưới giọng khi có lời, −14 LUFS), gắn bằng một thẻ `<audio id="mix" ... data-volume="1">`. Không dùng một vòng nhạc 30 s cho cả video. Ghi công nhạc (`music_credits.txt`) khi bàn giao.
   - Mỗi clip âm thanh / hình ảnh chồng lớp **phải có `data-track-index` riêng biệt**, không được trùng nhau.
4. **Quy tắc Phụ đề chân trang (Captions)**:
   - Đối với video dọc (9:16): Triển khai dạng **Karaoke Word-by-Word Runner**. Từng từ `<span class="w">` nhảy sáng màu Lime `#CBF73E` kết hợp phóng to `scale: 1.18x` theo đúng thời gian nói thực tế; không hiển thị huy hiệu model thừa.
   - Đối với video ngang (16:9): không dùng Karaoke; theo từng skill (dossier: nhãn ngày + dòng nguồn mỗi trang; chronicle: nhãn mono gõ từng chữ + cụm nhấn nền vàng).

### Bước 4: Kiểm tra Linter & Render Video
1. **Kiểm tra chuẩn HyperFrames** (phải đạt 0 errors):
   ```bash
   cd "<ROOT>/herk-edit-kit"
   npx hyperframes lint video-projects/<ten-du-an>
   ```
2. **Kết xuất video hoàn thiện**:
   ```bash
   cd "<ROOT>/herk-edit-kit"
   npx hyperframes render video-projects/<ten-du-an> --output ../output/<ten-video>.mp4
   ```
3. **Trích xuất ảnh kiểm tra**: Dùng FFmpeg trích xuất lưới 2×2 (4 phân cảnh) vào `<ROOT>/output/<ten-video>-qa.jpg` để đối soát trước khi bàn giao.
4. **Kiểm tra thành phẩm**: `python skills-v2/_shared/scripts/qa_video.py <ROOT>/output/<ten-video>.mp4 --project <thư-mục-dự-án>` phải ĐẠT trước khi bàn giao.

---

## 🚫 4. NGUYÊN TẮC CỐT LÕI (DO'S & DON'TS)

- **TUÂN THỦ PRESET GỐC**: Làm theo template có sẵn trong `skills-v2/` và đối chiếu ảnh trong `skills-v2/<preset>/reference/` (nếu có). Không tự ý vẽ lại layout, không đổi bảng màu hoặc font chữ ngoài quy định.
- **TỈ LỆ KHUNG HÌNH BẤT DI BẤT DỊCH**:
  + `explained-history-dossier`, `explained-history-chronicle`, `animated-story-ai`: Bắt buộc ngang **16:9** (1920×1080).
  + Tất cả các preset kinh tế, tài chính, bản đồ khác: Bắt buộc dọc **9:16** (1080×1920).
- **KHÔNG CHÈN TẠP ÂM / BADGE THỪA**: Không hiển thị các nhãn kỹ thuật như "VieNeu-TTS :: Thùy Dung" lên khung hình trừ khi người dùng yêu cầu rõ ràng.
- **FONT CHỮ NỘI BỘ**: Chỉ sử dụng font local đã nhúng trong `assets/fonts/` (Inter, BeVietnamPro, Roboto, IBM Plex Mono, Barlow Condensed) để chống lỗi vỡ chữ có dấu tiếng Việt khi render headless.
