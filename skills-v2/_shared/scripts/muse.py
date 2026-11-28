#!/usr/bin/env python3
"""Gọi Muse qua muse2api (chạy trên máy / mạng nội bộ, pool tài khoản) để tạo ẢNH và CLIP, thay Kie.ai.

Cấu hình trong <repo>/.env (mẫu .env.example, không commit):
  MUSE_HOST=127.0.0.1        máy chạy muse2api
  MUSE_PORT=18610            cổng muse2api (mặc định của muse2api)
  MUSE_API_KEY=m2a_...       khóa MUSE2API_KEY đã đặt khi chạy muse2api
  MUSE_IMAGE_MODEL=muse-image
  MUSE_VIDEO_MODEL=          để trống nếu muse2api không cần model cho video
  (hoặc MUSE_BASE_URL=http://host:port/v1 thay cho HOST+PORT)

  python muse.py check                                   kiểm tra kết nối muse2api
  python muse.py image "<prompt>" -o assets/img/x.jpg [--size 16:9]
  python muse.py batch <file-prompt.txt> <thư-mục-ra> --kind video|image [--duration 6] [--size 16:9]
                       [--first-frame-dir dir]
      File prompt "1. ...\\n\\n2. ..." (như broll-prompts.txt) → 01.mp4/01.jpg… đúng số thứ tự.
      Bỏ qua file đã có (chạy lại an toàn, tiếp tục khi gián đoạn). Clip ra dùng ngay:
      broll.py ingest <dự-án> <thư-mục-ra>.
Video muse2api: thời lượng 5, 6, 8 hoặc 10 s; khung 16:9 hoặc 9:16.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DURATIONS = (5, 6, 8, 10)


def load_env():
    path = os.path.join(REPO, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$", line)
            if m and m.group(1) not in os.environ:
                os.environ[m.group(1)] = m.group(2).strip('"').strip("'")


def base_url():
    if os.environ.get("MUSE_BASE_URL"):
        return os.environ["MUSE_BASE_URL"].rstrip("/")
    return f"http://{os.environ.get('MUSE_HOST', '127.0.0.1')}:{os.environ.get('MUSE_PORT', '18610')}/v1"


def call(method, path, body=None, timeout=900):
    url = path if path.startswith("http") else base_url() + path
    headers = {"Content-Type": "application/json", "User-Agent": "vidskill/1.0"}
    if os.environ.get("MUSE_API_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['MUSE_API_KEY']}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"muse2api lỗi HTTP {e.code} tại {url}: {e.read().decode(errors='replace')[:400]}")
    except urllib.error.URLError as e:
        sys.exit(f"Không kết nối được muse2api tại {url} ({e.reason}). Kiểm tra MUSE_HOST/MUSE_PORT và muse2api đang chạy.")
    return json.loads(raw)


def download(url, dest):
    if url.startswith("/"):
        url = base_url().rsplit("/v1", 1)[0] + url
    headers = {"User-Agent": "vidskill/1.0"}
    if os.environ.get("MUSE_API_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['MUSE_API_KEY']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=900) as r:
        open(dest, "wb").write(r.read())


def gen_image(prompt, dest, size="16:9"):
    res = call("POST", "/images/generations", {
        "model": os.environ.get("MUSE_IMAGE_MODEL", "muse-image"), "prompt": prompt,
        "size": size, "response_format": "b64_json"})
    item = res["data"][0]
    if item.get("b64_json"):
        open(dest, "wb").write(base64.b64decode(item["b64_json"]))
    else:
        download(item["url"], dest)
    return dest


def data_uri(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".").replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()


def gen_video(prompt, dest, duration=6, size="16:9", first_frame=None):
    duration = min((d for d in DURATIONS if d >= duration), default=DURATIONS[-1])
    body = {"prompt": prompt, "duration": duration, "size": size}
    if os.environ.get("MUSE_VIDEO_MODEL"):
        body["model"] = os.environ["MUSE_VIDEO_MODEL"]
    if first_frame:
        body["images"] = [{"url": data_uri(first_frame)}]
    task = call("POST", "/videos", body)
    tid = task.get("id") or task.get("task_id")
    if not tid:
        sys.exit(f"muse2api không trả id task: {json.dumps(task)[:300]}")
    waited = 0
    while waited < 1800:  # pool có thể xếp hàng lâu
        time.sleep(10)
        waited += 10
        st = call("GET", f"/videos/{tid}")
        status = st.get("status")
        if status in ("succeeded", "completed"):
            url = (st.get("result") or {}).get("url") or (st.get("data") or [{}])[0].get("url")
            download(url, dest)
            return dest
        if status in ("failed", "error", "cancelled"):
            sys.exit(f"Muse tạo clip thất bại: {json.dumps(st)[:300]}")
    sys.exit(f"Quá 30 phút chưa xong task {tid}")


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
    print(f"{len(todo)}/{len(items)} {'clip' if a.kind == 'video' else 'ảnh'} cần tạo qua {base_url()}")
    for n, p in todo:
        dest = os.path.join(a.out, f"{n:02d}.{ext}")
        t0 = time.time()
        if a.kind == "video":
            ff = None
            if a.first_frame_dir:
                ff = next((c for c in (os.path.join(a.first_frame_dir, f"{n:02d}.{e}") for e in ("jpg", "jpeg", "png", "webp"))
                           if os.path.exists(c)), None)
            gen_video(p, dest, a.duration, a.size, ff)
        else:
            gen_image(p, dest, a.size)
        print(f"  #{n:02d} -> {dest} ({time.time() - t0:.0f}s)", flush=True)


def cmd_check(a):
    try:
        res = call("GET", "/models", timeout=15)
        ids = [m.get("id") for m in res.get("data", [])]
        print(f"OK {base_url()}  models: {', '.join(i for i in ids if i) or '(không liệt kê)'}")
    except SystemExit as e:
        print(e)
        sys.exit(1)


def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    p = sub.add_parser("image")
    p.add_argument("prompt")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--size", default="16:9")
    p.set_defaults(fn=lambda a: print(gen_image(a.prompt, a.out, a.size)))
    p = sub.add_parser("batch")
    p.add_argument("prompts")
    p.add_argument("out")
    p.add_argument("--kind", choices=["video", "image"], default="video")
    p.add_argument("--duration", type=int, default=6)
    p.add_argument("--size", default="16:9")
    p.add_argument("--first-frame-dir")
    p.set_defaults(fn=cmd_batch)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
