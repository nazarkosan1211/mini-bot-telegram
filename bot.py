import os
import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =======================
# GANTI DI SINI TOKEN BOT MU
# =======================
TOKEN = "8707863883:AAGePtyGNttlo3EfLT1GXGKlBqFY9TBQ5G0"

# =======================
# SERVER URL PUBLIC (udah aku isi)
# =======================
SERVER_URL = "https://mini-bot-telegram-production.up.railway.app"

bot = Bot(token=TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = str(update.message.from_user.username)
    try:
        response = requests.get(f"{SERVER_URL}/user/{username}")
        if response.status_code == 200:
            data = response.json()["data"]
            points = data.get("points", 0)
            tasks = data.get("tasks", [])
            await update.message.reply_text(
                f"Hello @{username}!\nPoints: {points}\nTasks: {', '.join(tasks)}"
            )
        else:
            await update.message.reply_text(
                f"Hello @{username}!\nKamu belum terdaftar di server."
            )
    except Exception as e:
        await update.message.reply_text(f"Terjadi error: {e}")

if __name__ == "__main__":
    print("Bot jalan... Tekan Ctrl+C untuk stop")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
