#!/usr/bin/env python3
"""Chép lời tiếng Việt CHẠY TRÊN MÁY (faster-whisper), xuất transcript từng từ đúng định dạng herk-edit-kit.

Thay cho ElevenLabs Scribe trong các skill dựng video người nói của herk
(edit-video, cut-silences, cut-mistakes, short-form-edit).

  python transcribe_vi.py <video-hoặc-audio> [--model large-v3|medium|small] [--lang vi] [--device auto|cpu|cuda]
  → <cùng-tên>.json  {"text", "audio_duration_secs", "language", "words":[{"text","start","end","type":"word"}]}

Lần đầu tải model (large-v3 ~3 GB, small ~0,5 GB) vào cache Hugging Face; sau đó chạy offline.
Máy không có GPU: dùng --model small hoặc medium (large-v3 trên CPU rất chậm).
Cài: <ROOT>/VieNeu-TTS/.venv/Scripts/python.exe -m pip install faster-whisper  (setup_all.bat đã làm)
"""
import argparse
import json
import os
import subprocess
import sys


def probe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--lang", default="vi")
    ap.add_argument("--device", default="auto")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Chưa cài faster-whisper: <python> -m pip install faster-whisper")

    device = a.device
    if device == "auto":
        try:
            import ctranslate2
            device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
        except Exception:
            device = "cpu"
    compute = "float16" if device == "cuda" else "int8"
    print(f"model {a.model} trên {device} ({compute})...", flush=True)
    model = WhisperModel(a.model, device=device, compute_type=compute)
    # tự giải mã bằng ffmpeg: tránh lỗi lệch phiên bản PyAV của faster-whisper
    import numpy as np
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", a.media, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    segments, info = model.transcribe(audio, language=a.lang, word_timestamps=True, vad_filter=False,
                                      condition_on_previous_text=False)
    words, texts = [], []
    for seg in segments:
        texts.append(seg.text.strip())
        for w in seg.words or []:
            t = w.word.strip()
            if t:
                words.append({"text": t, "start": round(w.start, 3), "end": round(w.end, 3), "type": "word"})
        print(f"  {seg.start:7.2f}  {seg.text.strip()[:70]}", flush=True)
    if not words:
        sys.exit("Không nhận được từ nào (file câm hoặc sai ngôn ngữ).")
    out = a.out or os.path.splitext(a.media)[0] + ".json"
    dur = probe_duration(a.media) or words[-1]["end"]
    json.dump({"text": " ".join(texts), "audio_duration_secs": round(dur, 3), "language": info.language,
               "words": words}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"-> {out}  {len(words)} từ, {dur:.1f}s")


if __name__ == "__main__":
    main()
