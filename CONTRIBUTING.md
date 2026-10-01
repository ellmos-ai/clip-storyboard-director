# Contributing to clip-storyboard-director / Mitwirken an clip-storyboard-director

Welcome! We welcome contributions to `clip-storyboard-director` (Local-first AI storyboard director and video pipeline orchestrator). To maintain deterministic video staging, air-gapped process isolation, single-writer filesystem safety, and compliance across multi-host environments, all contributions must adhere to the quality standards and operational invariants defined below.

---

## English

### 1. General Principles & Quality Gates
1. **Local-First & Zero-Egress (`INV-LOCAL-01`)**: Core directorial server, dashboard, and CLI workflows operate strictly offline on localhost loopback (`127.0.0.1:8765` and `127.0.0.1:9222`). Zero external telemetry, tracking, or outbound sockets.
2. **Unprivileged User-Mode Execution (`INV-UNPRIV-02` / `RunAsInvoker`)**: All server, CDP automation, downloads watching, clue-frame extraction, and FFmpeg assembly execute strictly in unprivileged user space without administrative elevation or root privileges.
3. **Loopback IPC & Security Boundary (`INV-LOOPBACK-03`)**: Directorial server and browser bridges bind exclusively to localhost loopback interfaces; external network exposure is rejected by design.
4. **Isolated Subprocess Boundaries & Zero-Copyleft (`INV-SANDBOX-04`)**: Core engine is 100% MIT-licensed. External tools like FFmpeg/FFprobe and speech synthesis (edge-tts) execute strictly through parameterized external subprocesses, ensuring complete zero-copyleft runtime isolation.
5. **4D Persistence Buffer Continuity (`INV-CONTINUITY-05`)**: Declarative `project.yaml` ensures character, style, prop, and lighting continuity across shots and restarts.
6. **Clue-Frame Chaining (`INV-CLUEFRAME-06`)**: Automatic optical extraction of tail frames primes subsequent prompt conditioning without manual frame export.
7. **Standalone Decoupling (`INV-STANDALONE-07`)**: Operates as a completely independent CLI/GUI video director with zero mandatory dependencies on external cloud portals.
8. **Multi-OS Parity (`INV-MULTIOS-08`)**: Full compatibility across Windows, Linux, and macOS.
9. **Cloud-Sync & Lock Defense (`INV-SYNC-09`)**: Resilient against cloud synchronization conflicts, temporary files, and canonical multi-agent locks.
10. **48h Security & Governance SLA (`INV-SLA-10`)**: Maintain 48h acknowledgment and 5-business-day triage commitments for security reports.
11. **Version Freeze Discipline (`T-20260920-167562623`)**: Version 0.1.6 is strictly frozen across all manifests. Do not bump the version string. Document all advancements under `## [Unreleased]` in `CHANGELOG.md`.
12. **Clean Code & Regression Testing**: Every feature or fix must include regression tests in `tests/`. Keep test coverage at 100% pass rate.
13. **Bilingual Parity**: Maintain synchronized structural and navigational parity across `README.md` and `README_de.md` (18-point dual anchors `sec-01` through `sec-18`).

### 2. Local Development Workflow
```bash
# Install package with development dependencies
python -m pip install -e ".[dev]"

# Run comprehensive test suite
python -X utf8 -m pytest -ra -v

# Run linter
python -m ruff check src tests

# Check bytecode compilation
python -m compileall -q src tests

# Check whitespace and git diff cleanliness
git diff --check
```

### 3. Submission Protocol
- Open an issue for architectural discussions before large refactoring.
- Keep provider API keys, tokens, and private credentials strictly outside the repository.
- Ensure all 10 governance invariants (`INV-LOCAL-01` to `INV-SLA-10`) remain VERIFIED.

---

## Deutsch

### 1. Grundsätze & Qualitäts-Tore
1. **Local-First & Zero-Egress (`INV-LOCAL-01`)**: Sämtliche Regie-, Timeline- und CLI-Abläufe arbeiten standardmäßig zu 100% offline auf Loopback-Schnittstellen (`127.0.0.1:8765`, `127.0.0.1:9222`) ohne Telemetrie, Sockets oder externe Datenübertragung.
2. **Unprivilegierte Benutzer-Ausführung (`INV-UNPRIV-02` / `RunAsInvoker`)**: Sämtliche Server-, CDP-, Beobachtungs- und FFmpeg-Prozesse laufen strikt im unprivilegierten Standard-Benutzerkontext ohne administrative Rechte oder UAC-Elevation.
3. **Strikte Loopback-IPC-Isolation (`INV-LOOPBACK-03`)**: Regieserver und Browser-Brücken binden ausschließlich an lokale Loopback-Schnittstellen.
4. **Isolierte Subprozess-Grenzen & Zero-Copyleft (`INV-SANDBOX-04`)**: Der Kern ist 100% MIT-lizenziert. Externe Werkzeuge wie FFmpeg und Sprachgenerierung (edge-tts) werden strikt als externe Subprozesse isoliert ausgeführt.
5. **4D-Persistenzpuffer-Kontinuität (`INV-CONTINUITY-05`)**: Deklarative `project.yaml` sichert Figuren-, Szenen- und Requisiten-Kontinuität über alle Shots und Neustarts hinweg.
6. **Clue-Frame-Verkettung (`INV-CLUEFRAME-06`)**: Automatische Extraktion des letzten Frames zur nahtlosen visuellen Konditionierung von Folgeszenen.
7. **Eigenständige Entkopplung (`INV-STANDALONE-07`)**: Vollwertig autark als lokale Regie-Suite einsetzbar ohne proprietäre Cloud-Abhängigkeit.
8. **Multi-OS-Betriebsparitt (`INV-MULTIOS-08`)**: Gleichwertige Lauffähigkeit unter Windows, Linux und macOS.
9. **Cloud-Sync- & Lock-Resilienz (`INV-SYNC-09`)**: Robuste Abschirmung gegen Cloud-Synchronisationskonflikte und Multi-Agent-Sperren.
10. **48h Sicherheits- & Governance-SLA (`INV-SLA-10`)**: Einhaltung von 48h Reaktionszeit und 5 Werktagen Triage-Frist für Sicherheitsmeldungen.
11. **Strikte Versions-Freeze-Disziplin (`T-20260920-167562623`)**: Version 0.1.6 bleibt in allen Manifesten eingefroren. Keine Versionserhöhung vornehmen; alle Änderungen unter `## [Unreleased]` in `CHANGELOG.md` festhalten.
12. **Testabdeckung & Regressionstests**: Für jede Verhaltensänderung ist ein Vertragstest in `tests/` zu ergänzen. Die Testsuite muss zu 100% grün bleiben.
13. **Zweisprachige Dokumentationsparität**: `README.md` und `README_de.md` müssen strukturgleich und mit synchronen 18-Punkte-HTML-Ankern (`sec-01` bis `sec-18`) gepflegt werden.

### 2. Lokaler Entwicklungsablauf
```bash
# Entwicklungsumgebung einrichten
python -m pip install -e ".[dev]"

# Vollständige Testsuite ausführen
python -X utf8 -m pytest -ra -v

# Linter-Prüfung
python -m ruff check src tests

# Bytecode-Kompilierung
python -m compileall -q src tests

# Diff- und Whitespace-Prüfung
git diff --check
```

### 3. Einreichung
- Vor größeren Eingriffen ein Issue zur Abstimmung anlegen.
- LLM-API-Schlüssel, Zugriffstoken und vertrauliche Daten niemals ins Repository committen.
- Alle 10 Invarianten (`INV-LOCAL-01` bis `INV-SLA-10`) müssen erfüllt bleiben.
