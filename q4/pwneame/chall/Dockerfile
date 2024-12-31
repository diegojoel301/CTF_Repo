FROM ubuntu:22.04 AS base

FROM ubuntu:22.04
RUN apt update && apt install socat -y
RUN groupadd -r ctf && useradd -r -g ctf ctf
WORKDIR /home/ctf
EXPOSE 9001

COPY flag.txt .
COPY pwneame .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .
RUN chmod +x pwneame
RUN chmod +x libc.so.6
RUN chmod +x ld-linux-x86-64.so.2


CMD ["socat", "tcp-l:9001,reuseaddr,fork", "EXEC:./pwneame"]



