#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 DECK.md OUTPUT_DIR" >&2
  exit 2
fi

deck="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
output_dir="$(mkdir -p "$2" && cd "$2" && pwd)"
stem="$(basename "$deck" .md)"
html="$output_dir/$stem.html"
pdf="$output_dir/$stem.pdf"
pages="$(mktemp -d "${TMPDIR:-/tmp}/marp-pages.XXXXXX")"
trap 'rm -rf -- "$pages"' EXIT

nix run nixpkgs#marp-cli -- "$deck" --html --allow-local-files -o "$html"
nix run nixpkgs#marp-cli -- "$deck" --pdf --allow-local-files -o "$pdf"
nix shell 'nixpkgs#poppler-utils' nixpkgs#imagemagick -c bash -c '
  set -euo pipefail
  pdf="$1"
  pages="$2"
  contact="$3"
  pdftoppm -png -r 100 "$pdf" "$pages/page" >/dev/null 2>&1
  magick montage "$pages"/page-*.png -thumbnail 400x225 -tile 4x \
    -geometry +8+8 -background "#d8d8d8" "$contact"
' bash "$pdf" "$pages" "$output_dir/$stem-contact-sheet.png"

test -s "$html"
test -s "$pdf"
test -s "$output_dir/$stem-contact-sheet.png"
printf '%s\n%s\n%s\n' "$html" "$pdf" "$output_dir/$stem-contact-sheet.png"
