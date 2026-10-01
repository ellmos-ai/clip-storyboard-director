# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Ruhigeres Cockpit (Storyboard + Bridge)**: Eine Akzentfarbe statt sechs, keine Glows, Verläufe und Hover-Sprünge, deutlich weniger Emojis; `prefers-reduced-motion` wird respektiert, Textkontraste erfüllen WCAG AA. Die Timeline steht oben und bleibt beim Scrollen sichtbar; Persistenzpuffer und Konsistenz-Kartei folgen direkt darunter, standardmäßig aufgeklappt, mit Zählern im Kopf und einklappbar (Zustand wird gemerkt); Kamera/Licht/Ton je Shot ist ebenfalls aufgeklappt. Keine Funktion entfernt (Inventar in PR #3). Der aktuelle Shot ist in Timeline und Karte markiert; die Bridge-Spalte zeigt ihn zuerst, den Iframe-Hinweis nur noch auf Klick.
- **Ehrliche Statusanzeigen**: Download-Überwachung und CDP-Status werden vom Server gelesen statt statisch „Aktiv“ bzw. „Autopilot aktiv“ anzuzeigen; `/api/cowork/focus` liefert `has_hero`, damit das Cockpit „alle Shots fertig“ erkennt.

### Added
- **CI Lifecycle Workflows & Auto-Assign**: Provisioned `.github/workflows/auto-assign.yml` (automatic maintainer assignment for pull requests with concurrency group and 5-min timeout) and `.github/workflows/label-sync.yml` (automated standard label synchronization via workflow dispatch).
- **Canonical Standard Labels Manifest (`.github/labels.yml`)**: Added standard issue and pull request labels matching GOVERNANCE.md §4.2 specifications (`bug`, `enhancement`, `good first issue`, `help wanted`, `documentation`, `duplicate`, `wontfix`, `priority: high`, `priority: low`, `needs-triage`, `stale`, `security`, `dependencies`).
- **Bilingual Contributing Guidelines (`CONTRIBUTING.md`)**: Authored comprehensive bilingual (English & German) contribution standards detailing Local-First & Zero-Egress (`INV-LOCAL-01`), unprivileged user-mode (`INV-UNPRIV-02` / `RunAsInvoker`), isolated subprocess boundaries with Zero-Copyleft isolation (`INV-SANDBOX-04`), 48h Security SLA (`INV-SLA-10`), and version freeze discipline (`T-20260920-167562623`).
- **PEP 621 Contributing URL**: Registered canonical `"Contributing"` URL under `[project.urls]` in `pyproject.toml`.
- **Ideapad Multi-Host Guardrails (.gitignore)**: Hardened `.gitignore` against Lenovo Ideapad sync collision copies (`*-IDEAPAD*`, `*-IDEAPAD-GEI*`, `*-IDEAPAD-GEI.*`).
- **18-Point Bilateral Quick Navigation Anchors (`sec-01`..`sec-18`)**: Provisioned standardized bilateral HTML anchors `<a id="sec-01"></a>` through `<a id="sec-18"></a>` across both `README.md` and `README_de.md` for rock-solid cross-language references and deep link stability.
- **ASCII Four-View Architectural Projection**: Introduced four-view ASCII topology diagrams into Section 2 of both READMEs covering user/agent interaction, directorial control with Edge CDP browser automation (:9222), 4D persistence buffer & clue-frame staging, and unprivileged user space perimeter.
- **Level 1 SBOM Plain-Text Companion (`THIRD_PARTY_LICENSES.txt`)**: Authored comprehensive plain-text Level 1 SBOM companion file in the repository root detailing runtime dependency boundaries, zero-copyleft guarantee, `RunAsInvoker` non-elevation certification, and full SPDX license texts.
- **PEP 621 Topics & Metadata Saturation**: Saturated `keywords` in `pyproject.toml` with 20 GitHub repository topics, added `"Level 1 SBOM"`, `"Third-Party Licenses (Text)"`, and `"Plain-Text License"` to `[project.urls]`, and included `THIRD_PARTY_LICENSES.txt` in `license-files`.
- **Stale Issues & PRs Lifecycle Automation**: Added `.github/workflows/stale.yml` using `actions/stale@v9` with least-privilege permissions (`issues: write`, `pull-requests: write`), `timeout-minutes: 10`, concurrency group cancellation, and automated 30-day stale / 7-day close lifecycle.
- **Extended Multi-Host Sync & Lock Defense (.gitignore)**: Hardened `.gitignore` against cross-device conflict copies (`*conflicted copy*`, `* (Kopie)*`, `* (Copy)*`, `*-WORKSTATION*`, `*-WORKSTATION-LG*`, `*-ASUS*`, `*-ASUS-GEI*`, `*-LAPTOP*`, `*-Mac Studio*`, `*-MacBook*`), canonical lock-system files (`LOCK.user.*`, `LOCK.until.*`, `LOCK.condition.*`, `.automation-lock`), patch rejects (`*.rej`), merge remnants (`*.orig`), and tooling caches (`.tox/`, `.turbo/`, `.nyc_output/`, `.hypothesis/`, `.pytest_temp/`).
- **PEP 621 Standard URLs**: Registered canonical `"Notice"` and `"Bug Tracker"` URLs under `[project.urls]` in `pyproject.toml`.
- **Pytest Discovery Guardrails**: Configured `minversion = "7.0"` and explicit `norecursedirs` (`.git`, `.pytest_cache`, `__pycache__`, `build`, `dist`, `.venv`, `.pytest_temp`, `.tox`, `wheelhouse`) in `pyproject.toml`.

### Changed
- **Level 1 SBOM Plain-Text Companion & Markdown Re-Audit (Stand 2026-10-01)**: Re-audited `THIRD_PARTY_LICENSES.txt` and `THIRD_PARTY_LICENSES.md` with active audit timestamp `2026-10-01`, re-certifying Zero-Copyleft isolation, unprivileged user mode, loopback isolation, and runtime boundaries.
- **Attribution & SBOM Re-Audit**: Re-audited `THIRD_PARTY_LICENSES.md` (audit date 2026-09-29) and synchronized repository-root `NOTICE` with explicit cross-references to both `THIRD_PARTY_LICENSES.md` and `THIRD_PARTY_LICENSES.txt`.
- **Documentation & KI Context Parity**: Synchronized `README.md`, `README_de.md`, `llms.txt`, and `TODO.md` with active check timestamp 2026-10-01 and updated Shields.io badges.
- **Contract Test Suite Expansion**: Expanded `tests/test_metadata.py` with automated contract tests verifying bilateral quick navigation anchors `sec-01`..`sec-18`, ASCII Four-View Architectural Projection, Level 1 SBOM text companion, PEP 621 keywords saturation, extended project URLs, and CI lifecycle workflows. Version remains `0.1.6` (Pfad A hygiene and maintenance turnus, strict version-freeze per T-20260920-167562623).

## [0.1.6] - 2026-09-20

### Added
- **18-Point Quick Navigation Parity**: Upgraded `README.md` and `README_de.md` to a comprehensive 18-point navigation structure equipped with reciprocal dual HTML anchors (`<a id="..."></a>`) supporting English, German, and legacy anchor IDs.
- **10-Dimension Comparative Matrix**: Integrated an exhaustive comparative differentiation table into Section 11 of both READMEs benchmarking `clip-storyboard-director` against commercial video SaaS, manual browser workflows, heavy desktop NLEs, and ad-hoc scripts across 10 governance and technical criteria.
- **Root Attribution NOTICE**: Added repository-root [NOTICE](NOTICE) formally attributing Lukas Geiger, `ellmos-ai`, and `open-bricks` under the MIT License, and registered it in `pyproject.toml` under `license-files` following modern PEP 639 packaging standards.
- **Level 1 SBOM & Non-Elevation Governance**: Enhanced [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) with a Level 1 Software Bill of Materials (SBOM) Invariant Cross-Reference Matrix mapping all 10 governance invariants (`INV-LOCAL-01` through `INV-SLA-10`) and certified `RunAsInvoker` unprivileged execution.
- **Statutory Notice & Liability Limitation (§ 521 BGB)**: Added Section 18 to both READMEs declaring software provision as a statutory courtesy (*unentgeltliche Schenkung* / Gefälligkeit) under § 521 BGB with liability restricted to intent and gross negligence.
- **SEO & Discoverability Expansion**: Expanded `pyproject.toml` keywords with `zero-egress`, `ellmos-ai`, `open-bricks`, `edge-cdp`, and `browser-automation`, and documented High-Intent Discoverability in `MARKETING-LOG.txt`.
- **Contract Test Suite Hardening**: Expanded `tests/test_metadata.py` and `tests/test_director.py` with contract tests verifying the root `NOTICE` file, PEP 639 `license-files` declaration, 18-point dual navigation anchors, Mermaid clean syntax (semicolon-free class definitions), Level 1 SBOM invariants, and § 521 BGB statutory disclaimer.

### Changed
- **Version Bump**: Synchronized version `0.1.6` across `clip_director/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`, `llms.txt`, and automated test suites.
- **Badge Parity**: Updated Shields.io badges in `README.md` and `README_de.md` for version `0.1.6`, test status, Level 1 SBOM, RunAsInvoker, NOTICE attribution, and audit date `2026-09-20`.
- **Mermaid Diagram Cleanup**: Removed trailing semicolons from all `classDef` and `class` statements in architecture diagrams for 100% clean rendering across GitHub markdown viewers.

## [0.1.5] - 2026-09-13

### Added
- **PEP 561 Inline Typing Support**: Added `py.typed` marker in `src/clip_director/` and declared package-data in `pyproject.toml` (`["py.typed", "*.html", "*.yaml"]`) ensuring distribution wheels include static typing markers and all HTML/YAML cockpit templates.
- **Executable Module Entrypoint (`python -m clip_director`)**: Added `src/clip_director/__main__.py` and enhanced CLI parser with short `-v` version flag and optional `argv` passing for robust programmatic invocation and testing.
- **CI Workflow Hardening**: Added `timeout-minutes: 15` execution guardrail to test matrix in `.github/workflows/ci.yml` and standardized dependency installation via `pip install -e ".[dev]"`.
- **PEP 639 License Metadata Parity**: Standardized `pyproject.toml` with `license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]` and superseded legacy classifier with SPDX expression.
- **Ruff Linter Configuration**: Added explicit `[tool.ruff]` and `[tool.ruff.lint]` configurations in `pyproject.toml` (`line-length = 100`, `target-version = "py310"`, rules `["E", "F", "W"]`).
- **Contract Test Suite Expansion**: Added comprehensive test contracts in `tests/test_director.py` and `tests/test_metadata.py` verifying PEP 561 typing markers, PEP 639 license files, ruff configuration, CI timeout guardrails, dev extra installation, CLI `-v` and module execution, and TODO version parity.

### Changed
- **Version Bump**: Synchronized version `0.1.5` across `clip_director/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`, `llms.txt`, and automated test suites.
- **Badge Parity**: Updated Shields.io badges for version `0.1.5` and last-checked date `2026-09-13` across `README.md` and `README_de.md`.
- **Git Ignore Hardening**: Added typing cache patterns (`.mypy_cache/`, `.dmypy.json`, `dmypy.json`, `.pyre/`, `.pytype/`) and coverage wildcards (`.coverage.*`) to `.gitignore`.

## [0.1.4] - 2026-09-12

### Added
- **16-Point Quick Navigation Parity**: Restructured `README.md` and `README_de.md` to feature 16 standardized quick navigation anchors with 100% mutual link parity and bilingual cross-references.
- **Target Personas & Discoverability**: Documented 4 distinct target audience profiles (AI Filmmakers & Narrative Directors, Generative Media Engineers, Content Creators & YouTubers, Autonomous Coding Agents) along with a bilingual high-intent keyword search matrix.
- **Third-Party Licensing Audit & Invariants**: Documented full software inventory in `THIRD_PARTY_LICENSES.md` with explicit GPL-3.0 (`edge-tts`) and LGPL-2.1+ (`FFmpeg`) architectural boundaries and compliance invariants (`INV-LOCAL-01`, `INV-UNPRIV-02`, `INV-LOOPBACK-03`).
- **5-Way Competitive Matrix**: Added exhaustive 10-dimension competitive differentiation matrix in `MARKETING-LOG.txt` comparing against commercial SaaS, manual browser workflows, heavy NLEs, and ad-hoc scripts.
- **PEP 621 Extended Project URLs**: Added metadata links in `pyproject.toml` for `Third-Party Licenses`, `Marketing-Log`, and `LLM-Ready`.
- **Contract Test Suite Expansion**: Added automated contract assertions in `tests/test_metadata.py` for target personas, third-party licensing sections, PEP 621 extended URLs, marketing log structure, and changelog synchronization.

### Changed
- **Version Bump**: Synchronized version `0.1.4` across `clip_director/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`, `llms.txt`, and automated test suites.
- **Badge Parity**: Synchronized Shields.io badges for version 0.1.4, test suite passing, and last-checked date 2026-09-12 across documentation files.

## [0.1.3] - 2026-09-10

### Changed
- **Version Bump**: Synchronized version `0.1.3` across `clip_director/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`, `llms.txt`, and automated test suites.
- **Pytest Configuration Parity**: Hardened pytest options in `pyproject.toml` (`addopts = "-ra -v"`) and GitHub Actions CI workflow (`.github/workflows/ci.yml`) to standardized `-ra -v` flags.
- **Repository Hygiene & Git Ignore**: Hardened `.gitignore` against multi-host synchronization conflicts (`*-ASUS-GEI.*`, `*-WORKSTATION-LG.*`, `*-WORKSTATION.*`, `* (kopie)*`, `* (copy)*`), canonical multi-agent locks (`LOCK.permissions.json`, `uv.lock`), and coverage/packaging cache directories (`coverage/`, `wheelhouse/`, `.wheel-smoke/`).

### Added
- **Contract Test Suite Expansion**: Expanded `tests/test_metadata.py` with 4 new contract tests (`test_gitignore_hygiene_patterns`, `test_pytest_configuration_and_flags`, `test_ci_workflow_pytest_flags`, `test_changelog_recent_pfad_a_entry`) asserting repository hygiene, CI flags, and changelog synchronization.

## [0.1.2] - 2026-09-09

### Added
- **Bilingual Documentation Parity**: Deployed standardized English `README.md` and German `README_de.md` featuring 14-point quick navigation, dual Mermaid diagrams (architecture flowchart and production lifecycle sequence), 10 governance invariants, and a 17-project sibling ecosystem matrix.
- **Continuous Integration**: Added multi-OS GitHub Actions CI workflow (`.github/workflows/ci.yml`) covering Ubuntu, Windows, and macOS across Python 3.10, 3.11, 3.12, and 3.13 with concurrency control, ruff linter, compileall bytecode validation, and pytest runner.
- **Contract & Metadata Test Suite**: Added `tests/test_metadata.py` verifying document presence, version synchronization, badge parity, Mermaid syntax, and security SLAs.
- **Third-Party Licensing Inventory**: Created `THIRD_PARTY_LICENSES.md` documenting runtime and dev dependencies, system binaries (FFmpeg, Edge), and license texts.
- **Marketing & Discoverability Log**: Added `MARKETING-LOG.txt` recording Path B verification steps and release health.

### Changed
- **Version Bump**: Synchronized version `0.1.2` across `clip_director/__init__.py`, `pyproject.toml`, `ellmos-module.v2.json`, `llms.txt`, and test suites.
- **Packaging & Classifiers**: Added Python 3.13 and OS-independent classifiers to `pyproject.toml`, along with project URLs for parent organization and open-bricks umbrella.
- **Security Policy Hardening**: Upgraded `SECURITY.md` to full bilingual standard with 48h response SLA, 5-business-day triage commitment, and 10 core security invariants.
- **Git Ignore Hardening**: Expanded `.gitignore` with multi-agent lock patterns (`LOCK`, `LOCK.*`, `*.lock`, `LOCK*.txt`) and multi-host sync conflict copies.
- **Codebase Cleanliness**: Resolved all ruff lint errors and removed backslash escapes in f-strings across `src/clip_director/` for full Python 3.10 parity.

## [0.1.1] - 2026-09-08

### Changed
- **Path Neutrality**: Sanitized default download directory resolution in `DownloadsWatcher` to use dynamic user home (`~/Downloads`) instead of hardcoded paths.
- **Template Hygiene**: Replaced hardcoded personal user directories in `dashboard_template.html` with neutral references.
- **Microphone Labeling**: Renamed live recording speaker label to neutral `"Live-Aufnahme (Mikrofon)"`.
- **Git Ignore**: Aligned `.gitignore` with release gate criteria (explicit `__pycache__`, `*.pyc`, `.env`, `*.db`, `data/`, sync conflict patterns, and lock patterns).

### Added
- **AI Discoverability**: Added `llms.txt` specification detailing architecture, invariants, CLI usage, and security parameters.
- **Status & Tasks**: Added `TODO.md` with structured `STATUS` table.
- **Security Policy**: Added `SECURITY.md` documenting local-first guarantees and vulnerability reporting.
- **Plan-D Pointer**: Added `PLAN_D_POINTER.md` in the `.MODULES/.DOMAINS` mirror.
- **Hygiene Tests**: Added automated tests verifying path neutrality, metadata parity, and gitignore invariants.

## [0.1.0] - 2026-09-07

### Added
- Initial release of `clip-storyboard-director`.
- 4D persistence buffer for characters, locations, objects, and props.
- Clue-frame continuity chain extraction and visual handoff.
- Interactive timeline dashboard server and Edge dual-pane cockpit.
- Browser CDP prompt injection and download watcher.
- Multi-track audio assembly with speech synthesis (`edge-tts`) and dynamic ducking.
- Bi-directional handoff integration with `ai-media-editor`.
