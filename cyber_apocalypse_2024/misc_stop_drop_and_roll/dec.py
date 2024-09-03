mapa = {
    "GORGE": "STOP",
    "PHREAK": "DROP",
    "FIRE": "ROLL"
}

v = input().strip().split(',')

output = str()

for element in v:
    output += mapa[element.replace(" ", "")] + "-"

output = output[:len(output) - 1]

print(output)
