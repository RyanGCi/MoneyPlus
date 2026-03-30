CATEGORIAS = {
    "alimentacao": ["ifood", "restaurante", "mercado", "lanche", "pizza"],
    "transporte": ["uber", "99", "gasolina", "posto"],
    "moradia": ["aluguel", "luz", "agua", "internet"],
    "lazer": ["cinema", "netflix", "bar"],
}

def categorizar(descricao: str) -> str:
    descricao = descricao.lower()

    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in descricao:
                return categoria

    return "outros"