#!/usr/bin/env python3
"""
render_dashboard.py — Rendert ein visuelles, interaktives HTML5-Timeline-Dashboard aus project.yaml.
"""

import argparse
import html
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML nicht installiert.", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR / "dashboard_template.html"


def _esc(value):
    """HTML-Escaping fuer beliebige YAML-Werte (auch Zahlen/None)."""
    return html.escape(str(value))


def _js_arg(value):
    """String-Argument fuer einen JS-Aufruf in einem HTML-Attribut.

    json.dumps liefert ein korrekt maskiertes JS-Stringliteral, html.escape schuetzt
    das umgebende Attribut; der HTML-Parser dekodiert &quot; wieder zu ".
    Frueher: '{html.escape(name)}' - &#x27; wird vom Parser zu ' und bricht aus.
    """
    return html.escape(json.dumps(str(value)))


def _script_json(data):
    """JSON fuer einen <script>-Block: </script> und <!-- duerfen nicht auftauchen."""
    return (json.dumps(data, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))

def render_project(project_dir):
    project_path = Path(project_dir).resolve()
    yaml_file = project_path / "project.yaml"

    if not yaml_file.exists():
        print(f"[FEHLER] project.yaml nicht in {project_path} gefunden.", file=sys.stderr)
        sys.exit(1)

    if not TEMPLATE_PATH.exists():
        print(f"[FEHLER] Template {TEMPLATE_PATH} nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    proj = data.get("project", {})
    p_buf = data.get("persistence_buffer", {})
    shots = data.get("shots", [])

    chars_list = [f"{c.get('name')}: {c.get('appearance', '')}" if isinstance(c, dict) else str(c) for c in p_buf.get("characters", [])]
    characters_str = "; ".join(chars_list) or "Keine hinterlegt"

    props_list = [f"{p.get('name')}: {p.get('features', '')}" if isinstance(p, dict) else str(p) for p in p_buf.get("props", [])]
    props_str = "; ".join(props_list) or "Keine hinterlegt"

    locs_list = [f"{loc.get('name')}: {loc.get('features', '')}" if isinstance(loc, dict) else str(loc) for loc in p_buf.get("locations", [])]
    locations_str = "; ".join(locs_list) or "Keine hinterlegt"

    objects_list = [f"{o.get('name')}: {o.get('features', '')}" if isinstance(o, dict) else str(o) for o in p_buf.get("objects", [])]
    objects_str = "; ".join(objects_list) or "Keine hinterlegt"

    segments_html = []
    cards_html = []
    # Der aktuelle Shot = erster ohne Hero-Take (dieselbe Regel wie /api/cowork/focus)
    current_step = next((s.get("step_nr") for s in shots if not s.get("selected_take")), None)

    for s in shots:
        step_nr = s.get("step_nr")
        slug = s.get("slug", f"shot-{step_nr}")
        start = s.get("start_sec", 0)
        end = s.get("end_sec", 10)
        takes = s.get("takes", [])
        has_hero = bool(s.get("selected_take"))
        is_current = step_nr == current_step
        status_cls = "done" if has_hero else ("active" if is_current else "")
        aria_current = ' aria-current="step"' if is_current else ""

        seg = f'<a href="#shot-{step_nr}" class="timeline-segment {status_cls}"{aria_current}>#{step_nr} · {start}–{end} s</a>'
        segments_html.append(seg)

        hero_take_obj = next((t for t in takes if t.get("id") == s.get("selected_take")), None) if has_hero else None
        hero_video_rel = hero_take_obj.get("file") if hero_take_obj else None
        clue_img = s.get("clue_frame")

        if hero_video_rel and (project_path / hero_video_rel).exists():
            preview_inner = f'<video controls loop src="{html.escape(hero_video_rel)}" poster="{html.escape(clue_img or "")}"></video>'
            badge_text = f"Hero Video ({_esc(s.get('selected_take'))})"
        elif clue_img and (project_path / clue_img).exists():
            preview_inner = f'<img src="{html.escape(clue_img)}" alt="Clue Frame" draggable="true" ondragstart="onAssetDragStart(event, this, \'shot{step_nr:02d}_clueframe\')" class="draggable-asset" title="Greifen & in externen Chat ziehen">'
            badge_text = f"Hero Frame ({_esc(s.get('selected_take'))})"
        elif takes:
            preview_inner = '<span>Take(s) vorhanden, noch kein Hero-Video</span>'
            badge_text = f"{len(takes)} Take(s)"
        else:
            preview_inner = '<span>Ausstehend — Video generieren</span>'
            badge_text = "Noch kein Take"

        active_v = s.get("active_prompt_version", "v1")
        p_obj = next((p for p in s.get("prompts", []) if p.get("version") == active_v), None)
        prompt_text = p_obj.get("text", "") if p_obj else ""

        audio = s.get("audio", {})
        track1_invideo = audio.get("track1_invideo", "mute")
        track1_active = "active" if track1_invideo == "keep" else ""
        track1_label = "Spur 1: In-Video an" if track1_invideo == "keep" else "Spur 1: In-Video stumm"
        track2_active = "active" if audio.get("track2_bed") else ""
        track3_active = "active" if audio.get("track3_midi") else ""
        track4_active = "active" if audio.get("track4_sfx") else ""

        voice = s.get("voice", {})
        voice_html = ""
        if voice.get("enabled") and (voice.get("text") or voice.get("source_text")):
            rendered_audio = voice.get("rendered_file")
            audio_player_html = ""
            if rendered_audio and (project_path / rendered_audio).exists():
                audio_player_html = f'<audio controls src="{html.escape(rendered_audio)}" style="height: 30px; width: 100%; margin-top: 6px;"></audio>'

            src_text = voice.get("source_text") or voice.get("text") or ""
            trans_en = voice.get("translated_text_en") or ""

            en_block = ""
            en_prompt_btn = ""
            if trans_en:
                en_block = f'<div class="voice-line"><strong>EN:</strong> „{html.escape(trans_en)}“</div>'
                en_prompt_btn = f'''<button class="btn-copy-card" onclick="copyShotPromptOnly({step_nr}, 'en')" aria-describedby="shot-title-{step_nr}" title="Visueller Prompt + englische Dialoganweisung">Prompt + EN</button>'''

            voice_html = f"""<div class="voice-box">
              <div class="voice-head">
                <span><strong>Sprecher:</strong> {html.escape(voice.get("speaker") or "TTS")}</span>
                <span>
                  <span class="rec-timer" id="rec-timer-{step_nr}" style="display:none;">● 00:00</span>
                  <button class="rec-btn" id="rec-btn-{step_nr}" onclick="toggleRecord({step_nr})" aria-describedby="shot-title-{step_nr}">Aufnehmen</button>
                </span>
              </div>
              <div class="voice-line"><strong>DE:</strong> „{html.escape(src_text)}“</div>
              {en_block}
              <div class="voice-actions">
                <button class="btn-copy-card" onclick="copyShotPromptOnly({step_nr}, 'de')" aria-describedby="shot-title-{step_nr}" title="Visueller Prompt + deutsche Dialoganweisung">Prompt + DE</button>
                {en_prompt_btn}
                <button class="btn-copy-card" onclick="copyShotPromptOnly({step_nr}, 'silent')" aria-describedby="shot-title-{step_nr}" title="Visueller Prompt + Stumm-Direktive">Prompt + stumm</button>
              </div>
              <div id="voice-player-{step_nr}">{audio_player_html}</div>
            </div>"""

        current_cls = " is-current" if is_current else ""
        current_pill = '<span class="current-pill">aktuell</span>' if is_current else ""
        card = f"""
        <div class="shot-card{current_cls}" id="shot-{step_nr}">
          <div class="shot-header">
            <div class="step-tag" id="shot-title-{step_nr}">{step_nr:02d} · {html.escape(slug)}{current_pill}</div>
            <div class="time-tag">{start:02d}–{end:02d} s ({html.escape(str(s.get("duration_sec", end - start)))} s)</div>
          </div>
          <div class="shot-preview">
            {preview_inner}
            <div class="preview-badge">{badge_text}</div>
          </div>
          <div class="shot-body">
            <button type="button" class="prompt-box" onclick="copyShotPromptOnly({step_nr}, \'plain\')" title="Visuellen Prompt ohne Dialoganweisung kopieren">
              <span class="p-title">
                <span>Prompt {_esc(active_v)}</span>
                <span class="copy-hint-pill">Kopieren</span>
              </span>
              <span class="prompt-text">{html.escape(prompt_text)}</span>
            </button>
            <div class="link-import-bar">
              <input type="text" id="link-input-{step_nr}" aria-label="Video-Link für Shot {step_nr}" placeholder="Gemini-Sharelink oder Video-URL">
              <button class="btn-fetch-link" onclick="fetchVideoLink({step_nr})" aria-describedby="shot-title-{step_nr}">Abholen</button>
            </div>
            {voice_html}
            <details class="shot-more" open>
              <summary aria-describedby="shot-title-{step_nr}">Kamera, Licht &amp; Ton</summary>
              <div>
                <div class="grammar-row">
                  <div><strong>Perspektive</strong><span>{html.escape(s.get("perspective") or "-")}</span></div>
                  <div><strong>Kameraführung</strong><span>{html.escape(s.get("camera_movement") or "-")}</span></div>
                  <div><strong>Licht/Farbe</strong><span>{html.escape(s.get("lighting_color") or "-")}</span></div>
                  <div><strong>Dynamik</strong><span>Stärke {s.get("motion_intensity", 3)}/10</span></div>
                </div>
                <div class="audio-matrix">
                  <span class="audio-pill {track1_active}">{track1_label}</span>
                  <button class="audio-toggle-btn" onclick="toggleAudioTrack({step_nr})" aria-describedby="shot-title-{step_nr}" title="Zwischen Beibehalten und Stummschalten wechseln">Ton umschalten</button>
                  <span class="audio-pill {track2_active}">Spur 2: Bett</span>
                  <span class="audio-pill {track3_active}">Spur 3: MIDI</span>
                  <span class="audio-pill {track4_active}">Spur 4: SFX</span>
                </div>
              </div>
            </details>
            <div class="shot-footer">
              <span class="takes-count">{len(takes)} Take(s) · Übergang: {html.escape(audio.get("transition_video") or "cut")}</span>
              <button class="btn-copy-shot" onclick="copyShotDetails({step_nr})" aria-describedby="shot-title-{step_nr}" title="Kopiert vollständige Spezifikation + Prompt + Clueframe">Prompt &amp; Specs kopieren</button>
            </div>
          </div>
        </div>
        """
        cards_html.append(card)

    bible_entries = data.get("consistency_bible", [])
    bible_cards_html = []
    bible_dict = {}

    for idx, item in enumerate(bible_entries):
        i_id = item.get("id") or f"bible_item_{idx}"
        item["id"] = i_id
        bible_dict[i_id] = item
        i_name = item.get("name", "Element")
        i_cat = item.get("category", "Asset")
        i_desc = item.get("description", "")
        i_ref = item.get("reference_image")

        appearing_shots = []
        for s in shots:
            s_num = s.get("step_nr")
            s_p = s.get("persistence", {})
            prompt_t = " ".join([p.get("text", "") for p in s.get("prompts", [])])
            if (i_name.lower() in prompt_t.lower() or
                i_name in s_p.get("characters", []) or
                i_name in s_p.get("props", []) or
                i_name in s_p.get("locations", []) or
                i_name in s_p.get("objects", [])):
                appearing_shots.append(f"#{s_num}")

        shots_label = f"Shots: {', '.join(appearing_shots)}" if appearing_shots else "Projektweit relevant"

        if i_ref and (project_path / i_ref).exists():
            thumb_html = f'<img src="{html.escape(i_ref)}" alt="{html.escape(i_name)}" draggable="true" ondragstart="onAssetDragStart(event, this, {_js_arg(i_name)})" class="draggable-asset" title="Greifen & in externen Chat (z.B. Gemini) ziehen"><span class="drag-badge">Drag</span>'
            status_badge = '<span class="status-ok">bereit</span>'
        else:
            thumb_html = '<span>Offen</span>'
            status_badge = '<span class="status-warn">Vorlage fehlt</span>'

        b_card = f"""
        <button type="button" class="bible-card" onclick="copyBibleItem({_js_arg(i_id)})" aria-label="Konsistenz-Element {html.escape(i_name)} kopieren" aria-describedby="bible-cat-{idx} bible-desc-{idx} bible-meta-{idx}" title="Bild und Prompt kopieren">
          <span class="bible-thumb">{thumb_html}</span>
          <span class="bible-info">
            <span class="bible-title">
              <span>{html.escape(i_name)}</span>
              <span class="bible-card-meta">
                <span class="bible-cat" id="bible-cat-{idx}">{html.escape(i_cat)}</span>
                <span class="copy-hint-pill">Kopieren</span>
              </span>
            </span>
            <span class="bible-desc" id="bible-desc-{idx}">{html.escape(i_desc)}</span>
            <span class="bible-meta" id="bible-meta-{idx}">
              <span class="bible-shots">{shots_label}</span>
              <span>{status_badge}</span>
            </span>
          </span>
        </button>
        """
        bible_cards_html.append(b_card)

    if not bible_cards_html:
        bible_cards_html.append('<div class="bible-desc">Keine Konsistenz-Elemente im Puffer definiert.</div>')

    project_client_data = {
        "project": proj,
        "persistence_buffer": p_buf,
        "consistency_bible": bible_entries,
        "shots": {s.get("step_nr"): s for s in shots},
        "bible": bible_dict
    }
    project_data_json = _script_json(project_client_data)

    proj_name = proj.get("name", "master")
    master_file = project_path / f"{proj_name}_master.mp4"
    master_section = ""

    if master_file.exists():
        size_mb = master_file.stat().st_size / (1024 * 1024)
        first_clue = shots[0].get("clue_frame") if shots else ""
        first_poster_attr = f'poster="{html.escape(first_clue)}"' if first_clue and (project_path / first_clue).exists() else ''
        master_rel = f"{proj_name}_master.mp4"

        jumpers = []
        for s in shots:
            s_num = s.get("step_nr", 1)
            s_start = s.get("start_sec", 0)
            s_slug = s.get("slug", f"Shot {s_num}")
            jumpers.append(f'<button class="btn-jumper" onclick="jumpMasterVideo({s_start})" title="Sprung zu Shot {s_num} ({s_start}s)">{s_num} · {html.escape(s_slug)}</button>')
        jumpers_html = "\n      ".join(jumpers)

        master_section = f"""
  <!-- MASTER FILM PREMIERE SECTION -->
  <section class="master-player-card" id="master-player">
    <div class="master-header">
      <div class="master-title-group">
        <span class="premiere-badge">Masterfilm fertig</span>
        <h2>{html.escape(proj.get("title") or proj_name)}</h2>
        <span class="master-specs-tag">{_esc(proj.get("total_duration_sec", 40))} s · {_esc(proj.get("aspect_ratio", "16:9"))} · {_esc(proj.get("fps", 24))} fps</span>
      </div>
      <div class="master-actions">
        <button class="btn-master-action btn-explorer" onclick="openProjectFolder()" title="Öffnet den Projektordner im Windows Explorer und markiert das Master-Video">Im Explorer zeigen</button>
        <a href="{html.escape(master_rel)}" download="{html.escape(master_rel)}" class="btn-master-action btn-download" title="Master-Video lokal speichern">Herunterladen ({size_mb:.1f} MB)</a>
        <button class="btn-master-action btn-handoff" onclick="handoffToMediaEditor()" title="Übergibt das Master-Video an ai-media-editor zur Whisper-Transkription & Nachbearbeitung">An ai-media-editor</button>
        <button class="btn-master-action btn-assemble" onclick="triggerReassemble()" title="Führt FFmpeg-Assembly erneut aus">Neu schneiden</button>
      </div>
    </div>
    <div class="master-video-wrapper">
      <video id="main-master-video" controls playsinline preload="metadata" {first_poster_attr}>
        <source src="{html.escape(master_rel)}" type="video/mp4">
        Dein Browser unterstützt die HTML5-Videowiedergabe nicht.
      </video>
    </div>
    <div class="master-timeline-jumpers">
      <span class="jumper-label">Kapitel:</span>
      {jumpers_html}
    </div>
  </section>
"""

    rendered = html_template.format(
        project_title=html.escape(proj.get("title") or proj.get("name") or "Clip"),
        project_name=html.escape(proj.get("name") or "clip"),
        project_created=_esc(proj.get("created", "2026-09-07")),
        total_duration=_esc(proj.get("total_duration_sec", 30)),
        step_duration=_esc(proj.get("step_duration_sec", 10)),
        step_count=len(shots),
        aspect_ratio=_esc(proj.get("aspect_ratio", "16:9")),
        resolution=_esc(proj.get("resolution", "1080p")),
        fps=_esc(proj.get("fps", 24)),
        genre=html.escape(proj.get("default_genre", "Cinematic")),
        characters_str=html.escape(characters_str),
        props_str=html.escape(props_str),
        locations_str=html.escape(locations_str),
        objects_str=html.escape(objects_str),
        bible_cards="\n".join(bible_cards_html),
        timeline_segments="\n".join(segments_html),
        shot_cards="\n".join(cards_html),
        project_data_json=project_data_json,
        persistence_count=f"({sum(len(p_buf.get(k, []) or []) for k in ('characters', 'props', 'locations', 'objects'))})",
        bible_count=f"({len(bible_entries)} Karten, {sum(1 for i in bible_entries if i.get('reference_image') and (project_path / i['reference_image']).exists())} mit Bild)",
        master_section_before=master_section if current_step is None else "",
        master_section_after=master_section if current_step is not None else ""
    )

    out_file = project_path / "storyboard.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(rendered)

    print("[OK] Interaktives Storyboard-Dashboard erfolgreich generiert:")
    print(f"     -> {out_file}")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Generiert ein interaktives HTML-Timeline-Dashboard.")
    parser.add_argument("--project", default=".", help="Projektverzeichnis mit project.yaml")
    args = parser.parse_args()
    render_project(args.project)

if __name__ == "__main__":
    main()
