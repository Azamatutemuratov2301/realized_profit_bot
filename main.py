# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Realized Profit bot is working"}
main.py
import asyncio from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes from config import BOT_TOKEN from handlers.signal import send_signal from bot_logic import TradingBot
bot_instance = TradingBot()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(bot_instance.get_text('welcome'))
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Yordam: Buyruqlar ro‘yxati:\n/start - Boshlash\n/help - Yordam")
async def start_bot(): app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("help", help_command)) app.add_handler(CommandHandler("signal", send_signal)) print("Bot ishga tushdi...") await app.initialize() await app.start() await app.updater.start_polling() await app.updater.idle()
if name == "main": asyncio.run(start_bot())
