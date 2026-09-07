#!/usr/bin/env python3
r"""
start_cockpit.py — Startet das Dual-Pane Regie-Cockpit in Microsoft Edge.
Ablauf:
1. Startet bei Bedarf den lokalen Board-Server (Port 8765)
2. Rendert die aktuellen Cockpit- und Storyboard-HTML-Dateien
3. Öffnet Microsoft Edge als eigenständige Desktop-App mit aktivem CDP-Debugging
4. Legt eine Desktop-Verknüpfung 'STORYBOARD COCKPIT (Edge)' an
"""

import argparse
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DEFAULT_EDGE_PORT = 9222
DEFAULT_SERVER_PORT = 8765


def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def ensure_server_running(project_path, port=DEFAULT_SERVER_PORT):
    if is_port_in_use(port):
        print(f"[OK] Board-Server läuft bereits auf Port {port}.")
        return None

    print(f"[START] Starte Board-Server im Hintergrund auf Port {port}...")
    server_script = SCRIPT_DIR / "board_server.py"
    proc = subprocess.Popen(
        [sys.executable, "-u", str(server_script), "--project", str(project_path), "--port", str(port)],
        cwd=str(SKILL_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Warte bis Port offen ist
    for _ in range(15):
        time.sleep(0.4)
        if is_port_in_use(port):
            print(f"[OK] Board-Server erfolgreich gestartet (PID {proc.pid}).")
            return proc

    print("[WARNUNG] Server-Start konnte nicht innerhalb von 6s verifiziert werden.")
    return proc


def create_desktop_shortcut(url="http://localhost:8765/cockpit", edge_port=DEFAULT_EDGE_PORT):
    onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
    desktop = onedrive_desktop if onedrive_desktop.exists() else Path.home() / "Desktop"
    lnk_path = desktop / "STORYBOARD COCKPIT (Edge).lnk"
    user_data = Path.home() / ".gemini" / "antigravity" / "brain" / "edge_cockpit_profile"

    ps_cmd = f"""
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{lnk_path}')
    $Shortcut.TargetPath = '{DEFAULT_EDGE_PATH}'
    $Shortcut.Arguments = '--app="{url}" --remote-debugging-port={edge_port} --remote-allow-origins=* --user-data-dir="{user_data}" --no-first-run'
    $Shortcut.IconLocation = '{DEFAULT_EDGE_PATH},0'
    $Shortcut.Save()
    """
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[OK] Desktop-Shortcut (.lnk mit aktivem CDP) aktualisiert: {lnk_path.name}")
        old_url = desktop / "STORYBOARD COCKPIT (Edge).url"
        if old_url.exists():
            old_url.unlink()
    except Exception as e:
        print(f"[HINWEIS] Konnte LNK nicht anlegen: {e}")


def launch_edge_cockpit(project_name="sternenseufzer", edge_port=DEFAULT_EDGE_PORT, server_port=DEFAULT_SERVER_PORT):
    project_path = SKILL_ROOT / "projects" / project_name
    if not project_path.exists():
        print(f"[FEHLER] Projektverzeichnis {project_path} existiert nicht.", file=sys.stderr)
        sys.exit(1)

    # 1. HTML rendern
    try:
        from render_dashboard import render_project
        from render_cockpit import render_cockpit
        render_project(project_path)
        render_cockpit(project_path)
    except Exception as e:
        print(f"[WARNUNG] Rendering fehlgeschlagen: {e}")

    # 2. Server sicherstellen
    ensure_server_running(project_path, port=server_port)

    # 3. Desktop Shortcut
    cockpit_url = f"http://localhost:{server_port}/cockpit"
    create_desktop_shortcut(cockpit_url, edge_port=edge_port)

    # 4. Microsoft Edge starten
    if not Path(DEFAULT_EDGE_PATH).exists():
        print(f"[FEHLER] Microsoft Edge wurde unter {DEFAULT_EDGE_PATH} nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    user_data = Path.home() / ".gemini" / "antigravity" / "brain" / "edge_cockpit_profile"
    user_data.mkdir(parents=True, exist_ok=True)

    cmd = [
        DEFAULT_EDGE_PATH,
        f"--app={cockpit_url}",
        f"--remote-debugging-port={edge_port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data}",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1920,1080"
    ]

    print("=" * 65)
    print(f"[COCKPIT] Starte Microsoft Edge Regie-Cockpit...")
    print(f"[COCKPIT] App-URL: {cockpit_url}")
    print(f"[COCKPIT] CDP-Port: {edge_port}")
    print(f"[COCKPIT] Edge-Profil: {user_data}")
    print("=" * 65)

    proc = subprocess.Popen(cmd)
    print(f"[OK] Microsoft Edge gestartet (PID {proc.pid})!")
    return proc


def main():
    parser = argparse.ArgumentParser(description="Startet das Dual-Pane Storyboard Cockpit in Microsoft Edge.")
    parser.add_argument("--project", default="sternenseufzer", help="Projektname unter projects/")
    parser.add_argument("--edge-port", type=int, default=DEFAULT_EDGE_PORT, help="Edge CDP Port")
    parser.add_argument("--server-port", type=int, default=DEFAULT_SERVER_PORT, help="Board Server Port")

    args = parser.parse_args()
    launch_edge_cockpit(args.project, args.edge_port, args.server_port)


if __name__ == "__main__":
    main()
