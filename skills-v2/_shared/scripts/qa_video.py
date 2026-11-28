#!/usr/bin/env python3
"""Kiểm tra video thành phẩm trước khi bàn giao. Trả mã lỗi 1 nếu không đạt.

  python qa_video.py <video.mp4> [--project <thư-mục-dự-án>]

Đo:
  - Độ lớn tổng (mục tiêu -14 LUFS ± 1,5) và độ sống động (LRA; < 3 LU = phẳng, đều đều).
  - Khoảng nghỉ của giọng: lấy từ assets/timing.json nếu có --project, không thì ước lượng từ đường bao âm lượng.
    Đạt: ≥ 70% khoảng giữa câu ≥ 0,6 s; không đoạn nào đọc liền > 15 s không nghỉ.
  - Hình đứng yên: đoạn hình không đổi > 3,5 s (người xem rời đi). Đạt: không có đoạn nào.
  - Ô giữ chỗ còn sót trong index.html (ảnh/bản đồ giả) nếu có --project.
"""
import argparse
import json
import os
import re
import subprocess
import sys


def run(args):
    return subprocess.run(args, capture_output=True, text=True).stderr


def loudness(v):
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", v, "-af", "ebur128", "-f", "null", "-"])
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    lra = re.findall(r"LRA:\s+([\d.]+) LU", out)
    return float(i[-1]), float(lra[-1])


def gaps_from_envelope(v):
    # RMS mỗi 50 ms; nghỉ = đoạn thấp hơn trung vị lời nói ≥ 12 dB, dài ≥ 0,25 s (nhạc nền nhỏ vẫn tính là nghỉ)
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", v, "-af",
                          "aresample=16000,asetnsamples=800,astats=metadata=1:reset=1,"
                          "ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    lv = [float(x) if x not in ("-inf", "inf") else -120.0
          for x in re.findall(r"RMS_level=(-?[\d.]+|-inf)", out)]
    if not lv:
        return [], 0
    loud = sorted(x for x in lv if x > -60)
    speech = loud[int(len(loud) * 0.6)] if loud else -20
    thr = speech - 12
    gaps, run_len = [], 0
    for x in lv + [0]:
        if x < thr:
            run_len += 1
        else:
            if run_len * 0.05 >= 0.25:
                gaps.append(run_len * 0.05)
            run_len = 0
    return gaps, len(lv) * 0.05


def freezes(v):
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", v, "-vf", "freezedetect=n=0.002:d=3.5", "-map", "0:v", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", out)]
    durs = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", out)]
    return list(zip(starts, durs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--project")
    a = ap.parse_args()
    fails, rep = [], []

    i, lra = loudness(a.video)
    rep.append(f"Độ lớn: {i:.1f} LUFS (mục tiêu -14), LRA {lra:.1f} LU")
    if abs(i + 14) > 1.5:
        fails.append(f"độ lớn {i:.1f} LUFS lệch mục tiêu -14 → chạy mix_audio.py")
    if lra < 3.0:
        fails.append(f"âm thanh phẳng (LRA {lra:.1f} < 3): nhạc một màu, không có hồi → mix_audio.py --acts")

    tpath = os.path.join(a.project, "assets", "timing.json") if a.project else ""
    if tpath and os.path.exists(tpath):
        s = json.load(open(tpath, encoding="utf-8"))["sentences"]
        gaps = [x["pause_after"] for x in s[:-1]]
        longest, cur = 0.0, 0.0
        for x in s:
            cur += x["end"] - x["start"]
            if x["pause_after"] >= 0.6:
                longest, cur = max(longest, cur), 0.0
        longest = max(longest, cur)
        src = "timing.json"
    else:
        gaps, total = gaps_from_envelope(a.video)
        longest = 0.0  # ước lượng: khoảng lớn nhất giữa hai lần nghỉ ≥ 0,6 s
        src = "ước lượng từ âm thanh"
    good = sum(1 for g in gaps if g >= 0.6)
    ratio = good / len(gaps) if gaps else 0
    rep.append(f"Nghỉ giữa câu ({src}): {len(gaps)} khoảng, {good} khoảng ≥ 0,6 s ({ratio:.0%})"
               + (f", đoạn đọc liền dài nhất {longest:.1f} s" if longest else ""))
    if ratio < 0.7:
        fails.append(f"đọc dồn: chỉ {ratio:.0%} khoảng nghỉ ≥ 0,6 s → dùng build_voiceover.py (nghỉ 0,7/1,3/1,5 s)")
    if longest > 15:
        fails.append(f"đọc liền {longest:.1f} s không nghỉ → tách câu / thêm nghỉ")

    fr = freezes(a.video)
    rep.append(f"Hình đứng yên > 3,5 s: {len(fr)} đoạn" +
               (" (" + ", ".join(f"{s:.0f}s+{d:.1f}" for s, d in fr[:8]) + ("…" if len(fr) > 8 else "") + ")" if fr else ""))
    if fr:
        fails.append(f"{len(fr)} đoạn hình đứng yên → thêm chuyển động ≤ 2,5 s/lần (Ken Burns ảnh, đếm số, nhãn mới)")

    if a.project:
        page = open(os.path.join(a.project, "index.html"), encoding="utf-8").read()
        empty = re.findall(r"<!--asset:([\w-]+)--><!--/asset:\1-->", page)
        rep.append(f"Ô ảnh/bản đồ còn trống: {len(empty)}" + (f" ({', '.join(empty)})" if empty else ""))
        if empty:
            fails.append(f"còn ô giữ chỗ {', '.join(empty)} → fetch_assets.py hoặc ghi trong ASSETS.md cho người dùng thay")

    print("\n".join(rep))
    print("\nKẾT QUẢ: " + ("ĐẠT" if not fails else "CHƯA ĐẠT"))
    for f in fails:
        print("  - " + f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
