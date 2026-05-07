import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ganti dengan token bot kamu
TOKEN = "8707863883:AAGePtyGNttlo3EfLT1GXGKlBqFY9TBQ5G0"

# Ganti dengan URL server Railway kamu
SERVER_URL = "https://mini-bot-telegram-production.up.railway.app"

bot = Bot(token=TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = str(update.message.from_user.username)
    # Fetch data user dari server
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

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot jalan... Tekan Ctrl+C untuk stop")
    app.run_polling()
