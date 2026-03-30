from firebase_db import db
from collections import defaultdict
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

def get_resumo_mes():
    docs = db.collection("transacoes").stream()

    entradas = 0
    saidas = 0
    categorias = {}

    for doc in docs:
        d = doc.to_dict()
        valor = float(d["valor"])

        if valor > 0:
            entradas += valor
        else:
            saidas += abs(valor)

            cat = d.get("categoria", "outros")
            categorias[cat] = categorias.get(cat, 0) + abs(valor)

    saldo = entradas - saidas

    top = sorted(categorias.items(), key=lambda x: x[1], reverse=True)

    return entradas, saidas, saldo, top