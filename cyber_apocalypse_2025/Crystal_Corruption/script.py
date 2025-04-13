import torch

data = torch.load("eldorian_artifact.pth")

# Obtener la diagonal de la matriz
diagonal = torch.diag(data["hidden.weight"])

# Convertir cada valor en entero y luego a carácter ASCII
decoded_text = "".join(chr(int(x.item())) for x in diagonal)

print(decoded_text)
