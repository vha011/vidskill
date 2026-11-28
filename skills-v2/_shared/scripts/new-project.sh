#!/usr/bin/env bash
# Dùng: bash skills-v2/_shared/scripts/new-project.sh <skill> <slug> [--theme=<tên>] [thư-mục-herk-edit-kit]
#   --theme=list  : liệt kê màu của skill (nếu skill có thư mục themes/)
# Mã nguồn dự án: <ROOT>/herk-edit-kit/video-projects/<slug>/
# Video xuất ra : <ROOT>/output/   (cùng cấp với repo vidskill, không nằm trong herk-edit-kit)
set -euo pipefail
THEME=""; ARGS=()
for a in "$@"; do case "$a" in --theme=*) THEME="${a#--theme=}";; *) ARGS+=("$a");; esac; done
SKILL="${ARGS[0]:?thiếu tên skill}"; SLUG="${ARGS[1]:-}"
HERE="$(cd "$(dirname "$0")/../.." && pwd)"          # skills-v2
REPO="$(cd "$HERE/.." && pwd)"                        # vidskill
KIT="${ARGS[2]:-$REPO/../herk-edit-kit}"
OUT="$REPO/../output"

if [ "$THEME" = "list" ]; then
  ls "$HERE/$SKILL/themes" 2>/dev/null | sed 's/\.css$//' || true; exit 0
fi
[ -n "$SLUG" ] || { echo "thiếu slug"; exit 1; }
[ -f "$HERE/$SKILL/template/index.html" ] || { echo "Không có template cho $SKILL"; exit 1; }
DEST="$KIT/video-projects/$SLUG"
[ ! -e "$DEST" ] || { echo "$DEST đã tồn tại"; exit 1; }

mkdir -p "$DEST/assets/fonts" "$OUT"
cp "$HERE/$SKILL/template/index.html" "$DEST/index.html"
cp "$HERE/_shared/gsap.min.js" "$DEST/assets/"
cp "$HERE"/_shared/fonts/*.ttf "$DEST/assets/fonts/"
cp "$HERE"/_shared/audio/*.wav "$DEST/assets/"
cp "$KIT/examples/starter/meta.json" "$KIT/examples/starter/hyperframes.json" "$DEST/"

if [ -n "$THEME" ]; then
  F="$HERE/$SKILL/themes/$THEME.css"
  [ -f "$F" ] || { echo "Không có màu '$THEME' cho $SKILL. Có: $(ls "$HERE/$SKILL/themes" 2>/dev/null | sed 's/\.css$//' | tr '\n' ' ')"; rm -rf "$DEST"; exit 1; }
  awk -v css="$(cat "$F")" '{sub(/<\/head>/, "<style id=\"theme\">" css "</style></head>")}1' "$DEST/index.html" > "$DEST/index.tmp" && mv "$DEST/index.tmp" "$DEST/index.html"
  echo "Đã áp dụng màu: $THEME"
fi

echo "Đã tạo $DEST"
echo "Lint  : cd \"$KIT\" && npx hyperframes lint video-projects/$SLUG"
echo "Render: cd \"$KIT\" && npx hyperframes render video-projects/$SLUG --output \"$OUT/$SLUG.mp4\""
