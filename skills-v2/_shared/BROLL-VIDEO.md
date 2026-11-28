# Clip video AI (B-roll) cho video tài liệu

Cứ ~25–30 giây chèn 1 clip 5–8 giây do video-AI (Veo, Kling, Runway, Sora… tạo) thay cho phần hình động của trang đó. Áp dụng cho preset ngang 16:9 (`explained-history-chronicle`, `explained-history-dossier`).

## Quy trình
1. Làm giọng đọc trước: `build_voiceover.py` → `assets/timing.json`.
2. Lập kế hoạch vị trí clip:
   `python skills-v2/_shared/scripts/broll.py plan <thư-mục-dự-án> --theme <màu>`
   Ra `assets/broll_plan.json` (số thứ tự, thời điểm bắt đầu, độ dài, lời đọc tương ứng) và `broll_snippets.html` (thẻ `<video>` + GSAP fade 0,3 s, đã đặt đúng `data-start`/`data-duration`, track 5).
3. Viết file prompt `<ROOT>/output/<ten-video>-broll-prompts.txt` theo quy tắc dưới, **đúng số lượng và thứ tự slot trong plan**.
4. Kiểm tra: `python skills-v2/_shared/scripts/broll.py check <thư-mục-dự-án> <file-prompt.txt> --theme <màu>` → phải `OK`.
5. Người dùng chạy batch, lưu video thành `assets/broll/01.mp4`, `02.mp4`… (số = số thứ tự prompt). Dán `broll_snippets.html` vào `index.html`, lint, render. Chưa có file clip thì đừng dán thẻ video (render sẽ lỗi).
6. Nói rõ cho người dùng bảng slot (số, giây bắt đầu, độ dài, lời đọc) để họ chèn đúng chỗ.

## Định dạng file prompt (để import batch)
- Mỗi prompt **một đoạn văn duy nhất**, bắt đầu bằng `1. `, `2. `… liền mạch, **cách nhau một dòng trống**, không tiêu đề, không ghi chú xen giữa.
- Viết **tiếng Anh** (các model video hiểu tốt nhất).
- Cấu trúc một prompt: `N. <cảnh cụ thể: bối cảnh + chủ thể + hành động + ánh sáng + chuyển động máy> <KHỐI STYLE CHUNG>`.
- **Khối style chung** (cơ bản + màu phim + kỹ thuật + câu loại trừ) lấy bằng `python broll.py style --theme <màu>` và dán **nguyên văn, giống hệt ở mọi prompt** — đó là thứ giữ các clip đồng nhất. Nguồn: `explained-history-chronicle/broll-style.json` (mỗi bảng màu `paper`, `sepia-archive`, `ocean-chart` có tông màu phim riêng khớp với bảng màu đồ họa).

## Cách viết phần cảnh (≥ 300 ký tự mỗi prompt)
- Hợp nội dung lời đọc ở slot đó: minh họa bối cảnh/không khí, không minh họa con số hay chữ.
- Một cảnh liền, một chuyển động máy chậm (push-in, pan, tracking, cố định). Không cắt cảnh, không whip-pan.
- Chủ thể quay từ xa, từ phía sau, bóng đổ hoặc chỉ cảnh tay/đồ vật; **không** mặt cận cảnh người nhận diện được, không nhân vật có thật, không biểu tượng/logo/cờ có chữ.
- Không bắt model vẽ chữ, số, bản đồ có chữ, biểu đồ — phần đồ họa do template lo.
- Ánh sáng tự nhiên, chất liệu thật (tường bong sơn, ẩm, bụi). Thời kỳ lịch sử thì ghi rõ trang phục/phương tiện đúng thời.
- Chọn slot rơi vào trang hình ảnh/bản đồ; tránh đè lên trang có con số chủ chốt (nếu cần, dịch `--first` hoặc sửa tay `start` trong plan rồi ghi lại).

Ví dụ hoàn chỉnh: `explained-history-chronicle/examples/cuba-broll-prompts.txt` (3 clip cho video Cuba 75 s).
