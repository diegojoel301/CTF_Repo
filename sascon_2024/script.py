from pwn import *

io = remote("158.160.161.81", 13337)

print(io.recvall().decode())


