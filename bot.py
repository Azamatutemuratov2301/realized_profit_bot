import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, LANGUAGES, DEFAULT_LANG

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Realized_Profit botiga xush kelibsiz.")

# /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yordam: Buyruqlar ro‘yxati:\n/start - Boshlash\n/help - Yordam")

# Til funksiyalariga oid class
class TradingBot:
    def __init__(self, lang=DEFAULT_LANG):
        self.lang = lang
        self.token = BOT_TOKEN
        self.admin_id = ADMIN_ID
    
    def set_language(self, lang_code):
        if lang_code in LANGUAGES:
            self.lang = lang_code
            return self.get_text('language_changed')
        return self.get_text('invalid_language')

    def get_text(self, key, **kwargs):
        text = LANGUAGES[self.lang].get(key, key)
        return text.format(**kwargs) if kwargs else text

    def show_menu(self):
        menu = f"""
        {self.get_text('main_menu')}
        1. {self.get_text('calculate_profit')}
        2. {self.get_text('change_language')}
        3. {self.get_text('exit')}
        """
        print(menu)

    def calculate_profit(self, entry_price, exit_price, quantity):
        profit = (exit_price - entry_price) * quantity
        if profit >= 0:
            return self.get_text('profit_message', amount=profit)
        return self.get_text('loss_message', amount=abs(profit))

# Botni ishga tushirish
async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    # Yana boshqa komandalarni shu yerda qo‘shing

    print("Bot ishga tushdi...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
