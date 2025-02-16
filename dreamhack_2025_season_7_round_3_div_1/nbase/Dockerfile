FROM ubuntu:24.04@sha256:c920ba4cfca05503764b785c16b76d43c83a6df8d1ab107e7e6610000d94315c

RUN apt update
RUN apt-get install -y socat adduser

RUN adduser -u 1001 pwn

WORKDIR /home/pwn

COPY ./flag ./flag
COPY ./deploy/prob ./prob

RUN chmod 440 ./flag 
RUN chmod 755 ./prob

USER pwn

EXPOSE 8080
CMD socat TCP-LISTEN:8080,reuseaddr,fork EXEC:./prob,stderr
