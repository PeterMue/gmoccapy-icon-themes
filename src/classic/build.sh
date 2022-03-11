#!/usr/bin/env bash

THEME_NAME="classic"

pushd "$(dirname "$(realpath "$0")")" || exit
BASE_PATH=$(pwd)
TARGET_BASE="$BASE_PATH/../../target"
#TEMP_DIR="$TARGET_BASE/temp/$THEME_NAME"
TARGET_DIR="$TARGET_BASE/$THEME_NAME"
popd || exit

function do_clean() {
  rm -rf "$TARGET_DIR"
}

function do_compose() {
  mkdir -p "$TARGET_DIR"

  SIZES=( 16 24 32 48 )

  # create size-x-size folders
  for size in "${SIZES[@]}"; do
    mkdir -p "$TARGET_DIR/${size}x${size}/actions"
  done
  mkdir -p "$TARGET_DIR/scalable/actions"

  # rescale pixel images
  for file in "$BASE_PATH"/img/*.png; do
    filename=$(basename "$file")
    src_size=$(identify "$file" | awk '{ print $3 }' | cut -d "x" -f 1)

    for target_size in "${SIZES[@]}"; do
      # check source resolution (prevent upscaling)
      if [ "$src_size" -ge "$target_size" ]; then
        dimension="${target_size}x${target_size}"
        convert "$file" -resize "$dimension" "$TARGET_DIR/${target_size}x${target_size}/actions/$filename" || exit
        echo "resized $filename to $dimension"
      else
        echo "skipped $filename (no upscaling from ${src_size}x${src_size} to $dimension)"
      fi
    done
  done

  # copy scalable images
  cp "$BASE_PATH"/svg/*.svg "$TARGET_DIR/scalable/actions"
}

function do_index() {
  mkdir -p "$TARGET_DIR"
  cp -v "$BASE_PATH/index.theme" "$TARGET_DIR/index.theme"
}

function do_license() {
  mkdir -p "$TARGET_DIR"
  echo "Goal license: nothing to do yet"
}

function do_install() {
  if [ ! -d "$1" ]; then
    echo "Goal install must be followed by installation directory: install <install_dir>"
    exit
  fi
  dest="$1/$THEME_NAME"
  rm -rf "$dest"
  cp -r "$TARGET_DIR" "$dest"
  echo "installed to ${dest}"
}

if [[ $# -gt 0 ]]; then
  while [[ $# -gt 0 ]]; do
    case $1 in
      clean)
        clean=1
        shift # past argument
        ;;
      index)
        index=1
        shift # past argument
        ;;
      license)
        license=1
        shift # past argument
        ;;
      compose)
        compose=1
        shift # past argument
        ;;
      install)
        install=1
        install_dir="$2"
        shift # past argument
        shift
        ;;
      -*|--*)
        echo "Unknown option $1"
        ;;
      *)
        shift # past argument
        ;;
    esac
  done
else
  # default goals
  clean=1
  compose=1
  index=1
  license=1
fi

# run goals
if [ "$clean" == "1" ]; then
  do_clean
fi
if [ "$compose" == "1" ]; then
  do_compose
fi
if [ "$index" == "1" ]; then
  do_index
fi
if [ "$license" == "1" ]; then
  do_license
fi
if [ "$install" == "1" ]; then
  do_install "$install_dir"
fi
