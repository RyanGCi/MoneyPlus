import csv
from services.categorizer import categorizar
from firebase_db import db
from datetime import datetime

def process_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        linhas = csvfile.readlines()

        # 🔥 encontra onde começa a tabela
        inicio = 0
        for i, linha in enumerate(linhas):
            if "Data Lançamento" in linha:
                inicio = i
                break

        reader = csv.DictReader(linhas[inicio:], delimiter=';')

        for row in reader:
            try:
                descricao = row["Descrição"].strip()

                # 💰 tratar valor (formato brasileiro)
                valor_str = row["Valor"].replace(".", "").replace(",", ".")
                valor = float(valor_str)

                # 📅 converter data
                data = datetime.strptime(row["Data Lançamento"], "%d/%m/%Y")

                categoria = categorizar(descricao)

                # 🔁 evitar duplicação
                if not ja_existe(descricao, valor, data.isoformat()):
                    db.collection("transacoes").add({
                        "descricao": descricao,
                        "valor": valor,
                        "data": data.isoformat(),
                        "categoria": categoria,
                        "source": "csv_inter"
                    })

            except Exception as e:
                print("Erro ao processar linha:", row, e)

def ja_existe(descricao, valor, data):
    docs = db.collection("transacoes") \
        .where("descricao", "==", descricao) \
        .where("valor", "==", valor) \
        .where("data", "==", data) \
        .stream()

    return any(docs)