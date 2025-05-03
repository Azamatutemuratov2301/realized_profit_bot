from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
from master_trader import connect_master
from copy_trader import copy_positions_to_slave

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Copy trading bot ishga tushdi.")

async def copy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("Foydalanish: /copy login password server")
        return
    login = int(context.args[0])
    password = context.args[1]
    server = context.args[2]
    try:
        copy_positions_to_slave(login, password, server)
        await update.message.reply_text("Pozitsiyalar muvaffaqiyatli ko'chirildi.")
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

if __name__ == "__main__":
    connect_master()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("copy", copy))
    app.run_polling()
