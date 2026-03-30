from services.categorizer import categorizar
from firebase_db import db

def ja_existe(transacao):
    docs = db.collection("transacoes") \
        .where("descricao", "==", transacao["descricao"]) \
        .where("valor", "==", transacao["valor"]) \
        .where("data", "==", transacao["data"]) \
        .stream()

    return any(docs)


def run_pipeline(transactions):
    salvas = 0

    for t in transactions:
        t["categoria"] = categorizar(t["descricao"])
        t["source"] = "ofx"

        if not ja_existe(t):
            db.collection("transacoes").add(t)
            salvas += 1

    return salvas