import requests

def enviar_archivo_binario_via_get(url, archivo):
    with open(archivo, 'rb') as f:
        contenido_binario = f.read()

    parametros = {'uicolor': contenido_binario}
    headers = {'Cookie': 'session=sexoanalEEEEEEEE'}
    response = requests.get(url, params=parametros, headers = headers)
    
    return response

# Ejemplo de uso
url_destino = 'http://192.168.86.250:1337/set'
archivo_a_enviar = 'bin'

respuesta = enviar_archivo_binario_via_get(url_destino, archivo_a_enviar)
print(respuesta.text)
