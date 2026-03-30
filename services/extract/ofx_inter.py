from ofxparse import OfxParser, OfxParserException

def extract_ofx(file_path):
    limpar_ofx(file_path)
    transactions = []

    with open(file_path, encoding="utf-8") as f:
        try:
            ofx = OfxParser.parse(f)
        except OfxParserException as e:
            print("Erro ao parsear OFX:", e)
            raise Exception("OFX inválido ou com dados inconsistentes")

    for account in ofx.accounts:
        for t in account.statement.transactions:
            try:
                descricao = t.memo or t.payee or "sem descricao"

                transactions.append({
                    "descricao": descricao.strip(),
                    "valor": float(t.amount),
                    "data": t.date.isoformat()
                })

            except Exception as e:
                print("Transação ignorada:", e)

    return transactions

def limpar_ofx(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # 🔥 Corrige transações sem NAME
    conteudo = conteudo.replace("<NAME></NAME>", "<NAME>sem_nome</NAME>")
    conteudo = conteudo.replace("<NAME/>", "<NAME>sem_nome</NAME>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(conteudo)