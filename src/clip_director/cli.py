#!/usr/bin/env python3
r"""
cli.py — Zentrale Kommandozeilenschnittstelle für clip-storyboard-director.
Befehl: clip-director
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Fix Windows console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from clip_director import __version__


def cmd_doctor(args):
    """Prüft die System- und Tool-Voraussetzungen."""
    print("=" * 65)
    print(f"🩺 [clip-director doctor] Systemprüfung (v{__version__})")
    print("=" * 65)

    # 1. FFmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        print(f"✅ FFmpeg & FFprobe: GEFUNDEN ({ffmpeg_path})")
    else:
        print("❌ FFmpeg oder FFprobe: FEHLT im System-PATH!")

    # 2. Python-Version
    print(f"✅ Python: {sys.version.split()[0]} ({sys.executable})")

    # 3. edge-tts
    try:
        import edge_tts
        print("✅ edge-tts: INSTALLIERT")
    except ImportError:
        print("⚠️ edge-tts: Nicht installiert (pip install edge-tts)")

    # 4. PyYAML
    try:
        import yaml
        print("✅ PyYAML: INSTALLIERT")
    except ImportError:
        print("❌ PyYAML: FEHLT (pip install pyyaml)")

    # 5. Browser Automation (websocket-client)
    try:
        import websocket
        print("✅ websocket-client: INSTALLIERT")
    except ImportError:
        print("⚠️ websocket-client: FEHLT (pip install websocket-client)")

    # 6. Microsoft Edge
    edge_paths = [
        Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Microsoft/Edge/Application/msedge.exe"
    ]
    edge_found = any(p.exists() for p in edge_paths)
    if edge_found:
        print("✅ Microsoft Edge: GEFUNDEN")
    else:
        print("⚠️ Microsoft Edge: Standardpfad nicht gefunden")

    print("=" * 65)


def cmd_init(args):
    """Initialisiert ein neues Storyboard-Projekt."""
    from clip_director.storyboard_init import create_project
    create_project(
        name=args.name,
        title=getattr(args, "title", "") or args.name,
        total_duration=args.duration,
        step_duration=args.step,
        out_dir=getattr(args, "out_dir", None)
    )


def cmd_serve(args):
    """Startet den interaktiven Board-Server."""
    from clip_director.board_server import run_server
    run_server(args.project, port=args.port, enable_watcher=not args.no_watcher)


def cmd_cockpit(args):
    """Startet das Dual-Pane Storyboard-Cockpit in Microsoft Edge."""
    from clip_director.start_cockpit import start_cockpit
    start_cockpit(args.project, port=args.port)


def cmd_autopilot(args):
    """Startet den Autopiloten für browsergestützte Videogenerierung."""
    from clip_director.auto_pilot import run_production_loop
    proj_name = Path(args.project).name
    run_production_loop(proj_name)


def cmd_assemble(args):
    """Führt den finalen Master-Schnitt aus."""
    from clip_director.assemble import assemble_project
    assemble_project(args.project)


def cmd_ingest(args):
    """Verarbeitet Takes aus dem _inbox-Ordner."""
    from clip_director.ingest import process_inbox
    process_inbox(args.project, auto_advance=True)


def cmd_render(args):
    """Rendert Storyboard- und Cockpit-HTML."""
    from clip_director.render_dashboard import render_project
    from clip_director.render_cockpit import render_cockpit
    render_project(args.project)
    render_cockpit(args.project)


def main():
    parser = argparse.ArgumentParser(
        prog="clip-director",
        description="Local-first AI Storyboard Director & Video Pipeline Controller"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Verfügbare Befehle")

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Systemumgebung und Abhängigkeiten prüfen")
    p_doctor.set_defaults(func=cmd_doctor)

    # init
    p_init = subparsers.add_parser("init", help="Neues Storyboard-Projekt initialisieren")
    p_init.add_argument("name", help="Name des neuen Projekts (z. B. mein_clip)")
    p_init.add_argument("--title", default="", help="Titel des Filmclips")
    p_init.add_argument("--duration", type=int, default=30, help="Gesamtlaufzeit in Sekunden (Standard: 30)")
    p_init.add_argument("--step", type=int, default=10, help="Dauer pro Shot in Sekunden (Standard: 10)")
    p_init.add_argument("--out-dir", default=None, help="Zielverzeichnis (Standard: ./projects/<name>)")
    p_init.set_defaults(func=cmd_init)

    # serve
    p_serve = subparsers.add_parser("serve", help="Interaktiven Board-Server starten")
    p_serve.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    p_serve.add_argument("--port", type=int, default=8765, help="Port (Standard: 8765)")
    p_serve.add_argument("--no-watcher", action="store_true", help="Download-Watcher deaktivieren")
    p_serve.set_defaults(func=cmd_serve)

    # cockpit
    p_cockpit = subparsers.add_parser("cockpit", help="Cockpit im Edge-Browser starten")
    p_cockpit.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    p_cockpit.add_argument("--port", type=int, default=8765, help="Port (Standard: 8765)")
    p_cockpit.set_defaults(func=cmd_cockpit)

    # autopilot
    p_autopilot = subparsers.add_parser("autopilot", help="Autonomen Produktions-Loop starten")
    p_autopilot.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    p_autopilot.set_defaults(func=cmd_autopilot)

    # assemble
    p_assemble = subparsers.add_parser("assemble", help="Master-Video schneiden und mastern")
    p_assemble.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    p_assemble.set_defaults(func=cmd_assemble)

    # ingest
    p_ingest = subparsers.add_parser("ingest", help="Eingegangene Clips aus _inbox verarbeiten")
    p_ingest.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    p_ingest.set_defaults(func=cmd_ingest)

    # render
    p_render = subparsers.add_parser("render", help="Dashboard & Cockpit HTML neu rendern")
    p_render.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    p_render.set_defaults(func=cmd_render)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
