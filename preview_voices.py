"""Liệt kê giọng VieNeu-TTS và cho nghe thử để chọn.

Chạy bằng python của VieNeu-TTS (xem preview_voices.bat):
  python preview_voices.py            # menu tương tác: liệt kê, nghe thử, chọn
  python preview_voices.py --list     # chỉ liệt kê
  python preview_voices.py --all      # sinh file mẫu cho mọi giọng
  python preview_voices.py --voice "Thùy Dung" --text "Xin chào"
Kết quả: voice_samples/<giọng>.wav, giọng đã chọn ghi vào voice_choice.txt
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "VieNeu-TTS", "src"))

DEFAULT_TEXT = "Xin chào, đây là giọng đọc thuyết minh dùng cho video giải thích của bạn."
OUT_DIR = os.path.join(HERE, "voice_samples")


def slug(name):
    return re.sub(r"[^\w\-]+", "_", name, flags=re.UNICODE)


def play(path):
    try:
        if sys.platform.startswith("win"):
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME)
        elif sys.platform == "darwin":
            os.system(f'afplay "{path}"')
        else:
            os.system(f'(aplay -q "{path}" || paplay "{path}") 2>/dev/null')
    except Exception as e:
        print(f"  (không phát được tự động: {e}) Mở file: {path}")


def synth(tts, voice_id, text):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, slug(voice_id) + ".wav")
    audio = tts.infer(text, voice=voice_id)
    tts.save(audio, path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--voice")
    ap.add_argument("--text", default=DEFAULT_TEXT)
    ap.add_argument("--no-play", action="store_true")
    a = ap.parse_args()

    from vieneu import Vieneu

    tts = Vieneu()
    try:
        voices = tts.list_preset_voices()  # [(mô tả, id)]
        print("\nDanh sách giọng đọc:")
        for i, (desc, vid) in enumerate(voices, 1):
            print(f"  {i:2d}. {vid}  -  {desc}")
        if a.list:
            return

        if a.voice or a.all:
            targets = [v for v in voices if a.all or a.voice in (v[1], v[0])]
            if not targets:
                sys.exit(f"Không có giọng '{a.voice}'.")
            for desc, vid in targets:
                p = synth(tts, vid, a.text)
                print(f"-> {p}")
                if not a.no_play and not a.all:
                    play(p)
            return

        print("\nNhập số để nghe thử, 't' đổi câu thử, 'c <số>' để CHỌN giọng, 'q' thoát.")
        text = DEFAULT_TEXT
        while True:
            cmd = input("> ").strip()
            if cmd in ("q", "quit", ""):
                break
            if cmd == "t":
                text = input("Câu thử: ").strip() or DEFAULT_TEXT
            elif cmd.startswith("c "):
                idx = int(cmd[2:]) - 1
                vid = voices[idx][1]
                with open(os.path.join(HERE, "voice_choice.txt"), "w", encoding="utf-8") as f:
                    f.write(vid)
                print(f"Đã chọn giọng: {vid} (lưu trong voice_choice.txt)")
                break
            elif cmd.isdigit() and 1 <= int(cmd) <= len(voices):
                vid = voices[int(cmd) - 1][1]
                print(f"Đang sinh giọng {vid}...")
                play(synth(tts, vid, text))
            else:
                print("Lệnh không hợp lệ.")
    finally:
        tts.close()


if __name__ == "__main__":
    main()
