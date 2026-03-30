import requests
import os
from firebase_db import db

BASE_URL = "https://api.pluggy.ai"

def get_token():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={
            "clientId": os.getenv("PLUGGY_CLIENT_ID"),
            "clientSecret": os.getenv("PLUGGY_CLIENT_SECRET")
        }
    )

    return response.json()["apiKey"]

def create_connect_token():
    api_key = get_token()

    response = requests.post(
        f"{BASE_URL}/connect_token",
        headers={"X-API-KEY": api_key}
    )

    return response.json()["accessToken"]

def get_accounts():
    api_key = get_token()

    response = requests.get(
        f"{BASE_URL}/accounts",
        headers={"X-API-KEY": api_key}
    )

    return response.json()["results"]

def get_transactions(account_id):
    api_key = get_token()

    response = requests.get(
        f"{BASE_URL}/transactions",
        headers={"X-API-KEY": api_key},
        params={"accountId": account_id}
    )

    return response.json()["results"]

def sync_transactions():
    accounts = get_accounts()

    for acc in accounts:
        txs = get_transactions(acc["id"])

        for t in txs:
            db.collection("transacoes").add({
                "descricao": t["description"],
                "valor": t["amount"],
                "data": t["date"],
                "categoria": "auto",
                "source": "pluggy"
            })