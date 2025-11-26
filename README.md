# eml2pdf Converter – EML → PDF | 100% Paperless-ngx compatible
**Version 1.02 – 25 November 2025**  
© Michael Klissner – https://www.klissner.uk

Converts EML files (including all attachments) into a single, searchable, GoBD-compliant PDF – made for Paperless-ngx.

✅ Directly supported formats:

📄 Documents (via LibreOffice):
.doc, .docx (Word)
.xls, .xlsx (Excel)
.ppt, .pptx (PowerPoint)
.odt (OpenDocument Text)
.ods (OpenDocument Spreadsheet)
.odp (OpenDocument Presentation)
.rtf (Rich Text Format)
.pages (Apple Pages)
.numbers (Apple Numbers)

🖼️ Images (via PIL/Pillow):
.png
.jpg, .jpeg
.gif
.bmp
.tiff
.webp

📋 Already PDF:
.pdf (will be transferred directly)


## Official Images (GitHub Container Registry)

| Architecture           | Version 1.01 (stable)               | Latest (rolling)                   | Recommended for                               |
|------------------------|-------------------------------------|-------------------------------------|-----------------------------------------------|
| **x86_64** (Intel/AMD) | `ghcr.io/klissner/eml2pdf:1.02-x86` | `ghcr.io/klissner/eml2pdf:latest-x86` | Servers, desktops, NAS (Synology, QNAP, TrueNAS) |
| **ARM64** (aarch64)    | `ghcr.io/klissner/eml2pdf:1.02-arm` | `ghcr.io/klissner/eml2pdf:latest-arm`  | Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton |

Important: Always use the full tag with architecture suffix!

## Quick Start (Docker Compose)

```yaml
version: '3.8'
services:
  eml2pdf:
    image: ghcr.io/klissner/eml2pdf:1.02-x86      # x86 systems
    # image: ghcr.io/klissner/eml2pdf:1.02-arm    # Raspberry Pi / Apple Silicon
    container_name: eml2pdf
    restart: unless-stopped
    environment:
      - TZ=Europe/Berlin
      - LOGLEVEL=INFO
    volumes:
      - ./eml-import:/input
      - ./consume:/consume
      - ./eml-import/archiv:/eml-import/archiv
      - ./eml-import/error:/eml-import/error
      - ./config.json:/config.json

Start:bash

docker-compose up -d

Local folder structure

paperless/
├── docker-compose.yml
├── config.json
├── eml-import/           ← drop EML files here
│   ├── archiv/           ← archived EMLs
│   └── error/            ← failed files + logs
├── consume/              ← converted PDFs appear here
└── eml2pdf/              ← contains Dockerfile, main.py, requirements.txt

Configuration (config.json)json

{
  "separator_text": "Attachment {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 30,
  "max_logfile_size": 1048576,
  "max_logfile_backups": 2
}

What’s new in Version 1.02?
Full ARM64 support (Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton)  
Clear architecture separation (-x86 / -arm)  
Proper semantic versioning + stable tags  
Clean, multi-arch Dockerfile  


eml2pdf now truly runs everywhere – no compromises.
Donations & Support: Thank you for your support!  
PayPal → https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW
Bitcoin / Lightning / Bank → https://www.ksc-llp.uk/donateyoutubeContactMichael Klissner  
https://www.klissner.uk  
Mail: umschalter-excel-3e@icloud.com




# eml2pdf Converter – EML → PDF | 100% Paperless-ngx kompatibel
**Version 1.02 – 25. November 2025**  
(c) Michael Klissner – https://www.klissner.uk

Konvertiert EML-Dateien (inkl. Anhänge) GoBD-konform in ein einziges, durchsuchbares PDF – perfekt für Paperless-ngx.

✅ Direkt unterstützte Formate:

📄 Dokumente (via LibreOffice):
.doc, .docx (Word)
.xls, .xlsx (Excel)
.ppt, .pptx (PowerPoint)
.odt (OpenDocument Text)
.ods (OpenDocument Spreadsheet)
.odp (OpenDocument Presentation)
.rtf (Rich Text Format)
.pages (Apple Pages)
.numbers (Apple Numbers)

🖼️ Bilder (via PIL/Pillow):
.png
.jpg, .jpeg
.gif
.bmp
.tiff
.webp

📋 Bereits PDF:
.pdf (wird direkt übernommen)


## Offizielle Images (GitHub Container Registry)

| Architektur            | Version 1.01 (stabil)               | Aktuell (rolling)                  | Empfohlen für                                 |
|------------------------|-------------------------------------|-------------------------------------|-----------------------------------------------|
| **x86_64** (Intel/AMD) | `ghcr.io/klissner/eml2pdf:1.02-x86` | `ghcr.io/klissner/eml2pdf:latest-x86` | Server, Desktop, NAS (Synology, QNAP, TrueNAS) |
| **ARM64** (aarch64)    | `ghcr.io/klissner/eml2pdf:1.02-arm` | `ghcr.io/klissner/eml2pdf:latest-arm`  | Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton |

**Wichtig**: Immer den vollen Tag mit Architektur verwenden!

## Schnellstart (Docker Compose)

```yaml
version: '3.8'
services:
  eml2pdf:
    image: ghcr.io/klissner/eml2pdf:1.02-x86      # ← x86-Systeme
    # image: ghcr.io/klissner/eml2pdf:1.02-arm    # ← Raspberry Pi / Apple Silicon
    container_name: eml2pdf
    restart: unless-stopped
    environment:
      - TZ=Europe/Berlin
      - LOGLEVEL=INFO
    volumes:
      - ./eml-import:/input
      - ./consume:/consume
      - ./eml-import/archiv:/eml-import/archiv
      - ./eml-import/error:/eml-import/error
      - ./config.json:/config.json

Starten:bash

docker-compose up -d

Verzeichnisstruktur (lokal)

paperless/
├── docker-compose.yml
├── config.json
├── eml-import/           ← EML-Dateien hier reinlegen
│   ├── archiv/           ← archivierte EMLs
│   └── error/            ← fehlerhafte Dateien + Logs
├── consume/              ← fertige PDFs kommen hier raus
└── eml2pdf/              ← enthält Dockerfile, main.py, requirements.txt

Konfiguration (config.json)json

{
  "separator_text": "Anlage {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 30,
  "max_logfile_size": 1048576,
  "max_logfile_backups": 2
}

Was ist neu in Version 1.02?
Vollständige ARM64-Unterstützung (Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton)  
Klare Trennung der Architekturen (-x86 / -arm)  
Semantische Versionierung + stabile Tags  
Multi-arch-fähiges, sauberes Dockerfile  

Jetzt läuft eml2pdf wirklich überall – ohne Kompromisse. Spenden & Unterstützung. Vielen Dank für eure Unterstützung!  
PayPal → https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW
Bitcoin / Lightning / Bank → https://www.ksc-llp.uk/donateyoutubeKontaktMichael Klissner  
https://www.klissner.uk  
Mail: umschalter-excel-3e@icloud.com

