import shutil
import sys
import os
from shutil import rmtree, copyfile
from pathlib import Path
from _build_helper import Composer, Dimension

THEME_NAME = "material"
BASE_PATH = Path(__file__).parent.absolute()
TARGET_BASE = BASE_PATH.joinpath("../../target").resolve()
TEMP_DIR = TARGET_BASE.joinpath("temp", THEME_NAME)
TARGET_DIR = TARGET_BASE.joinpath(THEME_NAME)

DIMENSIONS = list(Dimension(s) for s in [16, 24, 32, 48])


def clean(dirs):
    """Delete each directory"""
    for dir in dirs:
        if dir.exists():
            rmtree(dir)
            print(f"deleted {dir}")


def compose_images():
    """Compose images"""

    composer = Composer(TARGET_DIR, TEMP_DIR)

    def svg(name):
        return Path(BASE_PATH).joinpath("svg", name)

    # ref
    ref_icons_svg = svg("ref_icons.inkscape.svg")
    composer.add("ref_all.symbolic.png",
                 src_file=ref_icons_svg,
                 context="actions",
                 layers=["origin", "all-arrows"]
                 )
    composer.add("unref_all.symbolic.png",
                 src_file=ref_icons_svg,
                 context="actions",
                 layers=["unref-all"]
                 )
    for axis in ["x", "y", "z", "a", "b", "c", "u", "v", "w"] + [str(i) for i in range(8)]:
        composer.add(f"ref_{axis}.symbolic.png",
                     src_file=ref_icons_svg,
                     context="actions",
                     layers=["origin", "up-right-arrow", axis]
                     )

    # translate
    translate_icons_svg = svg("translate_icons.inkscape.svg")
    for axis in ["x", "y", "z", "a", "b", "c", "u", "v", "w"]:
        composer.add(f"translate_{axis}.symbolic.png",
                     src_file=translate_icons_svg,
                     context="actions",
                     layers=["background", "question", axis]
                     )

    # touch off
    touch_icons_svg = svg("touch_icons.inkscape.svg")
    composer.add(f"touch_off.symbolic.png",
                 src_file=touch_icons_svg,
                 context="actions",
                 layers=["touch-off"]
                 )
    for axis in ["x", "y", "z", "a", "b", "c", "u", "v", "w"]:
        composer.add(f"touch_{axis}.symbolic.png",
                     src_file=touch_icons_svg,
                     context="actions",
                     layers=["background", axis]
                     )

    # power button & main switch
    power_icons_svg = svg("power_icons.inkscape.svg")
    for state in ["on", "off"]:
        composer.add(f"power_{state}.symbolic.png",
                     src_file=power_icons_svg,
                     context="actions",
                     layers=["background", state]
                     )

    main_switch_icons_svg = svg("main_switch_icons.inkscape.svg")
    composer.add(f"main_switch_off.symbolic.png",
                 src_file=main_switch_icons_svg,
                 context="actions",
                 layers=["active", "base"]
                 )
    composer.add(f"main_switch_on.symbolic.png",
                 src_file=main_switch_icons_svg,
                 context="actions",
                 layers=["idle"]
                 )

    # mode buttons
    mode_icons_svg = svg("mode_icons.inkscape.svg")
    for active in ["active", "inactive"]:
        for mode in ["manual", "mdi", "auto", "settings", "user_tabs"]:
            composer.add(f"mode_{mode}_{active}.symbolic.png",
                         src_file=mode_icons_svg,
                         context="actions",
                         layers=[active, mode]
                         )

    # back to app
    back_to_app_svg = svg("back_to_app.inkscape.svg")
    composer.add("back_to_app.symbolic.png",
                 src_file=back_to_app_svg,
                 context="actions",
                 layers=["base"]
                 )

    # logout
    logout_svg = svg("logout.inkscape.svg")
    composer.add("logout.symbolic.png",
                 src_file=logout_svg,
                 context="actions",
                 layers=["base"]
                 )

    # fullscreen
    fullscreen_icons_svg = svg("fullscreen_icons.inkscape.svg")
    for state in ["open", "close"]:
        composer.add(f"fullscreen_{state}.symbolic.png",
                     src_file=fullscreen_icons_svg,
                     context="actions",
                     layers=[state]
                     )

    # gremlin controls
    gremlin_control_icons_svg = svg("gremlin_control_icons.inkscape.svg")
    composer.add("toolpath.symbolic.png",
                 src_file=gremlin_control_icons_svg,
                 context="actions",
                 layers=["toolpath"]
                 )
    composer.add("clear.symbolic.png",
                 src_file=gremlin_control_icons_svg,
                 context="actions",
                 layers=["clear"]
                 )
    composer.add("dimensions.symbolic.png",
                 src_file=gremlin_control_icons_svg,
                 context="actions",
                 layers=["dimensions"]
                 )

    for zoom in ["zoom_in", "zoom_out"]:
        composer.add(f"{zoom}.symbolic.png",
                     src_file=gremlin_control_icons_svg,
                     context="actions",
                     layers=[zoom]
                     )

    composer.add(f"tool_axis_p.symbolic.png",
                 src_file=gremlin_control_icons_svg,
                 context="actions",
                 layers=["perspective_plane"]
                 )

    for axis in ["x", "y", "z"]:
        composer.add(f"tool_axis_{axis}.symbolic.png",
                     src_file=gremlin_control_icons_svg,
                     context="actions",
                     layers=["simple_plane", axis]
                     )

    composer.add(f"tool_axis_y_inv.symbolic.png",
                 src_file=gremlin_control_icons_svg,
                 context="actions",
                 layers=["simple_plane_inv", "y_inv"]
                 )

    # coolant controls
    coolant_icons_svg = svg("coolant_icons.inkscape.svg")
    for status in ["active", "inactive"]:
        for coolant in ["mist", "flood"]:
            composer.add(f"coolant_{coolant}_{status}.symbolic.png",
                         src_file=coolant_icons_svg,
                         context="actions",
                         layers=[f"{coolant}_{status}"]
                         )

    # spindle control icons
    spindle_icons_svg = svg("spindle_icons.inkscape.svg")
    for direction in ["left", "right"]:
        composer.add(f"spindle_{direction}.symbolic.png",
                     src_file=spindle_icons_svg,
                     context="actions",
                     layers=["spindle", "turn", direction]
                     )
        composer.add(f"spindle_{direction}_on.symbolic.png",
                     src_file=spindle_icons_svg,
                     context="actions",
                     layers=["spindle_on", "turn", direction]
                     )

    # spindle stop
    composer.add(f"spindle_stop_on.symbolic.png",
                 src_file=spindle_icons_svg,
                 context="actions",
                 layers=["spindle", "stop_on"]
                 )
    composer.add(f"spindle_stop.symbolic.png",
                 src_file=spindle_icons_svg,
                 context="actions",
                 layers=["spindle", "stop"]
                 )

    # jog speed
    jog_speed_svg = svg("jog_speed_icons.inkscape.svg")
    for speed in ["slow", "fast"]:
        composer.add(f"jog_speed_{speed}.symbolic.png",
                     src_file=jog_speed_svg,
                     context="actions",
                     layers=[speed]
                     )

    # single file for continuous jog speed
    composer.add(f"jog_continuous.symbolic.png",
                src_file=jog_speed_svg,
                context="actions",
                layers=["jog-continuous"]
                )

    # chevron
    chevron_icons_svg = svg("chevron_icons.inkscape.svg")
    for direction in ["left", "right", "up", "down"]:
        composer.add(f"chevron_{direction}.symbolic.png",
                     src_file=chevron_icons_svg,
                     context="actions",
                     layers=[direction]
                     )

    # auto menu icons
    auto_icons_svg = svg("auto_icons.inkscape.svg")
    for name in ["open_file", "refresh", "play", "stop", "pause", "pause_active", "step", "run_from_line",
                 "skip_optional_active", "skip_optional_inactive", "edit_code", "select_file"]:
        composer.add(f"{name}.symbolic.png",
                     src_file=auto_icons_svg,
                     context="actions",
                     layers=[name.replace("_", "-")]
                     )

    # folder icons
    folder_icons_svg = svg("folder_icons.inkscape.svg")
    for name in ["home_folder", "user_defined_folder"]:
        composer.add(f"{name}.symbolic.png",
                     src_file=folder_icons_svg,
                     context="actions",
                     layers=[name.replace("_", "-")]
                     )

    # edit icons
    edit_icons_svg = svg("edit_icons.inkscape.svg")
    for name in ["save", "save_as", "new_document", "keyboard", "keyboard_hide", "edit_undo", "edit_redo", "split_view", "comment"]:
        composer.add(f"{name}.symbolic.png",
                     src_file=edit_icons_svg,
                     context="actions",
                     layers=[name.replace("_", "-")]
                     )

    # tool
    tool_icons_svg = svg("tool_icons.inkscape.svg")
    for name in ["hsk_mill_tool", "mill_tool_change", "mill_tool_change_num", "mill_tool_set_num"]:
        composer.add(f"{name}.symbolic.png",
                     src_file=tool_icons_svg,
                     context="actions",
                     layers=[name.replace("_", "-")]
                     )

    # notification
    notification_icons_svg = svg("notification_icons.inkscape.svg")
    composer.add("window_close.symbolic.png",
                src_file=notification_icons_svg,
                context="actions",
                layers=["close"]
                )
    composer.add("dialog_information.symbolic.png",
                src_file=notification_icons_svg,
                context="status",
                layers=["info"]
                )
    composer.add("dialog_warning.symbolic.png",
                src_file=notification_icons_svg,
                context="status",
                layers=["warn"]
                )

    # compose all images
    composer.compose(DIMENSIONS)


def create_theme_index():
    """Create theme index file"""

    os.makedirs(TARGET_DIR, exist_ok=True)

    index = "index.theme"
    src = Path(BASE_PATH).joinpath(index)
    dest = copyfile(src, Path(TARGET_DIR).joinpath(index))
    if dest:
        print(f"copied {src} -> {dest}")


def copy_license_files():
    """Copy license files"""

    os.makedirs(TARGET_DIR, exist_ok=True)

    for file in ["LICENSE", "NOTICE"]:
        src = Path(BASE_PATH).joinpath(file)
        dest = copyfile(src, Path(TARGET_DIR).joinpath(file))
        if dest:
            print(f"copied {src} -> {dest}")


def build():
    """Default build steps"""

    clean([TARGET_DIR, TEMP_DIR])
    compose_images()
    clean([TEMP_DIR])
    create_theme_index()
    copy_license_files()


def install(install_dir):
    """Install to 'install_dir'"""
    dest = Path(install_dir).joinpath(THEME_NAME)
    clean([dest])
    dest = shutil.copytree(TARGET_DIR, dest)
    print(f"installed to {dest}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        build()
    else:
        if "clean" in sys.argv:
            clean([TARGET_DIR, TEMP_DIR])

        if "compose" in sys.argv:
            compose_images()

        if "index" in sys.argv:
            create_theme_index()

        if "license" in sys.argv:
            copy_license_files()

        if "install" in sys.argv:
            path_index = sys.argv.index("install") + 1
            if path_index >= len(sys.argv):
                print(f"Goal install must be followed by installation directory: install <install_dir>")
                sys.exit(1)
            install_dir = sys.argv[sys.argv.index("install") + 1]
            install(install_dir)
