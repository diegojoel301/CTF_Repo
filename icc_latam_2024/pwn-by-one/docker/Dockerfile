FROM ubuntu:22.04

RUN apt-get update

RUN apt install gcc -y



RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY pwn-by-one .
COPY flag.txt .
COPY ynetd .

RUN chmod +x ynetd

RUN chmod 644 flag.txt
RUN chmod 755 pwn-by-one

USER ctf
EXPOSE 1024
CMD ./ynetd -p 1024 ./pwn-by-one
