# TODO.md — Active work

- **Version:** 0.1.6
- **Updated:** 2026-09-20
- **Reason:** Pfad B discoverability, 18-point dual-anchor navigation parity, 10-dimension comparative matrix, Level 1 SBOM cross-reference, root NOTICE attribution, § 521 BGB statutory disclaimer, and contract test expansion
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
  - **Definition of Done:** Selektoren in `cdp_automator.py` abstrahiert und mit Mock-CDP getestet.

- [x] **TASK-CSD-03: Release-Hygiene & Gate-Bereitschaft (v0.1.1)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** Pfadneutralität in Templates und Watcher umgesetzt, `.gitignore` vervollständigt, `TODO.md` und `llms.txt` hinterlegt.

- [x] **TASK-CSD-04: Pfad B Discoverability, 16-Point Quick Navigation & Third-Party Audit (v0.1.4)** (`effort=low`, `scope=marketing`, priority `normal`).
  - **Result:** 16-Punkte-Schnellnavigation, Target Personas, Drittanbieter-Lizenzen, PEP 621 URLs und Marketing-Logbuch etabliert.

- [x] **TASK-CSD-05: Pfad A Technische Hygiene, PEP 561 Inline-Typisierung & CI-Härtung (v0.1.5)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Result:** `py.typed` integriert, `python -m clip_director` Executable Entrypoint mit `-v` / `--version` Flag, `timeout-minutes: 15` in CI-Matrix, package-data für HTML/YAML Templates in Wheel-Build, und Vertragstestsuite erweitert.

- [x] **TASK-CSD-06: Pfad B Discoverability, 18-Point Navigation Parity, 10-Dimension Comparative Matrix, Level 1 SBOM & NOTICE Attribution (v0.1.6)** (`effort=medium`, `scope=marketing`, priority `high`).
  - **Result:** 18-Punkte Navigationsparität mit reziproken dualen HTML-Ankern in beiden READMEs, 10-Dimensionen Vergleichsmatrix gegenüber 4 Alternativen, Level 1 SBOM Invarianten-Tabelle in THIRD_PARTY_LICENSES.md, formeller NOTICE Attributierungsnachweis, § 521 BGB Haftungshinweis, Mermaid-Syntaxbereinigung und erweiterte Vertragstest-Suite.


---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->
