#!/bin/bash

mv /flag.txt /flag-$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 15).txt

# Start supervisord
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf