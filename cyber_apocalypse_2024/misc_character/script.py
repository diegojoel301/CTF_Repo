from pwn import *

io = remote("83.136.248.36", 37582)

for i in range(200):
    io.sendlineafter("index:", str(i).encode())
    io.recvuntil(":")
    print(io.recvline().decode(), end="")

io.close()
