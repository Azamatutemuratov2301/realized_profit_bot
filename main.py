# main.py
import os
import asyncio
from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)

# Import your bot logic and configuration
from bot_logic import (
    start_command,
    change_language_command,
    handle_language_selection,
    calculate_profit_command,
    handle_price_input
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# FastAPI application
app = FastAPI()

# Initialize Telegram bot application
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Define Telegram bot handlers
def setup_bot_handlers():
    bot_app.add_handler(CommandHandler("start", start_command))
    bot_app.add_handler(CommandHandler("help", start_command))  # You can define a separate help_command
    bot_app.add_handler(MessageHandler(filters.Regex("^(🌐|Tilni o'zgartirish|Select language|Выберите язык|Тілді таңдаңыз)$"), change_language_command))
    bot_app.add_handler(MessageHandler(filters.Regex("^(uz|en|ru|kz)$"), handle_language_selection))
    bot_app.add_handler(MessageHandler(filters.Regex("^(📊|Foydani hisoblash|Your profit|Ваша прибыль|Сіздің пайдаңыз)$"), calculate_profit_command))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price_input))

@bot_app.on_message(filters.TEXT)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Any custom message handling can be done here
    pass

@app.get("/")
async def root():
    return {"message": "Realized Profit bot is working"}

@app.on_event("startup")
async def startup_event():
    setup_bot_handlers()
    # Start the Telegram bot polling in a separate task
    asyncio.create_task(bot_app.run_polling())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
