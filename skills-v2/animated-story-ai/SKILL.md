---
name: animated-story-ai
description: Làm video HOẠT HÌNH kể chuyện dài (5–15 phút) bằng nhân vật 3D do AI tạo, kiểu "Mario Wakes Up HUGE… What Did Bowser Do to Him?". Không phải motion graphics và không dựng hình bằng HyperFrames. Quy trình gồm sổ nhân vật (khối prompt cố định), kịch bản theo chương, danh sách shot 2 giây, tạo ảnh khóa rồi ảnh→video, ghép bằng HyperFrames. Dùng khi cần nhân vật diễn xuất, có phản diện, hài, hậu quả leo thang.
---

# animated-story-ai

Khác các skill `explained-*` (HyperFrames vẽ chữ, biểu đồ, bản đồ bằng HTML): ở đây **hình do mô hình AI tạo** (ảnh khóa → clip ngắn), HyperFrames chỉ **ghép clip + giọng + nhạc + phụ đề**.

## Nguồn phân tích và độ tin cậy
- Clip mẫu: `video-reference/mario-animation-ai.mp4` (68,2 s, bản nén của file anh gửi). Đây là **phần mở đầu** của video YouTube "Mario Wakes Up HUGE... What Did Bowser Do to Him?! 😱 Super Mario Odyssey Story" (kênh Mario Galaxy; tiêu đề lấy từ trang công khai của YouTube).
- **Em không xem được bản YouTube đầy đủ**: YouTube chặn tải từ máy chủ ("Sign in to confirm you're not a bot"). Mọi thứ ghi dưới đây về cấu trúc dài là **suy ra từ 68 s đầu + tiêu đề**, ghi rõ là "ĐỀ XUẤT" khi không đo được.
- Chưa nhận dạng lời thoại/giọng đọc, chưa phân tích nhạc nền (không có công cụ nhận dạng giọng): chưa biết video mẫu có lời thuyết minh hay chỉ nhạc + hiệu ứng.

## Đo được từ clip mẫu
| Mục | Giá trị |
|---|---|
| Khung | 1280×720, 16:9, 30 fps, HEVC |
| Âm thanh | −15,1 LUFS, không có đoạn lặng ≥0,3 s (ngưỡng −35 dB) |
| Nhịp cắt | 34 điểm cắt trong 68,2 s (ngưỡng cảnh 0,3); khoảng cách đa số **2,0 s ± 0,1** ⇒ mỗi shot ≈ 2 s |
| Phong cách | 3D hoạt hình điện ảnh: da/vải dạng đất sét, sáng ấm, rim light, độ sâu trường ảnh nông, màu bão hòa, mặt nhân vật rất lớn trong khung |
| Dấu hiệu công cụ | ngôi sao 4 cánh nhỏ ở góc phải dưới nhiều khung: dấu hiệu của công cụ Google (Gemini). Em chỉ **suy ra** từ dấu này |
| Lỗi AI thấy được | chữ phía sau cửa kính bị lật ngược ("GULRG"); chữ trên vật chính (lọ "BODY EXPANSION POWDER", biển "FREE PIZZA & BURGERS", áp phích "GRAND RACE") lại đúng |

Ảnh tham chiếu: `reference/am-sheet-2s.jpg` (1 khung / 2 s, đọc từ trái qua phải, trên xuống dưới), `am3` áp phích + hai nhân vật, `am9` đường chạy, `am13` Bowser cận mặt, `am22` Bowser + lọ bột, `am36` Luigi nghi ngờ + biển có logo Bowser, `am47` Bowser đầu bếp + pizza, `am66` Mario cầm burger.

## Câu chuyện 68 s đầu (đo từng shot, xem `worked-example-68s.md`)
1. **0–6 s Mục tiêu**: Mario & Luigi trước áp phích "GRAND RACE" (wide → medium → hai người cận).
2. **6–12 s Hành động**: hai người chạy trên đường đua sân vận động (3 shot di chuyển ngang).
3. **12–28 s Phản diện (người xem biết, nhân vật chưa biết)**: Bowser trong hang theo dõi màn hình, cầm lọ "BODY EXPANSION POWDER", cười.
4. **28–40 s Mồi nhử**: hai người gặp tiệm "FREE PIZZA & BURGERS"; Mario mừng, Luigi nhìn biển có biểu tượng Bowser.
5. **40–58 s Bẫy**: Bowser đội mũ đầu bếp phục vụ; cận pizza, bột tím rắc xuống.
6. **58–68 s Tiêu thụ**: Mario ăn pizza rồi cầm burger khổng lồ. Hậu quả ("thức dậy to lớn") **nằm ngoài 68 s**, suy ra từ tiêu đề.

## Quy tắc kể chuyện (quan sát, rồi diễn giải)
1. **Mỉa mai kịch tính**: cảnh phản diện đặt TRƯỚC khi nhân vật chính rơi vào bẫy, người xem lo thay.
2. **Đạo cụ có nhãn đọc được**: mỗi đạo cụ quan trọng có nhãn tiếng Anh ngắn, chữ lớn, ở giữa khung (poster, lọ, biển). Đây là cách video tránh lỗi chữ của AI.
3. **Dấu hiệu ẩn**: biểu tượng Bowser trên biển tiệm = manh mối cho người tinh ý.
4. **Nhân vật đối trọng**: Luigi nghi ngờ (diễn giải từ ánh mắt/khuôn mặt, không có lời thoại trong tay), Mario hồn nhiên.
5. **Độ phủ ba cỡ cảnh**: mỗi địa điểm mở bằng wide, rồi medium/qua vai, rồi cận (mặt hoặc đạo cụ). Dùng **gáy nhân vật chính ở tiền cảnh** để cho thấy phản diện hành động sau lưng họ.
6. **Cắt theo ánh nhìn**, không xoay camera 360° hay zoom dài.

## Cấu trúc video dài (ĐỀ XUẤT — chưa đo)
Video 10 phút ≈ 12 chương × 45–60 s. Mỗi chương lặp một vòng: **mục tiêu nhỏ → phản diện/biến cố → nhân vật chính sa bẫy hoặc xử lý sai → hậu quả leo thang → cliffhanger 1 câu hỏi**. Chương 1 = đúng 68 s mẫu. Tiêu đề (câu hỏi gây tò mò) = lời hứa phải trả ở chương cuối; hậu quả tăng dần (to hơn, khó che giấu hơn), không đảo ngược sớm.
Chi tiết: `templates/script-shotlist-template.md`.

## Quy trình (8 bước)
1. **Brief**: logline 1 câu, thời lượng, ngôn ngữ giọng đọc, nhân vật.
2. **Sổ nhân vật** (`templates/characters-sample.md`): mỗi nhân vật 1 khối prompt cố định + ảnh nhân vật 3 góc (trước, 3/4, nghiêng). **Dán nguyên văn khối này vào mọi prompt**, không viết lại.
3. **Kịch bản theo chương** + lời đọc từng câu; 1 câu ≈ 2–4 shot.
4. **Danh sách shot** (bảng): cỡ cảnh, góc, hành động, cảm xúc, nhãn chữ, câu thoại, độ dài (mặc định 2 s).
5. **Ảnh khóa** cho từng shot (ảnh mở đầu). Duyệt ảnh trước khi tạo clip vì ảnh rẻ hơn clip.
6. **Ảnh → video** (mỗi clip bám đúng động tác của shot; ghi "giữ nguyên nhân vật, không đổi trang phục, không thêm chữ").
7. **QA từng clip**: nhận diện nhân vật đúng, tay, nhãn chữ, hướng nhìn, màu/đạo cụ liên tục (lọ tím vẫn tím).
8. **Ghép bằng HyperFrames** (`templates/assemble/index.html`): clip video tắt tiếng nối trên một track; giọng đọc 1.0, nhạc nền 0.08–0.10, SFX có track riêng; phụ đề từ khóa nếu cần. Render 1920×1080, 30 fps. Quy tắc âm thanh theo `_shared/PIPELINE.md` và `AGENTS.md`.

**Đã kiểm chứng ghép clip**: composition 6 s gồm 2 thẻ `<video muted>` nối tiếp trên 1 track + 1 thẻ `<audio>`, `hyperframes lint` 0 lỗi/0 cảnh báo, render 1920×1080 30 fps có âm thanh (52 s render). Chưa thử composition 10 phút, chia theo chương (một composition mỗi chương) rồi nối bằng FFmpeg concat.

## Khối lượng công việc (ước tính, không phải số đo)
10 phút ÷ 2 s ≈ 300 shot. Nếu một nửa số lần tạo bị loại thì cần ≈ 450–600 lần tạo clip. Nên làm theo chương và duyệt ảnh khóa trước.

## Không làm
- Không viết lại mô tả nhân vật mỗi shot (nhân vật sẽ đổi mặt/trang phục).
- Không để chữ ở nền hoặc sau kính; chữ quan trọng đặt trên đạo cụ lớn giữa khung hoặc thêm bằng HyperFrames sau.
- Không cắt dài hơn ≈ 4 s trên một cú máy tĩnh; nhịp mẫu là 2 s.
- Không đổi hướng nhân vật giữa hai shot liền nhau (giữ nguyên vị trí trái/phải của hai nhân vật trong cùng một địa điểm).
- Không đưa hậu quả lớn vào chương 1 (video mẫu chỉ cho thấy nguyên nhân).

## Bản quyền
Mario, Luigi, Bowser là nhân vật của Nintendo; video mẫu là sản phẩm hâm mộ. Đăng, kiếm tiền hoặc dựng series có thể gặp khiếu nại bản quyền; việc đó anh tự cân nhắc. Phương pháp ở đây dùng được cho nhân vật gốc; khuyến nghị tạo nhân vật riêng nếu làm kênh lâu dài. `characters-sample.md` giữ ba nhân vật mẫu để học cách mô tả.
