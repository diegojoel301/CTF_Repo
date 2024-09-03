from pwn import *

io = remote("24.199.110.35", 42189)


io.sendlineafter("? ", b"20")

for i in range(19):

    print(i)

    io.recvuntil(b"what is ")

    res = eval(io.recv(8).decode().strip().replace("=", ""))

    io.sendline(str(res).encode())

io.interactive()
