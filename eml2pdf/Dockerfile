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

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libreoffice \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]