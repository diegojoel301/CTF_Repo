#!/bin/bash
socat -T180 TCP-LISTEN:13339,reuseaddr,fork exec:"./server.py"
