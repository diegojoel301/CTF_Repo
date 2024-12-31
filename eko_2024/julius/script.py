def buscar_cadena_y_extraer(datos, cadena):
    # Convierte los datos binarios a una cadena de texto para la búsqueda
    try:
        texto = datos.decode('latin1')  # Usamos latin1 para evitar errores con caracteres fuera de rango ASCII
        index = texto.find(cadena)  # Busca la cadena "EKO"
        
        if index != -1:
            # Extrae los datos después de la cadena "EKO"
            datos_despues = datos[index + len(cadena):]
            return datos_despues
        else:
            return None
    except UnicodeDecodeError:
        return None

def cifrar_cesar_con_clave(archivo_entrada, clave, cadena_buscada):
    try:
        # Abre el archivo binario en modo lectura
        with open(archivo_entrada, 'rb') as file_in:
            # Lee los datos del archivo
            datos = file_in.read()

        # Convertir la clave en una lista de desplazamientos basados en los valores ASCII
        desplazamientos = [ord(c) for c in clave]

        # Realiza hasta 100 desplazamientos
        for desplazamiento_indice in range(1000):
            # Calcula el desplazamiento con la clave cíclicamente
            desplazamiento = desplazamientos[desplazamiento_indice % len(desplazamientos)]

            # Cifra los datos con el cifrado César usando el desplazamiento basado en la clave
            datos_cifrados = bytearray()
            for byte in datos:
                byte_cifrado = (byte + desplazamiento) % 256
                datos_cifrados.append(byte_cifrado)

            # Busca la cadena y extrae lo que viene después
            resultado = buscar_cadena_y_extraer(datos_cifrados, cadena_buscada)
            if resultado:
                print(f"Cadena '{cadena_buscada}' encontrada en el desplazamiento {desplazamiento_indice + 1}.")
                print("Lo que sigue después de 'EKO':")
                print(resultado[:100])  # Imprime los primeros 100 bytes después de 'EKO' para no saturar la salida
                break
        else:
            print("Cadena no encontrada en ninguno de los desplazamientos.")

    except Exception as e:
        print(f"Error: {e}")

# Ejemplo de uso
archivo_entrada = 'julius'  # Ruta al archivo binario a cifrar
clave = 'caesar'  # Clave de cifrado (cadena)
cadena_buscada = 'EKO'  # Cadena a buscar

cifrar_cesar_con_clave(archivo_entrada, clave, cadena_buscada)
