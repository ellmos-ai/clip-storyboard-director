#!/usr/bin/env python3
r"""
link_resolver.py — Löst externe Video- & Sharelinks auf (z.B. Gemini Sharelinks, direkte URLs)
und lädt die fertige Videodatei in das Projekt herunter.
"""

import argparse
import json
import re
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def resolve_gemini_share(share_url, chrome_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
    """
    Nutzt headless Chrome mit CDP, öffnet den Gemini Sharelink,
    behandelt den Consent-Screen und extrahiert die direkte Video-URL.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()

    user_data_dir = Path.home() / ".gemini" / "antigravity" / "brain" / "cdp_gemini_fetch"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    node_script = f"""
import {{ spawn }} from 'child_process';

const chrome = spawn({json.dumps(chrome_path)}, [
  '--headless=new',
  '--disable-gpu',
  '--remote-debugging-port={port}',
  '--user-data-dir=' + {json.dumps(str(user_data_dir))},
  {json.dumps(share_url)}
], {{ stdio: 'ignore' }});

await new Promise(r => setTimeout(r, 2000));

try {{
  const listRes = await fetch('http://127.0.0.1:{port}/json/list');
  const pages = await listRes.json();
  const page = pages.find(p => p.type === 'page');
  if (!page) throw new Error('No page found');

  const ws = new WebSocket(page.webSocketDebuggerUrl);
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

  await new Promise(r => setTimeout(r, 4500));

  // Consent ablehnen falls vorhanden
  await send('Runtime.evaluate', {{
    expression: `
      (() => {{
        const btn = document.querySelector('[data-test-id="reject-button"]') || 
                    document.querySelector('button[aria-label*="ablehnen"]');
        if (btn) btn.click();
      }})()
    `
  }});

  await new Promise(r => setTimeout(r, 5500));

  // Video-URL extrahieren
  const res = await send('Runtime.evaluate', {{
    expression: `
      (() => {{
        const v = document.querySelector('video');
        if (v && (v.src || v.currentSrc)) return v.src || v.currentSrc;
        const source = document.querySelector('video source');
        if (source && source.src) return source.src;
        const imgs = Array.from(document.querySelectorAll('img'))
          .map(i => i.src)
          .filter(s => s && s.includes('googleusercontent.com') && !s.includes('default-user'));
        if (imgs.length > 0) return imgs[0];
        return null;
      }})()
    `,
    returnByValue: true
  }});

  const mediaUrl = res.result?.result?.value;
  if (mediaUrl) {{
    console.log('FOUND_MEDIA_URL:' + mediaUrl);
  }} else {{
    console.log('NO_MEDIA_FOUND');
  }}

  ws.close();
}} catch (e) {{
  console.error('Error in Node:', e);
}} finally {{
  chrome.kill();
}}
"""
    script_path = user_data_dir / "_run_fetch.mjs"
    script_path.write_text(node_script, encoding="utf-8")

    proc = subprocess.run(["node", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    for line in proc.stdout.splitlines():
        if line.startswith("FOUND_MEDIA_URL:"):
            return line.replace("FOUND_MEDIA_URL:", "").strip()
    return None


def download_media(url, dest_path):
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        f.write(resp.read())
    return dest


def fetch_link_to_file(raw_url, dest_file):
    url = raw_url.strip()
    print(f"[LINK-RESOLVER] Verarbeite URL: {url}")

    if "gemini.google" in url or "share.gemini" in url:
        print("[LINK-RESOLVER] Gemini Sharelink erkannt. Starte CDP-Extraktor...")
        media_url = resolve_gemini_share(url)
        if not media_url:
            raise RuntimeError("Konnte keine Video- oder Medien-URL aus dem Gemini Sharelink extrahieren.")
        print(f"[LINK-RESOLVER] Gefundene Medien-URL: {media_url[:80]}...")
        return download_media(media_url, dest_file)

    # Direkte Medien-URL
    print("[LINK-RESOLVER] Lade direkte Medien-URL herunter...")
    return download_media(url, dest_file)


def main():
    parser = argparse.ArgumentParser(description="Löst Sharelinks oder direkte URLs auf und lädt Medien herunter.")
    parser.add_argument("url", help="Gemini Sharelink oder direkte Video-URL")
    parser.add_argument("--out", required=True, help="Zieldatei (z.B. _inbox/shot01.mp4)")

    args = parser.parse_args()
    dest = fetch_link_to_file(args.url, args.out)
    print(f"[OK] Datei erfolgreich heruntergeladen: {dest} ({dest.stat().st_size} Bytes)")


if __name__ == "__main__":
    main()
