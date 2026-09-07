#!/usr/bin/env python3
r"""
board_server.py — Lokaler interaktiver Server für das Storyboard-Dashboard.
Unterstützt:
1. Automatische Überwachung des Download-Ordners (während der aktiven Session)
2. Abholen von Clips via Gemini Sharelink oder Video-URL (/api/fetch-link)
3. Drag & Drop von Video-Takes direkt auf Shot-Karten (/api/upload-clip)
4. Live-Sprecheraufnahmen direkt im Browser (/api/upload-voice)
5. Umschalten von In-Video Track-1 Audio (keep/mute) (/api/shot/audio-toggle)
"""

import argparse
import io
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

# Windows UTF-8 Output fix
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Lokale Skripte importieren
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

try:
    import yaml
    from ingest import process_inbox
    from render_dashboard import render_project
    from render_cockpit import render_cockpit
    from link_resolver import fetch_link_to_file
    from downloads_watcher import DownloadsWatcher
    from edge_bridge import check_edge_status, inject_prompt_to_gemini, open_or_focus_tab
except ImportError as e:
    print(f"[WARNUNG] Module konnten nicht geladen werden: {e}", file=sys.stderr)

GLOBAL_WATCHER = None


class StoryboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, project_dir=None, **kwargs):
        self.project_dir = Path(project_dir).resolve()
        super().__init__(*args, directory=str(self.project_dir), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ["/", "/index.html"]:
            self.path = "/storyboard.html"
            return super().do_GET()

        if parsed.path in ["/cockpit", "/cockpit.html"]:
            self.path = "/cockpit.html"
            return super().do_GET()

        if parsed.path == "/api/watcher/status":
            global GLOBAL_WATCHER
            is_active = GLOBAL_WATCHER.active if GLOBAL_WATCHER else False
            is_paused = GLOBAL_WATCHER.paused if GLOBAL_WATCHER else False
            dir_str = str(GLOBAL_WATCHER.downloads_dir) if GLOBAL_WATCHER else ""
            self.send_json_response({
                "active": is_active,
                "paused": is_paused,
                "directory": dir_str
            })
            return

        if parsed.path == "/api/edge/status":
            self.send_json_response(check_edge_status())
            return

        if parsed.path == "/api/cowork/focus":
            self.handle_cowork_focus()
            return

        if parsed.path == "/api/cowork/receipts":
            self.handle_cowork_receipts()
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/api/upload-clip":
            self.handle_upload_clip(params)
        elif parsed.path == "/api/upload-voice":
            self.handle_upload_voice(params)
        elif parsed.path == "/api/fetch-link":
            self.handle_fetch_link(params)
        elif parsed.path == "/api/watcher/toggle":
            self.handle_watcher_toggle()
        elif parsed.path == "/api/shot/audio-toggle":
            self.handle_audio_toggle(params)
        elif parsed.path == "/api/edge/inject-prompt":
            self.handle_edge_inject(params)
        elif parsed.path == "/api/edge/open-provider":
            self.handle_edge_open_provider(params)
        elif parsed.path == "/api/cowork/apply-offer":
            self.handle_cowork_apply_offer()
        elif parsed.path == "/api/open-folder":
            self.handle_open_folder()
        elif parsed.path == "/api/assemble":
            self.handle_assemble()
        elif parsed.path == "/api/handoff-editor":
            self.handle_handoff_editor()
        else:
            self.send_error(404, "Endpoint nicht gefunden")

    def handle_fetch_link(self, params):
        try:
            step_nr = int(params.get("step", [1])[0])
            url = params.get("url", [""])[0]

            if not url:
                # Prüfe ob im Body gesendet
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length > 0:
                    body = json.loads(self.rfile.read(content_length).decode("utf-8"))
                    url = body.get("url", "")
                    step_nr = int(body.get("step", step_nr))

            if not url:
                self.send_json_response({"status": "error", "message": "Keine URL übergeben"}, status_code=400)
                return

            print(f"[BOARD-SERVER] Hole Video aus Link für Step {step_nr}: {url}")
            inbox = self.project_dir / "_inbox"
            inbox.mkdir(parents=True, exist_ok=True)
            temp_file = inbox / f"fetched_shot{step_nr:02d}.mp4"

            # Resolver ausführen
            fetch_link_to_file(url, temp_file)

            # Ingest ausführen
            process_inbox(self.project_dir, step_override=step_nr, auto_advance=True)

            # Dashboard neu rendern
            render_project(self.project_dir)

            self.send_json_response({
                "status": "ok",
                "message": f"Video für Step {step_nr} erfolgreich aus Link importiert und verarbeitet.",
                "step": step_nr
            })

        except Exception as e:
            print(f"[BOARD-SERVER] Fehler bei Link-Fetch: {e}", file=sys.stderr)
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_watcher_toggle(self):
        global GLOBAL_WATCHER
        if GLOBAL_WATCHER:
            is_running = GLOBAL_WATCHER.toggle()
            state_text = "Aktiv" if is_running else "Pausiert"
            self.send_json_response({"status": "ok", "state": state_text, "running": is_running})
        else:
            self.send_json_response({"status": "error", "message": "Kein Watcher aktiv"}, status_code=500)

    def handle_audio_toggle(self, params):
        try:
            step_nr = int(params.get("step", [1])[0])
            yaml_file = self.project_dir / "project.yaml"
            if not yaml_file.exists():
                self.send_json_response({"status": "error", "message": "project.yaml fehlt"}, status_code=404)
                return

            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            new_state = "mute"
            for s in data.get("shots", []):
                if s.get("step_nr") == step_nr:
                    if not s.get("audio"):
                        s["audio"] = {}
                    curr = s["audio"].get("track1_invideo", "mute")
                    new_state = "keep" if curr == "mute" else "mute"
                    s["audio"]["track1_invideo"] = new_state

            with open(yaml_file, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)

            render_project(self.project_dir)
            self.send_json_response({
                "status": "ok",
                "step": step_nr,
                "track1_invideo": new_state,
                "message": f"In-Video Spur 1 für Step {step_nr} ist jetzt: {new_state}"
            })

        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_upload_clip(self, params):
        try:
            step_nr = int(params.get("step", [1])[0])
            content_length = int(self.headers.get("Content-Length", 0))
            raw_filename = params.get("filename", [f"upload_shot{step_nr:02d}.mp4"])[0]
            original_filename = unquote(raw_filename)

            inbox = self.project_dir / "_inbox"
            inbox.mkdir(parents=True, exist_ok=True)

            file_data = self.rfile.read(content_length)
            dest_path = inbox / original_filename
            with open(dest_path, "wb") as f:
                f.write(file_data)

            # Ingest ausführen
            process_inbox(self.project_dir, step_override=step_nr, auto_advance=True)

            # Dashboard neu rendern
            render_project(self.project_dir)

            response = {
                "status": "ok",
                "message": f"Clip für Step {step_nr} erfolgreich empfangen und verarbeitet.",
                "step": step_nr
            }
            self.send_json_response(response)

        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_upload_voice(self, params):
        try:
            step_nr = int(params.get("step", [1])[0])
            content_length = int(self.headers.get("Content-Length", 0))

            voice_dir = self.project_dir / "voice"
            voice_dir.mkdir(parents=True, exist_ok=True)

            raw_file = voice_dir / f"shot{step_nr:02d}_user_voice.webm"
            mp3_file = voice_dir / f"shot{step_nr:02d}_user_voice.mp3"

            # Audio-Stream speichern
            audio_data = self.rfile.read(content_length)
            with open(raw_file, "wb") as f:
                f.write(audio_data)

            # In MP3 konvertieren falls ffmpeg verfügbar
            saved_rel_path = f"voice/shot{step_nr:02d}_user_voice.mp3"
            try:
                subprocess.run(
                    ["ffmpeg", "-i", str(raw_file), "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", str(mp3_file), "-y"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
                )
            except Exception:
                saved_rel_path = f"voice/shot{step_nr:02d}_user_voice.webm"

            # In project.yaml eintragen
            yaml_file = self.project_dir / "project.yaml"
            if yaml_file.exists():
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                for s in data.get("shots", []):
                    if s.get("step_nr") == step_nr:
                        if not s.get("voice"):
                            s["voice"] = {}
                        s["voice"]["enabled"] = True
                        s["voice"]["speaker"] = "Lukas (Live-Aufnahme)"
                        s["voice"]["rendered_file"] = saved_rel_path

                with open(yaml_file, "w", encoding="utf-8") as f:
                    yaml.dump(data, f, allow_unicode=True, sort_keys=False)

            # Dashboard neu rendern
            render_project(self.project_dir)

            response = {
                "status": "ok",
                "message": f"Sprecheraufnahme für Step {step_nr} erfolgreich gespeichert.",
                "file": saved_rel_path,
                "step": step_nr
            }
            self.send_json_response(response)

        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_edge_open_provider(self, params):
        url = params.get("url", ["https://gemini.google.com"])[0]
        res = open_or_focus_tab(url)
        self.send_json_response(res)

    def handle_edge_inject(self, params):
        try:
            yaml_file = self.project_dir / "project.yaml"
            if not yaml_file.exists():
                self.send_json_response({"status": "error", "message": "project.yaml nicht gefunden"}, status_code=404)
                return

            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            shots = data.get("shots", [])
            # Target Step ermitteln
            step_param = params.get("step", [None])[0]
            if step_param:
                step_nr = int(step_param)
                target_shot = next((s for s in shots if s.get("step_nr") == step_nr), None)
            else:
                # Nächster offener Shot ohne hero take
                target_shot = next((s for s in shots if not s.get("selected_take")), shots[0] if shots else None)

            if not target_shot:
                self.send_json_response({"status": "error", "message": "Kein gültiger Shot gefunden"}, status_code=404)
                return

            step_nr = target_shot.get("step_nr")
            active_v = target_shot.get("active_prompt_version", "v1")
            p_obj = next((p for p in target_shot.get("prompts", []) if p.get("version") == active_v), None)
            prompt_text = p_obj.get("text", "") if p_obj else ""

            # Sprache / Direktive auswählen
            lang_param = params.get("lang", ["de"])[0]
            voice = target_shot.get("voice", {})
            directives = voice.get("directives", {})

            if lang_param == "de":
                audio_dir = directives.get("german") or (f'Spoken dialogue in German (clear voice): "{voice.get("source_text") or voice.get("text")}"' if voice.get("enabled") else "")
            elif lang_param == "en":
                audio_dir = directives.get("english") or (f'Spoken dialogue in English (clear voice): "{voice.get("translated_text_en")}"' if voice.get("translated_text_en") else "")
            elif lang_param == "silent":
                audio_dir = directives.get("silent") or "Silent video with ambient environmental sound only, strictly no human voice"
            else:
                audio_dir = ""

            full_prompt = prompt_text
            if audio_dir:
                full_prompt += f"\n\n{audio_dir}"

            res = inject_prompt_to_gemini(full_prompt, auto_submit=False)
            res["step"] = step_nr
            res["lang"] = lang_param
            self.send_json_response(res)
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_cowork_focus(self):
        try:
            yaml_file = self.project_dir / "project.yaml"
            if not yaml_file.exists():
                self.send_json_response({"status": "error", "message": "project.yaml nicht gefunden"}, status_code=404)
                return

            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            shots = data.get("shots", [])
            target_shot = next((s for s in shots if not s.get("selected_take")), shots[0] if shots else {})
            step_nr = target_shot.get("step_nr", 1)
            active_v = target_shot.get("active_prompt_version", "v1")
            p_obj = next((p for p in target_shot.get("prompts", []) if p.get("version") == active_v), {})

            packet = {
                "protocolVersion": "cowork.v1",
                "targetId": f"shot_{step_nr}",
                "step_nr": step_nr,
                "slug": target_shot.get("slug", ""),
                "timeframe": f"{target_shot.get('start_sec', 0)}s-{target_shot.get('end_sec', 10)}s",
                "active_prompt": p_obj.get("text", ""),
                "clue_frame": target_shot.get("clue_frame"),
                "voice": target_shot.get("voice", {}),
                "capabilities": ["suggest_prompt", "import_video", "set_audio_mode"],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.send_json_response(packet)
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_cowork_receipts(self):
        log_file = self.project_dir / "receipts.log"
        receipts = []
        if log_file.exists():
            for line in log_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        receipts.append(json.loads(line))
                    except Exception:
                        pass
        self.send_json_response({"status": "ok", "count": len(receipts), "receipts": receipts[-20:]})

    def handle_cowork_apply_offer(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length).decode("utf-8")) if content_length > 0 else {}
            step_nr = int(body.get("step", 1))
            offer = body.get("offer", {})

            yaml_file = self.project_dir / "project.yaml"
            if not yaml_file.exists():
                self.send_json_response({"status": "error", "message": "project.yaml nicht gefunden"}, status_code=404)
                return

            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            shots = data.get("shots", [])
            target_shot = next((s for s in shots if s.get("step_nr") == step_nr), None)
            if not target_shot:
                self.send_json_response({"status": "error", "message": f"Step {step_nr} nicht gefunden"}, status_code=404)
                return

            action = offer.get("action")
            receipt_id = f"rcpt_{int(time.time())}_{step_nr}"
            receipt_entry = {
                "receiptId": receipt_id,
                "step_nr": step_nr,
                "action": action,
                "offer": offer,
                "authorizedBy": "human_click_receipt",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            if action == "suggest_prompt" and offer.get("prompt"):
                prompts = target_shot.get("prompts", [])
                v_num = len(prompts) + 1
                new_v = f"v{v_num}"
                prompts.append({
                    "version": new_v,
                    "text": offer.get("prompt"),
                    "diff": offer.get("summary") or "Cowork Offer Prompt"
                })
                target_shot["prompts"] = prompts
                target_shot["active_prompt_version"] = new_v

            elif action == "set_audio_mode" and offer.get("mode"):
                if not target_shot.get("audio"):
                    target_shot["audio"] = {}
                target_shot["audio"]["track1_invideo"] = "keep" if offer.get("mode") in ["german", "english", "keep"] else "mute"

            elif action == "import_video" and offer.get("url"):
                inbox = self.project_dir / "_inbox"
                inbox.mkdir(parents=True, exist_ok=True)
                temp_file = inbox / f"cowork_shot{step_nr:02d}.mp4"
                fetch_link_to_file(offer.get("url"), temp_file)
                process_inbox(self.project_dir, step_override=step_nr, auto_advance=True)

            with open(yaml_file, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)

            log_file = self.project_dir / "receipts.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(receipt_entry, ensure_ascii=False) + "\n")

            render_project(self.project_dir)

            self.send_json_response({
                "status": "ok",
                "receiptId": receipt_id,
                "message": f"Cowork Offer für Step {step_nr} erfolgreich angewendet.",
                "details": receipt_entry
            })
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_open_folder(self):
        try:
            yaml_file = self.project_dir / "project.yaml"
            data = {}
            if yaml_file.exists():
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            proj_name = data.get("project", {}).get("name", "master")
            master_file = self.project_dir / f"{proj_name}_master.mp4"
            if master_file.exists():
                subprocess.Popen(["explorer.exe", f"/select,{str(master_file)}"])
            else:
                subprocess.Popen(["explorer.exe", str(self.project_dir)])
            self.send_json_response({"status": "ok", "message": "Explorer erfolgreich geöffnet"})
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_assemble(self):
        try:
            from assemble import assemble_project
            out_file = assemble_project(self.project_dir)
            render_project(self.project_dir)
            render_cockpit(self.project_dir)
            self.send_json_response({
                "status": "ok",
                "message": "Master-Video erfolgreich assembliert",
                "file": out_file.name if out_file else None
            })
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def handle_handoff_editor(self):
        try:
            yaml_file = self.project_dir / "project.yaml"
            data = {}
            if yaml_file.exists():
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            proj_name = data.get("project", {}).get("name", "master")
            master_file = self.project_dir / f"{proj_name}_master.mp4"
            if not master_file.exists():
                self.send_json_response({"status": "error", "message": "Master-Video existiert noch nicht. Bitte zuerst assemblieren."}, status_code=400)
                return

            editor_dir = Path(os.environ.get("AI_MEDIA_EDITOR_DIR", "C:/_Local_DEV/repos/ai-media-editor")).resolve()
            editor_script = editor_dir / "editor.py"
            if not editor_script.exists():
                self.send_json_response({"status": "error", "message": f"ai-media-editor nicht gefunden unter {editor_dir}"}, status_code=404)
                return

            cmd = [sys.executable, str(editor_script), "prepare", str(master_file), "--mode", "8", "--project", proj_name]
            proc = subprocess.Popen(cmd, cwd=str(editor_dir))
            self.send_json_response({
                "status": "ok",
                "message": f"Master-Video erfolgreich an ai-media-editor (UC8) übergeben (PID {proc.pid}).",
                "project": proj_name,
                "editor_dir": str(editor_dir)
            })
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status_code=500)

    def send_json_response(self, data, status_code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def run_server(project_dir, port=8765, enable_watcher=True):
    global GLOBAL_WATCHER
    project_path = Path(project_dir).resolve()
    handler = lambda *args, **kwargs: StoryboardHandler(*args, project_dir=project_path, **kwargs)

    if enable_watcher:
        GLOBAL_WATCHER = DownloadsWatcher(project_path)
        GLOBAL_WATCHER.start()

    server = ThreadingHTTPServer(("localhost", port), handler)
    print("=" * 65)
    print(f"[BOARD-SERVER] Server aktiv für Projekt: {project_path.name}")
    print(f"[BOARD-SERVER] URL: http://localhost:{port}")
    if GLOBAL_WATCHER:
        print(f"[BOARD-SERVER] Download-Watcher: AKTIV auf {GLOBAL_WATCHER.downloads_dir}")
    print("=" * 65)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server wird beendet...")
    finally:
        if GLOBAL_WATCHER:
            GLOBAL_WATCHER.stop()
        server.server_close()
        print("[INFO] Server und Watcher sauber gestoppt.")


def main():
    parser = argparse.ArgumentParser(description="Startet den interaktiven Storyboard-Server.")
    parser.add_argument("--project", required=True, help="Pfad zum Projektverzeichnis mit project.yaml")
    parser.add_argument("--port", type=int, default=8765, help="Port für den HTTP-Server (Standard: 8765)")
    parser.add_argument("--no-watcher", action="store_true", help="Deaktiviert den automatischen Download-Watcher")

    args = parser.parse_args()
    run_server(args.project, args.port, enable_watcher=not args.no_watcher)


if __name__ == "__main__":
    main()
