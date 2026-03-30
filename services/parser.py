import re
from datetime import datetime, timedelta

def parse_input(texto: str):
    texto = texto.lower()

    # valor
    valor_match = re.search(r'\d+[.,]?\d*', texto)
    valor = float(valor_match.group().replace(",", ".")) if valor_match else 0

    # descrição (remove valor)
    descricao = texto.replace(valor_match.group(), "").strip()

    # data
    data = datetime.now()

    if "ontem" in texto:
        data = datetime.now() - timedelta(days=1)

    return {
        "valor": valor,
        "descricao": descricao.strip(),
        "data": data.isoformat()
    }