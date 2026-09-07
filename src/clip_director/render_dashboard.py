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

    locs_list = [f"{l.get('name')}: {l.get('features', '')}" if isinstance(l, dict) else str(l) for l in p_buf.get("locations", [])]
    locations_str = "; ".join(locs_list) or "Keine hinterlegt"

    objects_list = [f"{o.get('name')}: {o.get('features', '')}" if isinstance(o, dict) else str(o) for o in p_buf.get("objects", [])]
    objects_str = "; ".join(objects_list) or "Keine hinterlegt"

    segments_html = []
    cards_html = []

    for s in shots:
        step_nr = s.get("step_nr")
        slug = s.get("slug", f"shot-{step_nr}")
        start = s.get("start_sec", 0)
        end = s.get("end_sec", 10)
        takes = s.get("takes", [])
        has_hero = bool(s.get("selected_take"))
        status_cls = "done" if has_hero else ""

        seg = f'<a href="#shot-{step_nr}" class="timeline-segment {status_cls}">#{step_nr} ({start}-{end}s)</a>'
        segments_html.append(seg)

        hero_take_obj = next((t for t in takes if t.get("id") == s.get("selected_take")), None) if has_hero else None
        hero_video_rel = hero_take_obj.get("file") if hero_take_obj else None
        clue_img = s.get("clue_frame")

        if hero_video_rel and (project_path / hero_video_rel).exists():
            preview_inner = f'<video controls loop src="{html.escape(hero_video_rel)}" poster="{html.escape(clue_img or "")}"></video>'
            badge_text = f"Hero Video ({s.get('selected_take')})"
        elif clue_img and (project_path / clue_img).exists():
            preview_inner = f'<img src="{html.escape(clue_img)}" alt="Clue Frame" draggable="true" ondragstart="onAssetDragStart(event, this, \'shot{step_nr:02d}_clueframe\')" class="draggable-asset" title="Greifen & in externen Chat ziehen">'
            badge_text = f"Hero Frame ({s.get('selected_take')})"
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
        track1_label = "🔊 Spur 1: In-Video (Aktiv)" if track1_invideo == "keep" else "🔇 Spur 1: In-Video (Mute)"
        track2_active = "active" if audio.get("track2_bed") else ""
        track3_active = "active" if audio.get("track3_midi") else ""
        track4_active = "active" if audio.get("track4_sfx") else ""

        voice = s.get("voice", {})
        voice_html = ""
        if voice.get("enabled") and (voice.get("text") or voice.get("source_text")):
            rendered_audio = voice.get("rendered_file")
            audio_player_html = ""
            if rendered_audio and (project_path / rendered_audio).exists():
                audio_player_html = f'<div style="margin-top: 8px;"><audio controls src="{html.escape(rendered_audio)}" style="height: 30px; width: 100%;"></audio></div>'

            src_text = voice.get("source_text") or voice.get("text") or ""
            trans_en = voice.get("translated_text_en") or ""
            directives = voice.get("directives", {})
            dir_de = directives.get("german") or f'Spoken dialogue in German (clear voice): "{src_text}"'
            dir_en = directives.get("english") or (f'Spoken dialogue in English (clear voice): "{trans_en}"' if trans_en else "")
            dir_silent = directives.get("silent") or "Silent video with ambient environmental sound only, strictly no human voice"

            en_block = ""
            en_copy_btn = ""
            if trans_en:
                en_block = f'<div style="margin-top: 4px; font-size: 12px; color: #a5b4fc;"><strong style="color: #93c5fd;">🇬🇧 EN Translation:</strong> <em>"{html.escape(trans_en)}"</em></div>'
                en_copy_btn = f'<button class="btn-copy-card" style="font-size: 11px; padding: 2px 7px;" onclick="copyCustomText({html.escape(json.dumps(dir_en))}, \'EN-Dialoganweisung kopiert!\')">📋 EN-Direktive</button>'

            voice_html = f"""<div class="voice-box">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span>🎙️ <strong>Voice & Dialog ({html.escape(voice.get("speaker") or "TTS")}):</strong></span>
                <div style="display: flex; align-items: center; gap: 6px;">
                  <span class="rec-timer" id="rec-timer-{step_nr}" style="display:none; color: #ef4444; font-weight: 700; font-size: 11px;">● 00:00</span>
                  <button class="rec-btn" id="rec-btn-{step_nr}" onclick="toggleRecord({step_nr})">🎙️ Aufnahme</button>
                </div>
              </div>
              <div style="font-size: 12.5px; color: #f3f4f6; margin-bottom: 2px;">
                <strong style="color: #e9d5ff;">🇩🇪 Source (DE):</strong> <em style="color: #e9d5ff;">"{html.escape(src_text)}"</em>
              </div>
              {en_block}
              <div style="display: flex; gap: 5px; margin-top: 8px; flex-wrap: wrap;">
                <button class="btn-copy-card" style="font-size: 11px; padding: 2px 7px; background: rgba(59, 130, 246, 0.2); border-color: #3b82f6; color: #93c5fd;" onclick="copyShotPromptOnly({step_nr}, \'de\')" title="Visueller Prompt + deutsche Dialoganweisung">📋 Prompt + 🇩🇪 DE</button>
                {f'<button class="btn-copy-card" style="font-size: 11px; padding: 2px 7px; background: rgba(139, 92, 246, 0.2); border-color: #8b5cf6; color: #c4b5fd;" onclick="copyShotPromptOnly({step_nr}, \'en\')" title="Visueller Prompt + englische Dialoganweisung">📋 Prompt + 🇬🇧 EN</button>' if trans_en else ''}
                <button class="btn-copy-card" style="font-size: 11px; padding: 2px 7px; background: rgba(107, 114, 128, 0.2); border-color: #6b7280; color: #d1d5db;" onclick="copyShotPromptOnly({step_nr}, \'silent\')" title="Visueller Prompt + Stumm-Direktive">🔇 Prompt + Stumm</button>
              </div>
              <div id="voice-player-{step_nr}">{audio_player_html}</div>
            </div>"""

        card = f"""
        <div class="shot-card" id="shot-{step_nr}">
          <div class="shot-header">
            <div class="step-tag">Step {step_nr:02d}: {html.escape(slug)}</div>
            <div class="time-tag">{start:02d}s – {end:02d}s ({s.get("duration_sec")}s)</div>
          </div>
          <div class="shot-preview">
            {preview_inner}
            <div class="preview-badge">{badge_text}</div>
          </div>
          <div class="shot-body">
            <div class="link-import-bar">
              <input type="text" id="link-input-{step_nr}" placeholder="Gemini Sharelink oder Video-URL einfügen...">
              <button class="btn-fetch-link" onclick="fetchVideoLink({step_nr})">📥 Abholen</button>
            </div>
            <div class="grammar-row">
              <div><strong>Perspektive</strong><span>{html.escape(s.get("perspective") or "-")}</span></div>
              <div><strong>Kameraführung</strong><span>{html.escape(s.get("camera_movement") or "-")}</span></div>
              <div><strong>Licht/Farbe</strong><span>{html.escape(s.get("lighting_color") or "-")}</span></div>
              <div><strong>Dynamik</strong><span>Stärke {s.get("motion_intensity", 3)}/10</span></div>
            </div>
            <div class="prompt-box" onclick="copyShotPromptOnly({step_nr}, \'plain\')" title="Klicken: Reinen visuellen Prompt in Zwischenablage kopieren (ohne Sprachen-Mix)">
              <div class="p-title">
                <span>Visueller Prompt (Version {active_v})</span>
                <span class="copy-hint-pill">⚡ Klick = Prompt kopieren</span>
              </div>
              <p>"{html.escape(prompt_text)}"</p>
            </div>
            {voice_html}
            <div class="audio-matrix">
              <span class="audio-pill {track1_active}">{track1_label}</span>
              <button class="audio-toggle-btn" onclick="toggleAudioTrack({step_nr})" title="Zwischen Beibehalten und Stummschalten wechseln">Ton umschalten</button>
              <span class="audio-pill {track2_active}">Spur 2: Bett</span>
              <span class="audio-pill {track3_active}">Spur 3: MIDI</span>
              <span class="audio-pill {track4_active}">Spur 4: SFX</span>
            </div>
            <div class="shot-footer">
              <span class="takes-count">{len(takes)} Take(s) generiert</span>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span>Übergang: {html.escape(audio.get("transition_video") or "cut")}</span>
                <button class="btn-copy-shot" onclick="copyShotDetails({step_nr})" title="Kopiert vollständige Spezifikation + Prompt + Clueframe">⚡ Prompt & Specs</button>
              </div>
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
            thumb_html = f'<img src="{html.escape(i_ref)}" alt="{html.escape(i_name)}" draggable="true" ondragstart="onAssetDragStart(event, this, \'{html.escape(i_name)}\')" class="draggable-asset" title="Greifen & in externen Chat (z.B. Gemini) ziehen"><div class="drag-badge">🤏 Drag</div>'
            status_badge = '<span style="color: var(--accent-green);">✅ Bereit</span>'
        else:
            thumb_html = '<span>Offen</span>'
            status_badge = '<span style="color: var(--accent-amber);">⚠️ Vorlage erzeugen</span>'

        b_card = f"""
        <div class="bible-card" onclick="copyBibleItem('{i_id}')" title="Klicken: Bild & Prompt in Zwischenablage kopieren">
          <div class="bible-thumb">{thumb_html}</div>
          <div class="bible-info">
            <div class="bible-title">
              <span>{html.escape(i_name)}</span>
              <div style="display: flex; gap: 6px; align-items: center;">
                <span class="bible-cat">{html.escape(i_cat)}</span>
                <button class="btn-copy-card" onclick="event.stopPropagation(); copyBibleItem('{i_id}')" title="Kopiert Bild + Konsistenz-Prompt für Image-Generatoren">⚡ Kopieren</button>
              </div>
            </div>
            <p class="bible-desc">{html.escape(i_desc)}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
              <span class="bible-shots">{shots_label}</span>
              <span style="font-size: 11px;">{status_badge}</span>
            </div>
          </div>
        </div>
        """
        bible_cards_html.append(b_card)

    if not bible_cards_html:
        bible_cards_html.append('<div style="color: var(--text-muted); font-size: 13px;">Keine Konsistenz-Elemente im Puffer definiert.</div>')

    project_client_data = {
        "project": proj,
        "persistence_buffer": p_buf,
        "consistency_bible": bible_entries,
        "shots": {s.get("step_nr"): s for s in shots},
        "bible": bible_dict
    }
    project_data_json = json.dumps(project_client_data, ensure_ascii=False)

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
            jumpers.append(f'<button class="btn-jumper" onclick="jumpMasterVideo({s_start})" title="Sprung zu Shot {s_num} ({s_start}s)">▶️ Shot {s_num} ({s_start}s) • {html.escape(s_slug)}</button>')
        jumpers_html = "\n      ".join(jumpers)

        master_section = f"""
  <!-- MASTER FILM PREMIERE SECTION -->
  <section class="master-player-card" id="master-player">
    <div class="master-header">
      <div class="master-title-group">
        <span class="premiere-badge">🎉 MASTER CLIP BEREIT</span>
        <h2>🎬 {html.escape(proj.get("title") or proj_name)} — Masterfilm</h2>
        <span class="master-specs-tag">⏱️ {proj.get("total_duration_sec", 40)}s Cut • {proj.get("aspect_ratio", "16:9")} • {proj.get("fps", 24)} FPS • de-DE-ConradNeural Voiceover & Veo Raumklang</span>
      </div>
      <div class="master-actions">
        <button class="btn-master-action btn-explorer" onclick="openProjectFolder()" title="Öffnet den Projektordner im Windows Explorer und markiert das Master-Video">📁 Ordner im Explorer öffnen</button>
        <a href="{html.escape(master_rel)}" download="{html.escape(master_rel)}" class="btn-master-action btn-download" title="Master-Video lokal speichern">📥 Video herunterladen ({size_mb:.2f} MB)</a>
        <button class="btn-master-action btn-assemble" onclick="triggerReassemble()" title="Führt FFmpeg-Assembly erneut aus">🔄 Neu schneiden</button>
      </div>
    </div>
    <div class="master-video-wrapper">
      <video id="main-master-video" controls playsinline preload="metadata" {first_poster_attr}>
        <source src="{html.escape(master_rel)}" type="video/mp4">
        Dein Browser unterstützt die HTML5-Videowiedergabe nicht.
      </video>
    </div>
    <div class="master-timeline-jumpers">
      <span class="jumper-label">Kapitel / Direktsprung:</span>
      {jumpers_html}
    </div>
  </section>
"""

    rendered = html_template.format(
        project_title=html.escape(proj.get("title") or proj.get("name") or "Clip"),
        project_name=html.escape(proj.get("name") or "clip"),
        project_created=proj.get("created", "2026-09-07"),
        total_duration=proj.get("total_duration_sec", 30),
        step_duration=proj.get("step_duration_sec", 10),
        step_count=len(shots),
        aspect_ratio=proj.get("aspect_ratio", "16:9"),
        resolution=proj.get("resolution", "1080p"),
        fps=proj.get("fps", 24),
        genre=html.escape(proj.get("default_genre", "Cinematic")),
        characters_str=html.escape(characters_str),
        props_str=html.escape(props_str),
        locations_str=html.escape(locations_str),
        objects_str=html.escape(objects_str),
        bible_cards="\n".join(bible_cards_html),
        timeline_segments="\n".join(segments_html),
        shot_cards="\n".join(cards_html),
        project_data_json=project_data_json,
        master_section=master_section
    )

    out_file = project_path / "storyboard.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] Interaktives Storyboard-Dashboard erfolgreich generiert:")
    print(f"     -> {out_file}")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Generiert ein interaktives HTML-Timeline-Dashboard.")
    parser.add_argument("--project", default=".", help="Projektverzeichnis mit project.yaml")
    args = parser.parse_args()
    render_project(args.project)

if __name__ == "__main__":
    main()
