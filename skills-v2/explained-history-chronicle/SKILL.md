---
name: explained-history-chronicle
description: Video giải thích lịch sử dài (15–30 phút) theo phong cách "biên niên sử trên giấy" (kiểu "Chiến tranh Triều Tiên"). Ngang 16:9, nền giấy xám sáng, chữ Barlow Condensed đen có nền vàng nhấn, nhãn mono đen/trắng/đỏ/xanh gõ từng chữ, ảnh polaroid dán băng keo, bản đồ vệ tinh đen trắng có vùng đỏ + ghim xanh + đường chấm. Mỗi trang 4–6 giây, một ý. Dùng cho lịch sử, chiến tranh, địa chính trị cần nhịp nhanh và nhiều mốc.
---

# explained-history-chronicle

Trích từ video film Chiến tranh Triều Tiên (Google Drive, 30:39): 1920×1080, 24 fps (dựng ở 30 fps), 1838,8 s (30:39), −14,0 LUFS, giọng đọc liền mạch (không có đoạn lặng ≥0,5 s ở ngưỡng −35 dB; 37 đoạn ≥0,3 s ở ngưỡng −40 dB). Khác `explained-history-dossier` (nền tối, 5–6 trang, ảnh đen trắng có hạt): chronicle là **nền sáng, chữ lớn, nhịp dày, ước tính hàng trăm trang (~350 trang nếu 5 s/trang)**.
Tham chiếu: `reference/hc-sheet_01..05.jpg` (1 khung / 20 s), `hc-first60.jpg` (60 giây đầu, 1 khung / 2 s: cho thấy nhịp trang và cách chữ hiện), `hc-typewriter-map.jpg` (vùng đỏ nhạt dần + nhãn gõ chữ, 4 khung/s), `hc30` (polaroid + số), `hc90` (tài liệu + nhãn đen + số lớn), `hc170` / `hc330` (câu hỏi giữa trang), `hc230` (bản đồ + ghim), `hc520` (tiêu đề trái + polaroid phải + nhãn đen), `hc1000` (polaroid ảnh minh hoạ AI, chừa trống nửa trái), `template-snapshot.jpg`.

## Cấu trúc câu chuyện (rút từ video mẫu)
1. **Hook bằng một cảnh cụ thể**: ngày + địa điểm + số người ("SÁNG 23-12-1950 · ~7.158 NGƯỜI"), không giới thiệu chung chung.
2. **Bối cảnh bằng bản đồ**: thế giới → khu vực → vùng đỏ; mốc năm (1910, 1945, 1948) xen trang giấy.
3. **Câu hỏi dẫn dắt** giữa trang trắng: "ĐƯỜNG CHIA ĐÔI TỪ ĐÂU RA?", "CẢ HAI ĐỀU MUỐN ĐÁNH".
4. **Nhân vật và quyết định**: chân dung cắt viền trắng + thẻ ghi chú kem trích lời.
5. **Diễn biến theo bản đồ**: mỗi mốc ngày = 1 trang bản đồ (ghim + đường chấm + nhãn địa danh), xen trang giấy giải thích bằng số.
6. **Số liệu đau**: một–hai số lớn có nền vàng ("17.500 XE", "91–98 NGHÌN DÂN").
7. **Cái giá, kết cục**: "CÁI GIÁ LÀ BAO NHIÊU?", bản đồ thế giới, rồi hình ảnh nhỏ (chiếc ghế trống, thuyền).
8. **Chốt bằng câu hỏi** hoặc liên hệ (video mẫu kết bằng bản đồ có Việt Nam tô vàng).

Nhịp: **4–6 s mỗi trang, 1 ý, 1 cụm nhấn vàng**. Xen **trang bản đồ (tối) – trang giấy (sáng)** để mắt nghỉ; không để quá 3 trang giấy liên tiếp chỉ có chữ.

## Thông số (đo từ khung hình, 1920×1080)

| Vai trò | Mã |
|---|---|
| Nền giấy | `#E1E1DB`, phủ đa giác mờ (`#D6D6CF` / `#ECECE7`, blur 10–12 px, opacity .5) — không có viền |
| Vàng nhấn (nền chữ, nhãn ngày, số) | `#F3C31B` |
| Mực chữ / nhãn đen | `#0F0F0F` |
| Nhãn trắng / viền polaroid | `#F9F9F9` / `#F9F3F3` |
| Đỏ (nhãn, dấu mộc) | `#D53F27` ; vùng tô trên bản đồ `#990303` rồi giảm còn 50% |
| Xanh (nhãn phe, ghim) | `#3F81BD` |
| Băng keo | `#CFC9BD`, rộng ~150×56 px, xoay −38° đến −40° |
| Thẻ ghi chú | kem `#F1EBCF`, chữ `#2B2A22`, tiêu đề mono có gạch chân |
| Bản đồ | nền `#151515`, đất xám `#636363` (ảnh vệ tinh đen trắng làm mờ), biên giới mảnh trắng, vignette tối ở rìa |

Chữ:
- **Tiêu đề / số**: Barlow Condensed ExtraBold (`assets/fonts/BarlowCondensed-ExtraBold.ttf`), HOA, 110–132 px (tiêu đề), 150–170 px (số lớn), line-height 1.05.
- **Nền vàng cụm nhấn**: `padding: 0 12px`, ôm sát một cụm 1–3 từ; mỗi trang chỉ 1 cụm (đôi khi 2 ở trang số).
- **Nhãn / phụ đề / nguồn**: IBM Plex Mono Bold, HOA, 34 px + giãn chữ 7 px (nhãn lớn), 15–26 px + giãn 2–5 px (nhãn nhỏ / địa danh / chú thích ảnh).
- Cả hai font phủ đủ chữ Việt. Barlow Condensed **không có `→`**: bọc `→` trong `.mono`.

## Thành phần (đã có trong template)
`.tag` (k/w/y/r/b, nền đen/trắng/vàng/đỏ/xanh), `.hl` (nền vàng), `.pol` + `.tp` (polaroid + băng keo + `.cp` chú thích ảnh), `.note` (thẻ kem), `.chk` (danh sách ☒ viền đỏ), `.stamp` (dấu mộc đỏ nghiêng −8°), `.cut` (chân dung cắt viền trắng) + `.cname`, `.lbl` (địa danh trên bản đồ), `.mapbg` + vùng đỏ + ghim + đường chấm, `.bignum`.

Ảnh: polaroid xoay ±1–2°, viền 16 px, bóng nhẹ; chú thích đáy trái nền đen mờ. **Ảnh tạo bằng AI phải ghi "ẢNH MINH HOẠ · TẠO BẰNG AI"** (như video mẫu); ảnh tư liệu ghi nguồn và năm.

## Chuyển động (trang tĩnh, vào bằng 0,3–0,7 s)
- Ảnh polaroid: `x ±160`, `rotation ±5°` → 0, `power3.out`; băng keo `scale 0 → 1` ngay sau.
- Nhãn mono: **gõ từng chữ**, `stagger .045`, trước khi số / tiêu đề vào.
- Tiêu đề, số: `y 34–40 → 0` + mờ dần vào, `power3.out`, 0,5 s; số thứ hai vào sau số thứ nhất 0,9 s.
- Thẻ kem: `y −30`, `rotation 2°` → 0; ô ☒ `scale 0 → 1` (`back.out(2.5)`), `stagger .5` bám lời đọc; dấu mộc `scale 2.2 → 1` (`power4.in`, 0,25 s).
- Bản đồ: nền hiện 0,3 s; vùng đỏ hiện đặc `#990303` rồi giảm xuống opacity .5 trong 1,2 s; ghim rơi từ trên (`back.out`), đường chấm vẽ bằng `mask` + `stroke-dashoffset` (1,4 s `power1.inOut`).
- Chuyển trang: cắt thẳng hoặc mờ ≤ 0,3 s; **không** zoom, parallax hay xoay cả trang.

## Quy trình
1. Chia kịch bản thành trang 4–6 s, mỗi trang ghi sẵn: loại trang (giấy / bản đồ), cụm nhấn vàng, ảnh cần có.
2. Giọng đọc và timing: theo `skills-v2/_shared/PIPELINE.md`; nhạc nền `data-volume` 0.08–0.10, giọng 1.0.
3. Copy `template/index.html` vào project, nhân bản các khối `#p1`…`#p7` (đổi `data-start`, `data-duration`, id duy nhất), bám timing từng trang. Video dài: tách thành nhiều composition ~3 phút rồi ghép.
4. Thay hộp polaroid giữ chỗ bằng ảnh thật; thay `.mapph` bằng ảnh vệ tinh đen trắng (`filter: grayscale(1) blur(6px)`), vẽ lại vùng đỏ theo polygon thật.
5. `hyperframes lint` (0 lỗi) → `snapshot` ở giữa mỗi loại trang → render.

## Không làm
- Không dùng màu ngoài bảng trên; không dùng gradient màu, emoji, icon hoạt hình.
- Không đặt hơn 1 cụm vàng cạnh tranh nhau trong một dòng; không bôi vàng cả câu.
- Không đổi sang dọc 9:16 (preset dọc khác dùng bộ khác).
- Không để chữ trắng trên nền giấy hay chữ đen trên bản đồ: **trang giấy = chữ đen, trang bản đồ = chữ trắng** (cụm vàng luôn chữ đen).
- Không dùng ảnh tạo bằng AI mà không ghi nhãn.

## Chưa có trong template
Template chỉ có 7 trang mẫu (42 s): polaroid + số, bản đồ + ghim, câu hỏi giữa trang, checklist + mộc + thẻ kem, chân dung cắt, hai số lớn, polaroid phải. Chưa có: đồng hồ, thước giá / biểu đồ cột nhỏ, bản đồ thế giới, mẫu nhiều ghim đồng thời, khung phim tư liệu. Bản đồ và chân dung trong template là hình giữ chỗ. Chưa trích lời đọc và nhạc nền của video mẫu; nhịp 4–6 s ước lượng bằng mắt từ 60 giây đầu và các khung 20 s.
