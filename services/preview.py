from collections import defaultdict
from services.categorizer import categorizar

def gerar_preview(transactions):
    entradas = 0
    saidas = 0
    categorias = defaultdict(float)

    for t in transactions:
        valor = float(t["valor"])

        if valor > 0:
            entradas += valor
        else:
            saidas += abs(valor)

        cat = categorizar(t["descricao"])
        categorias[cat] += abs(valor)

    top = sorted(categorias.items(), key=lambda x: x[1], reverse=True)

    return {
        "qtd": len(transactions),
        "entradas": entradas,
        "saidas": saidas,
        "saldo": entradas - saidas,
        "categorias": top[:3]
    }