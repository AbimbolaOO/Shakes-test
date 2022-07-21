import requests

url = "http://localhost:8000/gettoken"

payload = {"username": "yemi", "password": "12345678"}

response = requests.request("POST", url, data=payload)

print(response.text)
