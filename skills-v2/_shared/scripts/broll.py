#!/usr/bin/env python3
"""Lập kế hoạch clip video-AI (B-roll) cho video tài liệu, và kiểm tra file prompt.

  python broll.py plan  <thư-mục-dự-án> [--every 27] [--first 10] [--min 5] [--max 8] [--theme paper]
      Đọc assets/timing.json (do build_voiceover.py tạo). Ghi:
        assets/broll_plan.json   vị trí từng clip: số thứ tự, start, duration, lời đọc tương ứng
        broll_snippets.html      thẻ <video> + dòng GSAP để dán vào index.html (clip nào file nấy: assets/broll/NN.mp4)
  python broll.py check <thư-mục-dự-án> <file-prompt.txt> [--theme paper]
      Kiểm tra file prompt: đánh số 1..N đủ số slot, mỗi prompt 1 đoạn, cùng style, có câu loại trừ.

Quy tắc: cứ ~25–30 s có 1 clip 5–8 s; clip bắt đầu ở đầu một câu, kết thúc ở cuối một câu;
bỏ qua đoạn hook đầu bài và 4 s cuối (giữ CTA/câu hỏi chốt trên hình chữ).
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE_FILE = os.path.join(HERE, "..", "..", "explained-history-chronicle", "broll-style.json")


def load_style(theme):
    with open(STYLE_FILE, encoding="utf-8") as f:
        cfg = json.load(f)
    if theme not in cfg["themes"]:
        sys.exit(f"Không có style cho màu '{theme}'. Có: {', '.join(cfg['themes'])}")
    return cfg, cfg["themes"][theme]


def build_suffix(cfg, theme_cfg, duration=None):
    parts = [cfg["base"], theme_cfg["grade"], cfg["technical"]]
    return " ".join(p.strip() for p in parts), cfg["negative"].strip()


def write_snippets(project, slots):
    lines = ["<!-- Dán các thẻ này vào <div id=\"root\"> SAU các khối trang (để nằm trên cùng). Track 5 không dùng cho clip khác. -->"]
    gsap = ["// Dán vào khối timeline GSAP (tl là timeline chính)"]
    for s in slots:
        i = f"broll{s['n']:02d}"
        end = round(s["start"] + s["duration"], 2)
        lines.append(
            f'<video id="{i}" class="clip" src="{s["file"]}" data-start="{s["start"]}" '
            f'data-duration="{s["duration"]}" data-track-index="5" muted playsinline '
            f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;z-index:50"></video>')
        gsap.append(f'tl.from("#{i}",{{opacity:0,duration:.3}},{s["start"]}).to("#{i}",{{opacity:0,duration:.3}},{round(end - 0.3, 2)});')
    sp = os.path.join(project, "broll_snippets.html")
    open(sp, "w", encoding="utf-8").write("\n".join(lines) + "\n\n<script>\n" + "\n".join(gsap) + "\n</script>\n")


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def ingest(args):
    pp = os.path.join(args.project, "assets", "broll_plan.json")
    if not os.path.exists(pp):
        sys.exit("Chưa có broll_plan.json. Chạy `broll.py plan` trước.")
    plan_data = json.load(open(pp, encoding="utf-8"))
    dest = os.path.join(args.project, "assets", "broll")
    os.makedirs(dest, exist_ok=True)
    found = {}
    for name in sorted(os.listdir(args.folder)):
        m = re.match(r"^\D*(\d+)", name)
        if m and name.lower().endswith((".mp4", ".mov", ".webm", ".mkv")):
            found.setdefault(int(m.group(1)), os.path.join(args.folder, name))
    ready, notes = [], []
    for s in plan_data["slots"]:
        src = found.get(s["n"])
        if not src:
            notes.append(f"#{s['n']:02d}: THIẾU clip (slot {s['start']}s +{s['duration']}s) - bỏ qua, trang giữ đồ họa")
            continue
        out = os.path.join(dest, f"{s['n']:02d}.mp4")
        # chuẩn hoá: H.264 1920x1080 30fps, bỏ tiếng (tiếng chỉ đi qua giọng đọc)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-an",
                        "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
        d = probe(out)
        s = dict(s)
        if d + 0.05 < s["duration"]:
            notes.append(f"#{s['n']:02d}: clip {d:.1f}s ngắn hơn slot {s['duration']}s - rút slot còn {d:.1f}s")
            s["duration"] = round(d, 2)
        elif d > s["duration"] + 0.05:
            notes.append(f"#{s['n']:02d}: clip {d:.1f}s dài hơn slot {s['duration']}s - cắt bớt đuôi")
        ready.append(s)
    extra = sorted(set(found) - {s["n"] for s in plan_data["slots"]})
    if extra:
        notes.append(f"Clip thừa không có slot: {extra}")
    write_snippets(args.project, ready)
    print(f"Đã nhận {len(ready)}/{len(plan_data['slots'])} clip -> {dest}")
    print("\n".join(notes))
    print("Snippet đã cập nhật: broll_snippets.html (chỉ gồm các clip có file)")


def plan(args):
    tpath = os.path.join(args.project, "assets", "timing.json")
    if not os.path.exists(tpath):
        sys.exit(f"Thiếu {tpath}. Chạy build_voiceover.py trước.")
    data = json.load(open(tpath, encoding="utf-8"))
    sents, total = data["sentences"], data["total"]
    limit = total - 4.0
    slots, cursor = [], args.first
    while True:
        starts = [s for s in sents if s["start"] >= cursor]
        if not starts:
            break
        first = starts[0]
        # ưu tiên đầu câu sau một khoảng nghỉ chuyển cảnh/câu hỏi
        for s in [x for x in starts if x["start"] <= first["start"] + 3.0]:
            idx = s["i"] - 1
            if idx == 0 or sents[idx - 1]["kind"] in ("scene", "question"):
                first = s
                break
        end_candidates = [s for s in sents if s["i"] >= first["i"]
                          and args.min <= s["end"] - first["start"] <= args.max]
        if end_candidates:
            last = end_candidates[-1]
            dur = last["end"] - first["start"]
        else:
            last = first
            dur = min(args.max, max(args.min, first["end"] - first["start"]))
        if first["start"] + dur > limit:
            break
        covered = [s for s in sents if s["end"] > first["start"] and s["start"] < first["start"] + dur]
        slots.append({
            "n": len(slots) + 1,
            "start": round(first["start"], 2),
            "duration": round(dur, 2),
            "end": round(first["start"] + dur, 2),
            "file": f"assets/broll/{len(slots) + 1:02d}.mp4",
            "narration": " ".join(s["text"] for s in covered),
        })
        cursor = first["start"] + args.every - 2.0
    out = {"every": args.every, "total": total, "theme": args.theme, "slots": slots}
    pp = os.path.join(args.project, "assets", "broll_plan.json")
    json.dump(out, open(pp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    write_snippets(args.project, slots)

    print(f"{len(slots)} clip trong {total:.1f}s (mỗi ~{args.every}s) -> {pp}")
    for s in slots:
        print(f"  #{s['n']:02d}  {s['start']:6.2f}s  +{s['duration']:.1f}s  {s['narration'][:70]}")


def check(args):
    cfg, tcfg = load_style(args.theme)
    plan_path = os.path.join(args.project, "assets", "broll_plan.json")
    n_slots = len(json.load(open(plan_path, encoding="utf-8"))["slots"]) if os.path.exists(plan_path) else None
    raw = open(args.prompts, encoding="utf-8").read().strip()
    paras = [p for p in re.split(r"\n\s*\n", raw) if p.strip()]
    suffix, negative = build_suffix(cfg, tcfg)
    errors = []
    if n_slots is not None and len(paras) != n_slots:
        errors.append(f"Có {len(paras)} prompt nhưng kế hoạch có {n_slots} slot")
    for k, p in enumerate(paras, 1):
        m = re.match(r"^(\d+)\.\s+(.*)$", p.strip(), re.S)
        if not m or int(m.group(1)) != k:
            errors.append(f"Đoạn {k}: phải bắt đầu bằng '{k}. '")
            continue
        body = m.group(2)
        if "\n" in body.strip():
            errors.append(f"#{k}: prompt phải là MỘT đoạn, không xuống dòng")
        if suffix not in body:
            errors.append(f"#{k}: thiếu khối style chung (copy đúng từ `python broll.py style --theme {args.theme}`)")
        if negative not in body:
            errors.append(f"#{k}: thiếu câu loại trừ (chữ, logo, watermark...)")
        if len(body) < 300:
            errors.append(f"#{k}: quá ngắn ({len(body)} ký tự) — mô tả chủ thể, hành động, bối cảnh, ánh sáng, chuyển động máy")
    print("\n".join(errors) if errors else f"OK: {len(paras)} prompt hợp lệ")
    sys.exit(1 if errors else 0)


def style(args):
    cfg, tcfg = load_style(args.theme)
    suffix, negative = build_suffix(cfg, tcfg)
    print(suffix + " " + negative)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("plan")
    p1.add_argument("project")
    p1.add_argument("--every", type=float, default=27)
    p1.add_argument("--first", type=float, default=10)
    p1.add_argument("--min", type=float, default=5)
    p1.add_argument("--max", type=float, default=8)
    p1.add_argument("--theme", default="paper")
    p1.set_defaults(fn=plan)
    p2 = sub.add_parser("check")
    p2.add_argument("project")
    p2.add_argument("prompts")
    p2.add_argument("--theme", default="paper")
    p2.set_defaults(fn=check)
    p4 = sub.add_parser("ingest")
    p4.add_argument("project")
    p4.add_argument("folder")
    p4.set_defaults(fn=ingest)
    p3 = sub.add_parser("style")
    p3.add_argument("--theme", default="paper")
    p3.set_defaults(fn=style)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
