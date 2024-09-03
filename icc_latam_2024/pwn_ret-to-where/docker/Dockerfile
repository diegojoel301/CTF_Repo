FROM ubuntu:22.04

RUN apt-get update

RUN apt install gcc -y


RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY ret-to-where .
COPY flag.txt .
COPY ynetd .

RUN chmod +x ynetd

RUN chmod 644 flag.txt
RUN chmod 755 ret-to-where

USER ctf
EXPOSE 1027
CMD ./ynetd -p 1027 ./ret-to-where
