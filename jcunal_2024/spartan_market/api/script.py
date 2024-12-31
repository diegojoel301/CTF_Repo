import requests

url = "https://1u53gb91ge.execute-api.us-east-1.amazonaws.com"

def search_product(value):

    params = {
        "search": value
    }

    r = requests.get(url + "/products", params=params)

    return r.text

def create_product(product_id, name, price, rating, stockQuantity):

    data = {
        "productId": product_id,
        "name": name,
        "price": price, 
        "rating": rating, 
        "stockQuantity": stockQuantity
    }

    r = requests.post(url + "/products", data=data)

    return r.text

#print(create_product("e1f267e1-1d02-4e3e-a778-208bb0afc63fff' and pg_sleep(5) -- -", "hola", 1, 2, 3))

print(search_product(1))


#r = requests.get(url + "/")

#print(r.text)
