import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from services.finance import get_gastos_mes, get_ultimas, add_transacao

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

def autorizado(user_id):
    return user_id == USER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update.effective_user.id):
        return
    await update.message.reply_text("Bot financeiro ativo 💰")


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

    try:
        valor = float(context.args[0])
        descricao = " ".join(context.args[1:])
        add_transacao(descricao, -abs(valor))

        await update.message.reply_text("Transação adicionada ✅")
    except:
        await update.message.reply_text("Uso: /add 50 mercado")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gastos_mes", gastos_mes))
app.add_handler(CommandHandler("ultimas", ultimas))
app.add_handler(CommandHandler("add", add))