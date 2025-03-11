#!/bin/sh

docker build -t noprint .
docker run -d -p 1337:1337 -it noprint
