# Clip video AI (B-roll) cho video tài liệu

Cứ ~25–30 giây chèn 1 clip 5–8 giây do video-AI (Veo, Kling, Runway, Sora… tạo) thay cho phần hình động của trang đó. Áp dụng cho preset ngang 16:9 (`explained-history-chronicle`, `explained-history-dossier`).

## Quy trình
1. Làm giọng đọc trước: `build_voiceover.py` → `assets/timing.json`.
2. Lập kế hoạch vị trí clip:
   `python skills-v2/_shared/scripts/broll.py plan <thư-mục-dự-án> --theme <màu>`
   Ra `assets/broll_plan.json` (số thứ tự, thời điểm bắt đầu, độ dài, lời đọc tương ứng) và `broll_snippets.html` (thẻ `<video>` + GSAP fade 0,3 s, đã đặt đúng `data-start`/`data-duration`, track 5).
3. Viết file prompt `<ROOT>/output/<ten-video>-broll-prompts.txt` theo quy tắc dưới, **đúng số lượng và thứ tự slot trong plan**.
4. Kiểm tra: `python skills-v2/_shared/scripts/broll.py check <thư-mục-dự-án> <file-prompt.txt> --theme <màu>` → phải `OK`.
5. Người dùng chạy batch rồi đưa **đường dẫn một thư mục** chứa các clip, tên có số thứ tự prompt ở đầu (`1.mp4`, `01_havana.mp4`, `clip-02.mp4`… đều được). AI tự làm hết:
   `python skills-v2/_shared/scripts/broll.py ingest <thư-mục-dự-án> <thư-mục-clip>`
   Lệnh này ghép clip theo số, chuẩn hóa về 1920×1080 30 fps không tiếng (vào `assets/broll/NN.mp4`), đo độ dài thật, rút slot nếu clip ngắn hơn, báo clip thiếu/thừa và ghi lại `broll_snippets.html` chỉ gồm clip có file. AI dán snippet vào `index.html` (thẻ `<video>` vào `#root` sau các khối trang, dòng GSAP vào timeline), lint, render bản cuối. Slot thiếu clip thì trang giữ đồ họa, không dán thẻ video (render sẽ lỗi). Bản A (chưa có clip) vẫn render trước để xem nhịp.
6. Nói rõ cho người dùng bảng slot (số, giây bắt đầu, độ dài, lời đọc) để họ chèn đúng chỗ.

## Định dạng file prompt (để import batch)
- Mỗi prompt **một đoạn văn duy nhất**, bắt đầu bằng `1. `, `2. `… liền mạch, **cách nhau một dòng trống**, không tiêu đề, không ghi chú xen giữa.
- Viết **tiếng Anh** (các model video hiểu tốt nhất).
- Cấu trúc một prompt: `N. <cảnh cụ thể: bối cảnh + chủ thể + hành động + ánh sáng + chuyển động máy>. Sound design: <SFX của cảnh>. <KHỐI STYLE CHUNG>`.
- **Khối style chung** (cơ bản + màu phim + kỹ thuật + câu loại trừ) lấy bằng `python broll.py style --theme <màu>` và dán **nguyên văn, giống hệt ở mọi prompt** — đó là thứ giữ các clip đồng nhất. Nguồn: `explained-history-chronicle/broll-style.json` (mỗi bảng màu `paper`, `sepia-archive`, `ocean-chart` có tông màu phim riêng khớp với bảng màu đồ họa).

## Cách viết phần cảnh (≥ 300 ký tự mỗi prompt)
- **Âm thanh: chỉ SFX, không nhạc, không giọng.** Mỗi prompt có một câu riêng của cảnh bắt đầu bằng `Sound design:` liệt kê SFX/âm nền cụ thể thấy được trên hình (bước chân, gió, sóng, động cơ, vải, vật va chạm…). Câu đó **không** được nhắc music/voice/dialogue (checker bắt lỗi). Khối style chung đã có dòng `Audio:` (chỉ SFX tự nhiên) và câu loại trừ âm thanh (no music, no voice-over, no narration, no dialogue, no singing). Giọng đọc và nhạc nền luôn do pipeline thêm, không do video-AI.
- Khi `ingest`, tiếng của clip được tách thành `assets/broll/NN.wav` (fade vào/ra), chèn bằng thẻ `<audio>` riêng volume 0,35 để không át giọng đọc; video luôn `muted`. Model nào không sinh được tiếng thì clip chỉ có hình (lệnh báo rõ), SFX chung của template vẫn dùng bình thường.
- Hợp nội dung lời đọc ở slot đó: minh họa bối cảnh/không khí, không minh họa con số hay chữ.
- Một cảnh liền, một chuyển động máy chậm (push-in, pan, tracking, cố định). Không cắt cảnh, không whip-pan.
- Chủ thể quay từ xa, từ phía sau, bóng đổ hoặc chỉ cảnh tay/đồ vật; **không** mặt cận cảnh người nhận diện được, không nhân vật có thật, không biểu tượng/logo/cờ có chữ.
- Không bắt model vẽ chữ, số, bản đồ có chữ, biểu đồ — phần đồ họa do template lo.
- Ánh sáng tự nhiên, chất liệu thật (tường bong sơn, ẩm, bụi). Thời kỳ lịch sử thì ghi rõ trang phục/phương tiện đúng thời.
- Chọn slot rơi vào trang hình ảnh/bản đồ; tránh đè lên trang có con số chủ chốt (nếu cần, dịch `--first` hoặc sửa tay `start` trong plan rồi ghi lại).

Ví dụ hoàn chỉnh: `explained-history-chronicle/examples/cuba-broll-prompts.txt` (3 clip cho video Cuba 75 s).
