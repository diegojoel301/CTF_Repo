import requests

# URL base del juego
base_url = "http://blindmazerevenge.challs.open.ecsc2024.it/maze"

# Leer las direcciones desde el archivo "movs"
with open("movs", "r") as file:
    directions = [line.strip() for line in file.readlines()]

# Inicialización del juego
response = requests.get(base_url, params={"direction": "start"})
# Obtener la cookie de sesión
session_cookie = response.cookies["session"]

answer = str()

# Bucle principal para navegar por el laberinto
for direction in directions:
    # Hacer una solicitud con la dirección actual
    response = requests.get(
        base_url,
        params={"direction": direction},
        cookies={"session": session_cookie}
    )
    answer = response.text
    # Analizar la respuesta
    if "FAILED" not in response.text:
        # Si la solicitud fue exitosa, mostrar la última dirección
        print("Última dirección:", direction)
        # Actualizar la cookie de sesión
        session_cookie = response.cookies["session"]
        # Si se encuentra la flag, terminar el juego
        if "openECSC{" in response.text or "flag" in response.text:
            print("¡Flag encontrada!")
            print(response.text)
            exit()
    else:
        print(f"Intento de dirección {direction} fallido. Intentando de nuevo...")
print(answer)
