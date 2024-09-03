from pwn import *

mapa = {
    "GORGE": "STOP",
    "PHREAK": "DROP",
    "FIRE": "ROLL"
}

def f(cadena):
    v = cadena.decode().strip().split(',')

    output = str()

    for element in v:
        output += mapa[element.replace(" ", "")] + "-"
    
    output = output[:len(output) - 1]

    return output.encode()

    
io = remote("83.136.250.225", 45959)

#io.sendlineafter("Are you ready? (y/n) ", b"y\n")

io.recvline()

io.sendline(b"y")

io.recvuntil("Are you ready? (y/n) Ok then! Let's go!\n")


io.sendline(f(io.recvline()))

for i in range(500):
    io.recvuntil("What do you do?")
    output = f(io.recvline())
    print("[+] "+ (str(i + 1)) + ": ", output)
    io.sendline(output)

#io.recvuntil("What do you do?")
#output = f(io.recvline())
#print("[+]", output)
#io.sendline(output)

io.interactive()


#io.close()
