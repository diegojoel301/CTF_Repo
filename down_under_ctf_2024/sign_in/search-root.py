f_mem = open("no-pie-memory", "r")

memoria = dict()

for line in f_mem:
    
    elemento = line.strip().split(':')
    #memoria[elemento[0]] = [ hex(int(i, 16)) for i in elemento[1].strip().split("\t")]
    valores = elemento[1].strip().split("\t")
    memoria[elemento[0]] = hex(int(valores[0], 16))
    memoria[hex(int(elemento[0], 16) + 8)] = hex(int(valores[1], 16))

# Buscando referecias

for pos in memoria.keys():
    # Buscamos la referencia
    if memoria[pos] in memoria.keys():
        # De esa referencia vemos sus valores, nos interesa que el primer valor sea 0x0 ya que ese sera el UID
        valor = memoria[pos]

        if memoria[valor] == "0x0":
            estructura_de_datos = valor
            estructura_de_datos_int = int(valor, 16)

            print(f"[+] Encontrado {pos}")
            print(f"UID : {estructura_de_datos}")
            
            print(f"Username : {memoria[hex(estructura_de_datos_int + 8)]}")
            print(f"Password : {memoria[hex(estructura_de_datos_int + 8 + 8)]}")

f_mem.close()