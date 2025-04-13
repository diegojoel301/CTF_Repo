import requests

with open(f"Ashen_Outpost_Records_modified.csv", "r") as f:
	r = requests.post("http://94.237.51.67:39746/score", files={"csv_file": f})
	print(r.text)