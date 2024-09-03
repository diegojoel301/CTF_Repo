from Cryptodome.Cipher import AES

f = open("./key", "rb")

key = f.read()

f.close()

cipher = AES.new(bytes(key), AES.MODE_ECB)

print(cipher.encrypt("ls ŠŠŠŠŠŠŠŠŠŠŠŠŠ".encode("UTF-8").ljust(16, b"\x00")).hex())
#print(cipher.decrypt(b""))

