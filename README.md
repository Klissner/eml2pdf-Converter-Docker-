English Docoment
================ 

eml2pdf Converter Overview The eml2pdf converter is a tool specifically optimized for paperless workflows that converts EML files (including all attachments) into a single PDF document. Developed with a focus on GoBD (German Principles for Proper Management and Storage) compliance, it integrates seamlessly with Paperless and efficiently supports paperless document management. Furthermore, eml2pdf can also be used independently of Paperless for conversion. Function Input: Processes EML files including all attachments from an input directory.
Conversion: Converts EML files with LibreOffice into a PDF containing all attachments as separate pages.
Output: Saves the combined PDF in the consumption directory.
GoBD Compliance: Secures metadata and ensures verifiable conversion.

Performance Scalability: Processes multiple EML files simultaneously (depending on system resources).
Performance: Converting a typical EML file (approx. 1 MB) takes about 5-10 seconds (depending on the number and size of attachments).
Resources: Uses Python 3.11 with minimal dependencies (LibreOffice, Python packages).

Installation Requirements: Docker and Docker Compose installed.
Git for cloning the repository.
Access to the GitHub Container Registry (PAT required).

Steps: Clone the repository: bash

git clone https://github.com/Klissner/eml2pdf-Converter-Docker-.git
cd eml2pdf-Converter-Docker-

Pull the image: bash

docker pull ghcr.io/klissner/eml2pdf:latest

Adjust the configuration (see the "Configuration" section).
Start the container (see the "Docker Compose" section).

Configuration config.json The configuration file (config.json) is located next to the docker-compose.yml and controls the behavior of the converter. The last known version is: json

{
"separator_text": "Attachment {num}: {name}",
"poll_interval_seconds": 300,
"separator_page": "on",
"archive_retention_days": 30,
"max_logfile_size": 1048576,
"max_logfile_backups": 2
}

Parameters: separator_text: Text for attachment separators (e.g., "Attachment 1: file.pdf").
poll_interval_seconds: Interval in seconds to check the input directory (300 = 5 minutes).
separator_page: Inserts a separator page before attachments ("on"/"off").
archive_retention_days: Retention time for archive files in days (30).
max_logfile_size: Maximum log file size in bytes (1 MB = 1048576).
max_logfile_backups: Number of log backups (2).

Note: Adjust config.json to your needs and ignore it in .gitignore. Environment variables. Configurations can also be set via docker-compose.yml (see below). Docker Composed. The docker-compose.yml file orchestrates the container. The last known version, adapted: yaml

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

Parameter: image: Points to the pushed image.
build: Builds the image from the eml2pdf/ directory.
volumes: Connects local directories to the container (input, consumption, archive, errors, configuration).
environment: Sets the time zone (Asia/Bangkok) and log level (INFO).
restart: Automatically restarts the container.

Start: bash

docker-compose up -d

Stop: bash

docker-compose down

Directory structure /mnt/d/Docker Server/paperless/docker-compose.yml
config.json
eml-import/ (input directory for EML files)
consume/ (output directory for PDFs)
eml-import/archive/ (archive directory)
eml-import/error/ (error directory, contains log files)
eml2pdf/ (contains Dockerfile, main.py, requirements.txt)

Usage: Place EML files in eml-import/.
Start the container with docker-compose up -d.
Check the converted PDFs in consume/.
Logs can be found in the log file under eml-import/error/ (e.g., logfile.log).

License [License will be added later, once the README is complete.] Contact Author: Michael Klissner
Email: umschalter-excel-3e@icloud.com
Homepage: https://www.klissner.uk
Donate to support my work: https://www.ksc-llp.uk/donateyoutube




Deutsches Dokument
==================

eml2pdf ConverterÜberblickDer eml2pdf-Converter ist ein speziell für Paperless-Workflows optimiertes Tool, das EML-Dateien (einschließlich aller Anlagen) in ein einziges PDF-Dokument umwandelt. Entwickelt mit Fokus auf GoBD-Konformität (Grundsätze zur ordnungsmäßigen Führung und Aufbewahrung), ist es nahtlos in Paperless integrierbar und unterstützt papierlose Dokumentenverwaltung effizient. Darüber hinaus kann eml2pdf auch einzeln zur Konvertierung verwendet werden, unabhängig von Paperless.FunktionEingabe: Verarbeitung von EML-Dateien inklusive aller Anlagen aus einem Eingabeverzeichnis.
Umwandlung: Konvertiert EML-Dateien mit LibreOffice in ein PDF, das alle Anlagen als separate Seiten enthält.
Ausgabe: Speichert das kombinierte PDF im Konsumverzeichnis.
GoBD-Konformität: Sichert Metadaten und stellt eine nachprüfbare Konvertierung sicher.

LeistungSkalierbarkeit: Verarbeitet mehrere EML-Dateien gleichzeitig (abhängig von Systemressourcen).
Performance: Konvertierung einer typischen EML-Datei (ca. 1 MB) dauert etwa 5-10 Sekunden (je nach Anzahl und Größe der Anlagen).
Ressourcen: Nutzt Python 3.11 mit minimalen Abhängigkeiten (LibreOffice, Python-Pakete).

InstallationVoraussetzungenDocker und Docker Compose installiert.
Git für das Klonen des Repositories.
Zugriff auf GitHub Container Registry (PAT erforderlich).

SchritteRepository klonen:bash

git clone https://github.com/Klissner/eml2pdf-Converter-Docker-.git
cd eml2pdf-Converter-Docker-

Image ziehen:bash

docker pull ghcr.io/klissner/eml2pdf:latest

Konfiguration anpassen (siehe Abschnitt „Konfiguration“).
Container starten (siehe Abschnitt „Docker Compose“).

Konfigurationconfig.jsonDie Konfigurationsdatei (config.json) liegt neben der docker-compose.yml und steuert das Verhalten des Converters. Die letzte bekannte Version:json

{
  "separator_text": "Anlage {num}: {name}",
  "poll_interval_seconds": 300,
  "separator_page": "on",
  "archive_retention_days": 30,
  "max_logfile_size": 1048576,
  "max_logfile_backups": 2
}

Parameter:separator_text: Text für Anlagentrenner (z. B. „Anlage 1: datei.pdf“).
poll_interval_seconds: Intervall in Sekunden, um Eingabeverzeichnis zu prüfen (300 = 5 Minuten).
separator_page: Fügt eine Trennseite vor Anlagen ein („on“/„off“).
archive_retention_days: Aufbewahrungszeit für Archivdateien in Tagen (30).
max_logfile_size: Maximale Größe der Logdatei in Bytes (1 MB = 1048576).
max_logfile_backups: Anzahl der Log-Backups (2).

Hinweis: Passe config.json an deine Bedürfnisse an und ignoriere es in .gitignore.UmgebungsvariablenKonfigurationen können auch über docker-compose.yml gesetzt werden (siehe unten).Docker Composedocker-compose.ymlDie Datei docker-compose.yml orchestriert den Container. Die letzte bekannte Version, angepasst:yaml

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

Parameter:image: Verweist auf das gepushte Image.
build: Baut das Image aus dem eml2pdf/-Verzeichnis.
volumes: Verbindet lokale Verzeichnisse mit dem Container (Eingabe, Konsum, Archiv, Fehler, Konfiguration).
environment: Setzt Zeitzone (Asia/Bangkok) und Log-Stufe (INFO).
restart: Startet den Container automatisch neu.

Starten:bash

docker-compose up -d

Stoppen:bash

docker-compose down

Verzeichnisstruktur/mnt/d/Docker Server/paperless/docker-compose.yml
config.json
eml-import/ (Eingabeverzeichnis für EML-Dateien)
consume/ (Ausgabeverzeichnis für PDFs)
eml-import/archiv/ (Archivverzeichnis)
eml-import/error/ (Fehlerverzeichnis, enthält Logdateien)
eml2pdf/ (enthält Dockerfile, main.py, requirements.txt)

NutzungPlatziere EML-Dateien in eml-import/.
Starte den Container mit docker-compose up -d.
Überprüfe die konvertierten PDFs in consume/.
Logs finden in der Logdatei unter eml-import/error/ (z. B. logfile.log).

Lizenz[Lizenz wird später hinzugefügt, sobald die README fertig ist.]KontaktAutor: Michael Klissner
E-Mail: umschalter-excel-3e@icloud.com
Homepage: https://www.klissner.uk
Spende, meine Arbeit unterstützen: https://www.ksc-llp.uk/donateyoutube

