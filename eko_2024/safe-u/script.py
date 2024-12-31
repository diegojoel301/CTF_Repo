import itertools

# Fecha en formato numérico "29 de febrero de 1996" -> 29021996
fecha = "29021996"

# Generar todas las permutaciones posibles de 8 dígitos
permutaciones = itertools.permutations(fecha, 8)

# Convertir las permutaciones en números y almacenarlas en un conjunto (para eliminar duplicados)
permutaciones_numeros = {''.join(p) for p in permutaciones}

# Mostrar las permutaciones ordenadas
for perm in sorted(permutaciones_numeros):
    print(perm)
