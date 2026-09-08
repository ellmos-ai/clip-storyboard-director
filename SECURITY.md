# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

Sicherheitsrelevante Schwachstellen oder Fehler bitte vertraulich über GitHub Security Advisories oder direkt an die Betreiber melden:

- GitHub: https://github.com/ellmos-ai/clip-storyboard-director/security/advisories

Bitte übermittle aussagekräftige Schritte zur Reproduktion des Problems (PoC-Code, Logdateien, betroffene Plattform).

## Sicherheitsprinzipien & Datenschutz

1. **Local-First & Null-Telemetrie**: `clip-storyboard-director` überträgt keinerlei Nutzungsdaten, Telemetrie oder Analysedaten an Dritte.
2. **Lokale Netzwerkbindung**: Der integrierte Board-Server bindet standardmäßig ausschließlich an `127.0.0.1` (Localhost) und ist von externen Netzwerken isoliert.
3. **Dateisystem-Hygiene**: Datei- und Pfadoperationen validieren Projektpfade und unterbinden Directory-Traversal-Angriffe.
4. **Authentische Kodierung**: Alle Dokumentations- und Code-Ressourcen werden strikt in UTF-8 ohne BOM und mit korrekten deutschen Umlauten geführt.
