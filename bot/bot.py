# =======================
# bot.py (Final Railway Safe)
# =======================

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# =======================
# CONFIG
# =======================
# Ganti ini dengan URL server Flask kamu (pastikan online)
API_URL = "https://mini-bot-telegram-production.up.railway.app"

# =======================
# HELPER
# =======================
def post_to_server(endpoint, payload):
    """Kirim POST ke server Flask dan return response JSON"""
    try:
        res = requests.post(f"{API_URL}/{endpoint}", json=payload, timeout=10)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =======================
# COMMAND HANDLERS
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = {"user_id": str(user_id)}
    
    res = post_to_server("start_user", payload)
    
    if res.get("status") == "success":
        await update.message.reply_text(
            f"Hello @{update.effective_user.username}! Kamu terdaftar di server.\nUser ID: {user_id}"
        )
    else:
        await update.message.reply_text(f"Error mendaftar user: {res.get('message')}")

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = {"user_id": str(user_id), "amount": 1}  # setiap task +1 coin
    
    res = post_to_server("add_coin", payload)
    
    if res.get("status") == "success":
        await update.message.reply_text(
            f"Task berhasil!\nCoins: {res['coins']}\nTasks Done: {res['tasks_done']}\nRemaining Tasks: {res['remaining_tasks']}"
        )
    elif res.get("status") == "blocked":
        await update.message.reply_text("Limit daily task tercapai. Tunggu besok.")
    else:
        await update.message.reply_text(f"Error: {res.get('message')}")

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    # Paste token bot langsung di sini
    TOKEN = "8707863883:AAGePtyGNttlo3EfLT1GXGKlBqFY9TBQ5G0"

    # Build bot application
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", task))

    # Run polling (Railway safe, tunggu 1 instance aja)
    print("Bot running...")
    app.run_polling()
