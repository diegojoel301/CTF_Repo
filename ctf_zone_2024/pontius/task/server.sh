#!/usr/bin/env bash

socat tcp-l:1337,fork,reuseaddr exec:"sudo -u nobody env LD_PRELOAD=/task/libc.so.6 /task/ld.so /task/pontius"