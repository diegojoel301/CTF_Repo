from pwn import *

gs = '''
break *input+114
continue
'''

elf = context.binary = ELF("./pontius")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

shellcode = """
    mov rax, 60
    syscall
"""

shellcode = asm(shellcode)
io.recvuntil("Waiting for your shellcode...")
io.recvline()
io.recvuntil("Waiting for your shellcode...")

#io.send(shellcode)

io.interactive()
