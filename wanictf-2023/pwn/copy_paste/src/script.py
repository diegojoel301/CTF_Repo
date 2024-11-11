import sys
from pwn import *

elf = ELF("chall")
libc = ELF("libc.so.6")

def start():
    if args.REMOTE:
        return remote("83.136.252.167", 40382)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = process(elf.path, env = {"LD_PRELOAD":"./libc.so.6"})



io.interactive()
