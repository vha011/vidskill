# Dùng herk-edit-kit cho đúng (đọc trước khi làm video)

`herk-edit-kit` (github.com/nateherkai/herk-edit-kit) không chỉ là bộ render. Các video mẫu đẹp trong đó đến từ những phần sau; preset cũ của `vidskill` chỉ dùng phần render.

| Phần trong herk | Dùng để | Cách dùng trong vidskill |
|---|---|---|
| `style-library/01-vox-explainer` (106 card) | Video giải thích cắt dán kiểu Vox | Preset `explained-vox-cards` + `cards.py` |
| `style-library/02-kallaway` (300 card) | Card chữ/số cho video YouTuber, nói trước máy | `cards.py list --style kallaway` (chưa có preset) |
| `.agents/skills/motion-showreel` | Showreel / brand reel 10–30 s cắt theo nhịp nhạc 120–130 BPM | Dùng skill của herk trực tiếp; ảnh/clip tạo bằng Muse thay Kie |
| `.agents/skills/short-form-edit` | Dựng clip dọc từ video người nói (cắt, phụ đề, cảnh chèn) | Dùng trực tiếp khi có video quay thật |
| `.agents/skills/make-a-video`, `hyperframes` (house-style, patterns) | Quy trình phỏng vấn → storyboard → dựng; luật thiết kế chuyển động | Đọc `house-style.md` khi làm cảnh mới |
| `style-templates/` | Template nền (dark graph paper, glass popout) | Mở `DESIGN.md` từng cái |

Ví dụ hoàn chỉnh: `herk-edit-kit/examples/showcase/youtube-showreel.mp4` (15 s, motion-showreel).

## Đổi nhà cung cấp so với herk gốc
| Herk gốc dùng | Ở đây dùng | Ghi chú |
|---|---|---|
| Kie.ai (ảnh lookdev, clip Kling, nhạc Suno) | **Muse** (công cụ người dùng cấp) | Ảnh/clip: viết prompt như herk (`motion-showreel/references`), lưu file vào `assets/img/` rồi đưa vào `images`/`assets.json` bằng `"file"`. Không gọi `kie.mjs`. |
| ElevenLabs (giọng, SFX) | **VieNeu-TTS** (giọng), `_shared/audio` + SFX từ clip Muse | `build_voiceover.py` |
| Suno qua Kie (nhạc) | `mix_audio.py` (nhạc CC BY theo 4 hồi) hoặc nhạc Muse/của người dùng | `--music hook=file.mp3` |

**Gọi Muse bằng `skills-v2/_shared/scripts/muse.py`** (khóa API trong `<repo>/.env`, mẫu ở `.env.example`, không commit):
- Ảnh: `python muse.py image "<prompt>" -o assets/img/p3.jpg` (Meta Model API, `muse-image-1.0`). Dùng cho ô ảnh không tìm được ảnh thật; slot `source` ghi "ẢNH MINH HOẠ · TẠO BẰNG AI".
- Clip (cách làm B): `python muse.py batch output/<video>-broll-prompts.txt output/<video>-broll --kind video --duration 6` → in số clip và chi phí ước tính; **hỏi người dùng xác nhận** rồi chạy lại với `--yes`. Sau đó `broll.py ingest <dự-án> output/<video>-broll`. API chính thức của Meta chưa có video nên clip đi qua apimodels (`MUSE_VIDEO_BASE`); nhà cung cấp khác thì đổi biến này và kiểm tra lại định dạng trả về.
- Không gọi `kie.mjs` của herk.

## Cài
`setup_all.bat` đã clone herk và `npm install`. Lần đầu render, HyperFrames tự tải Chrome headless. Kiểm tra: `cd <ROOT>/herk-edit-kit && npx hyperframes lint video-projects/<slug>`.
