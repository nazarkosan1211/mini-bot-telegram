from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# ==========================
# CONFIGURATION
# ==========================
# Ganti TOKEN ini dengan token bot Telegram kamu
TOKEN = "8707863883:AAGePtyGNttlo3EfLT1GXGKlBqFY9TBQ5G0"

# URL server Flask persisten (Flask + PostgreSQL)
API_URL = "https://mini-bot-telegram-production.up.railway.app"

# ==========================
# COMMAND HANDLERS
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = None  # kalau mau referral, bisa diambil dari context.args[0]
    payload = {"user_id": user_id, "ref": ref}
    try:
        res = requests.post(f"{API_URL}/start_user", json=payload).json()
        await update.message.reply_text(f"Selamat datang, user_id: {res['user_id']}!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    amount = 1  # default 1 koin per task, bisa diubah sesuai task
    payload = {"user_id": user_id, "amount": amount}
    try:
        res = requests.post(f"{API_URL}/add_coin", json=payload).json()
        if res.get("status") == "success":
            await update.message.reply_text(
                f"Koin kamu: {res['coins']}\nTasks Done: {res['tasks_done']}\nRemaining Tasks: {res['remaining_tasks']}"
            )
        elif res.get("status") == "blocked":
            await update.message.reply_text("Daily limit reached, coba besok!")
        else:
            await update.message.reply_text(str(res))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", add_coin))  # /task → add_coin

    print("Bot is running...")
    app.run_polling()
