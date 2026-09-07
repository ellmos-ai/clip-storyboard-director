#!/usr/bin/env python3
"""
storyboard_init.py — Initialisiert ein neues Clip-Projekt mit berechnetem Shot-Raster.
"""

import argparse
import math
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML nicht installiert. Bitte 'pip install pyyaml' ausführen.", file=sys.stderr)
    sys.exit(1)


def create_project(name, title, total_duration, step_duration, aspect_ratio="16:9", fps=24, resolution="1080p", out_dir=None):
    if not out_dir:
        out_dir = Path.cwd() / "projects" / name
    else:
        out_dir = Path(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    # Subordner anlegen
    subfolders = [
        "_inbox",
        "video",
        "frames",
        "voice",
        "prompts",
        "out",
        "audio/track1_invideo",
        "audio/track2_bed",
        "audio/track3_midi",
        "audio/track4_sfx"
    ]
    for sub in subfolders:
        (out_dir / sub).mkdir(parents=True, exist_ok=True)

    # Schrittzahl berechnen
    step_count = math.ceil(total_duration / step_duration)

    shots = []
    current_time = 0

    for i in range(1, step_count + 1):
        cur_duration = min(step_duration, total_duration - current_time)
        end_time = current_time + cur_duration

        shot = {
            "step_nr": i,
            "slug": f"shot-{i:02d}",
            "type": "video",
            "start_sec": current_time,
            "end_sec": end_time,
            "duration_sec": cur_duration,
            "genre_style": "Standard (vom Projekt)",
            "lighting_color": "Natürliche Ausleuchtung",
            "perspective": "Medium Shot, Augenhöhe",
            "camera_movement": "Statisch oder sanftes Dolly",
            "motion_intensity": 3,
            "prompts": [
                {
                    "version": "v1",
                    "text": f"Szene {i}: Beschreibung für Shot {i:02d}...",
                    "diff": "Initialer Entwurf"
                }
            ],
            "active_prompt_version": "v1",
            "takes": [],
            "selected_take": None,
            "clue_frame": None,
            "audio": {
                "track1_invideo": "mute",
                "track2_bed": None,
                "track3_midi": None,
                "track4_sfx": None,
                "transition_video": "cut" if i < step_count else "fade_to_black",
                "transition_audio": "crossfade_1s" if i < step_count else "fade_out_1s"
            },
            "voice": {
                "enabled": False,
                "speaker": "en-US-AndrewNeural",
                "text": None,
                "rendered_file": None,
                "lip_sync": False
            }
        }
        shots.append(shot)
        current_time = end_time

    project_data = {
        "project": {
            "name": name,
            "title": title or name,
            "created": "2026-09-07",
            "total_duration_sec": total_duration,
            "step_duration_sec": step_duration,
            "calculated_steps": step_count,
            "aspect_ratio": aspect_ratio,
            "fps": fps,
            "resolution": resolution,
            "default_genre": "Cinematic",
            "lighting_mood": "Konsistente filmische Farbstimmung"
        },
        "persistence_buffer": {
            "props": [],
            "characters": [],
            "locations": [],
            "objects": []
        },
        "audio_defaults": {
            "master_loudness_target_lufs": -16,
            "voice_actor": "en-US-AndrewNeural",
            "background_bed_level_lufs": -36
        },
        "shots": shots,
        "branches": []
    }

    yaml_path = out_dir / "project.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(project_data, f, allow_unicode=True, sort_keys=False)

    print(f"[OK] Projekt '{name}' erfolgreich initialisiert unter:")
    print(f"     {out_dir}")
    print(f"     -> {step_count} Shots berechnet ({total_duration}s Gesamtlänge @ {step_duration}s Steps)")
    print(f"     -> Konfigurationsdatei: {yaml_path}")
    return yaml_path


def main():
    parser = argparse.ArgumentParser(description="Initialisiert ein neues Clip-Storyboard-Projekt.")
    parser.add_argument("--name", required=True, help="Projekt-Slug (z. B. 'sci-fi-teaser')")
    parser.add_argument("--title", default="", help="Titel des Filmclips")
    parser.add_argument("--duration", type=int, default=30, help="Gesamtlänge in Sekunden (z. B. 30, 60)")
    parser.add_argument("--step", type=int, default=10, help="Step-Intervall in Sekunden (z. B. 5, 10, 15)")
    parser.add_argument("--aspect", default="16:9", help="Seitenverhältnis (16:9, 9:16, 1:1)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    parser.add_argument("--out-dir", default=None, help="Zielordner (Standard: ./projects/<name>)")

    args = parser.parse_args()
    create_project(
        name=args.name,
        title=args.title,
        total_duration=args.duration,
        step_duration=args.step,
        aspect_ratio=args.aspect,
        fps=args.fps,
        out_dir=args.out_dir
    )


if __name__ == "__main__":
    main()
