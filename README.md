# 🇩🇪 Deutsch

## Release v2.01 – Bugfix

Datum und Zeit werden jetzt aus dem Email Header verwendet (GoBD konform) Bugfix

---

## Offizielle Images (GitHub Container Registry)

| Architektur            | Version 2.01 (stabil)               | Aktuell (rolling)                      | Empfohlen für                                       |
|------------------------|-------------------------------------|----------------------------------------|-----------------------------------------------------|
| **x86_64** (Intel/AMD) | `ghcr.io/klissner/eml2pdf:2.01-x86` | `ghcr.io/klissner/eml2pdf:latest-x86`  | Server, Desktop, NAS (Synology, QNAP, TrueNAS)      |
| **ARM64** (aarch64)    | `ghcr.io/klissner/eml2pdf:2.01-arm` | `ghcr.io/klissner/eml2pdf:latest-arm`  | Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton |

**Wichtig**: Immer den vollen Tag mit Architektur verwenden!

# EML2PDF Converter

### Übersicht

**EML2PDF Converter** ist ein vollautomatischer E-Mail‑zu‑PDF‑Konverter für Docker‑Umgebungen, optimiert für **Paperless‑ngx** und andere DMS‑Systeme.
Er verarbeitet `.eml`‑Dateien inklusive Anhängen und erzeugt **ein einziges, durchsuchbares PDF** pro E-Mail.

Der Fokus liegt auf:

* Stabilität
* Vollständiger Archivierung
* Sauberer Darstellung
* 100 % Offline‑Verarbeitung

---

### Funktionen

* Konvertiert `.eml` → **PDF**
* E-Mail‑Header auf Seite 1 (Von, An, CC, BCC, Betreff, Datum)
* HTML‑ und Text‑Bodies
* Automatische Zeitzonen‑Normalisierung
* Jede Anlage wird:

  * erkannt
  * ggf. konvertiert
  * im PDF eingebettet
* Vollständige Archivierung
* Fehlerhafte Dateien landen sicher im Error‑Verzeichnis

---

### Unterstützte Anhänge

#### Direkt konvertiert (LibreOffice headless)

* **DOC / DOCX / RTF / TXT**
* **XLS / XLSX / CSV**
* **PPT / PPTX**
* **ODT / ODS / ODP**
* **Pages / Numbers / Keynote**

#### Bilder (als PDF-Seiten)

* PNG
* JPG / JPEG
* GIF
* BMP
* TIFF
* WEBP

#### Bereits PDF

* PDF (wird unverändert übernommen)

#### Fallback (immer möglich)

* VCF
* Unbekannte Dateitypen
* Binärdateien → Hinweis‑PDF

#### Ignoriert

* EML‑Anhänge (Rekursionsschutz)

---

### Verzeichnisstruktur

```
/input        → Eingehende .eml Dateien
/consume      → Ausgabeverzeichnis oder auch z.B. Paperless consume Verzeichnis
/app/archiv   → Archivierte E-Mails (Jahr / Monat)
/app/error    → Fehlerhafte E-Mails + Logfile
```

---

## Offizielle Images (GitHub Container Registry)

| Architektur            | Version 2.00 (stabil)               | Aktuell (rolling)                      | Empfohlen für                                       |
|------------------------|-------------------------------------|----------------------------------------|-----------------------------------------------------|
| **x86_64** (Intel/AMD) | `ghcr.io/klissner/eml2pdf:2.00-x86` | `ghcr.io/klissner/eml2pdf:latest-x86`  | Server, Desktop, NAS (Synology, QNAP, TrueNAS)      |
| **ARM64** (aarch64)    | `ghcr.io/klissner/eml2pdf:2.00-arm` | `ghcr.io/klissner/eml2pdf:latest-arm`  | Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton |

**Wichtig**: Immer den vollen Tag mit Architektur verwenden!

---

### Konfiguration

Optional über `/config.json`:

```json
{
  "separator_text": "Anlage {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 730,
  "max_logfile_size": 1048576,
  "max_logfile_backups": 3,
}
```

---

### Architektur

* Python 3
* WeasyPrint (HTML → PDF)
* LibreOffice (Office‑Formate)
* Pillow (Bilder)
* pdftoppm (PDF‑Vorschau)
* Docker‑ready

Unterstützt:

* **x86_64**
* **ARM64 (aarch64)**

---

### Lizenz & Support

© 2025 - 2026 KSC LLP / Michael Klissner
[https://www.klissner.uk](https://www.klissner.uk)
 Admin-Handbuch https://www.klissner.uk/de/eml2pdf-offizielle-web-seite/ 

## Spenden & Unterstützung

Vielen Dank für eure Unterstützung!

* **PayPal** → [https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW](https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW)
* **Bitcoin / Lightning / Bank** → [https://www.ksc-llp.uk/donateyoutube](https://www.ksc-llp.uk/donateyoutube)

**Kontakt:** Michael Klissner
Web: [https://www.klissner.uk](https://www.klissner.uk)
Mail: [umschalter-excel-3e@icloud.com](mailto:umschalter-excel-3e@icloud.com)

---

---

# 🇬🇧 English

## Release v2.01 - Bugfix

Date and time are now taken from the email header (GoBD compliant) Bug fix

---

## Official images (GitHub Container Registry)

| Architecture           | Version 2.01 (stabil)               | Current (rolling)                      | Recommended for.                                    |
|------------------------|-------------------------------------|----------------------------------------|-----------------------------------------------------|
| **x86_64** (Intel/AMD) | `ghcr.io/klissner/eml2pdf:2.01-x86` | `ghcr.io/klissner/eml2pdf:latest-x86`  | Server, Desktop, NAS (Synology, QNAP, TrueNAS)      |
| **ARM64** (aarch64)    | `ghcr.io/klissner/eml2pdf:2.01-arm` | `ghcr.io/klissner/eml2pdf:latest-arm`  | Raspberry Pi 4/5, Apple Silicon M1/M2, AWS Graviton |

**Important**: Always use the full day for architecture!

### Overview

**EML2PDF Converter** is a fully automated email‑to‑PDF converter for Docker environments, optimized for **Paperless‑ngx** and other DMS systems.

Each `.eml` file (including attachments) is converted into **one searchable PDF**.

Designed for:

* Stability
* Long‑term archiving
* Clean layout
* 100 % offline processing

---

### Features

* Converts `.eml` → **PDF**
* Email headers on page 1 (From, To, CC, BCC, Subject, Date)
* HTML and plain‑text bodies
* Automatic timezone normalization
* Attachments are:

  * detected
  * converted if needed
  * embedded into the PDF
* Automatic archiving
* Failed files are safely moved to the error folder

---

### Supported Attachments

#### Native conversion (LibreOffice headless)

* **DOC / DOCX / RTF / TXT**
* **XLS / XLSX / CSV**
* **PPT / PPTX**
* **ODT / ODS / ODP**
* **Pages / Numbers / Keynote**

#### Images (as PDF pages)

* PNG
* JPG / JPEG
* GIF
* BMP
* TIFF
* WEBP

#### Already PDF

* PDF (kept unchanged)

#### Fallback (always possible)

* VCF
* Unknown file types
* Binary files → info PDF

#### Ignored

* EML attachments (recursion protection)

---

### Directory Structure

```
/input        → Incoming .eml files
/consume      → Output folder, e.g., Paperless consume directory
/app/archiv   → Archived emails (year / month)
/app/error    → Failed emails + logfile
```

---

### Configuration

Optional via `/config.json`:

```json
{
  "separator_text": "Anlage {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 730,
  "max_logfile_size": 1048576,

  "max_logfile_backups": 3,
}
```

---

### Architecture

* Python 3
* WeasyPrint (HTML → PDF)
* LibreOffice (Office formats)
* Pillow (images)
* pdftoppm (PDF preview)
* Docker‑ready

Supported platforms:

* **x86_64**
* **ARM64 (aarch64)**

---

### License & Support

© 2025 - 2026 KSC LLP / Michael Klissner
[https://www.klissner.uk](https://www.klissner.uk)
Administrator's Guide https://www.klissner.uk/de/eml2pdf-offizielle-web-seite/ 


## Donations & Support

Thank you very much for your support!

* **PayPal** → [https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW](https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW)
* **Bitcoin / Lightning / Bank** → [https://www.ksc-llp.uk/donateyoutube](https://www.ksc-llp.uk/donateyoutube)

**Contact:** Michael Klissner
Web: [https://www.klissner.uk](https://www.klissner.uk)
Mail: [umschalter-excel-3e@icloud.com](mailto:umschalter-excel-3e@icloud.com)





