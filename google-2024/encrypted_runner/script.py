from pwn import *
from Cryptodome.Cipher import AES
import subprocess

io = process(["python3", "chal.py"])
#r = remote("localhost", int(sys.argv[1]))
#io = remote("encrypted-runner.2024.ctfcompetition.com", 1337)

io.recvuntil(b"run command (e.g. 'run ")

#encrypted_echo = bytes.fromhex(io.recvline().split(b"'")[0].decode()) # Este es para el chall
encrypted_echo = bytes.fromhex("358fb3b17133dd4913e0eedcbbf7d164")

#io.sendline(b"encrypt ls " + b"a" * 13)

io.sendline(("encrypt ls " + "Š"*13).encode())

io.recvuntil(b"Encrypted command: ")
line = io.recvline().strip()
print(line)
io.sendline(b"run " + line)

io.recvuntil(b"Output: ls: cannot access ")
line = io.recvuntil(b": No such file or directory").rsplit(b":", 1)[0]

print(f"Leak: {line}")

cmd = b"echo -n " + line
print("cmd",cmd)
out = subprocess.check_output(["bash", "-c", cmd])

print("bash string", out)

for i in range(0, 256):
    key = [0, 0, 0] + [i ^ o for o in out]

    print(f"[+] Para: {i}: ", [hex(j) for j in key])

key = [0, 0, 0] + [82 ^ o for o in out]

print("Key: ", [hex(j) for j in key])

#cipher = AES.new(bytes(key), AES.MODE_ECB)
#pt = cipher.decrypt(encrypted_echo)

#print("Encrypted echo: ", encrypted_echo)
#print(pt)


#while not found:

# En mi caso es 82

for i in range(82, 256):
    found = False
    key = [0, 0, 0] + [i ^ o for o in out]

    print(f"[+] Para: {i}: ", [hex(j) for j in key])

    # Cheating for speedy healthcheck, normally we would start from zero.
    for a in range(76, 256):
        if found: break
        #print(a)
        key[0] = a
        for b in range(256):
            if found: break
            key[1] = b
            for c in range(256):
                key[2] = c
                cipher = AES.new(bytes(key), AES.MODE_ECB)
                pt = cipher.decrypt(encrypted_echo)
                if pt.startswith(b'echo'):
                    print("plaintext", pt)
                    found = True
                    break

    if found:
        break

print("full key", bytes(key))
cmd = b"echo ; whoami".ljust(16, b"\x00")
cipher = AES.new(bytes(key), AES.MODE_ECB)
ct = cipher.encrypt(cmd).hex()

io.sendline(b"run "+ct.encode())

io.interactive()
io.close()


