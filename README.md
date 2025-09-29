# 📑 eml2pdf Converter – English Document

## Overview
The **eml2pdf Converter** is a tool optimized for **Paperless workflows**, converting **EML files (including attachments)** into a single PDF document.  

Key Features:
- Focus on **GoBD compliance** (principles for proper record-keeping and retention).  
- **Seamless integration** with [Paperless](https://github.com/paperless-ngx/paperless-ngx).  
- Can also be used **standalone** to convert EML files.  

---

## Features
- **Input**: Processes EML files including attachments from an input directory.  
- **Conversion**: Converts via **LibreOffice** into a PDF (attachments as separate pages).  
- **Output**: Stored in the output directory (`consume`).  
- **GoBD compliance**: Metadata is preserved, conversion is traceable.  

---

## Performance
- **Scalability**: Handles multiple EML files simultaneously (depending on system resources).  
- **Speed**: Conversion of a typical EML file (~1 MB) takes ~5–10 seconds.  
- **Resources**: Built with **Python 3.11** and minimal dependencies (LibreOffice, Python packages).  

---

## Installation

### Requirements
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)  
- Git to clone the repository  
- Access to the **GitHub Container Registry** (PAT required)  

### Clone repository
```bash
git clone https://github.com/Klissner/eml2pdf-Converter-Docker-.git
cd eml2pdf-Converter-Docker-
```

### Pull image
```bash
docker pull ghcr.io/klissner/eml2pdf:latest
```

- Adjust configuration (see **Configuration** section)  
- Start the container (see **Docker Compose** section)  

---

## 🔧 Configuration (`config.json`)

The `config.json` file is located next to `docker-compose.yml` and controls the converter behavior.

```json
{
  "separator_text": "Attachment {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 30,
  "max_logfile_size": 1048576,
  "max_logfile_backups": 2
}
```

### Parameter description
- **separator_text** → Text for attachment separator (e.g., “Attachment 1: file.pdf”).  
- **poll_interval_seconds** → Interval in seconds (300 = every 5 minutes).  
- **separator_page** → Inserts a separator page before attachments (`on` / `off`).  
- **archive_retention_days** → Retention period for archived files in days (default: 30).  
- **max_logfile_size** → Maximum log file size in bytes (1 MB = `1048576`).  
- **max_logfile_backups** → Number of log backups (default: 2).  

👉 **Note**: Adjust `config.json` as needed and add it to `.gitignore` to prevent sensitive settings from being committed.  

---

## 🐳 Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  eml2pdf:
    image: ghcr.io/klissner/eml2pdf:latest
    build:
      context: ./eml2pdf
      dockerfile: Dockerfile
    volumes:
      - ./eml-import:/input
      - ./consume:/consume
      - ./eml-import/archiv:/eml-import/archiv
      - ./eml-import/error:/eml-import/error
      - ./config.json:/config.json
    environment:
      - TZ=Asia/Bangkok
      - LOGLEVEL=INFO
    restart: unless-stopped
```

### Parameter explanation
- **image** → Official container image (GitHub Container Registry).  
- **build** → Builds the image locally from the `./eml2pdf/` directory.  
- **volumes** → Maps local directories to container paths:  
  - `eml-import/` → Input for `.eml` files  
  - `consume/` → Output folder for generated PDFs  
  - `eml-import/archiv/` → Archived `.eml` files  
  - `eml-import/error/` → Error logs  
  - `config.json` → central configuration  
- **environment** → Container environment variables  
  - `TZ=Asia/Bangkok` → Time zone  
  - `LOGLEVEL=INFO` → Log level  
- **restart** → Container automatically restarts on failure or system reboot.  

---

## ▶️ Start & Stop

```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down
```

---

## 📂 Directory structure

```
/mnt/d/Docker Server/paperless/
│── docker-compose.yml
│── config.json
│── eml-import/            # Input (place EML files here)
│   ├── archiv/            # Archived EMLs
│   ├── error/             # Errors & logs
│── consume/               # Output directory for PDFs
│── eml2pdf/               # contains Dockerfile, main.py, requirements.txt
```

---

## 📬 Usage

1. Place **EML files** in `eml-import/`.  
2. **Start the container** with:  
   ```bash
   docker-compose up -d
   ```  
3. Converted **PDF files** appear in `consume/`.  
4. **Logs** can be found in `eml-import/error/` (e.g., `logfile.log`).  

---

## 📜 License

License information will be added later.  

---

## 📞 Contact

- **Author:** Michael Klissner  
- **E-Mail:** [umschalter-excel-3e@icloud.com](mailto:umschalter-excel-3e@icloud.com)  
- **Homepage:** [https://www.klissner.uk](https://www.klissner.uk)  
- **Support:** [https://www.ksc-llp.uk/donateyoutube](https://www.ksc-llp.uk/donateyoutube)  

---




# 📑 eml2pdf Converter – Deutsches Dokument

## Überblick
Der **eml2pdf Converter** ist ein für **Paperless-Workflows** optimiertes Tool, das **EML-Dateien (inklusive Anlagen)** in ein einziges PDF-Dokument umwandelt.  

Hauptmerkmale:
- Fokus auf **GoBD-Konformität** (Grundsätze zur ordnungsmäßigen Führung und Aufbewahrung).
- **Nahtlose Integration** in [Paperless](https://github.com/paperless-ngx/paperless-ngx).
- Auch **eigenständig nutzbar** zur Konvertierung von EML-Dateien.

---

## Funktionen
- **Eingabe**: Verarbeitung von EML-Dateien inkl. aller Anlagen aus einem Eingabeverzeichnis.  
- **Umwandlung**: Konvertierung per **LibreOffice** in ein PDF (Anlagen als separate Seiten).  
- **Ausgabe**: Speicherung im Ausgabeverzeichnis (`consume`).  
- **GoBD-Konformität**: Metadaten bleiben erhalten, Konvertierung ist nachvollziehbar.  

---

## Leistung
- **Skalierbarkeit**: Verarbeitung mehrerer EML-Dateien gleichzeitig (abhängig von Systemressourcen).  
- **Performance**: Konvertierung einer typischen EML-Datei (ca. 1 MB) dauert ~5–10 Sekunden.  
- **Ressourcen**: Entwickelt mit **Python 3.11** und minimalen Abhängigkeiten (LibreOffice, Python-Pakete).  

---

## Installation

### Voraussetzungen
- [Docker](https://docs.docker.com/get-docker/) und [Docker Compose](https://docs.docker.com/compose/install/)  
- Git zum Klonen des Repositories  
- Zugriff auf die **GitHub Container Registry** (PAT erforderlich)  

### Repository klonen
```bash
git clone https://github.com/Klissner/eml2pdf-Converter-Docker-.git
cd eml2pdf-Converter-Docker-
```

### Image ziehen
```bash
docker pull ghcr.io/klissner/eml2pdf:latest
```

- Konfiguration anpassen (siehe Abschnitt **Konfiguration**)  
- Container starten (siehe Abschnitt **Docker Compose**)  

---

## 🔧 Konfiguration (`config.json`)

Die Datei `config.json` liegt neben der `docker-compose.yml` und steuert das Verhalten des Converters.

```json
{
  "separator_text": "Anlage {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 30,
  "max_logfile_size": 1048576,
  "max_logfile_backups": 2
}
```

### Parameterbeschreibung
- **separator_text** → Text für Anlagentrenner (z. B. „Anlage 1: datei.pdf“).  
- **poll_interval_seconds** → Prüfintervall in Sekunden (300 = alle 5 Minuten).  
- **separator_page** → Fügt eine Trennseite vor Anhängen ein (`on` / `off`).  
- **archive_retention_days** → Aufbewahrungszeit für Archivdateien in Tagen (Standard: 30).  
- **max_logfile_size** → Max. Größe der Logdatei in Bytes (1 MB = `1048576`).  
- **max_logfile_backups** → Anzahl der Log-Backups (Standard: 2).  

👉 **Hinweis**: Passe `config.json` an deine Bedürfnisse an und füge sie in `.gitignore` ein, damit keine sensiblen Daten ins Repo gelangen.

---

## 🐳 Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  eml2pdf:
    image: ghcr.io/klissner/eml2pdf:latest
    build:
      context: ./eml2pdf
      dockerfile: Dockerfile
    volumes:
      - ./eml-import:/input
      - ./consume:/consume
      - ./eml-import/archiv:/eml-import/archiv
      - ./eml-import/error:/eml-import/error
      - ./config.json:/config.json
    environment:
      - TZ=Asia/Bangkok
      - LOGLEVEL=INFO
    restart: unless-stopped
```

### Erklärung der Parameter
- **image** → Offizielles Container-Image (GitHub Container Registry).  
- **build** → Baut das Image lokal aus dem Verzeichnis `./eml2pdf/`.  
- **volumes** → Verknüpft lokale Verzeichnisse mit Containerpfaden:  
  - `eml-import/` → Eingang für `.eml`-Dateien  
  - `consume/` → Ausgabeordner für fertige PDFs  
  - `eml-import/archiv/` → Archivierte `.eml`-Dateien  
  - `eml-import/error/` → Fehler-Logs  
  - `config.json` → zentrale Konfiguration  
- **environment** → Container-Umgebungsvariablen  
  - `TZ=Asia/Bangkok` → Zeitzone  
  - `LOGLEVEL=INFO` → Log-Level  
- **restart** → Container startet bei Fehlern oder Neustart automatisch neu.  

---

## ▶️ Start & Stop

```bash
# Container starten
docker-compose up -d

# Container stoppen
docker-compose down
```

---

## 📂 Verzeichnisstruktur

```
/mnt/d/Docker Server/paperless/
│── docker-compose.yml
│── config.json
│── eml-import/            # Eingang (EML-Dateien ablegen)
│   ├── archiv/            # Archivierte EMLs
│   ├── error/             # Fehler & Logs
│── consume/               # Ausgabeverzeichnis für PDFs
│── eml2pdf/               # enthält Dockerfile, main.py, requirements.txt
```

---

## 📬 Nutzung

1. **EML-Dateien** in `eml-import/` ablegen.  
2. **Container starten** mit:  
   ```bash
   docker-compose up -d
   ```  
3. Konvertierte **PDF-Dateien** erscheinen in `consume/`.  
4. **Logs** findest du in `eml-import/error/` (z. B. `logfile.log`).  

---

## 📜 Lizenz

Lizenzinformationen werden später ergänzt.  

---

## 📞 Kontakt

- **Autor:** Michael Klissner  
- **E-Mail:** [umschalter-excel-3e@icloud.com](mailto:umschalter-excel-3e@icloud.com)  
- **Homepage:** [https://www.klissner.uk](https://www.klissner.uk)  
- **Unterstützen:** [https://www.ksc-llp.uk/donateyoutube](https://www.ksc-llp.uk/donateyoutube)  

---
