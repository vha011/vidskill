#!/usr/bin/env bash
# Dùng: bash skills-v2/_shared/scripts/new-project.sh <explained-geo-map|explained-data-finance|...> <slug> [thư-mục-herk-edit-kit]
set -euo pipefail
SKILL="${1:?thiếu tên skill}"; SLUG="${2:?thiếu slug}"; KIT="${3:-../herk-edit-kit}"
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
DEST="$KIT/video-projects/$SLUG"
[ -f "$HERE/$SKILL/template/index.html" ] || { echo "Không có template cho $SKILL"; exit 1; }
[ ! -e "$DEST" ] || { echo "$DEST đã tồn tại"; exit 1; }
mkdir -p "$DEST/assets/fonts" "$DEST/renders"
cp "$HERE/$SKILL/template/index.html" "$DEST/index.html"
cp "$HERE/_shared/gsap.min.js" "$DEST/assets/"
cp "$HERE"/_shared/fonts/*.ttf "$DEST/assets/fonts/"
cp "$HERE"/_shared/audio/*.wav "$DEST/assets/"
cp "$KIT/examples/starter/meta.json" "$KIT/examples/starter/hyperframes.json" "$DEST/"
echo "Đã tạo $DEST. Tiếp theo: cd $DEST && npx hyperframes lint"
