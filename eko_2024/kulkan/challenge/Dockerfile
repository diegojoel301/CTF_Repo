FROM python:3.9-slim

WORKDIR /chall

COPY app/ /chall
COPY requirements.txt .
COPY flag.txt .
COPY read-flag.c .

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get install curl iputils-ping nmap dnsutils gcc -y \
    && gcc /chall/read-flag.c -o /chall/read-flag \
    && chmod 4755 /chall/read-flag \
    && chmod 400 /chall/flag.txt \
    && chown root:root /chall/flag.txt

EXPOSE 5000

ENV FLASK_APP app.py

CMD ["python3", "/chall/app.py"]

