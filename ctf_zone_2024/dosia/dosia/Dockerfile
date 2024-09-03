FROM ubuntu:22.04

RUN apt update && apt install socat python3 dosbox sudo -yqq \
  && rm -rf /var/lib/apt/lists/*

COPY ./app /app
RUN chmod 644 /app/FLAG; chmod 644 /app/a.exe

WORKDIR /app

EXPOSE 1337
ENTRYPOINT ./server.sh
