#!/usr/bin/env python3
"""Trộn giọng đọc + nhạc nền THEO HỒI (mở - thân - cao trào - kết), nhạc tự hạ khi có lời, chuẩn -14 LUFS.

  python mix_audio.py <thư-mục-dự-án> [--acts hook:0,build:12,climax:62,resolve:88]
                      [--music build=đường/dẫn.mp3] [--pick 0] [--gap 8] [--no-music]

Cần: assets/vo.wav + assets/timing.json (build_voiceover.py), ffmpeg trong PATH.
--acts   : % thời lượng nơi mỗi hồi bắt đầu (mặc định như trên). Có thể ghi theo câu: build:s5 (bắt đầu từ câu 5).
--music  : thay bài cho một vai trò bằng file của bạn (lặp lại được nhiều lần).
--pick   : chọn bài thứ mấy trong danh sách của mỗi vai trò (0,1,2) - đổi để ra màu nhạc khác.
--gap    : nhạc thấp hơn giọng bao nhiêu dB khi KHÔNG có lời (mặc định 8); khi có lời nhạc hạ thêm ~8-9 dB (đo: nhạc nằm ~15 dB dưới giọng, nghỉ thì nhạc nổi lên).
Ra: assets/mix.wav (giọng + nhạc, -14 LUFS, đỉnh -1.5 dBTP), assets/music_credits.txt.
Trong index.html dùng MỘT thẻ: <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="<tổng>" data-track-index="9" data-volume="1">
(bỏ thẻ vo.wav / bg_music riêng; SFX của template giữ nguyên, volume 0.35-0.5).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "music-library.json")
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "vidskill", "music")
ROLES = ["hook", "build", "climax", "resolve"]


def ff(*args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg lỗi:\n" + r.stderr[-1500:])
    return r.stderr


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def track_file(lib, title):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, title + ".mp3")
    if not os.path.exists(path):
        url = lib["base_url"] + urllib.parse.quote(title) + ".mp3"
        print(f"  tải nhạc: {title}")
        req = urllib.request.Request(url, headers={"User-Agent": "vidskill/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            open(path, "wb").write(r.read())
    return path


def loudnorm_2pass(src, dst, target, extra_pre=""):
    pre = (extra_pre + ",") if extra_pre else ""
    out = ff("-i", src, "-af", f"{pre}loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-")
    m = json.loads(out[out.rfind("{"):out.rfind("}") + 1])
    if m["input_i"] in ("-inf", "inf") or float(m["input_i"]) < -70:
        ff("-i", src, "-af", extra_pre or "anull", "-ar", "48000", "-ac", "2", dst)  # câm: không chuẩn hoá được
        return
    ff("-i", src, "-af",
       f"{pre}loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
       f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
       "-ar", "48000", "-ac", "2", dst)


def parse_acts(spec, timing):
    total = timing["total"]
    acts = []
    for part in spec.split(","):
        role, at = part.split(":")
        if role not in ROLES:
            sys.exit(f"Vai trò không hợp lệ: {role} (dùng {', '.join(ROLES)})")
        if at.startswith("s"):
            i = int(at[1:]) - 1
            t = timing["sentences"][i]["start"] - 0.3
        else:
            t = total * float(at) / 100.0
        acts.append((role, max(0.0, t)))
    acts.sort(key=lambda a: a[1])
    acts[0] = (acts[0][0], 0.0)
    return [(r, s, (acts[k + 1][1] if k + 1 < len(acts) else total)) for k, (r, s) in enumerate(acts)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--acts", default="hook:0,build:12,climax:62,resolve:88")
    ap.add_argument("--music", action="append", default=[])
    ap.add_argument("--pick", type=int, default=0)
    ap.add_argument("--gap", type=float, default=8.0)
    ap.add_argument("--no-music", action="store_true")
    a = ap.parse_args()

    assets = os.path.join(a.project, "assets")
    vo = os.path.join(assets, "vo.wav")
    timing = json.load(open(os.path.join(assets, "timing.json"), encoding="utf-8"))
    total = timing["total"]
    tmp = os.path.join(assets, "_mix")
    os.makedirs(tmp, exist_ok=True)

    vo_n = os.path.join(tmp, "vo_n.wav")
    loudnorm_2pass(vo, vo_n, -16)
    out = os.path.join(assets, "mix.wav")
    if a.no_music:
        loudnorm_2pass(vo_n, out, -14)
        print(f"-> {out} (chỉ giọng)")
        return

    lib = json.load(open(LIB, encoding="utf-8"))
    custom = dict(m.split("=", 1) for m in a.music)
    acts = parse_acts(a.acts, timing)
    credits, inputs, filters = [], [], []
    for k, (role, s, e) in enumerate(acts):
        if role in custom:
            src, title = custom[role], os.path.basename(custom[role])
        else:
            names = lib["roles"][role]["tracks"]
            title = names[a.pick % len(names)]
            src = track_file(lib, title)
            line = f'"{title}" Kevin MacLeod (incompetech.com). Licensed under {lib["license"]}'
            if line not in credits:
                credits.append(line)
        seg = os.path.join(tmp, f"act{k}.wav")
        off = lib.get("start", {}).get(title, 0)
        length = (e - s) + 2.0  # chồng 2 s để crossfade sang hồi sau
        # lặp bài nếu ngắn hơn hồi, chuẩn hoá độ lớn để các hồi không lệch nhau
        loudnorm_2pass(src, seg, -16 - a.gap,
                       extra_pre=f"aloop=loop=-1:size=2e9,atrim=start={off}:duration={length:.2f},asetpts=PTS-STARTPTS")
        fin = 0.4 if k == 0 else 1.5
        fo_start = max(0.0, length - (2.0 if k + 1 < len(acts) else 2.5))
        inputs += ["-i", seg]
        filters.append(f"[{k}:a]afade=t=in:d={fin},afade=t=out:st={fo_start:.2f}:d=2,"
                       f"adelay={int(s * 1000)}|{int(s * 1000)}[m{k}]")
        print(f"  {role:7s} {s:6.1f}-{e:6.1f}s  {title}")
    n = len(acts)
    music = os.path.join(tmp, "music.wav")
    ff(*inputs, "-filter_complex",
       ";".join(filters) + ";" + "".join(f"[m{k}]" for k in range(n)) +
       f"amix=inputs={n}:normalize=0:duration=longest,atrim=duration={total:.3f}[out]",
       "-map", "[out]", "-ar", "48000", "-ac", "2", music)
    raw = os.path.join(tmp, "raw.wav")
    # nhạc tự hạ khi có lời (sidechain theo giọng), trả lại trong khoảng nghỉ
    ff("-i", music, "-i", vo_n, "-filter_complex",
       "[1:a]asplit=2[sc][v];[0:a][sc]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=450:makeup=1[d];"
       "[d][v]amix=inputs=2:normalize=0:duration=longest[out]",
       "-map", "[out]", "-ar", "48000", "-ac", "2", raw)
    loudnorm_2pass(raw, out, -14)
    open(os.path.join(assets, "music_credits.txt"), "w", encoding="utf-8").write("\n".join(credits) + "\n")
    print(f"-> {out}  {duration(out):.2f}s, -14 LUFS")
    print(f'   <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{total}" data-track-index="9" data-volume="1"></audio>')
    print("   Ghi công nhạc: assets/music_credits.txt (dán vào mô tả video)")


if __name__ == "__main__":
    main()
