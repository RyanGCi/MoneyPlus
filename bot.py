import os
from dotenv import load_dotenv
from firebase_db import db
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from services.finance import get_gastos_mes, get_ultimas, add_transacao, get_resumo_mes
from services.parser import parse_input
from services.categorizer import categorizar
from services.pluggy import create_connect_token, sync_transactions
from services.extract.ofx_inter import extract_ofx
from services.pipeline import run_pipeline

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

def autorizado(user_id):
    return user_id == USER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update.effective_user.id):
        return
    await update.message.reply_text("Bot financeiro ativo 💰" \
    "\nComandos Suportados:" \
    "\n\n/adicionar" \
    "\n/gastos_mes" \
    "\n/resumo" \
    "\n/ultimas" \
    "\n/receber_ofx")


async def gastos_mes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update.effective_user.id):
        return

    total = get_gastos_mes()
    await update.message.reply_text(f"Gastos no mês: R$ {abs(total):.2f}")


async def ultimas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update.effective_user.id):
        return

    dados = get_ultimas()

    msg = "Últimas transações:\n"
    for d in dados:
        msg += f"{d['descricao']}: R$ {d['valor']}\n"

    await update.message.reply_text(msg)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update.effective_user.id):
        return

    texto = " ".join(context.args)

    parsed = parse_input(texto)

    categoria = categorizar(parsed["descricao"])

    db.collection("transacoes").add({
        "valor": -abs(parsed["valor"]),
        "descricao": parsed["descricao"],
        "categoria": categoria,
        "data": parsed["data"]
    })

    await update.message.reply_text(
        f"💸 {parsed['descricao']} - R$ {parsed['valor']:.2f} ({categoria})"
    )

async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, categorias = get_resumo_mes()

    msg = "📊 Resumo do mês\n\n"
    msg += f"💸 Total gasto: R$ {total:.2f}\n\n"

    msg += "📂 Categorias:\n"
    for cat, valor in categorias[:3]:
        porcentagem = (valor / total) * 100 if total > 0 else 0
        msg += f"- {cat}: R$ {valor:.2f} ({porcentagem:.1f}%)\n"

    if categorias:
        top_cat = categorias[0]
        msg += f"\n🔥 Maior gasto: {top_cat[0]}"

    await update.message.reply_text(msg)

async def conectar_banco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = create_connect_token()

    link = f"https://connect.pluggy.ai?connect_token={token}"

    await update.message.reply_text(
        f"🔗 Conecte sua conta:\n{link}"
    )

async def sync(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sync_transactions()
    await update.message.reply_text("✅ Transações sincronizadas!")

async def receber_arquivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name.lower()

    file = await document.get_file()
    file_path = f"/tmp/{document.file_name}"
    await file.download_to_drive(file_path)

    if file_name.endswith(".ofx"):
        from services.extract.ofx_inter import extract_ofx
        from services.pipeline import run_pipeline

        transactions = extract_ofx(file_path)
        total = run_pipeline(transactions)

        await update.message.reply_text(
            f"✅ {total} transações importadas (OFX)"
        )

    elif file_name.endswith(".csv"):
        await update.message.reply_text(
            "⚠️ CSV desativado por enquanto"
        )

    else:
        await update.message.reply_text(
            "❌ Formato não suportado"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gastos_mes", gastos_mes))
app.add_handler(CommandHandler("ultimas", ultimas))
app.add_handler(CommandHandler("adicionar", add))
app.add_handler(CommandHandler("resumo", resumo))
app.add_handler(CommandHandler("conectar", conectar_banco))
app.add_handler(CommandHandler("sincronizar", sync))
app.add_handler(MessageHandler(filters.Document.ALL, receber_arquivo))