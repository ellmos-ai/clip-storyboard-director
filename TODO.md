# TODO.md — Active work

**Version:** 0.1.1  
**Updated:** 2026-09-08  
**Reason:** Standardization, path neutrality, gate readiness, and AI discoverability  
**Purpose:** Track only work that remains open.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Core Director Pipeline | DONE | Project lifecycle, init, doctor, serve, cockpit, assemble verified and passing pytest (4/4 tests green). |
| Path Neutrality & Hygiene | DONE | Neutral paths (`~/Downloads`), sanitized docstrings, and strict `.gitignore` patterns aligned with gate standards. |
| AI Discoverability | DONE | Machine-readable `llms.txt`, PEP 621 classifiers, and schema v2 metadata parity established. |
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

---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->
