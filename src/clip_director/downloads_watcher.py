#!/usr/bin/env python3
r"""
downloads_watcher.py — Überwacht den lokalen Download-Ordner (~/Downloads)
NUR während der aktiven Arbeit am Projekt.
Neue Videodateien werden automatisch erkannt, stabilisiert, in _inbox/ verschoben
und via ingest.py in das Storyboard übernommen.
"""

import argparse
import os
import shutil
import sys
import threading
import time
from pathlib import Path

# Lokale Module importieren
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

try:
    from ingest import process_inbox
    from render_dashboard import render_project
except ImportError:
    pass


class DownloadsWatcher:
    def __init__(self, project_dir, downloads_dir=None, poll_interval=2.0):
        self.project_dir = Path(project_dir).resolve()
        user_profile = os.environ.get("USERPROFILE") or str(Path.home())
        self.downloads_dir = Path(downloads_dir or (Path(user_profile) / "Downloads")).resolve()
        self.poll_interval = poll_interval
        self.active = False
        self.paused = False
        self.start_time = None
        self.processed_files = set()
        self.thread = None

    def start(self):
        if self.active:
            return
        self.active = True
        self.paused = False
        self.start_time = time.time()
        print(f"[DOWNLOADS-WATCHER] Gestartet! Überwache: {self.downloads_dir}")
        print(f"[DOWNLOADS-WATCHER] Ziel-Projekt: {self.project_dir.name}")
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def pause(self):
        self.paused = True
        print("[DOWNLOADS-WATCHER] Pausiert.")

    def resume(self):
        self.paused = False
        print("[DOWNLOADS-WATCHER] Fortgesetzt.")

    def toggle(self):
        self.paused = not self.paused
        state = "Pausiert" if self.paused else "Aktiv"
        print(f"[DOWNLOADS-WATCHER] Status gewechselt zu: {state}")
        return not self.paused

    def stop(self):
        self.active = False
        print("[DOWNLOADS-WATCHER] Beendet.")

    def is_file_stable(self, file_path, wait_seconds=1.5):
        """Prüft, ob die Datei noch heruntergeladen wird (z.B. Chrome .crdownload oder wachsende Dateigröße)."""
        if not file_path.exists():
            return False
        if file_path.name.endswith(".crdownload") or file_path.name.endswith(".tmp") or file_path.name.endswith(".part"):
            return False

        try:
            size1 = file_path.stat().st_size
            if size1 == 0:
                return False
            time.sleep(wait_seconds)
            size2 = file_path.stat().st_size
            return size1 == size2
        except Exception:
            return False

    def _run_loop(self):
        while self.active:
            if not self.paused and self.downloads_dir.exists():
                try:
                    for ext in ["*.mp4", "*.webm", "*.mov"]:
                        for f in self.downloads_dir.glob(ext):
                            if not f.is_file():
                                continue
                            if str(f) in self.processed_files:
                                continue

                            # Prüfe Erstellungs-/Änderungszeitpunkt (nur Dateien seit Start)
                            try:
                                mtime = f.stat().st_mtime
                                if mtime < self.start_time - 5:
                                    continue
                            except Exception:
                                continue

                            # Datei stabilisieren
                            print(f"[DOWNLOADS-WATCHER] Neuer Video-Download erkannt: {f.name}")
                            if not self.is_file_stable(f):
                                print(f"[DOWNLOADS-WATCHER] Warte auf Fertigstellung von {f.name}...")
                                continue

                            self.processed_files.add(str(f))
                            inbox = self.project_dir / "_inbox"
                            inbox.mkdir(parents=True, exist_ok=True)
                            dest = inbox / f.name

                            print(f"[DOWNLOADS-WATCHER] Verschiebe {f.name} nach _inbox...")
                            shutil.move(str(f), str(dest))

                            # Ingest & Re-render
                            try:
                                process_inbox(self.project_dir, auto_advance=True)
                                render_project(self.project_dir)
                                print(f"[DOWNLOADS-WATCHER] {f.name} erfolgreich in Storyboard integriert!")
                            except Exception as e:
                                print(f"[DOWNLOADS-WATCHER] Fehler bei Ingest: {e}")

                except Exception as e:
                    print(f"[DOWNLOADS-WATCHER] Loop-Fehler: {e}")

            time.sleep(self.poll_interval)


def main():
    parser = argparse.ArgumentParser(description="Überwacht den Download-Ordner für das aktive Storyboard-Projekt.")
    parser.add_argument("--project", default=".", help="Projektverzeichnis mit project.yaml")
    parser.add_argument("--downloads", default=None, help="Pfad zum Downloads-Ordner")

    args = parser.parse_args()
    watcher = DownloadsWatcher(args.project, args.downloads)
    watcher.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()


if __name__ == "__main__":
    main()
