#!/bin/bash

# Función para mapear las acciones
map_actions() {
    case $1 in
        "GORGE") echo "STOP" ;;
        "PHREAK") echo "DROP" ;;
        "FIRE") echo "ROLL" ;;
    esac
}

# Conecta al servidor
exec 3<>/dev/tcp/83.136.254.223/41142

# Espera la bienvenida
read -r welcome <&3
echo "$welcome"

# Envía la respuesta inicial
echo "y" >&3

# Lee la situación del juego y responde
while read -r situation <&3; do
    actions=$(echo "$situation" | tr -d '[:space:]' | tr ',' '\n')
    response=""
    for action in $actions; do
        response+="$(map_actions "$action")-"
    done
    response=$(echo "$response" | sed 's/-$//')
    echo "$response" >&3
    read -r result <&3
    echo "$result"
done

# Cierra la conexión
exec 3<&-
exec 3>&-

