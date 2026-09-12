# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
