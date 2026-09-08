# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
