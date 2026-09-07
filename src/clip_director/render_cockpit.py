#!/usr/bin/env python3
r"""
render_cockpit.py — Rendert die Dual-Pane Cockpit-Oberfläche für das Storyboard.
"""

import argparse
import html
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML nicht installiert.", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR / "cockpit_template.html"


def render_cockpit(project_dir):
    project_path = Path(project_dir).resolve()
    yaml_file = project_path / "project.yaml"

    if not yaml_file.exists():
        print(f"[FEHLER] project.yaml nicht in {project_path} gefunden.", file=sys.stderr)
        sys.exit(1)

    if not TEMPLATE_PATH.exists():
        print(f"[FEHLER] Template {TEMPLATE_PATH} nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    proj = data.get("project", {})
    title = proj.get("title") or proj.get("name") or "Storyboard"
    proj_name = proj.get("name", "master")
    master_file = f"{proj_name}_master.mp4"
    master_exists = (project_path / master_file).exists()
    master_card_style = "" if master_exists else "display: none;"

    rendered = (template
                .replace("{project_title}", html.escape(title))
                .replace("{master_video_file}", html.escape(master_file))
                .replace("{master_card_style}", master_card_style))

    out_file = project_path / "cockpit.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] Storyboard Cockpit HTML erfolgreich generiert: {out_file}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Rendert die Cockpit-Oberfläche.")
    parser.add_argument("--project", default=".", help="Pfad zum Projektverzeichnis")
    args = parser.parse_args()
    render_cockpit(args.project)


if __name__ == "__main__":
    main()
