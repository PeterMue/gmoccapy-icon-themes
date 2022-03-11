#!/usr/bin/env sh

THEME_NAME="material-light"
THEME_COMMENT="Material icon theme for gmoccapy (optimized for light themes)"

BASE_COLOR="#212121"
SUCCESS_COLOR="#00c853"
WARN_COLOR="#ffd600"
ERROR_COLOR="#dd2c00"

pushd "$(dirname "$(realpath "$0")")"

# derive build script
sed -e "s/\"material\"/\"$THEME_NAME\"/g" -e "s/\.symbolic\.png/\.png/g" ../material/build.py > build.py

# derive index.theme
sed -e "s/^Name=\(.*\)$/Name=$THEME_NAME/g" -e "s/^Comment=\(.*\)$/Comment=$THEME_COMMENT/g" ../material/index.theme > index.theme

# derive SVGs
for svg in ../material/svg/*.svg; do
  FILENAME=$(basename $svg)
  sed -e "s/#000000/$BASE_COLOR/g" -e "s/#ff0000/$SUCCESS_COLOR/g" -e "s/#00ff00/$WARN_COLOR/g" -e "s/#0000ff/$ERROR_COLOR/g" $svg > "svg/$FILENAME"
done

popd