# Prompt tạo ảnh cho skill chronicle

Video mẫu dùng ảnh đen trắng kiểu tư liệu (ảnh thật năm 1950 và ảnh minh hoạ do AI tạo, có nhãn "ẢNH MINH HOẠ · TẠO BẰNG AI"). **Thiếu ảnh thì video trông khác mẫu ngay**, vì template chỉ có hộp xám giữ chỗ. Làm ảnh trước khi dựng.

## Quy tắc
- Mọi ảnh đen trắng, tỉ lệ ngang ~5:4 cho polaroid (mẫu 862×688 trong khung 1920×1080), hoặc 16:9 cho nền bản đồ.
- Ảnh tư liệu thật: ghi nguồn và năm ở chú thích (`.cp`). Ảnh AI: chú thích bắt buộc "ẢNH MINH HOẠ · TẠO BẰNG AI".
- Đặt ảnh vào `assets/img/<tên>.jpg`, rồi thay `<div class="im">…</div>` bằng:
  ```html
  <div class="im"><img src="assets/img/p1.jpg" alt=""><div class="cp mono">CHÚ THÍCH</div></div>
  ```
  và thêm vào CSS: `.pol .im img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.15)}` và `.pol .im:before{display:none}` để bỏ chữ giữ chỗ.
- Không đặt chữ trong ảnh AI (AI hay viết sai chữ). Chữ nào cần có thì thêm bằng HTML.

## Khối STYLE (dán đầu prompt ảnh polaroid)
```
black and white archival press photograph, 1950s, 35mm film grain, high contrast, slightly faded blacks, soft vignette, documentary realism, shallow depth of field, no color, no text, no watermark
```

## Ví dụ prompt theo loại trang (thay phần trong ngoặc)
| Loại | Prompt |
|---|---|
| Đám đông, sự kiện | `[STYLE], crowd of refugees and soldiers on the deck of a large cargo ship, wide shot, overcast sky, people carrying bundles` |
| Phòng họp | `[STYLE], delegates seated around a large round wooden conference table in a formal hall with tall windows, one empty leather chair in the foreground` |
| Hành quân | `[STYLE], long column of soldiers in heavy winter coats marching along a snowy mountain ridge, wide landscape` |
| Chân dung | `[STYLE], head-and-shoulders portrait of [mô tả: ví dụ a middle-aged man in a military uniform, mustache], plain background, facing slightly left` (sau đó cắt nền, viền trắng 4 px, xem `.cut`) |

## Bản đồ nền (trang bản đồ)
Mẫu dùng ảnh địa hình vệ tinh đen trắng, bị làm mờ nhẹ, đất xám trung bình (~`#636363`) trên nền gần đen (`#151515`), có vignette, đường biên trắng mảnh (~1,5 px, 45–55% độ đục).
- Prompt gợi ý: `dark grayscale satellite relief map of [khu vực], top-down, mountains and coastlines, low light, blurred, no labels, no text`.
- Hoặc ảnh địa hình thật (nguồn công khai, ghi nguồn).
- Phóng to để vùng đất chiếm 40–60% khung, bố trí vùng đất bên trái hoặc giữa, biển đen ở một phía.
- Template hiện dùng nền địa hình sinh bằng SVG (`feTurbulence`) làm giữ chỗ; thay bằng `<image href="assets/img/map.jpg">` bọc `clip-path` hoặc phủ nguyên khung khi có ảnh.
- Vùng tô đỏ `#990303` đặt trên ảnh bản đồ, chuyển từ đặc sang 50% độ đục.

## Chiều cao phần chữ trên ảnh
Nhãn trong khung ảnh (`.cp`) nằm dưới trái, nền `rgba(15,15,15,.85)`, chữ trắng, Plex Mono 15 px, giãn chữ 2 px.
