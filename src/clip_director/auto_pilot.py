#!/usr/bin/env python3
"""
auto_pilot.py — Vollautonomer Produktions-Orchestrator für Storyboard-Projekte.
"""

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_PORT = 9222
DEFAULT_SERVER_PORT = 8765

try:
    import websocket
except ImportError:
    print("[FEHLER] 'websocket-client' fehlt.", file=sys.stderr)
    sys.exit(1)


def get_cowork_focus(server_port=DEFAULT_SERVER_PORT):
    try:
        url = f"http://localhost:{server_port}/api/cowork/focus"
        with urllib.request.urlopen(url, timeout=2.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def get_gemini_tab(port=DEFAULT_PORT):
    try:
        url = f"http://127.0.0.1:{port}/json/list"
        with urllib.request.urlopen(url, timeout=2.0) as resp:
            tabs = json.loads(resp.read().decode("utf-8"))
            return next((t for t in tabs if "gemini.google" in t.get("url", "").lower()), None)
    except Exception:
        return None


def query_gemini_state(ws_url):
    ws = websocket.create_connection(ws_url, timeout=5)
    expr = """
    (() => {
        const text = document.body.innerText || '';
        const isAnon = text.includes('Anmelden') || text.includes('Sign in') || text.includes('3.5 Flash-Lite');
        const editable = document.querySelector('rich-textarea div[contenteditable="true"]') ||
                         document.querySelector('div[contenteditable="true"]') ||
                         document.querySelector('textarea');
        const sendBtn = document.querySelector('button[aria-label*="Senden"]') ||
                        document.querySelector('button[aria-label*="Send"]') ||
                        document.querySelector('button.send-button') ||
                        document.querySelector('button[mat-icon-button]');
        return JSON.stringify({
            title: document.title,
            isAnonymous: isAnon,
            hasEditable: !!editable,
            currentText: editable ? editable.innerText.trim() : '',
            sendBtnAvailable: sendBtn ? !sendBtn.disabled : false
        });
    })()
    """
    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == 1:
            val = msg.get("result", {}).get("result", {}).get("value")
            ws.close()
            return json.loads(val) if val else {}


def inject_and_send(ws_url, prompt_text, auto_submit=True):
    ws = websocket.create_connection(ws_url, timeout=5)
    ws.send(json.dumps({"id": 10, "method": "Page.bringToFront"}))
    time.sleep(0.3)

    expr = f"""
    (() => {{
        const editable = document.querySelector('rich-textarea div[contenteditable="true"]') ||
                         document.querySelector('div[contenteditable="true"]') ||
                         document.querySelector('textarea');
        if (!editable) return {{ success: false, error: 'Eingabefeld nicht gefunden' }};

        editable.focus();
        editable.innerText = {json.dumps(prompt_text)};
        editable.dispatchEvent(new Event('input', {{ bubbles: true, cancelable: true }}));
        editable.dispatchEvent(new Event('change', {{ bubbles: true, cancelable: true }}));

        let submitted = false;
        if ({json.dumps(auto_submit)}) {{
            const sendBtn = document.querySelector('button[aria-label*="Senden"]') ||
                            document.querySelector('button[aria-label*="Send"]') ||
                            document.querySelector('button.send-button') ||
                            document.querySelector('button[mat-icon-button]');
            if (sendBtn && !sendBtn.disabled) {{
                sendBtn.click();
                submitted = true;
            }}
        }}

        return {{ success: true, submitted: submitted, textLen: prompt_text.length }};
    }})()
    """
    ws.send(json.dumps({"id": 20, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == 20:
            val = msg.get("result", {}).get("result", {}).get("value")
            ws.close()
            return val


def run_assembly(project_path):
    print("\n" + "=" * 65)
    print("🎬 [AUTOPILOT] ALLE SHOTS KOMPLETT! STARTE FINALE ASSEMBLY...")
    print("=" * 65)
    assemble_script = SCRIPT_DIR / "assemble.py"
    res = subprocess.run([sys.executable, str(assemble_script), "--project", str(project_path)], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)


def run_production_loop(project_name="sternenseufzer"):
    project_path = SKILL_ROOT / "projects" / project_name
    print("=" * 65)
    print(f"🚀 [AUTOPILOT] STARTE VOLLAUTONOME PRODUKTION FÜR: {project_name}")
    print("=" * 65)

    while True:
        focus = get_cowork_focus()
        if not focus:
            print("[AUTOPILOT] Warten auf Board-Server...")
            time.sleep(3)
            continue

        yaml_file = project_path / "project.yaml"
        import yaml
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        all_shots = data.get("shots", [])
        pending = [s for s in all_shots if not s.get("selected_take")]

        if not pending:
            print(f"\n[OK] Alle {len(all_shots)} Shots haben ein Hero-Video!")
            run_assembly(project_path)
            print("\n🎉 [FERTIG] Gesamtes Video erfolgreich produziert!")
            break

        current_target = pending[0]
        step_nr = current_target.get("step_nr")
        slug = current_target.get("slug")
        p_obj = (current_target.get("prompts") or [{}])[0]
        prompt = p_obj.get("text", "")

        print(f"\n▶️ [SHOT {step_nr}/4] Ziel: '{slug}' ({current_target.get('start_sec')}s–{current_target.get('end_sec')}s)")
        print(f"   Prompt: {prompt[:90]}...")

        gemini_tab = get_gemini_tab()
        if not gemini_tab:
            print("[WARNUNG] Kein Gemini-Tab gefunden. Bitte stelle sicher, dass Gemini in Edge geöffnet ist.")
            time.sleep(4)
            continue

        ws_url = gemini_tab.get("webSocketDebuggerUrl")
        state = query_gemini_state(ws_url)

        if state.get("isAnonymous"):
            print("=" * 65)
            print("⚠️  [GOOGLE LOGIN ERFORDERLICH]")
            print("   Gemini läuft im abgemeldeten Modus (3.5 Flash-Lite).")
            print("   Für die Veo-Videogenerierung ist ein Google-Login nötig.")
            print("   👉 Klicke im Edge-Fenster auf 'Anmelden'!")
            print("=" * 65)
            time.sleep(6)
            continue

        print(f"[CDP] Injiziere Prompt für Shot {step_nr} in Gemini...")
        inj_res = inject_and_send(ws_url, prompt, auto_submit=True)
        print(f"[CDP] Ergebnis: {inj_res}")
        print(f"[AUTOPILOT] Prompt abgesendet! Warte auf Fertigstellung & Download von Shot {step_nr}...")

        while True:
            time.sleep(3)
            with open(yaml_file, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
            shot_check = next((s for s in d.get("shots", []) if s.get("step_nr") == step_nr), None)
            if shot_check and shot_check.get("selected_take"):
                print(f"✅ [ERFOLG] Shot {step_nr} importiert! (Take: {shot_check.get('selected_take')})")
                break


def main():
    parser = argparse.ArgumentParser(description="Autonomer Produktions-Loop für Storyboards")
    parser.add_argument("--project", default="sternenseufzer", help="Projektname")
    args = parser.parse_args()
    run_production_loop(args.project)


if __name__ == "__main__":
    main()
