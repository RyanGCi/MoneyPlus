import requests

r = requests.post(
    "https://api.pluggy.ai/auth",
    json={
        "clientId": "e4453bce-4d6d-499d-8297-6dfa59882bdf",
        "clientSecret": "55b59310-6c8f-4dbc-8fc9-ffd276814ac1"
    }
)

print(r.json())