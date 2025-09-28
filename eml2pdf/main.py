# ************************************************************************************
# (c) 2025 by Michael Klissner
#
# Homepage: www.klissner.uk                              Homepage: www.ksc-llp.uk
# Contact: https://www.klissner.uk/en/contact-me/        Kontakt: https://www.klissner.uk/de/kontakt-aufnehmen/
# 
# Donations and support:                                 Spenden und Unterstützung: 
# PayPal: https://www.paypal.com/donate?hosted_button_id=G8CZWPDCM3SNW
#
# Bank, Bitcoin and Lightning:                           Bank, Bitcoin und Lightning:  
# https://www.ksc-llp.uk/donateyoutube                   https://www.ksc-llp.uk/donateyoutube
# ************************************************************************************

import os
import sys
import json
import time
import tempfile
import logging
import gzip
from datetime import datetime
from pathlib import Path
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime, parseaddr
import pytz
import subprocess
import shutil
import html
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from weasyprint import HTML
from PIL import Image
from PyPDF2 import PdfMerger

def setup_logging(error_dir, max_logfile_size, max_logfile_backups):
    """Initialisiere Logging mit Rotation oder deaktiviere es."""
    os.makedirs(error_dir, exist_ok=True)
    log_file = os.path.join(error_dir, 'log.txt')
    
    if max_logfile_size == 0:
        logger = logging.getLogger()
        logger.handlers = []
        logger.setLevel(logging.CRITICAL + 1)
        for log_path in Path(error_dir).glob('log.*'):
            try:
                log_path.unlink()
                print(f"Logdatei gelöscht: {log_path}")
            except Exception as e:
                print(f"Fehler beim Löschen von {log_path}: {e}")
        print("Logging deaktiviert (max_logfile_size=0)")
        return

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    class SizeRotatingFileHandler(logging.FileHandler):
        def __init__(self, filename, maxBytes, backupCount):
            super().__init__(filename)
            self.maxBytes = maxBytes
            self.backupCount = backupCount

        def emit(self, record):
            if os.path.exists(self.baseFilename) and os.path.getsize(self.baseFilename) > self.maxBytes:
                self.rotate()
            super().emit(record)

        def rotate(self):
            if self.backupCount > 0:
                for i in range(self.backupCount - 1, 0, -1):
                    src = f"{self.baseFilename}.{i}"
                    dst = f"{self.baseFilename}.{i + 1}"
                    if os.path.exists(src):
                        if os.path.exists(dst):
                            os.remove(dst)
                        os.rename(src, dst)
                        if os.path.exists(dst):
                            with open(dst, 'rb') as f_in:
                                with gzip.open(f"{dst}.gz", 'wb') as f_out:
                                    f_out.writelines(f_in)
                            os.remove(dst)
                            logging.debug(f"Logdatei komprimiert: {dst}.gz")
                dst = f"{self.baseFilename}.1"
                if os.path.exists(dst):
                    os.remove(dst)
                os.rename(self.baseFilename, dst)
                if os.path.exists(dst):
                    with open(dst, 'rb') as f_in:
                        with gzip.open(f"{dst}.gz", 'wb') as f_out:
                            f_out.writelines(f_in)
                    os.remove(dst)
                    logging.debug(f"Logdatei komprimiert: {dst}.gz")
            else:
                open(self.baseFilename, 'w').close()

    file_handler = SizeRotatingFileHandler(log_file, maxBytes=max_logfile_size, backupCount=max_logfile_backups)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    console = logging.StreamHandler()
    console.setLevel(os.getenv('LOGLEVEL', 'INFO'))
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console)

    logging.getLogger('weasyprint').setLevel(logging.CRITICAL)
    
    logging.info(f"Logging initialisiert mit max_logfile_size={max_logfile_size}, max_logfile_backups={max_logfile_backups}")

def load_config(config_path):
    """Lade config.json."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden der config.json: {e}")
        return {
            "separator_text": "Anlage {num}: {name}",
            "poll_interval_seconds": 300,
            "separator_page": "on",
            "archive_retention_days": 30,
            "max_logfile_size": 1048576,
            "max_logfile_backups": 2
        }

def delete_old_files_and_dirs(archive_dir, retention_days):
    """Lösche Dateien und leere Verzeichnisse im Archiv."""
    if retention_days == 0:
        logging.info("Archiv-Löschung deaktiviert")
        return
    
    try:
        now = time.time()
        cutoff_time = now - (retention_days * 24 * 60 * 60)
        archive_path = Path(archive_dir)
        
        for item in archive_path.rglob('*'):
            try:
                if item.is_file():
                    mtime = item.stat().st_mtime
                    if mtime < cutoff_time:
                        item.unlink()
                        logging.debug(f"Datei gelöscht: {item}")
            except Exception as e:
                logging.error(f"Fehler beim Löschen von {item}: {e}")
        
        for item in sorted(archive_path.rglob('*'), reverse=True):
            try:
                if item.is_dir() and not any(item.iterdir()):
                    item.rmdir()
                    logging.debug(f"Leeres Verzeichnis gelöscht: {item}")
            except Exception as e:
                logging.error(f"Fehler beim Löschen von Verzeichnis {item}: {e}")
    except Exception as e:
        logging.error(f"Fehler beim Verarbeiten des Archivordners {archive_dir}: {e}")

def convert_office_to_pdf(input_path, output_dir):
    """Konvertiere Office-Dateien zu PDF."""
    supported = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp', '.pages', '.numbers']
    ext = Path(input_path).suffix.lower()
    if ext not in supported:
        logging.warning(f"Datei {input_path} hat nicht unterstütztes Format: {ext}")
        return None
    try:
        logging.debug(f"Konvertiere Office-Datei: {input_path} (Größe: {os.path.getsize(input_path)} Bytes)")
        output_pdf = os.path.join(output_dir, Path(input_path).stem + '.pdf')
        result = subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', output_dir, input_path
        ], check=True, capture_output=True, text=True, timeout=180)
        logging.debug(f"LibreOffice Ausgabe: {result.stdout}")
        if not os.path.exists(output_pdf):
            logging.error(f"Konvertierung hat kein PDF erstellt für {input_path}")
            return None
        logging.info(f"Office-Datei zu PDF konvertiert: {output_pdf}")
        return output_pdf
    except subprocess.TimeoutExpired as e:
        logging.error(f"Timeout bei der Konvertierung von {input_path}: {e}")
        return None
    except subprocess.CalledProcessError as e:
        logging.error(f"LibreOffice Fehler bei {input_path}: {e.stderr}")
        return None
    except Exception as e:
        logging.error(f"Fehler bei der Konvertierung von {input_path}: {e}")
        return None

def create_separator_pdf(attachment_num, attachment_name, output_path, separator_text, from_, to_, date_, original_date):
    """Erstelle eine Trennseite als PDF."""
    try:
        try:
            dt = parsedate_to_datetime(date_)
            local_tz = pytz.timezone(os.getenv('TZ', 'UTC'))
            local_dt = dt.astimezone(local_tz)
            formatted_date = local_dt.strftime('%a, %d %b %Y %H:%M:%S %z')
        except Exception as e:
            logging.warning(f"Fehler bei der Zeitkonvertierung: {e}")
            formatted_date = date_

        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        text = separator_text.format(num=attachment_num, name=attachment_name)
        y = height - 100
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, text)
        y -= 30
        c.setFont("Helvetica", 12)
        c.drawString(100, y, f"Von: {from_}")
        y -= 20
        c.drawString(100, y, f"An: {to_}")
        y -= 20
        c.drawString(100, y, f"Datum/Uhrzeit (Ortszeit): {formatted_date}")
        y -= 20
        c.drawString(100, y, f"Datum/Uhrzeit (Original): {original_date}")
        c.save()
        logging.debug(f"Trennseite erstellt: {output_path}")
    except Exception as e:
        logging.error(f"Fehler beim Erstellen der Trennseite {output_path}: {e}")
        raise

def extract_and_convert_attachments(msg, output_dir):
    """Extrahiere und konvertiere Anhänge zu PDFs."""
    attachments = []
    attachment_filenames = []
    counter = 1
    for part in msg.walk():
        disposition = part.get_content_disposition()
        if disposition in ['attachment', 'inline']:
            filename = part.get_filename()
            if not filename:
                content_type = part.get_content_type()
                if content_type.startswith('image/'):
                    filename = f"image_{counter}.jpg"
                    counter += 1
                else:
                    logging.debug(f"Anhang ohne Dateinamen und nicht Bild: {content_type}")
                    continue
            attachment_filenames.append(filename)
    expected_count = len(attachment_filenames)
    logging.debug(f"Erwartete Anhänge: {expected_count}")
    
    counter = 1
    for part in msg.walk():
        disposition = part.get_content_disposition()
        if disposition in ['attachment', 'inline']:
            filename = part.get_filename()
            if not filename:
                content_type = part.get_content_type()
                if content_type.startswith('image/'):
                    filename = f"image_{counter}.jpg"
                    counter += 1
                else:
                    continue
            filepath = os.path.join(output_dir, filename)
            ext = Path(filename).suffix.lower()
            try:
                with open(filepath, 'wb') as f:
                    payload = part.get_payload(decode=True)
                    if payload is None:
                        logging.warning(f"Kein Payload für Anhang {filename}")
                        continue
                    f.write(payload)
                logging.debug(f"Anhang extrahiert: {filepath}")
                if ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp'):
                    img_pdf = os.path.join(output_dir, Path(filename).stem + '.pdf')
                    try:
                        img = Image.open(filepath)
                        img.verify()
                        img = Image.open(filepath)
                        img.save(img_pdf, 'PDF', resolution=100.0)
                        logging.debug(f"Bild zu PDF konvertiert: {img_pdf}")
                        attachments.append((len(attachments) + 1, img_pdf, filename))
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                    except Exception as e:
                        logging.error(f"Fehler bei Bildkonvertierung {filepath}: {e}")
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                        raise
                elif ext == '.pdf':
                    attachments.append((len(attachments) + 1, filepath, filename))
                else:
                    att_pdf = convert_office_to_pdf(filepath, output_dir)
                    if att_pdf:
                        attachments.append((len(attachments) + 1, att_pdf, filename))
                    else:
                        logging.error(f"Fehler bei der Konvertierung von {filename}")
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                        raise
                    if os.path.exists(filepath):
                        os.unlink(filepath)
            except Exception as e:
                logging.error(f"Fehler bei der Verarbeitung von Anhang {filename}: {e}")
                if os.path.exists(filepath):
                    os.unlink(filepath)
                raise
    logging.info(f"Verarbeitete Anhänge: {len(attachments)}")
    return attachments, len(attachments) == expected_count

def eml_to_pdf(eml_path, output_dir, archive_dir, error_dir, config):
    """Konvertiere eine EML-Datei zu PDF und verschiebe sie."""
    logging.info(f"Verarbeite EML: {eml_path}")
    try:
        with open(eml_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        from_header = msg.get('From', 'Unbekannt')
        to_header = msg.get('To', 'Unbekannt')
        from_name, from_addr = parseaddr(from_header)
        to_name, to_addr = parseaddr(to_header)
        if not from_addr and from_header == 'Unbekannt':
            logging.warning(f"Kein 'From'-Header in {eml_path}: {msg.get('From', 'Kein Header')}")
        if not to_addr and to_header == 'Unbekannt':
            logging.warning(f"Kein 'To'-Header in {eml_path}: {msg.get('To', 'Kein Header')}")
        from_ = f"{from_name} <{from_addr}>" if from_name and from_addr else from_addr or from_header or 'Unbekannt'
        to_ = f"{to_name} <{to_addr}>" if to_name and to_addr else to_addr or to_header or 'Unbekannt'
        from_escaped = html.escape(from_)
        to_escaped = html.escape(to_)
        original_date = msg.get('Date', 'Unbekannt')
        
        try:
            dt = parsedate_to_datetime(original_date)
            local_tz = pytz.timezone(os.getenv('TZ', 'UTC'))
            local_dt = dt.astimezone(local_tz)
            formatted_date = local_dt.strftime('%a, %d %b %Y %H:%M:%S %z')
        except Exception as e:
            logging.warning(f"Fehler bei der Zeitkonvertierung: {e}")
            formatted_date = original_date

        subject = msg.get('Subject', 'Kein Betreff')
        logging.info(f"Header: Betreff={subject}, Von={from_escaped}, An={to_escaped}, Datum (Ortszeit)={formatted_date}")

        body_html = None
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                payload = part.get_payload(decode=True)
                if payload:
                    body_html = payload.decode('utf-8', errors='ignore')
                    break
        if not body_html:
            body_part = msg.get_body(preferencelist=('plain', 'html'))
            if body_part:
                payload = body_part.get_payload(decode=True)
                if payload:
                    body_html = f"<p>{html.escape(payload.decode('utf-8', errors='ignore'))}</p>"
                else:
                    body_html = "<p>Kein Text-Body gefunden</p>"
            else:
                body_html = "<p>Kein Text-Body gefunden</p>"
        logging.debug("Body extrahiert")

        header_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12pt; }}
                h1 {{ font-size: 16pt; font-weight: bold; }}
                p {{ margin: 5px 0; }}
                strong {{ font-weight: bold; }}
                hr {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>Betreff: {html.escape(subject)}</h1>
            <p><strong>Von:</strong> {from_escaped}</p>
            <p><strong>An:</strong> {to_escaped}</p>
            <p><strong>Datum/Uhrzeit (Ortszeit):</strong> {html.escape(formatted_date)}</p>
            <p><strong>Datum/Uhrzeit (Original):</strong> {html.escape(original_date)}</p>
            <hr>
            {body_html}
        </body>
        </html>
        """
        logging.debug(f"Header HTML (Von/An): <p><strong>Von:</strong> {from_escaped}</p><p><strong>An:</strong> {to_escaped}</p>")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp:
            tmp.write(header_html)
            tmp_html = tmp.name
        logging.debug(f"Temporäres HTML erstellt: {tmp_html}")

        output_pdf = os.path.join(output_dir, Path(eml_path).stem + '.pdf')
        email_pdf = output_pdf.replace('.pdf', '_email.pdf')
        HTML(filename=tmp_html).write_pdf(email_pdf)
        os.unlink(tmp_html)
        logging.info(f"Email zu PDF gerendert: {email_pdf}")

        with tempfile.TemporaryDirectory() as temp_dir:
            attachments, all_processed = extract_and_convert_attachments(msg, temp_dir)
            merger = PdfMerger()
            merger.append(email_pdf)

            if config.get('separator_page', 'on').lower() == 'on':
                for num, att_pdf, att_name in attachments:
                    sep_pdf = os.path.join(temp_dir, f'sep{num}.pdf')
                    create_separator_pdf(num, att_name, sep_pdf, 
                                        config.get('separator_text', 'Anlage {num}: {name}'),
                                        from_, to_, original_date, original_date)
                    merger.append(sep_pdf)
                    merger.append(att_pdf)
                    if os.path.exists(att_pdf):
                        os.unlink(att_pdf)
            else:
                for _, att_pdf, _ in attachments:
                    merger.append(att_pdf)
                    if os.path.exists(att_pdf):
                        os.unlink(att_pdf)
            logging.info(f"Anhänge verarbeitet: {len(attachments)}")

            merger.write(output_pdf)
            merger.close()
            logging.info(f"Finales PDF erstellt: {output_pdf}")

        if os.path.exists(email_pdf):
            os.unlink(email_pdf)

        if not all_processed:
            logging.error(f"Nicht alle Anhänge von {eml_path} erfolgreich verarbeitet")
            os.makedirs(error_dir, exist_ok=True)
            shutil.move(eml_path, os.path.join(error_dir, Path(eml_path).name))
            logging.info(f"EML in Fehlerordner verschoben: {eml_path}")
            return False

        now = datetime.now()
        archive_path = os.path.join(archive_dir, f"{now.year}/{now.strftime('%m')}")
        os.makedirs(archive_path, exist_ok=True)
        shutil.move(eml_path, os.path.join(archive_path, Path(eml_path).name))
        logging.debug(f"EML archiviert: {archive_path}")
        return True

    except Exception as e:
        logging.error(f"Fehler bei {eml_path}: {e}")
        os.makedirs(error_dir, exist_ok=True)
        shutil.move(eml_path, os.path.join(error_dir, Path(eml_path).name))
        logging.info(f"EML in Fehlerordner verschoben: {eml_path}")
        return False

def main():
    """Hauptfunktion: Verarbeite EMLs im Input-Ordner in Intervallen."""
    input_dir = '/input'
    output_dir = '/consume'
    archive_dir = '/eml-import/archiv'
    error_dir = '/eml-import/error'
    config_path = '/config.json'

    config = load_config(config_path)
    poll_interval = config.get('poll_interval_seconds', 300)
    retention_days = config.get('archive_retention_days', 30)
    max_logfile_size = config.get('max_logfile_size', 1048576)
    max_logfile_backups = config.get('max_logfile_backups', 2)

    setup_logging(error_dir, max_logfile_size, max_logfile_backups)
    
    if max_logfile_size == 0:
        print(f"Starte Überwachung von {input_dir} alle {poll_interval} Sekunden...")
    else:
        logging.info(f"Starte Überwachung von {input_dir} alle {poll_interval} Sekunden...")
    
    processed_files = set()
    
    while True:
        try:
            start_time = time.time()
            logging.debug("Beginne neuen Verarbeitungszyklus")

            delete_old_files_and_dirs(archive_dir, retention_days)

            os.makedirs(output_dir, exist_ok=True)
            eml_files = list(Path(input_dir).glob('*.eml'))
            if not eml_files:
                logging.debug(f"Keine EML-Dateien in {input_dir} gefunden")
            
            batch_size = 10
            for i in range(0, len(eml_files), batch_size):
                batch = eml_files[i:i + batch_size]
                for eml_file in batch:
                    if eml_file.name not in processed_files:
                        logging.info(f"Neue EML gefunden: {eml_file}")
                        success = eml_to_pdf(eml_file, output_dir, archive_dir, error_dir, config)
                        if success:
                            processed_files.add(eml_file.name)
            
            elapsed_time = time.time() - start_time
            sleep_time = max(0, poll_interval - elapsed_time)
            logging.info(f"Warte {sleep_time:.2f} Sekunden bis zur nächsten Prüfung...")
            time.sleep(sleep_time)
        except Exception as e:
            logging.error(f"Fehler im Hauptprozess: {e}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    main()