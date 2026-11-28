# Dùng herk-edit-kit cho đúng (đọc trước khi làm video)

`herk-edit-kit` (github.com/nateherkai/herk-edit-kit) không chỉ là bộ render. Các video mẫu đẹp trong đó đến từ những phần sau; preset cũ của `vidskill` chỉ dùng phần render.

| Phần trong herk | Dùng để | Cách dùng trong vidskill |
|---|---|---|
| `style-library/01-vox-explainer` (106 card) | Video giải thích cắt dán kiểu Vox | Preset `explained-vox-cards` + `cards.py` |
| `style-library/02-kallaway` (300 card) | Card chữ/số cho video YouTuber, nói trước máy | `cards.py list --style kallaway` (chưa có preset) |
| `.agents/skills/motion-showreel` | Showreel / brand reel 10–30 s cắt theo nhịp nhạc 120–130 BPM | Dùng skill của herk trực tiếp; ảnh/clip tạo bằng Muse thay Kie |
| `.agents/skills/short-form-edit`, `edit-video`, `cut-silences`, `cut-mistakes` | Dựng video người nói quay thật: bỏ lặng, cắt câu vấp, phụ đề, card, cảnh chèn | Preset `talking-head-edit` (chép lời tiếng Việt trên máy bằng `transcribe_vi.py` thay ElevenLabs) |
| `.agents/skills/make-a-video`, `hyperframes` (house-style, patterns) | Quy trình phỏng vấn → storyboard → dựng; luật thiết kế chuyển động | Đọc `house-style.md` khi làm cảnh mới |
| `style-templates/` | Template nền (dark graph paper, glass popout) | Mở `DESIGN.md` từng cái |

Ví dụ hoàn chỉnh: `herk-edit-kit/examples/showcase/youtube-showreel.mp4` (15 s, motion-showreel).

## Đổi nhà cung cấp so với herk gốc
| Herk gốc dùng | Ở đây dùng | Ghi chú |
|---|---|---|
| Kie.ai (ảnh lookdev, clip Kling, nhạc Suno) | **Muse qua muse2api** (`muse.py`) | Ảnh/clip: viết prompt như herk (`motion-showreel/references`), lưu file vào `assets/img/` rồi đưa vào `images`/`assets.json` bằng `"file"`. Không gọi `kie.mjs`. |
| ElevenLabs (giọng, SFX, chép lời Scribe) | **VieNeu-TTS** (giọng), **transcribe_vi.py** (chép lời), `_shared/audio` + SFX từ clip Muse | `build_voiceover.py` |
| Suno qua Kie (nhạc) | `mix_audio.py` (nhạc CC BY theo 4 hồi) hoặc nhạc Muse/của người dùng | `--music hook=file.mp3` |


## Cài
`setup_all.bat` đã clone herk và `npm install`. Lần đầu render, HyperFrames tự tải Chrome headless. Kiểm tra: `cd <ROOT>/herk-edit-kit && npx hyperframes lint video-projects/<slug>`.

## Muse
**Gọi Muse bằng `skills-v2/_shared/scripts/muse.py` qua muse2api** (chạy trên máy hoặc mạng nội bộ, pool tài khoản Muse, không tính tiền theo lượt). Cấu hình trong `<repo>/.env` (mẫu `.env.example`, không commit): `MUSE_HOST`, `MUSE_PORT` (mặc định 18610), `MUSE_API_KEY` (khóa MUSE2API_KEY), `MUSE_IMAGE_MODEL` (mặc định `muse-image`), `MUSE_VIDEO_MODEL` (để trống nếu không cần).
- Kiểm tra kết nối: `python muse.py check`.
- Ảnh: `python muse.py image "<prompt>" -o assets/img/p3.jpg --size 16:9`. Dùng cho ô ảnh không tìm được ảnh thật; slot `source` ghi "ẢNH MINH HOẠ · TẠO BẰNG AI".
- Clip (cách làm B, cảnh chèn của video người nói): `python muse.py batch output/<video>-broll-prompts.txt output/<video>-broll --kind video --duration 6` → `01.mp4`, `02.mp4`… đúng số prompt, bỏ qua file đã có (chạy lại để tiếp tục). Thời lượng muse2api: 5/6/8/10 s (số khác tự làm tròn lên). Sau đó `broll.py ingest <dự-án> output/<video>-broll`.
- Không gọi `kie.mjs` của herk.
