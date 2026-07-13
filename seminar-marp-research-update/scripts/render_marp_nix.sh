#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 DECK.md OUTPUT_DIR" >&2
  exit 2
fi

deck="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
output_dir="$(mkdir -p "$2" && cd "$2" && pwd)"
stem="$(basename "$deck" .md)"
staging="$(mktemp -d "$output_dir/.${stem}.render.XXXXXX")"
html="$staging/$stem.html"
pdf="$staging/$stem.pdf"
contact="$staging/$stem-contact-sheet.png"
pages="$staging/pages"
mkdir -p "$pages"
trap 'rm -rf -- "$staging"' EXIT

nix run nixpkgs#marp-cli -- "$deck" --html --allow-local-files -o "$html"
nix run nixpkgs#marp-cli -- "$deck" --pdf --allow-local-files -o "$pdf"
fontconfig="$(nix build --no-link --print-out-paths nixpkgs#fontconfig.out)"
font_root="$(nix build --no-link --print-out-paths nixpkgs#dejavu_fonts)"
font="$font_root/share/fonts/truetype/DejaVuSans.ttf"
nix shell 'nixpkgs#poppler-utils' nixpkgs#imagemagick nixpkgs#fontconfig -c bash -c '
  set -euo pipefail
  pdf="$1"
  pages="$2"
  contact="$3"
  fontconfig="$4"
  font="$5"
  export FONTCONFIG_FILE="$fontconfig/etc/fonts/fonts/fonts.conf"
  expected="$(pdfinfo "$pdf" | awk "\$1 == \"Pages:\" { print \$2 }")"
  test -n "$expected"
  pdftoppm -png -r 100 "$pdf" "$pages/page" >/dev/null 2>&1
  actual="$(find "$pages" -maxdepth 1 -name "page-*.png" | wc -l | tr -d " ")"
  test "$actual" -eq "$expected"
  magick montage "$pages"/page-*.png -font "$font" -thumbnail 400x225 -tile 4x \
    -geometry +8+8 -background "#d8d8d8" "$contact"
' bash "$pdf" "$pages" "$contact" "$fontconfig" "$font"

test -s "$html"
test -s "$pdf"
test -s "$contact"

final_html="$output_dir/$stem.html"
final_pdf="$output_dir/$stem.pdf"
final_contact="$output_dir/$stem-contact-sheet.png"
mv -f -- "$html" "$final_html"
mv -f -- "$pdf" "$final_pdf"
mv -f -- "$contact" "$final_contact"
printf '%s\n%s\n%s\n' "$final_html" "$final_pdf" "$final_contact"
