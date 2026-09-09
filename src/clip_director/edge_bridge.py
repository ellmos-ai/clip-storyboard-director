#!/usr/bin/env python3
r"""
edge_bridge.py — Schnittstelle zu Microsoft Edge über das Chrome DevTools Protocol (CDP).
Ermöglicht:
1. Statusprüfung der Edge-CDP-Verbindung (/json/list)
2. Auffinden und Öffnen von Generator-Tabs (z. B. Gemini, Runway, Kling)
3. Automatische Prompt-Injektion in das aktive Eingabefeld von Gemini Web
4. Optionales automatisches Absenden
"""

import argparse
import json
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_EDGE_PORT = 9222
DEFAULT_EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def check_edge_status(port=DEFAULT_EDGE_PORT):
    """Prüft, ob Edge auf dem Debugging-Port erreichbar ist."""
    import socket
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.2):
            pass
    except Exception:
        return {
            "connected": False,
            "error": "Port nicht aktiv",
            "port": port
        }

    try:
        url = f"http://127.0.0.1:{port}/json/version"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=0.8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "connected": True,
                "browser": data.get("Browser", "Microsoft Edge"),
                "protocol": data.get("Protocol-Version", "1.3"),
                "port": port
            }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
            "port": port
        }


def list_edge_tabs(port=DEFAULT_EDGE_PORT):
    """Gibt alle offenen Browser-Tabs zurück."""
    try:
        url = f"http://127.0.0.1:{port}/json/list"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            tabs = json.loads(resp.read().decode("utf-8"))
            return [t for t in tabs if t.get("type") == "page"]
    except Exception:
        return []


def run_node_cdp_script(script_content):
    """Führt ein Node.js ESM-Skript aus (nutzt das in Node 22+ integrierte WebSocket)."""
    temp_dir = Path.home() / ".gemini" / "antigravity" / "brain" / "edge_cdp_runner"
    temp_dir.mkdir(parents=True, exist_ok=True)
    runner_file = temp_dir / "_run_bridge.mjs"
    runner_file.write_text(script_content, encoding="utf-8")

    proc = subprocess.run(
        ["node", str(runner_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    return proc.stdout, proc.stderr, proc.returncode


def open_or_focus_tab(target_url, port=DEFAULT_EDGE_PORT):
    """Öffnet einen neuen Tab oder fokussiert einen bestehenden."""
    try:
        tabs = list_edge_tabs(port)
        for t in tabs:
            if target_url.lower() in t.get("url", "").lower():
                ws_url = t.get("webSocketDebuggerUrl")
                if ws_url:
                    node_script = f"""
                    const ws = new WebSocket({json.dumps(ws_url)});
                    await new Promise(r => ws.onopen = r);
                    ws.send(JSON.stringify({{ id: 1, method: 'Page.bringToFront' }}));
                    await new Promise(r => setTimeout(r, 200));
                    ws.close();
                    """
                    run_node_cdp_script(node_script)
                return {"status": "ok", "action": "focused", "tab": t}

        new_url = f"http://127.0.0.1:{port}/json/new?{urllib.parse.quote(target_url)}"
        req = urllib.request.Request(new_url, method="PUT")
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"status": "ok", "action": "created", "tab": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def inject_prompt_to_gemini(prompt_text, port=DEFAULT_EDGE_PORT, auto_submit=False):
    """
    Sucht den Gemini-Tab in Edge und injiziert den Prompt-Text
    in das Rich-Text-Eingabefeld.
    """
    tabs = list_edge_tabs(port)
    gemini_tab = next((t for t in tabs if "gemini.google" in t.get("url", "").lower()), None)

    if not gemini_tab:
        # Versuche Tab automatisch zu öffnen
        open_or_focus_tab("https://gemini.google.com", port=port)
        time.sleep(3.5)
        tabs = list_edge_tabs(port)
        gemini_tab = next((t for t in tabs if "gemini.google" in t.get("url", "").lower()), None)

    if not gemini_tab:
        return {
            "status": "error",
            "message": "Kein offener Gemini-Tab in Edge gefunden und automatisches Öffnen fehlgeschlagen. Bitte stelle sicher, dass Edge mit Port 9222 läuft."
        }

    ws_url = gemini_tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return {"status": "error", "message": "Keine WebSocket-URL für den Gemini-Tab verfügbar."}

    node_script = f"""
const ws = new WebSocket({json.dumps(ws_url)});
let reqId = 1;
const pending = new Map();

ws.onmessage = (msg) => {{
  const data = JSON.parse(msg.data);
  if (data.id && pending.has(data.id)) {{
    pending.get(data.id)(data);
    pending.delete(data.id);
  }}
}};

await new Promise(r => ws.onopen = r);

function send(method, params = {{}}) {{
  const id = reqId++;
  return new Promise(resolve => {{
    pending.set(id, resolve);
    ws.send(JSON.stringify({{ id, method, params }}));
  }});
}}

await send('Page.enable');
await send('Runtime.enable');
await send('Page.bringToFront');

const promptText = {json.dumps(prompt_text)};
const autoSubmit = {json.dumps(auto_submit)};

const evalRes = await send('Runtime.evaluate', {{
  expression: `
    (() => {{
      const editable = document.querySelector('rich-textarea div[contenteditable="true"]') ||
                       document.querySelector('div[contenteditable="true"]') ||
                       document.querySelector('textarea');
                       
      if (!editable) {{
        return {{ success: false, error: 'Eingabefeld auf gemini.google.com nicht gefunden.' }};
      }}

      editable.focus();
      editable.innerText = promptText;
      editable.dispatchEvent(new Event('input', {{ bubbles: true, cancelable: true }}));
      editable.dispatchEvent(new Event('change', {{ bubbles: true, cancelable: true }}));

      let submitted = false;
      if (autoSubmit) {{
        const sendBtn = document.querySelector('button[aria-label*="Senden"]') ||
                        document.querySelector('button[aria-label*="Send"]') ||
                        document.querySelector('button.send-button') ||
                        document.querySelector('button[mat-icon-button]');
        if (sendBtn && !sendBtn.disabled) {{
          sendBtn.click();
          submitted = true;
        }}
      }}

      return {{ success: true, submitted: submitted, textLength: promptText.length }};
    }})()
  `,
  returnByValue: true
}});

const result = evalRes.result?.result?.value;
console.log('INJECT_RESULT:' + JSON.stringify(result));

ws.close();
"""

    stdout, stderr, code = run_node_cdp_script(node_script)

    for line in stdout.splitlines():
        if line.startswith("INJECT_RESULT:"):
            res_json = json.loads(line.replace("INJECT_RESULT:", ""))
            if res_json.get("success"):
                return {
                    "status": "ok",
                    "message": "Prompt erfolgreich in Gemini übertragen!",
                    "details": res_json
                }
            else:
                return {
                    "status": "error",
                    "message": res_json.get("error", "Unbekannter Fehler bei Injektion"),
                    "details": res_json
                }

    return {
        "status": "error",
        "message": f"Keine Antwort vom Injektions-Skript erhalten. StdErr: {stderr[:200]}"
    }


def main():
    parser = argparse.ArgumentParser(description="Edge CDP Bridge für Storyboard Cockpit")
    parser.add_argument("--status", action="store_true", help="Prüft den Verbindungsstatus zu Edge")
    parser.add_argument("--list-tabs", action="store_true", help="Listet offene Browser-Tabs auf")
    parser.add_argument("--inject-gemini", help="Injiziert Text in den offenen Gemini-Tab")
    parser.add_argument("--submit", action="store_true", help="Löst nach Injektion sofort den Sende-Button aus")
    parser.add_argument("--port", type=int, default=DEFAULT_EDGE_PORT, help="Edge CDP Port")

    args = parser.parse_args()

    if args.status:
        st = check_edge_status(args.port)
        print(json.dumps(st, indent=2))
    elif args.list_tabs:
        tabs = list_edge_tabs(args.port)
        print(f"Offene Tabs in Edge ({len(tabs)}):")
        for t in tabs:
            print(f" - [{t.get('id')[:6]}] {t.get('title')}: {t.get('url')}")
    elif args.inject_gemini:
        res = inject_prompt_to_gemini(args.inject_gemini, port=args.port, auto_submit=args.submit)
        print(json.dumps(res, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
