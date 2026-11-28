#!/usr/bin/env python3
"""Lấy ẢNH THẬT và BẢN ĐỒ THẬT cho dự án, gắn thẳng vào index.html, xuất danh sách asset để thay sau.

  python fetch_assets.py <thư-mục-dự-án> assets.json [--no-download]

assets.json (mỗi mục = 1 chỗ trong template có marker <!--asset:ID--><!--/asset:ID-->):
  [
    {"id": "p1", "kind": "photo", "query": "Falcon 9 landing 2015", "source": "nasa|commons|auto",
     "page": "P1 0-6s", "caption": "ẢNH: ..."},
    {"id": "p2", "kind": "map", "highlight": ["CUB"], "focus": ["CUB", "USA", "BHS"],
     "pins": [{"lon": -82.38, "lat": 23.13, "label": "HAVANA"}],
     "route": [[-80.19, 25.76], [-82.38, 23.13]], "page": "P2 6-12s"}
  ]
  photo: tìm Wikimedia Commons (ảnh tự do: PD / CC0 / CC BY / CC BY-SA) và NASA Images (PD).
         "file": "đường/dẫn.jpg" = dùng ảnh của người dùng, không tải.
  map  : vẽ từ Natural Earth (ranh giới quốc gia thật, PD), mã quốc gia ISO-3 (VNM, USA, CUB...).

Kết quả: assets/img/ID.jpg, assets/maps/ID.svg, index.html đã gắn ảnh/bản đồ,
ASSETS.md + credits.txt (copy sang <ROOT>/output/) — danh sách từng chỗ, nguồn, giấy phép, cách thay.
Chỗ không tìm được ảnh: giữ ô giữ chỗ, ghi PLACEHOLDER trong ASSETS.md kèm gợi ý tìm.
"""
import html
import json
import math
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request

UA = "vidskill-explainer/1.0 (https://github.com/vha011/vidskill)"
OK_LICENSE = re.compile(r"^(public domain|pd|cc0|cc by(-sa)?( \d\.\d)?|cc-by(-sa)?)", re.I)
NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "vidskill")
W, H = 1920, 1080


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    return data if binary else json.loads(data.decode("utf-8"))


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", html.unescape(s or "")).strip()


def search_commons(query, n=12):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": n, "prop": "imageinfo",
        "iiprop": "url|size|extmetadata", "iiurlwidth": 1920})
    data = get("https://commons.wikimedia.org/w/api.php?" + q)
    out = []
    for p in sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = strip_tags(meta.get("LicenseShortName", {}).get("value", ""))
        if ii.get("width", 0) < 1200 or not OK_LICENSE.match(lic):
            continue
        out.append({"url": ii.get("thumburl") or ii.get("url"), "w": ii["width"], "h": ii["height"],
                    "license": lic, "author": strip_tags(meta.get("Artist", {}).get("value", ""))[:80],
                    "page": ii.get("descriptionurl", ""), "title": p["title"], "source": "Wikimedia Commons"})
    return out


def search_nasa(query, n=10):
    data = get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": query, "media_type": "image"}))
    out = []
    for it in data.get("collection", {}).get("items", [])[:n]:
        d = it["data"][0]
        try:
            files = get(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(d['nasa_id'])}")
        except Exception:
            continue
        hrefs = [x["href"] for x in files["collection"]["items"]]
        pick = next((h for h in hrefs if "~large" in h), None) or next((h for h in hrefs if "~orig" in h), None)
        if pick:
            out.append({"url": pick.replace("http://", "https://"), "w": 0, "h": 0, "license": "Public domain (NASA)",
                        "author": d.get("center", "NASA"), "page": f"https://images.nasa.gov/details/{d['nasa_id']}",
                        "title": d.get("title", ""), "source": "NASA Images"})
    return out


def landscape_first(cands):
    # ảnh ngang lên trước (khung polaroid ~5:4, bản đồ/toàn khung 16:9)
    return sorted(cands, key=lambda c: 0 if (c["w"] == 0 or c["w"] >= c["h"]) else 1)


def fetch_photo(item, proj):
    os.makedirs(os.path.join(proj, "assets", "img"), exist_ok=True)
    dest = os.path.join(proj, "assets", "img", f"{item['id']}.jpg")
    if item.get("file"):
        shutil.copyfile(item["file"], dest)
        return {"status": "USER", "file": dest, "license": "của người dùng", "source": item["file"], "author": ""}
    src = item.get("source", "auto")
    cands = []
    try:
        if src == "nasa":
            cands += search_nasa(item["query"])
        else:
            cands += search_commons(item["query"])
            if src == "auto" and not cands:
                cands += search_nasa(item["query"])
    except Exception as e:
        print(f"  {item['id']}: lỗi tìm ảnh ({e})")
    for c in landscape_first(cands):
        try:
            data = get(c["url"], binary=True)
        except Exception:
            continue
        if len(data) < 30000:
            continue
        open(dest, "wb").write(data)
        return {"status": "OK", "file": dest, **c}
    return {"status": "PLACEHOLDER", "file": "", "license": "", "source": "", "author": ""}


# ---------- bản đồ ----------

def merc(lon, lat):
    lat = max(-85.0, min(85.0, lat))
    return math.radians(lon), math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def load_countries():
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "ne_50m_admin_0_countries.geojson")
    if not os.path.exists(path):
        print("  tải Natural Earth (3 MB, chỉ lần đầu)...")
        open(path, "wb").write(get(NE_URL, binary=True))
    feats = json.load(open(path, encoding="utf-8"))["features"]
    for f in feats:
        p = f["properties"]
        f["code"] = p.get("ADM0_A3") if p.get("ISO_A3") in (None, "-99") else p.get("ISO_A3")
    return feats


def polys(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def build_map(item, proj):
    feats = load_countries()
    by = {f["code"]: f for f in feats}
    focus = item.get("focus") or item.get("highlight") or []
    pts = []
    for code in focus:
        if code not in by:
            sys.exit(f"Mã quốc gia không có: {code} (dùng ISO-3, ví dụ VNM, USA, CUB)")
        for poly in polys(by[code]["geometry"]):
            pts += [merc(*xy) for xy in poly[0]]
    for p in item.get("pins", []):
        pts.append(merc(p["lon"], p["lat"]))
    for xy in item.get("route", []):
        pts.append(merc(*xy))
    if not pts:
        sys.exit(f"Bản đồ {item['id']}: cần highlight/focus/pins")
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    pad = item.get("pad", 0.35)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    dx, dy = max(x1 - x0, 0.02), max(y1 - y0, 0.02)
    x0, x1, y0, y1 = x0 - dx * pad, x1 + dx * pad, y0 - dy * pad, y1 + dy * pad
    s = min(W / (x1 - x0), H / (y1 - y0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

    def px(lon, lat):
        x, y = merc(lon, lat)
        return (W / 2 + (x - cx) * s, H / 2 - (y - cy) * s)

    def path_for(geom):
        d = []
        for poly in polys(geom):
            for ring in poly:
                pr = [px(*xy) for xy in ring]
                if max(p[0] for p in pr) < -50 or min(p[0] for p in pr) > W + 50 or \
                   max(p[1] for p in pr) < -50 or min(p[1] for p in pr) > H + 50:
                    continue
                keep, last = [], None
                for p in pr:
                    if last is None or abs(p[0] - last[0]) + abs(p[1] - last[1]) > 1.2:
                        keep.append(p)
                        last = p
                if len(keep) >= 3:
                    d.append("M" + "L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in keep) + "Z")
        return "".join(d)

    mid = item["id"]
    land, hl = [], []
    for f in feats:
        d = path_for(f["geometry"])
        if not d:
            continue
        land.append(d)
        if f["code"] in item.get("highlight", []):
            hl.append(f'<path class="hl" id="{mid}-hl-{f["code"]}" d="{d}" style="fill:var(--redmap)"/>')
    svg = [f'<svg viewBox="0 0 {W} {H}" style="position:absolute;inset:0">',
           f'<defs><clipPath id="{mid}-land"><path d="{"".join(land)}"/></clipPath>'
           f'<filter id="{mid}-relief" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
           f'baseFrequency="0.011 0.016" numOctaves="5" seed="7"/><feColorMatrix type="matrix" '
           f'values="1.6 0 0 0 -0.35 1.6 0 0 0 -0.35 1.6 0 0 0 -0.35 0 0 0 1 0"/><feGaussianBlur stdDeviation="4"/></filter></defs>',
           f'<g clip-path="url(#{mid}-land)"><rect width="{W}" height="{H}" style="fill:var(--land)"/>'
           f'<rect width="{W}" height="{H}" filter="url(#{mid}-relief)" opacity=".45"/></g>',
           f'<path d="{"".join(land)}" fill="none" stroke="#e8e8e8" stroke-width="1.2" opacity=".45"/>',
           *hl]
    route = item.get("route", [])
    if len(route) >= 2:
        rp = [px(*xy) for xy in route]
        (ax, ay), (bx, by_) = rp[0], rp[-1]
        mx, my = (ax + bx) / 2, (ay + by_) / 2 - 0.18 * math.hypot(bx - ax, by_ - ay)
        d = f"M{ax:.1f} {ay:.1f} Q{mx:.1f} {my:.1f} {bx:.1f} {by_:.1f}" if len(rp) == 2 else \
            "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in rp)
        svg.append(f'<defs><mask id="{mid}-rm"><path id="{mid}-route-mask" d="{d}" fill="none" stroke="#fff" '
                   f'stroke-width="30" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></mask></defs>'
                   f'<path id="{mid}-route" d="{d}" fill="none" stroke="#dfeeff" stroke-width="7" '
                   f'stroke-linecap="round" stroke-dasharray="0.1 18" mask="url(#{mid}-rm)"/>')
    svg.append("</svg>")
    pins = []
    for k, p in enumerate(item.get("pins", []), 1):
        x, y = px(p["lon"], p["lat"])
        pins.append(f'<svg id="{mid}-pin{k}" class="pin" style="position:absolute;left:{x - 30:.0f}px;top:{y - 68:.0f}px;'
                    f'width:60px;height:70px" viewBox="0 0 60 70"><path d="M5 5 H55 V40 L30 66 L5 40Z" style="fill:var(--blue)" '
                    f'stroke="#fff" stroke-width="4"/><circle cx="30" cy="20" r="7" fill="#fff"/></svg>')
        if p.get("label"):
            pins.append(f'<div id="{mid}-lbl{k}" class="lbl mono" style="left:{x + 26:.0f}px;top:{y - 12:.0f}px">'
                        f'{html.escape(p["label"])}</div>')
    os.makedirs(os.path.join(proj, "assets", "maps"), exist_ok=True)
    frag = "".join(svg) + "".join(pins)
    open(os.path.join(proj, "assets", "maps", f"{mid}.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="--land:#383838;--redmap:#990303">'
        + "".join(svg[1:-1]) + "</svg>")
    return frag, {"status": "OK", "license": "Public domain (Natural Earth)", "source": "Natural Earth 1:50m",
                  "author": "naturalearthdata.com", "file": f"assets/maps/{mid}.svg"}


def patch(index_html, aid, content):
    pat = re.compile(rf"(<!--asset:{re.escape(aid)}-->).*?(<!--/asset:{re.escape(aid)}-->)", re.S)
    if not pat.search(index_html):
        print(f"  {aid}: KHÔNG thấy marker <!--asset:{aid}--> trong index.html - chưa gắn")
        return index_html, False
    return pat.sub(lambda m: m.group(1) + content + m.group(2), index_html), True


def short_credit(r):
    lic = re.sub(r"Public domain.*", "PD", r["license"])
    who = r.get("author") or ""
    if not who or "unknown" in who.lower():
        who = r.get("source", "")
    return f"ẢNH: {who[:40]} · {lic}".upper()


def set_caption(page, aid, caption):
    pat = re.compile(rf'(<!--/asset:{re.escape(aid)}-->\s*<div class="cp mono">)[^<]*(</div>)')
    return pat.sub(lambda m: m.group(1) + html.escape(caption) + m.group(2), page)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    proj, spec = sys.argv[1], sys.argv[2]
    items = json.load(open(spec, encoding="utf-8"))
    idx_path = os.path.join(proj, "index.html")
    page = open(idx_path, encoding="utf-8").read()
    rows, credits = [], []
    for it in items:
        print(f"- {it['id']} ({it['kind']})")
        if it["kind"] == "map":
            frag, r = build_map(it, proj)
            page, placed = patch(page, it["id"], frag)
        else:
            r = fetch_photo(it, proj)
            if r["status"] == "PLACEHOLDER":
                placed = False
            else:
                img = (f'<img src="assets/img/{it["id"]}.jpg" alt="">'
                       f'<div class="cr mono">{html.escape(short_credit(r))}</div>')
                page, placed = patch(page, it["id"], img)
                if placed and it.get("caption"):
                    page = set_caption(page, it["id"], it["caption"])
        r["placed"] = placed
        rows.append((it, r))
        if r["status"] in ("OK",):
            credits.append(f"{it['id']}: {r.get('title', '')} — {r.get('author', '')} — {r['license']} — {r.get('page', r.get('source', ''))}")
    open(idx_path, "w", encoding="utf-8").write(page)

    md = ["# Danh sách asset hình ảnh", "",
          "Thay ảnh: chép file mới đè lên đúng tên trong cột *File* (giữ tên), hoặc sửa `assets.json` thêm "
          '`"file": "đường/dẫn.jpg"` rồi chạy lại `fetch_assets.py`. Ảnh AI phải ghi caption "ẢNH MINH HOẠ · TẠO BẰNG AI".', "",
          "| ID | Trang / thời điểm | Loại | Trạng thái | File | Nguồn · giấy phép | Gợi ý tìm / thay |",
          "|---|---|---|---|---|---|---|"]
    for it, r in rows:
        f = os.path.relpath(r["file"], proj) if r.get("file") and os.path.isabs(r["file"]) else r.get("file", "")
        status = r["status"] + ("" if r.get("placed") else " (chưa gắn)")
        src = f'{r.get("source", "")} · {r.get("license", "")}' if r["status"] != "PLACEHOLDER" else "—"
        hint = it.get("query", "") if it["kind"] != "map" else "bản đồ vẽ từ dữ liệu thật; sửa pins/highlight trong assets.json"
        md.append(f"| {it['id']} | {it.get('page', '')} | {it['kind']} | {status} | `{f}` | {src} | {hint} |")
    md += ["", "## Ghi công (đưa vào mô tả video)", ""] + [f"- {c}" for c in credits]
    open(os.path.join(proj, "ASSETS.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    open(os.path.join(proj, "credits.txt"), "w", encoding="utf-8").write("\n".join(credits) + "\n")
    out_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "output"))
    if os.path.isdir(out_dir):
        slug = os.path.basename(os.path.abspath(proj))
        shutil.copyfile(os.path.join(proj, "ASSETS.md"), os.path.join(out_dir, f"{slug}-ASSETS.md"))
    ok = sum(1 for _, r in rows if r["status"] != "PLACEHOLDER" and r.get("placed"))
    print(f"\n{ok}/{len(rows)} chỗ đã có hình thật. Danh sách: {os.path.join(proj, 'ASSETS.md')}")
    for it, r in rows:
        if r["status"] == "PLACEHOLDER":
            print(f"  PLACEHOLDER {it['id']}: không tìm thấy ảnh tự do cho '{it.get('query')}' — đổi query hoặc đưa file")


if __name__ == "__main__":
    main()
