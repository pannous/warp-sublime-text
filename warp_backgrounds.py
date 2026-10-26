"""Builds the color schemes Warp.sublime-settings names: Sublime's default day and night schemes with warp's own
backgrounds and the warp rules of this package's scheme overlays. Rebuilt into Packages/User whenever the plugin loads,
so they follow updates of the default schemes."""
import os

import sublime

DAY_BACKGROUND = "#ffffff"
NIGHT_BACKGROUND = "#0a1028"
WARP_SCHEMES = {  # generated scheme: (base scheme, background)
    "Warp Day": ("Breakers", DAY_BACKGROUND),
    "Warp Night": ("Mariana", NIGHT_BACKGROUND),
}
BASE_SCHEMES = "Packages/Color Scheme - Default/{}.sublime-color-scheme"
WARP_OVERLAYS = "Packages/Warp/{}.sublime-color-scheme"


def warp_scheme(name, base, overlay, background):
    return dict(base, name=name,
                globals=dict(base.get("globals", {}), background=background),
                rules=base.get("rules", []) + overlay.get("rules", []))


def load_scheme(path):
    try:
        return sublime.decode_value(sublime.load_resource(path))
    except (IOError, ValueError):
        return {}


def plugin_loaded():
    user_folder = os.path.join(sublime.packages_path(), "User")
    for name, (base_name, background) in WARP_SCHEMES.items():
        base = load_scheme(BASE_SCHEMES.format(base_name))
        if not base:
            print("warp_backgrounds: default scheme {} not found, {} not built".format(base_name, name))
            continue
        scheme = warp_scheme(name, base, load_scheme(WARP_OVERLAYS.format(base_name)), background)
        path = os.path.join(user_folder, name + ".sublime-color-scheme")
        text = sublime.encode_value(scheme, True)
        if not os.path.exists(path) or open(path, encoding="utf-8").read() != text:
            with open(path, "w", encoding="utf-8") as file:
                file.write(text)
