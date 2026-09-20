<p align="center">
  <img src="assets/banner.png" alt="clip-storyboard-director — Local-First KI-Regisseur & Szenen-Kontinuitäts-Orchestrator" width="100%">
</p>
<!-- alternate banner: assets/banner.svg (swap on occasion) -->

# clip-storyboard-director

<p align="center">
  <strong>Local-First KI-Regisseur & Szenen-Kontinuitäts-Orchestrator</strong><br>
  <em>Verbindet generative KI-Videomodelle, Browser-Automatisierung (CDP), 4D-Persistenzpuffer und Mehrspur-Audio-Mastering zu einer konsistenten filmischen Pipeline.</em>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> |
  <a href="README_de.md"><strong>Deutsch</strong></a>
</p>

<p align="center">
  <a href="https://github.com/ellmos-ai/clip-storyboard-director/actions/workflows/ci.yml"><img src="https://github.com/ellmos-ai/clip-storyboard-director/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://img.shields.io/badge/pytest-passing-brightgreen"><img src="https://img.shields.io/badge/pytest-passing-brightgreen" alt="Tests"></a>
  <a href="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue"><img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue" alt="Python"></a>
  <a href="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey"><img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Plattformen"></a>
  <a href="https://img.shields.io/badge/privacy-100%25%20Local--First%20%7C%20Zero--Egress-brightgreen"><img src="https://img.shields.io/badge/privacy-100%25%20Local--First%20%7C%20Zero--Egress-brightgreen" alt="Datenschutz"></a>
  <a href="https://img.shields.io/badge/security-RunAsInvoker%20%7C%20Localhost%20Isolated-blue"><img src="https://img.shields.io/badge/security-RunAsInvoker%20%7C%20Localhost%20Isolated-blue" alt="Sicherheit"></a>
  <a href="https://img.shields.io/badge/security%20SLA-48h%20response%20%7C%205d%20triage-blue"><img src="https://img.shields.io/badge/security%20SLA-48h%20response%20%7C%205d%20triage-blue" alt="Sicherheits-SLA"></a>
  <a href="https://img.shields.io/badge/code%20style-ruff-000000.svg"><img src="https://img.shields.io/badge/code%20style-ruff-000000.svg" alt="Code Style: Ruff"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="Lizenz: MIT"></a>
  <a href="https://github.com/ellmos-ai"><img src="https://img.shields.io/badge/ecosystem-ellmos--ai-purple.svg" alt="Ökosystem"></a>
  <a href="https://github.com/open-bricks"><img src="https://img.shields.io/badge/umbrella-open--bricks-blueviolet.svg" alt="Dachorganisation"></a>
  <a href="https://github.com/ellmos-ai/clip-storyboard-director/releases"><img src="https://img.shields.io/badge/version-0.1.5-blue.svg" alt="Version 0.1.5"></a>
  <a href="llms.txt"><img src="https://img.shields.io/badge/llms.txt-Discovery%20Context-informational" alt="llms.txt"></a>
  <a href="MARKETING-LOG.txt"><img src="https://img.shields.io/badge/last%20checked-2026--09--13-informational" alt="Zuletzt geprüft"></a>
</p>

---

### 🧭 Schnellnavigation

- [1. Warum dieses Projekt existiert](#warum-dieses-projekt-existiert)
- [2. Systemarchitektur & Workflow](#systemarchitektur--workflow)
- [3. Das Regie- & Cutter-Duo](#das-regie---cutter-duo)
- [4. 4D-Persistenz & Bündige Kontinuität](#4d-persistenz--bündige-kontinuität)
- [5. Clue-Frame Kontinuitätskette](#clue-frame-kontinuitätskette)
- [6. Dual-Pane Regie-Cockpit](#dual-pane-regie-cockpit)
- [7. Mehrspur-Audio-Staging & Dynamisches Ducking](#mehrspur-audio-staging--dynamisches-ducking)
- [8. Governance- & Laufzeit-Invarianten](#governance---laufzeit-invarianten)
- [9. End-to-End Medien- & Produktions-Lebenszyklus](#end-to-end-medien---produktions-lebenszyklus)
- [10. Zielgruppen & Auffindbarkeit](#zielgruppen--auffindbarkeit)
- [11. Drittanbieter-Lizenzen & Transparenz](#drittanbieter-lizenzen--transparenz)
- [12. Geschwisterwerkzeuge & Partner-Matrix](#geschwisterwerkzeuge--partner-matrix)
- [13. Installation & CLI-Befehlsreferenz](#installation--cli-befehlsreferenz)
- [14. Referenzproduktion „Sternenseufzer“](#referenzproduktion-sternenseufzer)
- [15. Sicherheit & Datenschutz](#sicherheit--datenschutz)
- [16. Entwicklung & Verifikation](#entwicklung--verifikation)

---

## Warum dieses Projekt existiert

Einzelne KI-Videoclips über Modelle wie Veo, Kling, Sora oder Runway zu generieren, ist heute unkompliziert. Aus isolierten Kurzclips jedoch einen **zusammenhängenden narrativen Film** zu erstellen, scheitert in der Praxis an grundlegenden Hürden:

1. **Kontinuitäts-Drift**: Figuren verändern von Einstellung zu Einstellung Kleidung, Gesichtszüge oder Haarfarbe.
2. **Kontext-Amnesie**: Hintergrund-Schauplätze und Requisiten verformen sich oder verschwinden zwischen Schnitten.
3. **Manueller Download- & Upload-Frust**: Benutzer müssen Clips ständig händisch herunterladen, umbenennen, letzte Frames extrahieren und als Referenzbild wieder hochladen.
4. **Desynchronisierte Audio-Ebenen**: Synthetisierte Stimmen, Umweltgeräusche und Musik werden meist nachträglich ohne sauberes Timing oder Lautstärke-Ducking zusammengefügt.

`clip-storyboard-director` löst diese Herausforderungen durch eine automatisierte, lokale Regie-Pipeline. Das Werkzeug verwaltet einen **4D-Persistenzpuffer** über alle Szenen, extrahiert automatisch optische **Clue-Frames**, steuert Web-Generatoren über das **Chrome DevTools Protocol (CDP)**, überwacht Downloads und montiert mehrspurige Schnittfassungen – vollständig offline und ohne Telemetrie.

---

## Systemarchitektur & Workflow

```mermaid
flowchart TD
    subgraph Input["1. Drehbuch & Shot-Aufteilung"]
        Script["Story-Skript & Konzept"] --> Init["storyboard_init.py"]
        Init --> Config["project.yaml<br/>(4D-Persistenzpuffer & Shots)"]
    end

    subgraph Directing["2. Regieführung & Automatisierung"]
        Config --> Server["board_server.py<br/>(Port 8765)"]
        Server --> Cockpit["start_cockpit.py<br/>(Dual-Pane Edge-Cockpit)"]
        Server --> Bridge["edge_bridge.py<br/>(CDP-Automation :9222)"]
        Bridge --> Gen["KI-Videogenerator<br/>(Gemini / Runway / Kling)"]
    end

    subgraph Ingestion["3. Ingest & Kontinuität"]
        Gen --> DL["Downloads-Watcher"]
        DL --> Ingest["ingest.py"]
        Ingest --> Clue["Frame-Extraktor<br/>(Shot N Clue-Frame)"]
        Clue -.->|"Nächster Prompt + Bildreferenz"| Bridge
    end

    subgraph Assembly["4. Audio-Staging & Endschnitt"]
        Config --> Voice["TTS / Mikrofon-Aufnahme"]
        Ingest --> Assemble["assemble.py<br/>(FFmpeg Video-Assembler)"]
        Voice --> Assemble
        Assemble --> Master["Master-Video (.mp4)<br/>+ Audio-Staging"]
        Master -.-> Handoff["ai-media-editor<br/>(Timeline-Postproduktion)"]
    end

    classDef core fill:#2563eb,stroke:#1d4ed8,color:#ffffff;
    classDef buffer fill:#7c3aed,stroke:#6d28d9,color:#ffffff;
    classDef io fill:#059669,stroke:#047857,color:#ffffff;
    class Server,Bridge,Ingest,Assemble core;
    class Config,Clue,Master buffer;
    class Cockpit,Gen,DL,Voice io;
```

---

## Das Regie- & Cutter-Duo

`clip-storyboard-director` ist gezielt als der **Regisseur** in einem spezialisierten Zwei-Agenten-Medienproduktionsmodell konzipiert:

| Rolle | Werkzeug | Fokus & Kernaufgaben |
| :--- | :--- | :--- |
| **Regisseur (Director)** | `clip-storyboard-director` | **Pre-Production & Generierung**: Drehbuchauflösung, Shot-Timing, Prompt-Formulierung, Pflege des 4D-Persistenzpuffers, Edge-CDP-Injektion, optische Clue-Frame-Verkettung, Download-Auto-Ingestion und Rohschnitt-Montage. |
| **Cutter (Editor)** | `ai-media-editor` | **Post-Production**: Nicht-lineare Schnittbearbeitung, Multi-Track-Schnitt, Color-Grading, sanfte Übergangskurven, dynamisches Audio-Ducking, subframe-genaue Schnitte und finale Ausspielung. |

> **Eigenständigkeits-Garantie**: `clip-storyboard-director` arbeitet zu 100 % autonom. Es setzt `ai-media-editor` nicht voraus, um vollständige Filme zu planen, zu generieren und zu montieren. Ist `ai-media-editor` vorhanden, gelingt die Übergabe reibungslos über standardisierte Projektordner oder Exportformate.

---

## 4D-Persistenz & Bündige Kontinuität

Im Filmbereich umfasst Kontinuität drei Raumdimensionen plus die Zeitachse ($3D + T = 4D$). `clip-storyboard-director` sichert diese Parameter deklarativ über den `persistence_buffer` in `project.yaml`:

- **Figuren (Characters)**: Feste Identifikatoren, Kleidungsdetails, Statur, Haarfarbe und Gesichtsmerkmale.
- **Schauplätze (Locations)**: Raumaufbau, Architektur, Lichtverhältnisse und Kamerawinkel.
- **Requisiten (Props & Objects)**: Schlüsselobjekte, Materialeigenschaften, Gebrauchsspuren und physischer Zustand.
- **Atmosphäre (Palette)**: Farb-Grading-Stimmung, Wetterbedingungen, Tageszeiten und Raumakustik.

Jeder vom Regisseur erzeugte Prompt erbt automatisch diese Persistenzmerkmale, wodurch Stilbrüche und Modellhalluzinationen wirksam verhindert werden.

---

## Clue-Frame Kontinuitätskette

Die kritischste Bruchstelle bei sequentiellen KI-Videos ist der Schnittübergang. `clip-storyboard-director` etabliert die **Clue-Frame-Kontinuitätskette**:

1. **Deterministische Letzt-Frame-Extraktion**: Beim Ingest eines Takes $N$ nutzt `ingest.py` `ffprobe` und `ffmpeg`, um den exakt letzten sichtbaren Frame ($T_{\text{end}}$) verlustfrei zu sichern.
2. **Optische Referenz-Ablage**: Der Frame wird unter `projects/<name>/frames/shot<N>_lastframe.png` abgelegt.
3. **Automatische Prompt-Koppelung**: Vor der Erzeugung von Shot $N+1$ übergibt das System den Clue-Frame per CDP direkt an das Generator-Webinterface oder legt ihn arbeitsbereit auf dem Desktop ab.
4. **Nahtlose Bewegungskontinuität**: Das Videomodell startet exakt auf Basis des vorangegangenen Endbildes – ohne Bildspringen, mit konsistenter Kamerapositionierung und flüssiger Bewegung.

---

## Dual-Pane Regie-Cockpit

Der Regisseur bietet ein webbasiertes Timeline-Cockpit, das über `start_cockpit.py` im Microsoft Edge App-Modus gestartet wird (`--app=http://localhost:8765/cockpit.html`):

- **Linkes Panel (Storyboard-Timeline)**: Szenenkarten mit Laufzeiten, aktiven Prompts, Clue-Frame-Vorschauen, Sprachwiedergabe und Take-Auswahl.
- **Rechtes Panel (Generierungs-Studio)**: Paralleles Browser-Fenster, das via CDP verbunden ist und Prompts per Klick direkt in Gemini, Kling oder Runway einfügt.
- **Echtzeit-Zustandssynchronisation**: Alle Änderungen im UI synchronisieren unmittelbar in die lokale `project.yaml` über REST-Endpunkte (`/api/projects/update_shot`).

---

## Mehrspur-Audio-Staging & Dynamisches Ducking

Filmische Erzählungen leben vom mehrschichtigen Klang. `clip-storyboard-director` strukturiert das Audio in drei Ebenen:

1. **Dialog- & Sprachspur**: Lokale Sprachsynthese über `edge-tts` oder Live-Mikrofonaufnahmen direkt im Cockpit-Interface.
2. **Raumatmosphäre & Geräusche**: Szenenspezifische Umweltklänge (z. B. Sternwarten-Brummen, Windrauschen, Schritte).
3. **Filmmusik**: Musikalischer Soundtrack mit automatischer Lautstärkeabsenkung (Ducking) bei gesprochenen Dialogen via FFmpeg-Filter `sidechaincompress` und `amix`.

---

## Governance- & Laufzeit-Invarianten

Die folgenden 10 Kern-Invarianten garantieren die Zuverlässigkeit und Sicherheit von `clip-storyboard-director`:

| Garantie | Invarianten-Code | Durchsetzungs-Mechanismus | Verifikations-Regel |
| :--- | :--- | :--- | :--- |
| **1. 100% Local-First Datenschutz** | `INV-LOCAL-01` | Null Telemetrie, keine externen Serverzugriffe. | Code-Audit belegt vollständige Offline-Fähigkeit. |
| **2. Unprivilegierte Ausführung** | `INV-UNPRIV-02` | Normaler Benutzermodus (`RunAsInvoker`). | `SECURITY.md` und Systemprüfung fordern keine Root-Rechte. |
| **3. Loopback-Port-Isolation** | `INV-LOOPBACK-03` | Server bindet strikt an `127.0.0.1:8765`. | Netzwerkprüfungen weisen `0.0.0.0` strikt ab. |
| **4. Subprozess-Sandboxing** | `INV-SANDBOX-04` | Parameter-Arrays für `ffmpeg` und `msedge`. | Kein `shell=True` in der gesamten Codebasis. |
| **5. 4D-Persistenz-Kontinuität** | `INV-CONTINUITY-05` | Puffer für Figuren/Orte in `project.yaml`. | Prompt-Kompilierung prüft Persistenz-Attribute. |
| **6. Clue-Frame-Verkettung** | `INV-CLUEFRAME-06` | Automatische Letzt-Frame-Extraktion je Take. | `ingest.py` garantiert Clue-Frame-Ablage. |
| **7. Autonome Entkopplung** | `INV-STANDALONE-07` | Lauffähig ohne `ai-media-editor`. | Test `test_standalone_without_media_editor` grün. |
| **8. Plattform-Parität** | `INV-MULTIOS-08` | `pathlib.Path` auf Windows, Linux und macOS. | CI-Matrix testet alle drei Betriebssysteme. |
| **9. Cloud-Sync-Resilienz** | `INV-SYNC-09` | Ausschlussmuster für Locks und Konfliktkopien. | `.gitignore` filtert Mutex- und Konfliktdateien. |
| **10. 48h Sicherheits-SLA** | `INV-SLA-10` | Bestätigung binnen 48h, Triage in 5 Tagen. | In `SECURITY.md` und Contract-Tests verankert. |

---

## End-to-End Medien- & Produktions-Lebenszyklus

```mermaid
sequenceDiagram
    autonumber
    actor Regisseur as Mensch / LLM-Regisseur
    participant Engine as clip-director Engine
    participant Server as Board Server (:8765)
    participant Edge as Edge Browser (CDP :9222)
    participant KI as KI-Generator (Gemini/Runway)
    participant Watcher as Downloads-Watcher
    participant FFmpeg as FFmpeg Assembler

    Regisseur->>Engine: clip-director init --name film --duration 60
    Engine->>Server: Lokalen Server & Watcher starten
    Regisseur->>Server: Dual-Pane Cockpit öffnen
    Server->>Edge: Edge im App-Modus via CDP starten
    Regisseur->>Edge: Prompt für Shot 1 per CDP injizieren
    Edge->>KI: Video-Clip berechnen (Shot 1)
    KI-->>Watcher: Fertigen Clip in ~/Downloads ablegen
    Watcher->>Engine: Clip automatisch nach projects/film/video/ übernehmen
    Engine->>FFmpeg: Letzten Frame als Shot 1 Clue-Frame extrahieren
    Engine->>Server: Timeline aktualisieren & Clue-Frame anzeigen
    Regisseur->>Edge: Shot 2 Prompt + Clue-Frame als Referenz übergeben
    Edge->>KI: Anschließenden Clip berechnen (Shot 2)
    KI-->>Watcher: Fertigen Clip herunterladen
    Watcher->>Engine: Shot 2 übernehmen & nächsten Clue-Frame extrahieren
    Regisseur->>Engine: clip-director assemble --project film
    Engine->>FFmpeg: Takes schneiden + Voiceover & Musik mischen
    FFmpeg-->>Regisseur: film_master.mp4 fertig zur Wiedergabe
```

---

## Zielgruppen & Auffindbarkeit

`clip-storyboard-director` wurde für vier zentrale Nutzergruppen im Ökosystem generativer Medien entwickelt:

| Zielgruppe | Herausforderungen & Frustrationen | Lösung & Nutzenversprechen | Typischer Workflow |
| :--- | :--- | :--- | :--- |
| **KI-Filmschaffende & Narrative Regisseure** | Figuren- und Kostüm-Drift zwischen Einstellungen, unzusammenhängende Schnitte, manuelles Prompt-Kopieren. | Deklarativer 4D-Persistenzpuffer (`project.yaml`) und automatische optische Clue-Frame-Verkettung zwischen Shot-Ende und Folgeeinstellung. | `clip-director init` -> 4D-Puffer definieren -> Clue-Frames prüfen -> Schnitt assemblieren. |
| **Generative Medien-Entwickler** | Webbasierte Videoportale bieten keine skriptfähige lokale Automation oder strukturierte Dateiübernahme. | Chrome DevTools Protocol (CDP) Bridge auf Port 9222 und Echtzeit-Download-Watcher mit automatischer Dateieinordnung. | Edge CDP Bridge starten -> Skriptbasierten Take-Loop ausführen -> Clips auto-ingesten. |
| **Content Creator & YouTuber** | Manuelle Stimmaufnahme, Timing und Abmischung mit Hintergrundmusik in komplexen Schnittprogrammen kostet Stunden. | Integrierte Sprachsynthese über `edge-tts` und automatisches Side-Chain-Audio-Ducking über vier dedizierte Tonspuren. | Szenendialoge schreiben -> `clip-director voice` -> `clip-director assemble`. |
| **Autonome Coding-Agenten** | Cloud-abhängige Tools erfordern Login-Tokens, Administrator-Rechte oder blockieren ohne Benutzeroberfläche. | 100% Local-First Zero-Egress Architektur (`INV-LOCAL-01`), unprivilegierte `RunAsInvoker`-CLI und maschinenlesbarer `llms.txt`-Kontext. | Headless-Ausführung per `clip-director auto` -> Systemprüfung per `clip-director doctor`. |

### Suchbegriffe mit hoher Absicht (High-Intent Keywords)

- **Deutsch**: `clip-storyboard-director lokale KI-Regie`, `KI Storyboard Regisseur Python`, `Szenen-Kontinuität generative Videomodelle`, `Clue-Frame optische Bildverkettung`, `Lokale Video-Orchestrierung ohne Cloud-Zwang`, `Edge CDP Browser-Automatisierung KI Video`, `4D-Persistenzpuffer Charakter-Kontinuität`, `Mehrspur-Audio-Staging und Ducking FFmpeg`.
- **Englisch**: `ai storyboard director`, `scene continuity python`, `clue-frame video generator`, `local-first ai video orchestrator`, `veo kling runway automation`, `edge cdp video workflow`, `4d persistence buffer`, `automated audio staging and ducking python`.

---

## Drittanbieter-Lizenzen & Transparenz

`clip-storyboard-director` folgt strengen Open-Source-Governance-Standards, permissiven Lizenzen und Zero-Egress-Laufzeitgarantien:

- **Hauptmodul**: Lizenziert unter der permissiven [MIT-Lizenz](LICENSE).
- **Laufzeit-Abhängigkeiten**:
  - `PyYAML` (MIT-Lizenz): Deklarative Projektkonfiguration und Persistenzpuffer-Parsing.
  - `edge-tts` (GNU GPL-3.0): Eigenständiger lokaler Sprachsynthese-Subprozess.
  - `websocket-client` (Apache-2.0): Lokale Chrome DevTools Protocol Socket-Kommunikation.
  - `requests` (Apache-2.0): Lokale HTTP-Zielerkennung auf `127.0.0.1:9222`.
- **System-Binärdateien**:
  - `FFmpeg / FFprobe` (LGPL-2.1+ / GPL-2.0+): Medieninspektion, Clue-Frame-Extraktion und Video-Assemblierung über System-`PATH`.
  - `Microsoft Edge`: Optionaler Host-Browser für Dual-Pane Cockpit und CDP-Automatisierung.
- **Compliance & Local-First Invarianten**:
  - `INV-LOCAL-01`: 100% offline, null Cloud-Tracking, null externe Telemetrie.
  - `INV-UNPRIV-02`: Ausführung streng im unprivilegierten Benutzermodus (`RunAsInvoker`).
  - Ein vollständiges Softwareinventar und Lizenztexte sind in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) dokumentiert.

---

## Geschwisterwerkzeuge & Partner-Matrix

`clip-storyboard-director` ist Teil des **ellmos-ai**-Ökosystems und der Dachorganisation **open-bricks**:

| Repository | Domäne & Schwerpunkt | Beziehung zum Director |
| :--- | :--- | :--- |
| [ai-media-editor](https://github.com/ellmos-ai/ai-media-editor) | Postproduktion & Timeline-Editor | **Cutter-Partner**: Übernimmt assemblierte Schnitte zum Feinschliff. |
| [ellmos-voice-io](https://github.com/ellmos-ai/ellmos-voice-io) | Sprachsynthese & Audio-I/O | Liefert Stimmmodelle und Mehrfiguren-Audio-Staging. |
| [system-auditor](https://github.com/ellmos-ai/system-auditor) | Multi-Host Audit Engine | Überprüft Code-Hygiene, Lock-Governance und Metadaten-Parität. |
| [system-explorer](https://github.com/ellmos-ai/system-explorer) | Lokale System-Introspektion | Erkennt Hardware-Encoder (NVENC/VAAPI) und System-Codecs. |
| [ellmos-controlcenter-mcp](https://github.com/ellmos-ai/ellmos-controlcenter-mcp) | Governance & Capability Control | Steuert Agentenberechtigungen und Werkzeugfreigaben. |
| [ellmos-delegation-authority](https://github.com/ellmos-ai/ellmos-delegation-authority) | Autonome Aufgabendelegation | Koordiniert vollautonome Produktionsläufe. |
| [sqlite-transit-sync](https://github.com/ellmos-ai/sqlite-transit-sync) | Konfliktfreie Datenbank-Synchronisation | Gleicht Storyboard-Zustände zwischen Arbeitsstationen ab. |
| [memoryhooker-provenance](https://github.com/ellmos-ai/memoryhooker-provenance) | Kontext-Hooking & Gedächtnis | Hält Regie-Entscheidungen über lange Projekte konsistent. |
| [workflowhooker-provenance](https://github.com/ellmos-ai/workflowhooker-provenance) | Workflow-Tracking & Nachvollziehbarkeit | Dokumentiert Prompt-Historien, Take-Varianten und Modellversionen. |
| [automation-master](https://github.com/ellmos-ai/automation-master) | Enterprise Workflow-Automation | Steuert Hintergrund-Renderings und automatische Dateiübernahmen. |
| [automizer-for-claude-desktop](https://github.com/ellmos-ai/automizer-for-claude-desktop) | Claude Desktop Integration | Verbindet LLM-Assistenten direkt mit dem Timeline-Cockpit. |
| [WikiStub-Seed](https://github.com/ellmos-ai/WikiStub-Seed) | World-Building Wissensgraphen | Generiert detaillierte Hintergründe für den 4D-Persistenzpuffer. |
| [ProSync](https://github.com/file-bricks/prosync) | Resiliente Dateispiegelung | Spiegelt Videodaten zwischen Schnittplätzen. |
| [CleanMarkdown](https://github.com/doc-bricks/cleanmarkdown) | Dokumentations-Bereiniger | Formatiert Drehbücher, Skripte und Regieanweisungen. |
| [PrivacyMailDesk](https://github.com/dev-bricks/privacymaildesk) | Lokale E-Mail-Verarbeitung | Benachrichtigt Produzenten nach Renderschritten ohne Cloud-Tracking. |
| [prompt-archaeology-casestudy2](https://github.com/research-line/prompt-archaeology-casestudy2) | Prompt-Engineering-Forschung | Liefert praxiserprobte Prompts für Videomodelle. |
| [open-bricks](https://github.com/open-bricks/open-bricks) | Open-Source Dachorganisation | Definiert Governance-Standards, Sicherheits-SLAs und Release-Richtlinien. |

---

## Installation & CLI-Befehlsreferenz

### Voraussetzungen

- **Python**: 3.10, 3.11, 3.12 oder 3.13
- **FFmpeg & FFprobe**: Im System-`PATH` erforderlich für Frame-Extraktion und Video-Schnitt
- **Microsoft Edge** (oder Chrome): Für optionale CDP-Browser-Automatisierung
- **Optionale Python-Pakete**: `edge-tts` (Sprachsynthese), `websocket-client` (CDP-Bridge)

### Installation

```bash
# Repository klonen
git clone https://github.com/ellmos-ai/clip-storyboard-director.git
cd clip-storyboard-director

# Paket im Entwicklungsmodus installieren
pip install -e ".[dev]"
```

### Systemprüfung (`doctor`)

Prüft alle Binärdateien, Python-Module und Browser-Verbindungen:

```bash
clip-director doctor
```

### Befehlsübersicht

```bash
# 1. Neues Storyboard-Projekt anlegen (60s Gesamtzeit, 10s je Einstellung)
clip-director init --name my_film --title "Mein Spielfilm" --duration 60 --step 10

# 2. Interaktives HTML-Timeline-Dashboard generieren
clip-director render --project projects/my_film

# 3. Lokalen Board-Server starten (Standard-Port 8765)
clip-director serve --project projects/my_film --port 8765

# 4. Dual-Pane Regie-Cockpit in Microsoft Edge öffnen
clip-director cockpit --project my_film

# 5. Verbindungsstatus zu Edge CDP prüfen
clip-director cdp-status --port 9222

# 6. Downloads-Ordner überwachen und neue Clips automatisch einbinden
clip-director ingest --project projects/my_film --watch

# 7. Dialogstimmen für eine bestimmte Szene synthetisieren
clip-director voice --project projects/my_film --step 1

# 8. Finales Master-Video inklusive Tonmischung ausspielen
clip-director assemble --project projects/my_film

# 9. Autonomen Produktionsdurchlauf starten
clip-director auto --project projects/my_film
```

---

## Referenzproduktion „Sternenseufzer“

Das Repository enthält unter `projects/sternenseufzer/` eine vollständige Referenzproduktion:

- **Genre**: Sci-Fi-Drama / Kurzfilm
- **Handlung**: Ein Astronom in einer Gebirgssternwarte empfängt ein akustisches Resonanzsignal in Sternenlichtdaten.
- **Kontinuitäts-Matrix**: 4D-Persistenzpuffer für Dr. Alistair Vance, die Sternwartenkuppel und das Quanten-Spektrometer.
- **Sprachspuren**: Zweisprachige Direktiven (deutsche Quelle, englische Übersetzung) und Stummanweisungen.

Referenzprojekt direkt erkunden:
```bash
clip-director render --project projects/sternenseufzer
clip-director assemble --project projects/sternenseufzer
```

---

## Sicherheit & Datenschutz

- **Null-Telemetrie**: Keine Tracking-Pixel, keine Nutzungsstatistiken und keine externen Serveranfragen.
- **Unprivilegierter Modus**: Läuft vollständig im Benutzermodus (`RunAsInvoker`).
- **Localhost-Bindung**: Web-Dienste lauschen strikt auf `127.0.0.1`.
- **Sicherheits-SLA**: Bestätigung von Meldungen binnen 48 Stunden, qualifizierte Triage in 5 Werktagen. Siehe [SECURITY.md](SECURITY.md).

---

## Entwicklung & Verifikation

### Code-Prüfung & Bytecode-Kompilierung

```bash
ruff check src tests
python -m compileall -q src tests
```

### Testsuite ausführen

```bash
pytest -v
```

---

<p align="center">
  Teil der <strong><a href="https://github.com/ellmos-ai">ellmos-ai</a></strong> Werkzeugfamilie unter dem Dach von <strong><a href="https://github.com/open-bricks">open-bricks</a></strong>.
</p>
