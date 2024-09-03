import os
import sys
import time

maps = open("/proc/self/maps", "r").readlines()
maps = list(filter(lambda i: i.strip().split(' ')[-1] == '/python3.12/bin/python3.12', maps))[0]
python_base = maps.split('-')[0]
print(f"You desired python base is 0x{python_base}")

print("Gimme the off:", end=' ', flush=True)
off = int(input(), 16)
print("Gimme the loot:", end=' ', flush=True)
value = sys.stdin.buffer.read(2)

memory = open("/proc/self/mem", "wb")
memory.seek(off, os.SEEK_SET)
memory.write(value)
memory.close()

print('Okay!')