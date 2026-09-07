# clip-storyboard-director — KI-Storyboard-Regisseur & Video-Pipeline-Controller

`clip-storyboard-director` ist das Bindeglied zwischen kreativer Drehbuch-/Story-Idee und präziser,
generativer Video- und Clip-Produktion. Er zerlegt eine Story in diskrete Zeitschritte (Shots),
sichert über einen 4-dimensionalen Persistenzpuffer (Charaktere, Orte, Objekte, Requisiten) die
visuelle Kontinuität, steuert KI-Videogeneratoren (Google Veo, Runway, Kling etc.) via Edge CDP &
Cowork Protocol vollautonom an und mastern die Hero-Takes zu einem vollständigen Filmclip.

---

## 🎭 Die zwei Seiten der Medaille: Regisseur vs. Cutter

| Rolle | Tool | Zuständigkeit |
|---|---|---|
| **Regisseur (Pre-Production)** | **`clip-storyboard-director`** *(dieses Repo)* | Story-Planung, Shot-Matrix, 4D-Persistenz, Clue-Frames, Browser-CDP-Injektion, Audio-Staging, Roh-/Master-Schnitt |
| **Cutter (Post-Production)** | **`ai-media-editor`** (`_Local_DEV/repos/ai-media-editor`) | Lokale Whisper-Transkription, Versprecher- & Pausen-Schnitt (`cut_view`), Frame-Kontaktabzüge (`frame_view`), HyperFrames |

---

## 🚀 Quickstart & CLI

Installierbar via:
```bash
pip install -e .
```

### Die wichtigsten Befehle (`clip-director`):

```bash
# 0. Systemvoraussetzungen prüfen (FFmpeg, Edge, Python-Module)
clip-director doctor

# 1. Neues Storyboard-Projekt im Zeitraster initialisieren
clip-director init mein_film --title "Mein Film" --duration 40 --step 10

# 2. Interaktiven Board-Server starten (Port 8765)
clip-director serve --project projects/mein_film

# 3. Dual-Pane Cockpit in Microsoft Edge starten (Remote-Debugging & Split-View)
clip-director cockpit --project projects/mein_film

# 4. Vollautonomen Produktions-Loop starten (CDP-Prompt-Injektion & Ingest-Watcher)
clip-director autopilot --project projects/mein_film

# 5. Master-Video mastern (FFmpeg-Stitch, Voiceover-Mischung & Ducking)
clip-director assemble --project projects/mein_film

# 6. HTML-Dashboards neu rendern
clip-director render --project projects/mein_film
```

---

## 🏗️ Kern-Architektur & Komponenten

1. **4D-Persistenzpuffer (`project.yaml`):**
   - Charaktere, Orte/Kulissen, Objekte und Requisiten werden projektweit definiert.
   - Bild-Referenzen (`assets/refs/`) garantieren konsistente Figuren und Umgebungen.

2. **Clue-Frame Kontinuitätskette:**
   - Das letzte Frame von Shot $N$ (`frames/shot0N_v01_lastframe.png`) dient automatisch als optischer Anschluss für Shot $N+1$.

3. **Dual-Pane Cockpit (Edge Edition):**
   - **Linke Spalte:** Interaktive Storyboard-Timeline (`storyboard.html`) mit Master-Player, Take-Status und Audio-Matrix.
   - **Rechte Spalte:** Generator-Brücke (Gemini Veo, Runway, Kling) mit automatischer CDP-Prompt-Injektion und Download-Watcher.

4. **Mastering & Audio-Matrix:**
   - 4 Spuren: In-Video (Veo-Sound), Hintergrund-Bett (Musik/Drohne), MIDI/Melodie, SFX.
   - Integrierte Sprecherstimmen via `edge-tts` (z. B. `de-DE-ConradNeural`).
   - Dynamisches Ducking des Videoraumklangs zur optimalen Sprachverständlichkeit.

---

## 🧪 Tests & Qualitätssicherung

```bash
pytest tests/
```
