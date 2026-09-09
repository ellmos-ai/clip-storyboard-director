# Security Policy

[English](#english) | [Deutsch](#deutsch)

---

## English

### Supported Versions

The following versions of `clip-storyboard-director` currently receive security updates and maintenance:

| Version | Supported          | Status                                 |
| ------- | ------------------ | -------------------------------------- |
| `0.1.x` | :white_check_mark: | Active release & security maintenance  |
| `< 0.1` | :x:                | Superseded; please upgrade             |

---

### Core Security & Privacy Invariants

`clip-storyboard-director` is engineered from the ground up for strict local-first, privacy-respecting, and high-assurance multi-host video orchestration:

1. **100% Local-First & Zero-Egress Privacy**:
   - `clip-storyboard-director` executes locally on user workstations.
   - It contains zero telemetry, zero usage tracking, and zero remote analytics.
   - No prompts, voice synthesis audio, or generated video frames are ever transmitted to third-party tracking servers.

2. **Unprivileged Non-Elevation (`RunAsInvoker`)**:
   - The CLI and cockpit run strictly in standard user space.
   - No administrator, root, or elevated privileges are ever required or requested.

3. **Strict Loopback IPC & Port Isolation**:
   - The integrated board server binds exclusively to `127.0.0.1` (port `8765`), completely isolated from external local area networks.
   - Browser automation via Chrome DevTools Protocol (CDP) binds strictly to `127.0.0.1` (port `9222`).

4. **Safe Subprocess Sandboxing & Argument Escaping**:
   - Invocations of external binaries (`ffmpeg`, `ffprobe`, `msedge`) use parameterized argument arrays with zero shell interpolation.
   - Guarded against command injection, shell piping risks, and path traversal exploits.

5. **4D Persistence Continuity Buffer Isolation**:
   - Character appearances, locations, and continuity metadata are stored strictly in local project files (`project.yaml`).
   - In-memory representations prevent unintended leakage across separate project workspaces.

6. **Clue-Frame Optical Chaining Integrity**:
   - Keyframe extraction and optical continuity clues are stored with deterministic hashing and relative path validation.
   - Directory traversal attacks during media ingestion are rejected.

7. **Standalone Decoupling & Graceful Degradation**:
   - The director operates fully standalone without requiring `ai-media-editor`.
   - Missing optional dependencies (`edge-tts`, `websocket-client`, Edge browser) trigger informative notices rather than catastrophic failure.

8. **Multi-OS Operating Parity**:
   - Path handling uses Python's `pathlib.Path` ensuring identical security boundaries across Windows, Linux, and macOS.

9. **Cloud-Sync Conflict & Lock Resilience**:
   - File writes are atomic, defending against sync collisions from cloud storage mirrors (OneDrive/Nextcloud) and multi-agent concurrency.
   - Dedicated ignore rules filter lock files and conflict copies.

10. **48h Security Response & 5-Day Triage SLA**:
    - Incoming vulnerability reports receive formal acknowledgement within 24 to 48 hours, with triage analysis within 5 business days.

---

### Reporting a Vulnerability

If you discover a security vulnerability, privilege escalation flaw, or data leakage in `clip-storyboard-director`:

- **Maintainer Contact**: `security@ellmos.ai`
- **Umbrella Security**: `security@open-bricks.org` / `lukas@open-bricks.org` / `support@lukasgeiger.com`
- **GitHub Security Advisory**: [Report a Vulnerability](https://github.com/ellmos-ai/clip-storyboard-director/security/advisories)

Please provide:
1. Clear steps to reproduce or a minimal proof-of-concept.
2. Operating system, Python version, and `clip-storyboard-director` version.
3. Impact assessment and remediation suggestions if known.

We acknowledge incoming vulnerability reports within **24 to 48 hours**, provide an initial triage assessment within **5 business days**, and coordinate disclosure and patch releases via GitHub Security Advisories.

---

## Deutsch

### Unterstützte Versionen

Folgende Versionen von `clip-storyboard-director` erhalten aktiv Sicherheits- und Wartungsaktualisierungen:

| Version | Unterstützt        | Status                                      |
| ------- | ------------------ | ------------------------------------------- |
| `0.1.x` | :white_check_mark: | Aktive Version & Sicherheitswartung         |
| `< 0.1` | :x:                | Abgelöst; bitte auf aktuelle Version heben  |

---

### Sicherheits- und Datenschutz-Invarianten

`clip-storyboard-director` folgt strengen Grundsätzen für belegbare, lokale Datensicherheit und Orchestrierungsintegrität:

1. **100% Local-First & Zero-Egress**:
   - Läuft vollständig lokal auf der Arbeitsstation des Nutzers.
   - Keine Telemetrie, keine Nutzungsstatistiken und keine externen Serveranfragen.
   - Prompts, Audioaufnahmen und Frames verlassen niemals die lokale Arbeitsumgebung.

2. **Unprivilegierter User-Mode (Non-Elevation / RunAsInvoker)**:
   - CLI und Cockpit operieren ausschließlich mit normalen Benutzerrechten.
   - Keine Administrator- oder Root-Rechte erforderlich.

3. **Strikte Loopback-Netzwerkbindung & Port-Isolation**:
   - Der Board-Server bindet ausschließlich an `127.0.0.1` (Port `8765`), isoliert von externen Netzwerken.
   - Die CDP-Browser-Automatisierung lauscht strikt auf `127.0.0.1` (Port `9222`).

4. **Sicheres Subprozess-Sandboxing**:
   - Aufrufe von `ffmpeg`, `ffprobe` und `msedge` erfolgen über parameterisierte Argumentlisten ohne Shell-Interpolation (`shell=False`).
   - Schutz vor Command-Injection und Path-Traversal-Angriffen.

5. **4D-Persistenz- & Kontinuitätspuffer-Schutz**:
   - Kontinuitätsmerkmale für Figuren, Requisiten und Schauplätze werden ausschließlich lokal in `project.yaml` geführt.
   - Keine Vermischung oder Lecks zwischen verschiedenen Projekten.

6. **Optische Clue-Frame-Integrität**:
   - Letzte Frames und optische Referenzen werden deterministisch und mit relativer Pfadprüfung gespeichert.
   - Path-Traversal bei Medien-Ingest wird abgewiesen.

7. **Eigenständige Entkopplung & Graceful Degradation**:
   - Funktioniert vollständig autonom ohne die Präsenz von `ai-media-editor`.
   - Fehlende optionale Werkzeuge lösen verständliche Diagnosehinweise aus.

8. **Plattformübergreifende Betriebsparität**:
   - Einheitliche Sicherheits- und Pfadsemantik über `pathlib.Path` auf Windows, Linux und macOS.

9. **Cloud-Sync- & Lock-Resilienz**:
   - Atomare Dateioperationen schützen vor Konfliktkopien und Multi-Agenten-Races.

10. **48h Sicherheits- & 5-Tage-Triage-SLA**:
    - Bestätigung eingehender Berichte innerhalb von 24–48 Stunden, qualifizierte Triage innerhalb von 5 Werktagen.

---

### Meldung von Sicherheitslücken

Bei Verdacht auf eine Sicherheitslücke oder Schwachstelle wenden Sie sich bitte an:

- **E-Mail Maintainer**: `security@ellmos.ai`
- **Dachorganisation**: `security@open-bricks.org` / `lukas@open-bricks.org` / `support@lukasgeiger.com`
- **GitHub Security Advisory**: [Schwachstelle vertraulich melden](https://github.com/ellmos-ai/clip-storyboard-director/security/advisories)
