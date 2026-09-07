#!/usr/bin/env python3
"""
ingest.py — Überwacht Inbox/Projektroot, sortiert Takes ein, extrahiert Clue-Frames per ffmpeg und aktualisiert project.yaml.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML nicht installiert.", file=sys.stderr)
    sys.exit(1)


def extract_last_frame(video_path, output_png_path):
    """
    Extrahiert das exakt letzte Frame aus einer Videodatei mittels ffmpeg.
    """
    cmd = [
        "ffmpeg",
        "-sseof", "-0.2",
        "-i", str(video_path),
        "-update", "1",
        "-q:v", "2",
        str(output_png_path),
        "-y"
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and output_png_path.exists() and output_png_path.stat().st_size > 0:
            return True
        # Fallback auf -vframes 1
        fallback_cmd = [
            "ffmpeg",
            "-sseof", "-1",
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(output_png_path),
            "-y"
        ]
        res2 = subprocess.run(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res2.returncode == 0 and output_png_path.exists()
    except Exception as e:
        print(f"[WARNUNG] ffmpeg Frame-Extraktion fehlgeschlagen: {e}", file=sys.stderr)
        return False


def detect_step_from_filename(filename, shots):
    """
    Versucht anhand des Dateinamens die Step-Nummer zu erraten.
    """
    # Suche Muster wie shot02, shot-2, step2, step_02, s02
    match = re.search(r'(?:shot|step|s)[-_]?(\d+)', filename, re.IGNORECASE)
    if match:
        step_nr = int(match.group(1))
        if any(s.get("step_nr") == step_nr for s in shots):
            return step_nr

    # Fallback: erster Shot ohne gewählten Take
    for s in shots:
        if not s.get("takes") or not s.get("selected_take"):
            return s.get("step_nr")

    return 1


def process_inbox(project_dir, step_override=None, engine_name="ki-generator", auto_advance=True):
    project_path = Path(project_dir)
    yaml_file = project_path / "project.yaml"

    if not yaml_file.exists():
        print(f"[FEHLER] project.yaml nicht in {project_path} gefunden.", file=sys.stderr)
        sys.exit(1)

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    shots = data.get("shots", [])
    inbox_dir = project_path / "_inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    # Suche Dateien in _inbox und im Projekt-Root
    candidate_files = []
    for ext in ["*.mp4", "*.mov", "*.webm", "*.png", "*.jpg"]:
        candidate_files.extend(list(inbox_dir.glob(ext)))
        # Auch im Projekt-Root (ausserhalb bekannter Unterordner)
        for f in project_path.glob(ext):
            if f.is_file():
                candidate_files.append(f)

    if not candidate_files:
        print(f"[INFO] Keine neuen Mediendateien in '{inbox_dir}' oder '{project_path}' gefunden.")
        return

    processed_count = 0

    for media_file in candidate_files:
        if not media_file.exists():
            continue

        step_nr = step_override or detect_step_from_filename(media_file.name, shots)
        target_shot = next((s for s in shots if s.get("step_nr") == step_nr), None)

        if not target_shot:
            print(f"[WARNUNG] Konnte {media_file.name} keinem gültigen Step zuordnen. Überspringe.")
            continue

        existing_takes = target_shot.get("takes", [])
        take_nr = len(existing_takes) + 1
        take_id = f"v{take_nr:02d}"

        dest_ext = media_file.suffix.lower()
        new_filename = f"shot{step_nr:02d}_{take_id}{dest_ext}"
        dest_video = project_path / "video" / new_filename

        shutil.move(str(media_file), str(dest_video))
        print(f"[OK] Datei einsortiert: {media_file.name} -> video/{new_filename}")

        # Clue-Frame extrahieren (falls Video)
        clue_frame_rel = None
        if dest_ext in [".mp4", ".mov", ".webm"]:
            frame_filename = f"shot{step_nr:02d}_{take_id}_lastframe.png"
            frame_dest = project_path / "frames" / frame_filename
            if extract_last_frame(dest_video, frame_dest):
                clue_frame_rel = f"frames/{frame_filename}"
                print(f"[OK] Clue-Frame erfolgreich extrahiert: {clue_frame_rel}")
            else:
                print(f"[HINWEIS] Letzter Frame konnte nicht extrahiert werden.")
        elif dest_ext in [".png", ".jpg"]:
            # Standbild ist selbst das Clue-Frame
            clue_frame_rel = f"video/{new_filename}"

        # In project.yaml eintragen
        take_entry = {
            "id": take_id,
            "file": f"video/{new_filename}",
            "engine": engine_name,
            "notes": f"Auto-Ingest aus {media_file.name}"
        }
        existing_takes.append(take_entry)
        target_shot["takes"] = existing_takes

        # Wenn noch kein Take gewählt ist, diesen als Hero wählen
        if not target_shot.get("selected_take"):
            target_shot["selected_take"] = take_id
            if clue_frame_rel:
                target_shot["clue_frame"] = clue_frame_rel

        processed_count += 1

        # YAML speichern
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        # Handoff für Folgeschritt auslösen (nur wenn in config/project aktiviert)
        if auto_advance and step_nr < len(shots):
            next_step = step_nr + 1
            try:
                from desktop_handoff import handoff_step, get_default_desktop, is_desktop_handoff_enabled
                if is_desktop_handoff_enabled(project_path):
                    print(f"[INFO] Bereite automatischen Desktop-Handoff für Step {next_step} vor...")
                    handoff_step(project_path, next_step, get_default_desktop())
                else:
                    print(f"[INFO] Dashboard-Modus aktiv: Step {next_step} ist im Web-Board bereit (Desktop-Dateien übersprungen).")
            except Exception as e:
                print(f"[HINWEIS] Handoff-Aufruf fehlgeschlagen: {e}")

    print(f"\n[FERTIG] {processed_count} Datei(en) verarbeitet und in project.yaml aktualisiert.")


def main():
    parser = argparse.ArgumentParser(description="Ingest-Watcher für neue Video- und Asset-Dateien.")
    parser.add_argument("--project", default=".", help="Projektverzeichnis")
    parser.add_argument("--step", type=int, default=None, help="Erzwingt Zuweisung zu bestimmtem Step")
    parser.add_argument("--engine", default="ki-generator", help="Name der Generator-Engine (z.B. kling, runway)")
    parser.add_argument("--no-advance", action="store_true", help="Deaktiviert automatischen Folgeschritt-Handoff")

    args = parser.parse_args()
    process_inbox(
        project_dir=args.project,
        step_override=args.step,
        engine_name=args.engine,
        auto_advance=not args.no_advance
    )


if __name__ == "__main__":
    main()
