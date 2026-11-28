#!/usr/bin/env python3
"""Sinh giọng đọc từng câu, ghép thành vo.wav với khoảng nghỉ đủ dài, xuất timing.json.

Dùng (bằng python của VieNeu-TTS, hoặc python bất kỳ nếu các file câu đã có sẵn):
  python build_voiceover.py <thư-mục-dự-án> script.json

script.json:
  {
    "voice": "<ID giọng, xem preview_voices.bat>",
    "pauses": {"sentence": 0.7, "scene": 1.3, "question": 1.5},   # tùy chọn
    "lead": 0.5, "tail": 1.5,                                     # tùy chọn
    "sentences": [
      {"text": "Câu 1.", "pause": "sentence"},
      {"text": "Câu cuối của cảnh.", "pause": "scene"},
      {"text": "Câu hỏi dẫn dắt?", "pause": "question"}
    ]
  }
`pause` = khoảng lặng SAU câu đó. Câu cuối cảnh dùng "scene" để chuyển cảnh không bị dồn.

Kết quả (trong <thư-mục-dự-án>/assets/):
  vo_NN.wav  từng câu | vo.wav  bản ghép | timing.json  thời điểm bắt đầu/kết thúc mỗi câu
Thời lượng cảnh trên timeline = end của câu cuối cảnh + khoảng nghỉ (đã có trong "scene_end").
"""
import json
import os
import sys
import wave

DEFAULT_PAUSES = {"sentence": 0.7, "scene": 1.3, "question": 1.5}


def synth(texts, voice, paths):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", "..", ".."))
    sys.path.insert(0, os.path.join(root, "VieNeu-TTS", "src"))
    from vieneu import Vieneu

    tts = Vieneu()
    try:
        for text, path in zip(texts, paths):
            if os.path.exists(path):
                continue
            tts.save(tts.infer(text, voice=voice), path)
    finally:
        tts.close()


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    proj, script_path = sys.argv[1], sys.argv[2]
    cfg = json.load(open(script_path, encoding="utf-8"))
    pauses = {**DEFAULT_PAUSES, **cfg.get("pauses", {})}
    lead, tail = float(cfg.get("lead", 0.5)), float(cfg.get("tail", 1.5))
    items = cfg["sentences"]
    assets = os.path.join(proj, "assets")
    os.makedirs(assets, exist_ok=True)
    paths = [os.path.join(assets, f"vo_{i + 1:02d}.wav") for i in range(len(items))]

    if not all(os.path.exists(p) for p in paths):
        synth([s["text"] for s in items], cfg.get("voice"), paths)

    params, frames, timing = None, [], []
    t = lead
    out_frames = []

    def silence(sec):
        n = int(round(sec * params.framerate))
        return b"\x00" * (n * params.nchannels * params.sampwidth)

    for i, (item, path) in enumerate(zip(items, paths)):
        with wave.open(path, "rb") as w:
            p = w.getparams()
            data = w.readframes(w.getnframes())
        if params is None:
            params = p
            out_frames.append(silence(lead))
        elif (p.nchannels, p.sampwidth, p.framerate) != (params.nchannels, params.sampwidth, params.framerate):
            sys.exit(f"{path}: định dạng WAV khác các câu trước")
        dur = p.nframes / p.framerate
        kind = item.get("pause", "sentence")
        gap = pauses[kind] if i < len(items) - 1 else tail
        out_frames += [data, silence(gap)]
        timing.append({
            "i": i + 1, "text": item["text"], "start": round(t, 3), "end": round(t + dur, 3),
            "pause_after": gap, "kind": kind, "scene_end": round(t + dur + gap, 3),
        })
        t += dur + gap

    out = os.path.join(assets, "vo.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(params.nchannels)
        w.setsampwidth(params.sampwidth)
        w.setframerate(params.framerate)
        w.writeframes(b"".join(out_frames))
    json.dump({"total": round(t, 3), "sentences": timing},
              open(os.path.join(assets, "timing.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"{out}  tổng {t:.2f}s, {len(items)} câu")
    for x in timing:
        print(f"  {x['i']:02d} {x['start']:7.2f}-{x['end']:7.2f}  nghỉ {x['pause_after']:.1f}s ({x['kind']})")


if __name__ == "__main__":
    main()
