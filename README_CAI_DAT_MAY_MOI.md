# 🚀 HƯỚNG DẪN CÀI ĐẶT EXPLAINED VIDEO ENGINE CHO MÁY MỚI (PHƯƠNG ÁN B)

Phương án B sử dụng script tự động clone mã nguồn từ GitHub và thiết lập toàn bộ môi trường cho cả 2 hệ thống cốt lõi:
1. **`herk-edit-kit`**: Hệ thống Motion Graphics & Video Editing (HyperFrames, GSAP, 400+ motion cards).
2. **`VieNeu-TTS`**: Hệ thống Giọng đọc AI Tiếng Việt Offline.
3. **`explained-video-maker` Skill**: Kỹ năng chuyên gia điều phối sản xuất video giải thích cho Antigravity & Claude Code.

---

## 📋 1. Chuẩn Bị Trước Khi Chạy (Trên Máy Mới)

Đảm bảo máy tính mới đã cài 4 công cụ nền tảng sau:
- [x] **Git**: Tải tại [git-scm.com](https://git-scm.com/)
- [x] **Node.js (LTS >= 22.x)**: Tải tại [nodejs.org](https://nodejs.org/)
- [x] **Python (3.10 - 3.12)**: Tải tại [python.org](https://www.python.org/) *(Lưu ý: Tích chọn "Add python.exe to PATH" khi cài)*
- [x] **FFmpeg**: Mở PowerShell gõ `winget install Gyan.FFmpeg` hoặc tải từ [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) rồi thêm vào PATH.

---

## ⚡ 2. Cài Đặt Tự Động (Chỉ 1 Click)

1. Mở thư mục gốc của repo.
2. Nhấp đúp chuột vào file:
   👉 **`setup_all.bat`**

Script sẽ tự động thực hiện:
- Kiểm tra các công cụ hệ thống (Git, Node, Python, FFmpeg).
- `git clone https://github.com/nateherkai/herk-edit-kit.git` và chạy `npm install`.
- `git clone https://github.com/pnnbao97/VieNeu-TTS.git`, tạo virtualenv `.venv` và cài đặt PyTorch / VieNeu-TTS.
- Nạp sẵn model AI offline (nếu có thư mục `models_offline`) hoặc tự động tải về khi chạy lần đầu.
- Tự động đăng ký Skill `explained-video-maker` vào hệ thống AI Antigravity / Claude Code.

---

## 🎥 3. Tự Động Phân Tích & Làm Ra Skill / Preset Từ Video Mẫu

Nếu anh có một video giải thích mẫu (ví dụ: phong cách Biocodex, Greenland, hay bất kỳ video nào trên YouTube/TikTok):
1. **Gửi file video hoặc đường link** cho Antigravity.
2. Em sẽ tự động:
   - Dùng FFmpeg bóc tách khung hình (keyframes), lời thuyết minh, và nhịp độ (BPM).
   - Nhận diện các hiệu ứng chữ động (kinetic text), hiệu ứng chuyển cảnh (whip pan, zoom, push in), và bảng màu.
   - Viết mã code tái hiện lại thành một **Style Template** trong `herk-edit-kit/style-templates/`.
   - Đóng gói thành một **Preset** hoặc **Skill** riêng để từ đó về sau anh chỉ cần nhập nội dung là video sẽ tự động xuất ra đúng phong cách đó!

## Chọn giọng đọc

Chạy `preview_voices.bat`: liệt kê toàn bộ giọng, gõ số để nghe thử, `c <số>` để chọn (lưu vào `voice_choice.txt`).
