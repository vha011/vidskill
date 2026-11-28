#!/usr/bin/env python3
"""Gọi Muse (Meta) để tạo ẢNH và CLIP thay cho Kie.ai của herk-edit-kit.

Khóa API (không commit): biến môi trường hoặc file <repo>/.env
  MUSE_API_KEY=...            khóa dùng chung cho ảnh và video
  MUSE_IMAGE_KEY / MUSE_VIDEO_KEY   (tùy chọn) khóa riêng nếu hai nhà cung cấp khác nhau
  MUSE_IMAGE_BASE=https://api.meta.ai/v1          (mặc định: Meta Model API, model muse-image-1.0)
  MUSE_VIDEO_BASE=https://api.apimodels.app/v1    (mặc định: API Meta chưa có video; Muse Video qua apimodels)
  MUSE_VIDEO_PRICE=0.037      USD/giây, chỉ để ước tính chi phí

  python muse.py image "<prompt>" -o assets/img/x.jpg [--size 1792x1024]
  python muse.py batch <file-prompt.txt> <thư-mục-ra> --kind video|image [--duration 6] [--first-frame-dir dir] [--yes]
      File prompt dạng "1. ...\\n\\n2. ..." (giống broll-prompts.txt). Ra 01.mp4/01.jpg... đúng số thứ tự,
      bỏ qua file đã có (chạy lại an toàn). Không có --yes: chỉ in số lượng + chi phí ước tính rồi dừng.
      Clip ra dùng ngay: broll.py ingest <dự-án> <thư-mục-ra>.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def load_env():
    path = os.path.join(REPO, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r"\s*([A-Z_]+)\s*=\s*(.*?)\s*$", line)
            if m and m.group(1) not in os.environ:
                os.environ[m.group(1)] = m.group(2).strip('"').strip("'")


def key(kind):
    k = os.environ.get(f"MUSE_{kind.upper()}_KEY") or os.environ.get("MUSE_API_KEY") or os.environ.get("MODEL_API_KEY")
    if not k:
        sys.exit(f"Thiếu khóa Muse: đặt MUSE_API_KEY trong {os.path.join(REPO, '.env')} hoặc biến môi trường")
    return k


def call(method, url, k, body=None, raw=False, timeout=300):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {k}", "Content-Type": "application/json", "User-Agent": "vidskill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"Muse lỗi HTTP {e.code} tại {url}: {e.read().decode(errors='replace')[:500]}")
    return out if raw else json.loads(out)


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "vidskill/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r:
        open(dest, "wb").write(r.read())


def gen_image(prompt, dest, size="1792x1024"):
    base = os.environ.get("MUSE_IMAGE_BASE", "https://api.meta.ai/v1").rstrip("/")
    res = call("POST", f"{base}/images/generations", key("image"),
               {"model": os.environ.get("MUSE_IMAGE_MODEL", "muse-image-1.0"), "prompt": prompt, "n": 1, "size": size})
    item = res["data"][0]
    if item.get("b64_json"):
        open(dest, "wb").write(base64.b64decode(item["b64_json"]))
    else:
        download(item["url"], dest)
    return dest


def data_uri(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".").replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()


def gen_video(prompt, dest, duration=6, aspect="16:9", first_frame=None):
    base = os.environ.get("MUSE_VIDEO_BASE", "https://api.apimodels.app/v1").rstrip("/")
    k = key("video")
    body = {"model": os.environ.get("MUSE_VIDEO_MODEL", "muse-video"), "prompt": prompt,
            "duration": int(duration), "aspect_ratio": aspect}
    if first_frame:
        body["image_url"] = data_uri(first_frame)
    res = call("POST", f"{base}/video/generations", k, body)
    task = (res.get("data") or {}).get("taskId") or res.get("id")
    if not task:
        sys.exit(f"Muse không trả taskId: {json.dumps(res)[:300]}")
    for _ in range(120):  # tối đa ~30 phút
        time.sleep(15)
        st = call("GET", f"{base}/video/generations?task_id={task}", k)
        d = st.get("data") or {}
        if d.get("state") == "completed":
            download(d["resultUrls"][0], dest)
            return dest
        if d.get("state") == "failed":
            sys.exit(f"Muse tạo clip thất bại: {json.dumps(d)[:300]}")
    sys.exit(f"Quá thời gian chờ task {task}")


def read_prompts(path):
    raw = open(path, encoding="utf-8").read().strip()
    out = []
    for p in re.split(r"\n\s*\n", raw):
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", p.strip(), re.S)
        if m:
            out.append((int(m.group(1)), " ".join(m.group(2).split())))
    return out


def cmd_batch(a):
    items = read_prompts(a.prompts)
    os.makedirs(a.out, exist_ok=True)
    ext = "mp4" if a.kind == "video" else "jpg"
    todo = [(n, p) for n, p in items if not os.path.exists(os.path.join(a.out, f"{n:02d}.{ext}"))]
    if a.kind == "video":
        price = float(os.environ.get("MUSE_VIDEO_PRICE", "0.037"))
        print(f"{len(todo)}/{len(items)} clip cần tạo × {a.duration}s ≈ {len(todo) * a.duration * price:.2f} USD")
    else:
        print(f"{len(todo)}/{len(items)} ảnh cần tạo")
    if not a.yes:
        print("Chưa gọi Muse. Xác nhận với người dùng rồi chạy lại với --yes.")
        return
    for n, p in todo:
        dest = os.path.join(a.out, f"{n:02d}.{ext}")
        print(f"  #{n:02d} ...", flush=True)
        if a.kind == "video":
            ff = None
            if a.first_frame_dir:
                cand = [os.path.join(a.first_frame_dir, f"{n:02d}.{e}") for e in ("jpg", "jpeg", "png", "webp")]
                ff = next((c for c in cand if os.path.exists(c)), None)
            gen_video(p, dest, a.duration, a.aspect, ff)
        else:
            gen_image(p, dest, a.size)
        print(f"  #{n:02d} -> {dest}")


def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("image")
    p.add_argument("prompt")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--size", default="1792x1024")
    p.set_defaults(fn=lambda a: print(gen_image(a.prompt, a.out, a.size)))
    p = sub.add_parser("batch")
    p.add_argument("prompts")
    p.add_argument("out")
    p.add_argument("--kind", choices=["video", "image"], default="video")
    p.add_argument("--duration", type=int, default=6)
    p.add_argument("--aspect", default="16:9")
    p.add_argument("--size", default="1792x1024")
    p.add_argument("--first-frame-dir")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(fn=cmd_batch)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
