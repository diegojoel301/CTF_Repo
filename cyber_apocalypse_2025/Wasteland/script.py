import pandas as pd
import requests

# Cargar el archivo CSV
df = pd.read_csv("Ashen_Outpost_Records.csv")

# Aumentar la reputación del SurvivorID 1337 y manipular otras columnas
df.loc[df['SurvivorID'] == 1337, 'Reputation'] = 61  # Subir la reputación a 61
df.loc[df['SurvivorID'] == 1337, 'Dragonfire_Resistance'] = 100  # Ejemplo de aumentar resistencia
df.loc[df['SurvivorID'] == 1337, 'Shadow_Crimes'] = 0  # Reducir los crímenes
df.loc[df['SurvivorID'] == 1337, 'Corruption_Mutations'] = 0  # Reducir las mutaciones

# Guardar el archivo modificado
df.to_csv("Ashen_Outpost_Records_modified.csv", index=False)

# Enviar el archivo modificado
with open("Ashen_Outpost_Records_modified.csv", "r") as f:
    r = requests.post("http://IP:PORT/score", files={"csv_file": f})
    print(r.text)
