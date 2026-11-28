#!/usr/bin/env python3
"""Dựng video giải thích từ thư viện card của herk-edit-kit (style-library, 406 card).

  python cards.py list  [--style vox-explainer] [--purpose stat] [--tier tier1]
      Liệt kê card + slot (tên, kiểu, số ký tự tối đa) để viết storyboard.
  python cards.py build <thư-mục-dự-án> storyboard.json [--kit <ROOT>/herk-edit-kit]
      Ghép card thành index.html: mỗi beat một sub-composition (compositions/bNN.html) đã điền chữ,
      ảnh, thời lượng theo assets/timing.json; gắn assets/mix.wav nếu có (mix_audio.py).

storyboard.json:
  {"style": "vox-explainer",
   "beats": [
     {"card": "vox-explainer.t1.stat.torn", "from": 1, "to": 2,
      "slots": {"stat": "7.158", "kicker": "HƯNG NAM · 1950", "label": "người lên <em>một con tàu</em>"},
      "images": {"scrap": "assets/img/p1.jpg"}}
   ]}
  from/to = số thứ tự câu trong timing.json (1-based). Beat bắt đầu 0,3 s trước câu "from",
  kéo tới đầu beat sau (beat cuối tới hết). Không có timing.json: dùng "duration" (giây) mỗi beat.
  Slot không ghi giữ nguyên chữ mẫu của card — nên ghi đủ, đặc biệt "source".
"""
import argparse
import html as htmllib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_kit(arg):
    for k in [arg, os.path.join(HERE, "..", "..", "..", "..", "herk-edit-kit"), os.path.join(os.getcwd(), "herk-edit-kit")]:
        if k and os.path.exists(os.path.join(k, "style-library", "registry.json")):
            return os.path.abspath(k)
    sys.exit("Không tìm thấy herk-edit-kit (cần style-library/registry.json). Dùng --kit <đường dẫn>.")


def load_style(kit, style):
    reg = json.load(open(os.path.join(kit, "style-library", "registry.json"), encoding="utf-8"))
    for s in reg["styles"]:
        if s["id"] == style:
            folder = os.path.join(kit, "style-library", s.get("folder", "").strip("/") or "")
            if not os.path.isdir(folder):
                folder = next(os.path.join(kit, "style-library", d) for d in os.listdir(os.path.join(kit, "style-library"))
                              if d.endswith(style))
            sj = json.load(open(os.path.join(folder, "style.json"), encoding="utf-8"))
            return folder, {c["id"]: c for c in sj["cards"]}
    sys.exit(f"Không có style '{style}'. Có: {', '.join(s['id'] for s in reg['styles'])}")


def cmd_list(a):
    kit = find_kit(a.kit)
    _, cards = load_style(kit, a.style)
    for cid, c in cards.items():
        if a.purpose and c.get("purpose") != a.purpose:
            continue
        if a.tier and c.get("tier") != a.tier:
            continue
        slots = ", ".join(f'{s["name"]}:{s["type"]}' + (f'≤{s["maxChars"]}' if s.get("maxChars") else "")
                          for s in c.get("slots", []))
        d = c.get("duration", {})
        print(f'{cid:48s} {d.get("min", "?")}-{d.get("max", "?")}s  {slots}')


def move_scale_zero_to_gsap(styles, body):
    # lint gsap_css_transform_conflict: CSS `transform: scaleX(0)` + tween scaleX → đặt trạng thái đầu bằng gsap.set
    sels = []
    styles = re.sub(r"([^{}]+)\{([^}]*?)(transform:\s*scale([XY])\(0\);?)([^}]*)\}",
                    lambda m: (sels.append((m.group(1).strip(), m.group(4))) or
                               m.group(1) + "{" + m.group(2) + m.group(5) + "}"), styles)
    if sels:
        sets = "".join(f'gsap.set({json.dumps(s)},{{scale{ax}:0}});' for s, ax in sels)
        body = re.sub(r"<script>", "<script>" + sets, body, count=1)
    return styles, body


def card_parts(path):
    src = open(path, encoding="utf-8").read()
    styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
    m = re.search(r'<div[^>]*data-composition-id="([^"]+)"', src)
    if not m:
        sys.exit(f"{path}: không thấy data-composition-id")
    cid = m.group(1)
    body = re.search(r"<body[^>]*>(.*)</body>", src, re.S).group(1)
    body = re.sub(r'<script[^>]*src="[^"]*gsap[^"]*"[^>]*>\s*</script>', "", body)
    return cid, styles, body


def fill_slot(body, name, value, is_image):
    pat = re.compile(rf'(<(\w+)([^>]*\bdata-slot="{re.escape(name)}"[^>]*)>)(.*?)(</\2>)', re.S)
    m = pat.search(body)
    if not m:
        print(f"    cảnh báo: card không có slot '{name}'")
        return body
    if is_image:
        attrs = m.group(3)
        style = (f"background-image:url('{value}');background-size:cover;background-position:center;"
                 "filter:grayscale(1) contrast(1.1);")
        if 'style="' in attrs:
            attrs = attrs.replace('style="', f'style="{style}', 1)
        else:
            attrs += f' style="{style}"'
        return body[:m.start()] + f"<{m.group(2)}{attrs}>" + m.group(4) + m.group(5) + body[m.end():]
    return body[:m.start()] + m.group(1) + value + m.group(5) + body[m.end():]


def cmd_build(a):
    kit = find_kit(a.kit)
    proj = os.path.abspath(a.project)
    sb = json.load(open(a.storyboard, encoding="utf-8"))
    folder, cards = load_style(kit, sb.get("style", "vox-explainer"))
    tokens = open(os.path.join(folder, "tokens.css"), encoding="utf-8").read()
    # HyperFrames tự nhúng font Google theo tên khi render; @import ngoài làm chậm/lỗi khi mất mạng
    tokens = re.sub(r"@import url\([^)]*\);", "", tokens)
    # Caveat không có dấu tiếng Việt (vỡ "CỨU HỘ") → font viết tay có bộ tiếng Việt
    tokens = re.sub(r'--font-hand:\s*"Caveat"', '--font-hand: "Patrick Hand"', tokens)
    tpath = os.path.join(proj, "assets", "timing.json")
    timing = json.load(open(tpath, encoding="utf-8")) if os.path.exists(tpath) else None
    beats = sb["beats"]

    starts = []
    for k, b in enumerate(beats):
        if timing and "from" in b:
            starts.append(0.0 if k == 0 else max(0.0, timing["sentences"][b["from"] - 1]["start"] - 0.3))
        else:
            starts.append(sum(x.get("duration", 6) for x in beats[:k]))
    total = timing["total"] if timing else starts[-1] + beats[-1].get("duration", 6)
    os.makedirs(os.path.join(proj, "compositions"), exist_ok=True)

    hosts, warns = [], []
    for k, b in enumerate(beats):
        start = round(starts[k], 3)
        end = round(starts[k + 1] if k + 1 < len(beats) else total, 3)
        dur = round(end - start, 3)
        card = cards.get(b["card"]) or sys.exit(f"Không có card {b['card']} (xem `cards.py list`)")
        rng = card.get("duration", {})
        if rng.get("max") and dur > rng["max"] + 2:
            warns.append(f"b{k+1:02d} dài {dur:.1f}s > card thiết kế {rng['max']}s: nên tách thành 2 card")
        cid, styles, body = card_parts(os.path.join(folder, card["file"]))
        styles, body = move_scale_zero_to_gsap(styles, body)
        new_id = f"b{k+1:02d}-{cid}"
        slot_types = {s["name"]: s["type"] for s in card.get("slots", [])}
        for name, val in b.get("slots", {}).items():
            mx = next((s.get("maxChars") for s in card.get("slots", []) if s["name"] == name), None)
            plain = re.sub(r"<[^>]+>", "", val)
            if mx and len(plain) > mx:
                warns.append(f"b{k+1:02d}.{name}: {len(plain)} ký tự > {mx} (dễ tràn khung)")
            body = fill_slot(body, name, val, False)
        for name, img in b.get("images", {}).items():
            if not os.path.exists(os.path.join(proj, img)):
                warns.append(f"b{k+1:02d}.{name}: thiếu file ảnh {img} (fetch_assets.py hoặc ảnh Muse)")
            if slot_types.get(name) != "image":
                warns.append(f"b{k+1:02d}: slot ảnh '{name}' không có trong card")
            body = fill_slot(body, name, htmllib.escape(img), True)
        # đổi id để dùng cùng một card nhiều lần không đụng nhau (CSS, JS, timeline)
        styles_n = styles.replace(cid, new_id)
        body_n = body.replace(cid, new_id)
        body_n = re.sub(r'(data-composition-id="[^"]+"[^>]*?)data-start="0"', r"\1data-start=\"0\"", body_n)
        body_n = re.sub(r'(<div[^>]*data-composition-id="%s"[^>]*?)(>)' % re.escape(new_id),
                        lambda m: (m.group(1) if "data-duration" in m.group(1) else m.group(1) + f' data-duration="{dur}"') + m.group(2),
                        body_n, count=1)
        comp = (f'<template id="{new_id}-template">\n<style>\n{tokens}\n{styles_n}\n</style>\n'
                f"{body_n.strip()}\n</template>\n")
        open(os.path.join(proj, "compositions", f"b{k+1:02d}.html"), "w", encoding="utf-8").write(comp)
        hosts.append(f'  <div id="host{k+1:02d}" class="clip host" data-composition-id="{new_id}" data-composition-src="compositions/b{k+1:02d}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="1"></div>')
        print(f"  b{k+1:02d} {start:7.2f}s +{dur:5.2f}s  {b['card']}")

    mix = os.path.exists(os.path.join(proj, "assets", "mix.wav"))
    audio = (f'  <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{total}" '
             f'data-track-index="9" data-volume="1"></audio>' if mix else "  <!-- chưa có assets/mix.wav: chạy mix_audio.py -->")
    # host trôi rất chậm suốt beat: card giữ khung cuối khi beat dài hơn animation của nó
    drift = "\n".join(f'tl.fromTo("#host{k+1:02d}",{{scale:1}},{{scale:1.035,duration:{round((starts[k+1] if k+1 < len(beats) else total) - starts[k], 3)},ease:"none"}},{round(starts[k], 3)});'
                      for k in range(len(beats)))
    page = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script>
<style>html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#000}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden}}.host{{position:absolute;inset:0;transform-origin:50% 50%}}</style>
</head><body>
<div id="root" data-composition-id="root" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{audio}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
{drift}
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script></body></html>
"""
    open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(page)
    gs = os.path.join(proj, "assets", "gsap.min.js")
    if not os.path.exists(gs):
        src = os.path.join(HERE, "..", "gsap.min.js")
        os.makedirs(os.path.dirname(gs), exist_ok=True)
        open(gs, "wb").write(open(src, "rb").read())
    print(f"-> {os.path.join(proj, 'index.html')}  {len(beats)} beat, {total:.1f}s" + ("" if mix else "  (chưa có nhạc/giọng)"))
    for w in warns:
        print("  ! " + w)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--style", default="vox-explainer")
    p.add_argument("--purpose")
    p.add_argument("--tier")
    p.add_argument("--kit")
    p.set_defaults(fn=cmd_list)
    p = sub.add_parser("build")
    p.add_argument("project")
    p.add_argument("storyboard")
    p.add_argument("--kit")
    p.set_defaults(fn=cmd_build)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
