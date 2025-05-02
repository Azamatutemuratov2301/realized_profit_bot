# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Realized Profit bot is working"}

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
from bot_logic import TradingBot

bot = TradingBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(bot.get_text("welcome"))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yordam:\n/start - Boshlash\n/help - Yordam")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot ishga tushdi...")
    app.run_polling()

if name == "main":
    main()

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
import asyncio
import os

from config import BOT_TOKEN
from bot_logic import (
    start_command,
    change_language_command,
    handle_language_selection,
    calculate_profit_command,
    handle_price_input
)

# FastAPI ilovasi
app = FastAPI()

# Telegram bot ilovasi
bot_app = Application.builder().token(BOT_TOKEN).build()

# Handlerlar
bot_app.add_handler(CommandHandler("start", start_command))
bot_app.add_handler(MessageHandler(filters.Regex("^(🌐|Tilni o'zgartirish|Select language|Выберите язык|Тілді таңдаңыз)$"), change_language_command))
bot_app.add_handler(MessageHandler(filters.Regex("^(uz|en|ru|kz)$"), handle_language_selection))
bot_app.add_handler(MessageHandler(filters.Regex("^(📊|Foydani hisoblash|Your profit|Ваша прибыль|Сіздің пайдаңыз)$"), calculate_profit_command))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price_input))

# Asosiy ishga tushirish
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_app.run_polling())

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Realized_Profit botiga xush kelibsiz.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yordam: Buyruqlar ro‘yxati:\n/start - Boshlash\n/help - Yordam")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot ishga tushdi...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if name == "main":
    asyncio.run(main())
