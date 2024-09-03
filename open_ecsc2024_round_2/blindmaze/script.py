import requests

# URL base del juego
base_url = "http://blindmaze.challs.open.ecsc2024.it/maze"

# Inicialización del juego
response = requests.get(base_url, params={"direction": "start"})
# Obtener la cookie de sesión
session_cookie = response.cookies["session"]

# Bucle principal para navegar por el laberinto
while True:
    # Direcciones a probar
    directions = ["up", "left", "right", "down"]
    
    # Iterar sobre las direcciones
    for direction in directions:
        # Hacer una solicitud con la dirección actual
        response = requests.get(
            base_url,
            params={"direction": direction},
            cookies={"session": session_cookie}
        )
        # Analizar la respuesta
        if "FAILED" not in response.text:
            # Si la solicitud fue exitosa, mostrar la última dirección
            print("Última dirección:", direction)
            # Actualizar la cookie de sesión
            session_cookie = response.cookies["session"]
            # Si se encuentra la flag, terminar el juego
            if "openECSC{" in response.text:
                print("¡Flag encontrada!")
                print(response.text)
                exit()
            break
        else:
            print(f"Intento de dirección {direction} fallido. Intentando de nuevo...")

