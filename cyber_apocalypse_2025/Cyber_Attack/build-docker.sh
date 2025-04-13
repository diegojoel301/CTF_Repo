#!/bin/bash
clear
docker rm -f cyber_attack || true
docker build -t cyber_attack .
docker run --name=cyber_attack --rm -p1337:80 -it cyber_attack