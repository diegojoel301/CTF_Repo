#!/bin/sh

docker build -t einstein .
docker run -p 1337:1337 -it einstein
