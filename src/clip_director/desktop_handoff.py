#!/usr/bin/env python3
"""
desktop_handoff.py — Platziert Clue-Frame und Prompt für den nächsten Schritt auf dem Desktop.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

import json

try:
    import yaml
except ImportError:
    print("PyYAML nicht installiert.", file=sys.stderr)
    sys.exit(1)


def is_desktop_handoff_enabled(project_dir=None):
    """
    Prüft, ob der Desktop-Handoff-Modus aktiviert ist.
    Priorität:
    1. project.yaml -> settings.desktop_handoff_enabled
    2. config.json im Skill-Root -> einstellungen.desktop_handoff_enabled
    Standard: False (da Dashboard der primäre Arbeitsplatz ist)
    """
    # 1. Check project.yaml
    if project_dir:
        p_yaml = Path(project_dir) / "project.yaml"
        if p_yaml.exists():
            try:
                with open(p_yaml, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                p_settings = data.get("settings", {})
                if "desktop_handoff_enabled" in p_settings:
                    return bool(p_settings["desktop_handoff_enabled"])
            except Exception:
                pass

    # 2. Check skill config.json
    skill_root = Path(__file__).resolve().parent.parent
    config_file = skill_root / "config.json"
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                c_data = json.load(f)
            einst = c_data.get("einstellungen", {})
            if "desktop_handoff_enabled" in einst:
                return bool(einst["desktop_handoff_enabled"])
        except Exception:
            pass

    return False


def get_default_desktop():
    # OneDrive Desktop hat Vorrang (aktiver Windows Explorer Desktop bei Cloud-Sync)
    onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
    if onedrive_desktop.exists():
        return onedrive_desktop
    desktop = Path.home() / "Desktop"
    return desktop


def clean_desktop(desktop_path=None):
    desktop = Path(desktop_path or get_default_desktop())
    removed = 0
    for name in ["NEXT_SHOT_PROMPT.txt", "NEXT_SHOT_CLUEFRAME.png", "NEXT_SHOT_CLUEFRAME.jpg", "NEXT_SHOT_INFO.txt"]:
        target = desktop / name
        if target.exists():
            try:
                target.unlink()
                removed += 1
            except Exception as e:
                print(f"[WARNUNG] Konnte {target.name} nicht löschen: {e}")
    print(f"[OK] Desktop bereinigt ({removed} Handoff-Dateien entfernt).")


def handoff_step(project_dir, step_nr, desktop_path=None, force=False):
    project_path = Path(project_dir)
    if not force and not is_desktop_handoff_enabled(project_path):
        print(f"[INFO] Desktop-Handoff ist in config.json deaktiviert (Dashboard-Modus aktiv). Keine Dateien auf Desktop erzeugt.")
        return

    yaml_file = project_path / "project.yaml"
    if not yaml_file.exists():
        print(f"[FEHLER] Keine project.yaml in {project_path} gefunden.", file=sys.stderr)
        sys.exit(1)

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    shots = data.get("shots", [])
    target_shot = None
    prev_shot = None

    for s in shots:
        if s.get("step_nr") == step_nr:
            target_shot = s
        elif s.get("step_nr") == step_nr - 1:
            prev_shot = s

    if not target_shot:
        print(f"[FEHLER] Step {step_nr} nicht im Projekt gefunden (Max Steps: {len(shots)}).", file=sys.stderr)
        sys.exit(1)

    desktop = Path(desktop_path)
    desktop.mkdir(parents=True, exist_ok=True)

    # 1. Clue-Frame aus vorherigem Step kopieren
    clue_src = None
    if prev_shot and prev_shot.get("clue_frame"):
        clue_rel = prev_shot.get("clue_frame")
        clue_cand = project_path / clue_rel
        if clue_cand.exists():
            clue_src = clue_cand

    dest_frame = desktop / "NEXT_SHOT_CLUEFRAME.png"
    if clue_src:
        shutil.copy2(clue_src, dest_frame)
        print(f"[OK] Clue-Frame auf Desktop bereitgestellt: {dest_frame.name} (aus Step {step_nr - 1})")
    else:
        if dest_frame.exists():
            dest_frame.unlink()
        if step_nr == 1:
            print("[INFO] Step 1 ist der Eröffnungsshot (kein vorheriges Clue-Frame).")
        else:
            print(f"[HINWEIS] Kein Clue-Frame für Step {step_nr - 1} hinterlegt.")

    # 2. Prompt-Text & Audio-Direktiven formulieren
    active_v = target_shot.get("active_prompt_version", "v1")
    prompt_obj = next((p for p in target_shot.get("prompts", []) if p.get("version") == active_v), None)
    prompt_text = prompt_obj.get("text", "") if prompt_obj else ""

    p_buf = data.get("persistence_buffer", {})
    props_str = ", ".join([p.get("name") if isinstance(p, dict) else str(p) for p in p_buf.get("props", [])]) or "-"
    chars_str = ", ".join([c.get("name") if isinstance(c, dict) else str(c) for c in p_buf.get("characters", [])]) or "-"
    locs_str = ", ".join([l.get("name") if isinstance(l, dict) else str(l) for l in p_buf.get("locations", [])]) or "-"

    voice = target_shot.get("voice", {})
    directives = voice.get("directives", {})
    dir_de = directives.get("german") or (f'Spoken dialogue in German (clear voice): "{voice.get("source_text") or voice.get("text")}"' if voice.get("enabled") else "None")
    dir_en = directives.get("english") or (f'Spoken dialogue in English (clear voice): "{voice.get("translated_text_en")}"' if voice.get("translated_text_en") else "None")
    dir_silent = directives.get("silent") or "Silent video with ambient environmental sound only, strictly no human voice"

    content = f"""======================================================================
NEXT SHOT HANDOFF: STEP {step_nr} von {len(shots)}
Projekt: {data.get('project', {}).get('title', 'Clip')}
Slug: {target_shot.get('slug')}
Zeitbereich: {target_shot.get('start_sec')}s bis {target_shot.get('end_sec')}s ({target_shot.get('duration_sec')}s)
======================================================================

--- FILM- & KAMERAPARAMETER ---
Perspektive:       {target_shot.get('perspective')}
Kameraführung:     {target_shot.get('camera_movement')}
Beleuchtung/Farbe: {target_shot.get('lighting_color')}
Bewegungsstärke:   {target_shot.get('motion_intensity', 3)} / 10

--- PERSISTENZPUFFER (KONTINUITÄT) ---
Charaktere:  {chars_str}
Requisiten:  {props_str}
Orte/Kulisse: {locs_str}

======================================================================
>>> 1. BILD- & KAMERA-PROMPT (VERSION {active_v}) <<<
======================================================================

{prompt_text}

======================================================================
>>> 2. AUDIO- & SPRACH-OPTIONEN (MULTIMODAL: GEMINI / VEO / SORA) <<<
======================================================================
Wähle je nach gewünschtem Ergebnis eine Anweisung für den Video-Generator:

[OPTION A: DEUTSCHER O-TON / SPRACHE]
{dir_de}

[OPTION B: ENGLISCHE ÜBERSETZUNG / SPRACHE]
{dir_en}

[OPTION C: STUMM / NUR AMBIENT & SCORE (SPUR 1 MUTE)]
{dir_silent}

======================================================================
WORKFLOW-HINWEISE:
1. Falls 'NEXT_SHOT_CLUEFRAME.png' auf dem Desktop liegt, nutze es im
   Generator als Start-Bild (Image-to-Video).
2. Kopiere den Bild-Prompt und ggf. eine Audio-Option in das Textfeld.
3. Generiere den Clip und lade ihn herunter oder kopiere den Sharelink.
   - Bei Download: Der Hintergrund-Watcher importiert ihn automatisch!
   - Bei Sharelink: Füge die URL im Storyboard-Dashboard ein.
======================================================================
"""
    dest_prompt = desktop / "NEXT_SHOT_PROMPT.txt"
    with open(dest_prompt, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Prompt-Vorlage auf Desktop geschrieben: {dest_prompt}")


def main():
    parser = argparse.ArgumentParser(description="Handoff-Manager für Desktop-Dateien.")
    parser.add_argument("--project", default=".", help="Projektverzeichnis")
    parser.add_argument("--step", type=int, default=1, help="Schritt-Nummer für den Handoff")
    parser.add_argument("--clean", action="store_true", help="Bereinigt Handoff-Dateien vom Desktop")
    parser.add_argument("--force", action="store_true", help="Erzwingt Desktop-Handoff auch wenn in config.json deaktiviert")
    parser.add_argument("--desktop", default=None, help="Pfad zum Desktop")

    args = parser.parse_args()
    desktop_dir = args.desktop or get_default_desktop()

    if args.clean:
        clean_desktop(desktop_dir)
    else:
        handoff_step(args.project, args.step, desktop_dir, force=args.force)


if __name__ == "__main__":
    main()
