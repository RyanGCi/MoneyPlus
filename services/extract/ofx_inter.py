from ofxparse import OfxParser

def extract_ofx(file_path):
    with open(file_path, encoding="utf-8") as f:
        ofx = OfxParser.parse(f)

    transactions = []

    for account in ofx.accounts:
        for t in account.statement.transactions:
            transactions.append({
                "descricao": t.memo or t.payee or "sem descricao",
                "valor": float(t.amount),
                "data": t.date.isoformat()
            })

    return transactions