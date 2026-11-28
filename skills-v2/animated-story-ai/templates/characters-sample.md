# Sổ nhân vật mẫu (phân tích từ clip Mario, dùng làm khuôn)

Mô tả đọc từ khung hình (`reference/am*.jpg`). Viết prompt bằng **tiếng Anh** và dán nguyên khối cho mọi shot (thường giúp nhân vật ổn định hơn tiếng Việt; hãy thử trên công cụ anh dùng).

## Khối PHONG CÁCH (STYLE) — dán đầu mọi prompt
```
stylized 3D animated feature-film look, clay-like soft skin and felt-like fabric textures, subsurface scattering, warm cinematic key light with soft rim light, shallow depth of field, saturated colors, rounded cartoon proportions with large expressive heads, 16:9, high detail, no text artifacts
```

## Khối NEGATIVE — dán cuối mọi prompt (hoặc ô negative nếu có)
```
different outfit, different face, extra fingers, deformed hands, realistic human skin, photo-realistic, mirrored or garbled text, extra logos, watermark, subtitles, blurry
```

## MARIO
```
Mario: cartoon plumber, big round head, large round peach-colored nose, thick dark brown mustache, big blue eyes with thick dark eyebrows, brown hair with sideburns under a bright red cap with a white circle containing a red letter M, red long-sleeve shirt, blue denim overalls with two gold buttons, white gloves, short stout body
```
Biểu cảm thấy trong clip: háo hức (hai nắm tay siết, miệng cười lộ răng), nhắm mắt hạnh phúc chỉ tay, ngạc nhiên mắt tròn.

## LUIGI
```
Luigi: cartoon plumber, taller and thinner than Mario, longer face, large round peach-colored nose, thick dark brown mustache, blue eyes, brown hair under a green cap with a white circle containing a green letter L, green long-sleeve shirt, blue denim overalls with two gold buttons, white gloves
```
Vai trò: nhân vật đối trọng; trong clip quan sát được khuôn mặt nghi ngờ nhìn biển có biểu tượng Bowser.

## BOWSER (hai bộ trang phục)
```
Bowser: huge bipedal koopa king, yellow-orange scaly skin with hexagonal scale texture, cream-colored large muzzle with sharp teeth, two large curved cream horns, flaming red-orange spiky hair and thick red eyebrows, green scaly patches around red-orange eyes, green spiked shell with cream rim, black leather spiked collar and black spiked wristbands with silver studs, clawed hands, heavy menacing but comedic expression
```
Phụ kiện đầu bếp (cảnh tiệm): thêm `wearing a tall white chef hat and a flour-stained white apron`.

## Đạo cụ có nhãn (đọc đúng trong clip)
| Đạo cụ | Nhãn | Ghi chú tạo |
|---|---|---|
| Áp phích | "MUSHROOM KINGDOM GRAND RACE" | chữ cong lớn, vàng cam viền đỏ, có cúp và cờ ca-rô |
| Lọ bột | "BODY EXPANSION POWDER" | lọ thủy tinh nắp kim loại, bột/nhãn tím, nhãn giấy cũ |
| Biển tiệm | "FREE PIZZA & BURGERS" | bảng đèn bóng, chữ kem viền nâu, **biểu tượng Bowser nhỏ ở góc dưới** |
Chỉ 3–4 từ in HOA, chữ lớn, giữa khung, nền tương phản.

## Mẫu prompt ảnh khóa (ví dụ shot 47 s: Bowser đầu bếp đặt pizza trước Mario)
```
[STYLE] [BOWSER + chef hat and apron] leaning over a steel counter placing a round cheesy pepperoni pizza on a metal tray, grinning mischievously, [MARIO] in the right foreground looking at the pizza in awe, mouth open, medium two-shot, eye-level, cozy pizzeria kitchen with brass pans and warm lights, subtle purple glow in the background, [NEGATIVE]
```

## Mẫu prompt ảnh→video (cho cùng shot)
```
Camera: slow push-in. Bowser slides the pizza forward with a sly smile, Mario leans in and gasps. Steam rises from the pizza. Keep both characters identical to the reference image, same outfits, no added text, no new characters. 2 seconds.
```
