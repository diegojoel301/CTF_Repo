#!/bin/sh
socat tcp-listen:15557,reuseaddr,fork exec:"./loginator"

