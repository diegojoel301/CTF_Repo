from pwn import *

io = remote("chal-lz56g6.wanictf.org", 9003)
io.sendline(b"10")
io.interactive()
