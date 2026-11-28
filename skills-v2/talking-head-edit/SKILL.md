# talking-head-edit — dựng video người nói (quay thật) bằng skill của herk-edit-kit

Dùng khi người dùng **có video tự quay** (nói trước máy, podcast, livestream) và muốn ra video đã dựng: bỏ khoảng lặng, cắt câu nói vấp / quay lại, phụ đề, card chữ-số, cảnh chèn (B-roll), nhạc nền, SFX.
- Dọc 9:16 (Reels / Shorts / TikTok, quảng cáo ngắn) → skill `short-form-edit` của herk.
- Ngang 16:9 dài (YouTube) → skill `edit-video` của herk.

Herk đã có đầy đủ quy trình này. vidskill chỉ thay các dịch vụ trả phí:

| Bước | Herk gốc | Ở đây |
|---|---|---|
| Chép lời từng từ | ElevenLabs Scribe (trả phí) | `python skills-v2/_shared/scripts/transcribe_vi.py <video>` (faster-whisper, chạy trên máy, tiếng Việt) |
| Cảnh chèn AI (B-roll) | Kie.ai | `muse.py` qua muse2api (xem `_shared/HERK-KIT.md`) |
| Nhạc | Suno qua Kie | `mix_audio.py --no-music` cho giọng, nhạc CC BY theo hồi hoặc nhạc của người dùng |
| Giọng đọc | không cần (người thật nói) | — |

## Quy trình
1. Tạo `<ROOT>/herk-edit-kit/video-projects/<slug>/`, chép video gốc vào `assets/raw.mp4` (giữ nguyên bản gốc).
2. Chép lời: `<ROOT>/VieNeu-TTS/.venv/Scripts/python.exe skills-v2/_shared/scripts/transcribe_vi.py assets/raw.mp4` → `assets/raw.json` (định dạng herk: `words[{text,start,end}]`). Máy có GPU NVIDIA: mặc định `large-v3`. Chỉ có CPU: `--model medium` (chậm) hoặc `small` (nhanh, sai chính tả nhiều hơn). Đọc lại toàn bộ lời, sửa chữ sai trong JSON trước khi làm phụ đề; không sửa thời gian.
3. Đọc và làm theo skill của herk **từ bước sau chép lời**, chạy trong thư mục `<ROOT>/herk-edit-kit`:
   - `.agents/skills/cut-silences/SKILL.md` → bỏ khoảng lặng (`--apply` để cắt video).
   - `.agents/skills/cut-mistakes/SKILL.md` → tìm câu vấp / quay lại, xem từng đề xuất rồi cắt.
   - Dọc: `.agents/skills/short-form-edit/SKILL.md` (mở đầu 3 giây, open loop, phụ đề, cảnh chèn, nhạc, SFX). Ngang: `.agents/skills/edit-video/SKILL.md`.
   - Card chữ/số: `style-library` (`02-kallaway` hợp video nói trước máy, `01-vox-explainer` cho đoạn giải thích); xem bằng `cards.py list --style kallaway`.
4. Cảnh chèn AI: viết prompt theo `BROLL-VIDEO.md` (chỉ SFX, không nhạc, không giọng) → `muse.py batch ...` → chèn theo kế hoạch của skill herk.
5. Render vào `<ROOT>/output/`, chạy `qa_video.py` (bỏ qua mục nghỉ giữa câu: người thật nói, đã được cut-silences xử lý).

## Lưu ý
- **Cần ffmpeg 7 trở lên**: bước cắt của herk dùng cú pháp `-/filter_complex`; ffmpeg 6 báo `Unrecognized option '/filter_complex'`. `winget install Gyan.FFmpeg` (setup_all.bat) cài bản mới.
- Không bao giờ ghi đè video gốc. Mọi lần cắt sau đều tính lại thời gian từ EDL (herk đã làm sẵn).
- Phụ đề tiếng Việt: dùng font có dấu (Be Vietnam Pro, Inter); kiểm tra snapshot có đủ dấu.
- Đã kiểm thử: chép lời 30 s tiếng Việt (model small, CPU, 14 s) → `cut-silences` cắt video đúng (30,02 s → 29,24 s) → `cut-mistakes` sinh danh sách đề xuất.
