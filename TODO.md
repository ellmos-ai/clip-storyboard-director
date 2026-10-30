# TODO.md — Active work

- **Version:** 0.1.6
- **Updated:** 2026-10-30
- **Reason:** Pfad B Cockpit UI Ergonomics, Single-Source Prompt Engine Parity, Sequence Diagram Hardening & Metadata Parity Stand 2026-10-30
- **Purpose:** Track only work that remains open.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Core Director Pipeline | DONE | Project lifecycle, init, doctor, serve, cockpit, assemble verified and passing pytest. |
| Path Neutrality & Hygiene | DONE | Neutral paths (`~/Downloads`), sanitized docstrings, and strict `.gitignore` patterns aligned with gate standards. |
| AI Discoverability & Navigation | DONE | Machine-readable `llms.txt`, 18-point quick navigation with dual anchors, 10-dimension comparative matrix, and PEP 621 metadata parity established. |
| Ecosystem Integration | DONE | Bi-directional handoff with `ai-media-editor`, catalog registration in `.MODULES/.DOMAINS`, Plan-D pointer configured. |
| Legal & Transparency | DONE | Root NOTICE file, Level 1 SBOM cross-reference matrix in THIRD_PARTY_LICENSES.md, and § 521 BGB statutory disclaimer in READMEs. |
| Public Release Gate | USER | MIT License selected; explicit public visibility approval pending from user. |

## Formalized next tasks

- [ ] **TASK-CSD-01: Multi-Track Audio Ducking Fine-Tuning** (`effort=medium`, `scope=audio`, priority `normal`).
  - **Goal:** Feinabstimmung der automatischen Lautstärke-Absenkung (Ducking) bei parallelem Veo-Raumklang und `edge-tts`-Sprecherspuren.
  - **Definition of Done:** Schwellenwerte und Attack/Release-Zeiten konfigurierbar in `project.yaml`; automatisierte Testsuite für Audio-Mischung erweitert.

- [ ] **TASK-CSD-02: Erweiterte Generator-Profile für Kling 1.5 & Runway Gen-3** (`effort=medium`, `scope=cdp`, priority `normal`).
  - **Goal:** Vorkonfigurierte CDP-Injektionsskripte und Selektor-Matrizen für weitere KI-Videogeneratoren bereitstellen.
  - **Definition of Done:** Selektoren in `src/clip_director/edge_bridge.py` abstrahiert und mit Mock-CDP getestet.

- [x] **TASK-CSD-03: Release-Hygiene & Gate-Bereitschaft (v0.1.1)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** Pfadneutralität in Templates und Watcher umgesetzt, `.gitignore` vervollständigt, `TODO.md` und `llms.txt` hinterlegt.

- [x] **TASK-CSD-04: Pfad B Discoverability, 16-Point Quick Navigation & Third-Party Audit (v0.1.4)** (`effort=low`, `scope=marketing`, priority `normal`).
  - **Result:** 16-Punkte-Schnellnavigation, Target Personas, Drittanbieter-Lizenzen, PEP 621 URLs und Marketing-Logbuch etabliert.

- [x] **TASK-CSD-05: Pfad A Technische Hygiene, PEP 561 Inline-Typisierung & CI-Härtung (v0.1.5)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** `py.typed` integriert, `python -m clip_director` Executable Entrypoint mit `-v` / `--version` Flag, `timeout-minutes: 15` in CI-Matrix, package-data für HTML/YAML Templates in Wheel-Build, und Vertragstestsuite erweitert.

- [x] **TASK-CSD-06: Pfad B Discoverability, 18-Point Navigation Parity, 10-Dimension Comparative Matrix, Level 1 SBOM & NOTICE Attribution (v0.1.6)** (`effort=medium`, `scope=marketing`, priority `high`).
  - **Result:** 18-Punkte Navigationsparität mit reziproken dualen HTML-Ankern in beiden READMEs, 10-Dimensionen Vergleichsmatrix gegenüber 4 Alternativen, Level 1 SBOM Invarianten-Tabelle in THIRD_PARTY_LICENSES.md, formeller NOTICE Attributierungsnachweis, § 521 BGB Haftungshinweis, Mermaid-Syntaxbereinigung und erweiterte Vertragstest-Suite.

- [x] **TASK-CSD-07: Pfad A Technische Hygiene, Stale Lifecycle Workflow & Multi-Host Lock Defense (2026-09-24)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** .github/workflows/stale.yml (actions/stale@v9 mit timeout-minutes: 10 und Concurrency) angelegt, .gitignore um Multi-Host Machine Suffixes (*-WORKSTATION*, *-ASUS*, *-LAPTOP*, *-Mac Studio*, * (Kopie)*, * (Copy)*) und kanonische Locks (LOCK.user.*, LOCK.until.*, LOCK.condition.*, .automation-lock) gehärtet, PEP 621 Standard-URLs (Notice, Bug Tracker) und pytest minversion/norecursedirs in pyproject.toml ergänzt, NOTICE und THIRD_PARTY_LICENSES.md re-auditiert, und Vertragstestsuite erweitert.

- [x] **TASK-CSD-09: Pfad B Cockpit UI Architecture, Single-Source Prompt Engine & Discoverability (2026-10-30)** (ffort=medium, scope=marketing, priority high).
  - **Result:** Split-Screen Cockpit-Layout-Architektur in Abschnitt 6 von README.md und README_de.md integriert, Single-Source Prompt Engine (prompt_builder.py) vollständig dokumentiert, Sequenzdiagramm in Abschnitt 9 um PromptBuilder-Kompilierung erweitert, llms.txt synchronisiert und Vertragstestsuite erweitert.

- [x] **TASK-CSD-08: Pfad B Discoverability, 18-Point Navigation Parity, ASCII Four-View Topology & Level 1 SBOM Text Companion (2026-09-29)** (`effort=medium`, `scope=marketing`, priority `high`).
  - **Result:** Bilaterale 18-Punkte-Navigationsanker sec-01..sec-18 in README.md und README_de.md, vierstufige ASCII-Architekturprojektion in Abschnitt 2, Level 1 SBOM Text-Companion THIRD_PARTY_LICENSES.txt, PEP 621 Sättigung auf 20 Topics in pyproject.toml, Standard-Projekt-URLs und Vertragstest-Erweiterung.


## TASKPLAN-Register (2026-09-20)

- TASKPLAN #488 registriert für TASK-CSD-01; Quelle bleibt TODO.md, Einstufung effort=medium, scope=local, Priorität medium (TODO: normal).
- TASKPLAN #489 registriert für TASK-CSD-02; Quelle bleibt TODO.md, Einstufung effort=medium, scope=local, Priorität medium (TODO: normal).
- Beide Tasks sind offen; kein Task wurde ausgeführt. Die USER-Freigabe im Status bleibt unberührt.

---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->

## Offen nach Prompt-Sync-Fix (2026-10-10)
- **Generator-spezifische Prompt-Bereinigung** (aus `docs/GUI_IMPROVEMENTS_FEEDBACK_2026-10-04.md` Punkt 2): Trennung interne Spezifikation (`copyShotDetails`, enthält Markdown-Header und deutsche Menü-Tags) vs. purer Generator-Prompt; Zielgenerator-Dropdown (Veo/Runway/Luma/Sora) als weiterer Parameter von `prompt_builder.build_prompt`. Nächster Schritt: Modus-Parameter `target` ergänzen, Voranstellung bei aktivem Anschlussbild.
- **Anschlussbild 1-Klick** (Feedback Punkt 1): Bildkopie in Zwischenablage existiert im Storyboard (`writeToClipboard` mit PNG), im Cockpit fehlt der Knopf; Desktop-Ablage per Knopf fehlt.
- **Workflow-Modus Neuer Chat vs. Verlängerung** (Feedback Punkt 3): braucht Differenz-Prompts, Design offen.
- **Doppelte Vorlagen**: `templates/cockpit_template.html` und `templates/dashboard_template.html` sind von keinem Code geladen und veraltet (Quelle ist `src/clip_director/`). Entfernen nach Rücksprache.
- Hinweis „ungespeicherte Änderungen“: im Editor gibt es kein Bearbeiten von Prompts im Browser (project.yaml ist die Quelle); sinnvoll erst mit einem Prompt-Editor-Endpunkt.
