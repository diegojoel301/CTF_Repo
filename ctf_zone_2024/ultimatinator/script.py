import hashlib
import string
import itertools

def find_fast_matching_hash(target_suffix):
    base_string = 'abcdefghijklmnopqrstuvwxyzabcdef'  # Cadena base de 32 caracteres (solo letras)
    
    
    # Iterar sobre todas las combinaciones posibles de los últimos 6 caracteres usando solo letras
    for suffix in itertools.product(string.ascii_lowercase, repeat=6):
        candidate = (base_string[:-6] + ''.join(suffix)).encode()  # Modifica solo los últimos 6 caracteres
        candidate_hash = hashlib.sha256(candidate).hexdigest()
        
        if candidate_hash[-6:] == target_suffix:
            return candidate.decode()

# El hash objetivo proporcionado por el servidor
target_suffix = '52d83f'  # Cambia esto según el hash que te proporcionen
result = find_fast_matching_hash(target_suffix)

print(f"Entrada encontrada: {result}")

