from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("chall.lac.tf", 31338)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.interactive()