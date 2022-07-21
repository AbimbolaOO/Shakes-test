import requests

url = "http://localhost:8000/v1/currency/all/"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5ZW1pIiwiZXhwIjoxNjU4Mzk2NDU0fQ.9440tul8O_DwHmrERbSZBEA9Xhp1u1kp0aA66lJaBxU"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
