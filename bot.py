from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if str(user_id) == str(ADMIN_ID):
        await update.message.reply_text("Assalomu alaykum, admin! Bot ishga tushdi.")
    else:
        await update.message.reply_text("Assalomu alaykum! Sizda to‘liq ruxsat yo‘q.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("✅ Bot ishga tushdi...")
app.run_polling()
