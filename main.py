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
