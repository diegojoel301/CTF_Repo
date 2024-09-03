from pwn import *

mapa = {
    "GORGE": "STOP",
    "PHREAK": "DROP",
    "FIRE": "ROLL"
}

conn = remote("83.136.254.223", 41142)

conn.sendlineafter("Are you ready? (y/n) ", b"y\n")

conn.recvuntil("What do you do?")

while True:
    # Recibe la situación actual del juego
    situation = conn.recvline().decode().strip()
    print(situation)

    # Sale del bucle si el juego ha terminado
    if not situation:
        break

    # Mapea las acciones y forma la respuesta
    actions = [mapa[element.strip()] for element in situation.split(',')]
    response = '-'.join(actions)

    # Envía la respuesta al servidor
    conn.sendline(response.encode())

    print(conn.recvline().decode())  # Imprime la respuesta del servidor

conn.close()

