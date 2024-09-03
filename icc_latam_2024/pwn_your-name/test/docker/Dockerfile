FROM ubuntu:22.04

RUN apt-get update

RUN apt install gcc gcc-multilib -y


RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

COPY libc.so.6 /lib32/libc.so.6


WORKDIR /home/ctf

COPY your-name .
COPY flag.txt .
COPY ynetd .


RUN chmod +x ynetd

RUN chmod 644 flag.txt
RUN chmod 755 your-name

USER ctf
EXPOSE 1025
CMD ./ynetd -p 1025 ./your-name
