FROM ubuntu:22.04

RUN apt-get update && apt-get install socat sudo -yqq \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /task

COPY ./flag.txt /tmp
COPY ./server.sh /
COPY pontius libc.so.6 ld.so ./

EXPOSE 1337
ENTRYPOINT /server.sh
