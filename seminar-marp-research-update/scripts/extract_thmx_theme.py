#!/usr/bin/env python3
"""Extract the primary color and font scheme from an OOXML THMX file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"a": DRAWING_NS}


def extract_theme(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("theme/theme/theme1.xml"))

    color_scheme = root.find(".//a:clrScheme", NS)
    colors: dict[str, str] = {}
    if color_scheme is not None:
        for entry in color_scheme:
            value = next(iter(entry), None)
            if value is None:
                continue
            key = entry.tag.rsplit("}", 1)[-1]
            raw = value.attrib.get("val") or value.attrib.get("lastClr")
            if raw:
                colors[key] = f"#{raw.upper()}"

    fonts: dict[str, dict[str, str]] = {}
    for family in ("majorFont", "minorFont"):
        node = root.find(f".//a:{family}", NS)
        if node is None:
            continue
        fonts[family] = {
            child.tag.rsplit("}", 1)[-1]: child.attrib.get("typeface", "")
            for child in node
            if child.tag.rsplit("}", 1)[-1] in {"latin", "ea", "cs"}
        }

    return {
        "source": str(path.resolve()),
        "color_scheme": color_scheme.attrib.get("name") if color_scheme is not None else None,
        "colors": colors,
        "fonts": fonts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("theme", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = extract_theme(args.theme)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
