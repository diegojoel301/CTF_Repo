from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generar una clave AES de 256 bits (32 bytes)
key = os.urandom(16)

# Generar un vector de inicialización (IV) de 128 bits (16 bytes)
iv = os.urandom(16)

# Guardar la clave y el IV en un fichero llamado "key"
with open('key_test', 'wb') as f:
    f.write(key)
    #f.write(iv)

print("Clave y IV guardados en 'key'")
print(f"Clave AES: {key.hex()}")
print(f"Vector de inicialización (IV): {iv.hex()}")

