from collections import defaultdict
from services.categorizer import categorizar

def gerar_preview(transactions):
    total = 0
    categorias = defaultdict(float)

    for t in transactions:
        valor = float(t["valor"])

        if valor < 0:
            total += abs(valor)

        cat = categorizar(t["descricao"])
        categorias[cat] += abs(valor)

    top = sorted(categorias.items(), key=lambda x: x[1], reverse=True)

    return {
        "qtd": len(transactions),
        "total": total,
        "categorias": top[:3]
    }