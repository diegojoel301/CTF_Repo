from pwn import *

io = process("./chall")

for i in range(0, 3):
    print(i)
    challengue = str(100 - i)
    challengue = " "*(3 - len(challengue)) + challengue

    io.recvuntil(f"| your score: {i}, remaining {challengue} challenges |")
    io.recvuntil("+-----------------------------------------+")

    sum_math = io.recvuntil('=').strip()[:-1]

    io.sendline(str(eval(sum_math)).encode())


io.interactive()
