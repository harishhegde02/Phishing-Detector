import requests

url = "http://127.0.0.1:8000/api/v1/analyze"
payload = {"text": "URGENT: Your bank account is locked!"}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
