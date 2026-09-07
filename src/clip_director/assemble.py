#!/usr/bin/env python3
r"""
assemble.py — Finaler Video-Assembler für Storyboard-Projekte.
Fügt alle Hero-Takes (Shot 1–4) mit Audio, Voiceover und Übergängen
zu einem finalen Master-Video (sternenseufzer_master.mp4) zusammen.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("[FEHLER] PyYAML fehlt.", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent


def ensure_voice_audio(project_path, shot):
    """Erzeugt via edge-tts die deutsche Sprecherstimme, falls noch keine Audiodatei vorliegt."""
    voice = shot.get("voice", {})
    if not voice.get("enabled"):
        return None

    step_nr = shot.get("step_nr", 1)
    text = voice.get("source_text") or voice.get("text") or ""
    if not text:
        return None

    voice_dir = project_path / "voice"
    voice_dir.mkdir(parents=True, exist_ok=True)
    voice_file = voice_dir / f"shot{step_nr:02d}_tts.mp3"

    if not voice_file.exists():
        speaker = voice.get("speaker") or "de-DE-ConradNeural"
        print(f"[ASSEMBLE] Generiere Sprecherstimme für Shot {step_nr} ({speaker})...")
        try:
            cmd = [sys.executable, "-m", "edge_tts", "--voice", speaker, "--text", text, "--write-media", str(voice_file)]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[OK] Voiceover gespeichert: {voice_file.name}")
        except Exception as e:
            print(f"[WARNUNG] Konnte edge-tts nicht ausführen: {e}")
            return None

    return voice_file


def assemble_project(project_path):
    project_dir = Path(project_path).resolve()
    yaml_file = project_dir / "project.yaml"

    if not yaml_file.exists():
        print(f"[FEHLER] {yaml_file} nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    proj = data.get("project", {})
    proj_name = proj.get("name", "master")
    shots = data.get("shots", [])

    print("=" * 65)
    print(f"🎬 [ASSEMBLE] Starte Master-Schnitt für: {proj.get('title', proj_name)}")
    print("=" * 65)

    valid_clips = []
    for s in shots:
        step_nr = s.get("step_nr")
        takes = s.get("takes", [])
        sel_id = s.get("selected_take")
        hero_take = next((t for t in takes if t.get("id") == sel_id), None)
        if not hero_take or not hero_take.get("file"):
            print(f"[FEHLER] Shot {step_nr} hat noch kein Hero-Video! Bitte erst alle Shots komplettieren.", file=sys.stderr)
            return None

        video_path = project_dir / hero_take.get("file")
        if not video_path.exists():
            print(f"[FEHLER] Videodatei {video_path} nicht gefunden!", file=sys.stderr)
            return None

        voice_audio = ensure_voice_audio(project_dir, s)
        valid_clips.append({
            "step_nr": step_nr,
            "video": video_path,
            "voice": voice_audio,
            "duration": s.get("duration_sec", 10),
            "transition": s.get("audio", {}).get("transition_video", "dissolve_1s")
        })

    print(f"[ASSEMBLE] {len(valid_clips)} Shots verifiziert. Erstelle Schnittliste...")

    # Concat-Liste für FFmpeg
    concat_txt = project_dir / "_concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in valid_clips:
            # Pfad mit forward slashes
            p_str = str(c["video"]).replace("\\", "/")
            f.write(f"file '{p_str}'\n")

    out_video = project_dir / f"{proj_name}_master.mp4"

    # 1. Video-Stitch via FFmpeg concat demuxer
    temp_stitched = project_dir / "_temp_stitched.mp4"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(temp_stitched)
    ]

    print("[ASSEMBLE] Führe Video-Clips zusammen...")
    res = subprocess.run(cmd_concat, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FEHLER] FFmpeg Concat fehlgeschlagen: {res.stderr[:300]}", file=sys.stderr)
        return None

    # 2. Voiceover & Audio-Mischung
    # Erstelle vollständigen Voiceover-Track
    voice_clips = [c["voice"] for c in valid_clips if c["voice"]]
    if voice_clips and len(voice_clips) == len(valid_clips):
        print("[ASSEMBLE] Mische deutsche Sprecherstimme mit Video...")
        # Baue Filter für Voiceover-Timing: Jede Stimme startet zur jeweiligen Shot-Zeit
        filter_inputs = ["-i", str(temp_stitched)]
        filter_parts = []
        for idx, c in enumerate(valid_clips):
            filter_inputs.extend(["-i", str(c["voice"])])
            delay_ms = idx * 10 * 1000  # 10s pro Shot
            filter_parts.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms},volume=1.25[a{idx+1}]")

        mix_inputs = "".join([f"[a{i+1}]" for i in range(len(valid_clips))])
        filter_complex = f"[0:a]volume=0.35[bg];{';'.join(filter_parts)};[bg]{mix_inputs}amix=inputs={len(valid_clips)+1}:duration=first:dropout_transition=2:normalize=0[aout]"

        cmd_mix = [
            "ffmpeg", "-y",
            *filter_inputs,
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "256k",
            "-shortest",
            str(out_video)
        ]

        try:
            res_mix = subprocess.run(cmd_mix, capture_output=True, text=True)
            if res_mix.returncode == 0:
                print(f"[OK] Voiceover erfolgreich gemischt!")
                if temp_stitched.exists():
                    temp_stitched.unlink()
            else:
                print(f"[HINWEIS] Amix-Filter fehlgeschlagen, nutze Video-Originalton: {res_mix.stderr[:200]}")
                if out_video.exists():
                    out_video.unlink()
                temp_stitched.rename(out_video)
        except Exception as e:
            print(f"[HINWEIS] Audio-Mischung übersprungen: {e}")
            temp_stitched.rename(out_video)
    else:
        if out_video.exists():
            out_video.unlink()
        temp_stitched.rename(out_video)

    if concat_txt.exists():
        concat_txt.unlink()

    print("=" * 65)
    print(f"🎉 [FERTIG] Master-Video erfolgreich exportiert:")
    print(f"   -> {out_video}")
    print(f"   -> Größe: {out_video.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 65)
    return out_video


def main():
    parser = argparse.ArgumentParser(description="Master Video Assembler")
    parser.add_argument("--project", default="projects/sternenseufzer", help="Pfad zum Projektverzeichnis")
    args = parser.parse_args()
    assemble_project(args.project)


if __name__ == "__main__":
    main()
