FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y socat dash python3 git gdb python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /bin/dash /bin/sh

RUN git clone https://github.com/pwndbg/pwndbg && \
    cd pwndbg && \
    ./setup.sh

RUN pip install pwntools --break-system-packages

EXPOSE 1337

RUN groupadd -r ctf && useradd -r -g ctf ctf

COPY challenge/ /home/ctf/

WORKDIR /home/ctf

RUN chown -R ctf:ctf /home/ctf && chmod +x /home/ctf/recruitment

USER root

CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./recruitment"]
