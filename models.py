from firebase_db import get_conn

def criar_tabelas():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id SERIAL PRIMARY KEY,
        descricao TEXT,
        valor NUMERIC,
        data DATE,
        categoria TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()