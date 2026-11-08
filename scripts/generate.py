#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.colorscheme from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def roles(variant):
    """Map each role to "r,g,b"; a role missing from the palette raises KeyError later."""
    return {
        role: ",".join(map(str, color["rgb"]))
        for color in variant["colors"].values()
        for role in color["usage"]
    }


def scheme(name, r):
    sections = {
        "Background": r["ui.bg"],
        "BackgroundFaint": r["ui.bg"],
        "BackgroundIntense": r["ui.bg"],
        "Foreground": r["ui.fg"],
        "ForegroundFaint": r["ui.fg_dim"],
        "ForegroundIntense": r["term.bright_white"],
    }
    for i, c in enumerate(ANSI):
        sections[f"Color{i}"] = r[f"term.{c}"]
        sections[f"Color{i}Faint"] = r[f"term.{c}"]
        sections[f"Color{i}Intense"] = r[f"term.bright_{c}"]
    out = [f"[{s}]\nColor={v}\n" for s, v in sorted(sections.items())]
    out.append(
        "[General]\nBlur=false\nColorRandomization=false\n"
        f"Description=Kanagawa {name}\nFillStyle=Tile\nOpacity=1\nWallpaper=\n"
    )
    return "\n".join(out)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.colorscheme"
        out.parent.mkdir(exist_ok=True)
        out.write_text(scheme(v.capitalize(), roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
