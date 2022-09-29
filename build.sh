#!/usr/bin/env sh
cd "$(dirname "$(realpath "$0")")/src"
# build each icon theme like this:
# python3 -m ${THEME_DIR}.build $@
python3 -m material.build $@
python3 -m material_light.build $@
cd -
