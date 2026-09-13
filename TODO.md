# TODO.md — Active work

- **Version:** 0.1.5
- **Updated:** 2026-09-13
- **Reason:** Pfad A technical hygiene, PEP 561 inline typing, PEP 639 license-files, CI dev install hardening, and contract test suite expansion
- **Purpose:** Track only work that remains open.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Core Director Pipeline | DONE | Project lifecycle, init, doctor, serve, cockpit, assemble verified and passing pytest. |
| Path Neutrality & Hygiene | DONE | Neutral paths (`~/Downloads`), sanitized docstrings, and strict `.gitignore` patterns aligned with gate standards. |
| AI Discoverability & Navigation | DONE | Machine-readable `llms.txt`, 16-point quick navigation, target personas, and PEP 621 metadata parity established. |
| Ecosystem Integration | DONE | Bi-directional handoff with `ai-media-editor`, catalog registration in `.MODULES/.DOMAINS`, Plan-D pointer configured. |
| Public Release Gate | USER | MIT License selected; explicit public visibility approval pending from user. |

## Formalized next tasks

- [ ] **TASK-CSD-01: Multi-Track Audio Ducking Fine-Tuning** (`effort=medium`, `scope=audio`, priority `normal`).
  - **Goal:** Feinabstimmung der automatischen Lautstärke-Absenkung (Ducking) bei parallelem Veo-Raumklang und `edge-tts`-Sprecherspuren.
  - **Definition of Done:** Schwellenwerte und Attack/Release-Zeiten konfigurierbar in `project.yaml`; automatisierte Testsuite für Audio-Mischung erweitert.

- [ ] **TASK-CSD-02: Erweiterte Generator-Profile für Kling 1.5 & Runway Gen-3** (`effort=medium`, `scope=cdp`, priority `normal`).
  - **Goal:** Vorkonfigurierte CDP-Injektionsskripte und Selektor-Matrizen für weitere KI-Videogeneratoren bereitstellen.
  - **Definition of Done:** Selektoren in `cdp_automator.py` abstrahiert und mit Mock-CDP getestet.

- [x] **TASK-CSD-03: Release-Hygiene & Gate-Bereitschaft (v0.1.1)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** Pfadneutralität in Templates und Watcher umgesetzt, `.gitignore` vervollständigt, `TODO.md` und `llms.txt` hinterlegt.

- [x] **TASK-CSD-04: Pfad B Discoverability, 16-Point Quick Navigation & Third-Party Audit (v0.1.4)** (`effort=low`, `scope=marketing`, priority `normal`).
  - **Result:** 16-Punkte-Schnellnavigation, Target Personas, Drittanbieter-Lizenzen, PEP 621 URLs und Marketing-Logbuch etabliert.

- [x] **TASK-CSD-05: Pfad A Technische Hygiene, PEP 561 Inline-Typisierung & CI-Härtung (v0.1.5)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** `py.typed` integriert, `python -m clip_director` Executable Entrypoint mit `-v` / `--version` Flag, `timeout-minutes: 15` in CI-Matrix, package-data für HTML/YAML Templates in Wheel-Build, und Vertragstestsuite erweitert.

---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->
