from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_ID

# Signal yuborish komandasi
async def send_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_ID):
        await update.message.reply_text("Sizda signal yuborish huquqi yo‘q.")
        return

    if not context.args:
        await update.message.reply_text("Iltimos, yuboriladigan signal matnini yozing.")
        return

    signal_text = " ".join(context.args)
    
    # Tugma (optional)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Realized Profit", url="https://t.me/Realized_Profit")],
    ])

    # Barcha obunachilarga yuborish
    for user_id in context.bot_data.get("users", []):
        try:
            await context.bot.send_message(chat_id=user_id, text=signal_text, reply_markup=keyboard)
        except:
            pass

    await update.message.reply_text("Signal muvaffaqiyatli yuborildi!")
