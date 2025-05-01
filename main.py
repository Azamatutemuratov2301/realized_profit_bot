from fastapi import FastAPI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_HERE")

app = FastAPI()
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.on_event("startup")
async def startup_event():
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [["O'zbek", "Русский"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Tilni tanlang / Выберите язык:", reply_markup=reply_markup)

    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    from fastapi import FastAPI
from bot import run_bot

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    run_bot()
