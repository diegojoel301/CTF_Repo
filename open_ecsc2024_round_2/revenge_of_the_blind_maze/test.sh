#!/bin/bash

# Definir una función para enviar la solicitud y buscar la cadena de texto
check_maze() {
    mov=$1
    result=$(curl -s "http://blindmazerevenge.challs.open.ecsc2024.it/maze?direction=$mov" -H "Cookie: session=dV6Iyt5K89iD23ArIFg49t_ACnpXueU4r-q3dQSiJ3k" | grep -i "openECSC")
    if [ ! -z "$result" ]; then
        echo "¡Se encontró una coincidencia para la dirección $mov!"
        echo "$result"
    fi
}

# Exportar la función para que esté disponible para xargs
export -f check_maze

# Procesar cada movimiento en paralelo
cat movs | xargs -n 1 -P 10 -I {} bash -c 'check_maze "{}"'

