import os
import sys
import time
import shutil
import string
import random
import tempfile
import subprocess

print("Welcome to DOSia!")
print("Gimme the size of your input >>", flush=True)

size = int(input())
if not 0 < size < 512:
    print("Do not hack me plz")
    exit(0)

print("Gimme your input >>", flush=True)

buffer = sys.stdin.buffer.read(size)

workdir = tempfile.TemporaryDirectory()
dirname = workdir.name

os.chdir(dirname)
os.symlink('/app/a.exe', './a.exe')
os.symlink('/app/FLAG', './FLAG')

f = open("./INPUT", "wb+")
f.write(str(size).encode()+b"\n")
f.write(buffer)
f.close()

p = subprocess.Popen(["dosbox", "-c", "mount c ./", "-c", "c:\\a.exe > c:\\OUTPUT"])
time.sleep(3)
if p:
    p.terminate()

data = b'No output...'

if os.path.exists('OUTPUT'):
    with open('OUTPUT', 'rb') as f:
        data = f.read()

print(data.decode(), flush=True)
