from firebase_db import db
from datetime import datetime

def get_gastos_mes():
    docs = db.collection("transacoes").stream()

    total = 0
    now = datetime.now()

    for doc in docs:
        d = doc.to_dict()
        data = datetime.fromisoformat(d["data"])

        if data.month == now.month and data.year == now.year:
            if d["valor"] < 0:
                total += float(d["valor"])

    return total


def get_ultimas():
    docs = db.collection("transacoes") \
        .order_by("data", direction="DESCENDING") \
        .limit(5).stream()

    return [doc.to_dict() for doc in docs]


def add_transacao(descricao, valor):
    db.collection("transacoes").add({
        "descricao": descricao,
        "valor": valor,
        "data": datetime.now().isoformat(),
        "categoria": "outros"
    })