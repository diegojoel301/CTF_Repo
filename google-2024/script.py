from pwn import *
import hashlib

gs = '''
b* command+853
continue
'''

elf = ELF("./chal")

def start():
    if args.REMOTE:
        return remote("83.136.252.167", 40382)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

#io.sendline("plain plain flag{m4g0_3stuv0_4qu1}")
io.sendline(b"plain plain 1")
io.sendline(b"plain plain 12")
io.sendline(b"plain plain 123")
io.sendline(b"plain plain 1234")
io.sendline(b"plain plain 12345")
io.sendline(b"plain plain 123456")
io.sendline(b"plain plain 1234567")
io.sendline(b"plain plain 12345678")
io.sendline(b"plain plain 123456789")

cadena = "sexo"

sha256_hash = hashlib.sha256(cadena.encode('utf-8')).hexdigest()

"""
io.sendline(f"hex plain {sha256_hash}".encode())

io.recvuntil(b"Result: \xc1")

print(sha256_hash)

leak_hash = b"\xc1"+ io.recvline()

print(f"[+] Mira: {leak_hash.strip()}")
"""
io.interactive()
