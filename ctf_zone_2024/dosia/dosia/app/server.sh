#!/usr/bin/env bash

socat tcp-l:1337,fork,reuseaddr exec:"sudo -u nobody SDL_VIDEODRIVER=dummy env python3 /app/service.py"
