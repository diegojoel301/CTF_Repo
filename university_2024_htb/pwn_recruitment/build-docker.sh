#!/bin/sh
docker build --tag=recruitment .
docker run -it -p 1337:1337 --rm --name=recruitment recruitment
