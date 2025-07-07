#!/usr/bin/env bash

mkdir -p _data
output="_data/icon-matrix.yml"

# Gather themes in a text file
echo "themes:" > "$output"
for theme in assets/themes/*; do
  theme_name=$(basename "$theme")
  theme_desc=$(grep -m 1 "Comment" "$theme/index.theme" | sed "s/^.*=//")
  echo "  - name: $theme_name" >> "$output"
  echo "    description: $theme_desc" >> "$output"
done
echo "icons:" >> "$output"

# Gather icon keys in a text file
tempfile="$(mktemp)"

find assets/themes -type f -name "*.png" | while read -r file; do
  base=$(basename "$file")
  name="${base%.symbolic.png}"
  name="${name%.png}"
  category=$(basename "$(dirname "$file")")
  echo "$category|$name" >> "$tempfile"
done

# Remove duplicates
sort -u "$tempfile" | while IFS="|" read -r category name; do
  echo "  - category: \"$category\"" >> "$output"
  echo "    name: \"$name\"" >> "$output"
  echo "    sizes:" >> "$output"
  for size in 16x16 24x24 32x32 48x48; do
    echo "      - size: \"$size\"" >> "$output"
    echo "        themes:" >> "$output"
    for theme in assets/themes/*; do
      theme_name=$(basename "$theme")
      found="missing"
      for variant in "$theme/$size/$category/$name.png" "$theme/$size/$category/$name.symbolic.png"; do
        if [ -f "$variant" ]; then
          found="$variant"
          break
        fi
      done
      echo "          $theme_name: \"$found\"" >> "$output"
    done
  done
done

rm "$tempfile"
