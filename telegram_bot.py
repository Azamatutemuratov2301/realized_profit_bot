# telegram_bot.py
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

API_URL = "http://127.0.0.1:8000"  # FastAPI manzili
TELEGRAM_TOKEN = "8158588417:AAEVoM7CdKJztk_eJHrHvipbUkRXYfHKowA"
ADMIN_ID = 313652330

keyboard = [["BUY GOLD", "SELL GOLD"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Ruxsat yo‘q.")
        return
    await update.message.reply_text("Savdoga tayyor. Tanlang:", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Ruxsat yo‘q.")
        return

    text = update.message.text
    if text == "BUY GOLD":
        response = requests.post(f"{API_URL}/trade", json={
            "symbol": "XAUUSD",
            "lot": 0.1,
            "order_type": "buy"
        })
        await update.message.reply_text(f"BUY yuborildi: {response.json()}")

    elif text == "SELL GOLD":
        response = requests.post(f"{API_URL}/trade", json={
            "symbol": "XAUUSD",
            "lot": 0.1,
            "order_type": "sell"
        })
        await update.message.reply_text(f"SELL yuborildi: {response.json()}")

    else:
        await update.message.reply_text("Menyudan tanlang.")

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    run_bot()
