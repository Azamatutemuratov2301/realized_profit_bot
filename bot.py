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
from config import LANGUAGES, DEFAULT_LANG, BOT_TOKEN, ADMIN_ID

class TradingBot:
    def init(self, lang=DEFAULT_LANG):
        self.lang = lang
        self.token = BOT_TOKEN
        self.admin_id = ADMIN_ID
    
    def set_language(self, lang_code):
        """Tilni o'zgartirish metodi"""
        if lang_code in LANGUAGES:
            self.lang = lang_code
            return self.get_text('language_changed')
        return self.get_text('invalid_language')

    def get_text(self, key, **kwargs):
        """Tilga mos matnni qaytarish"""
        text = LANGUAGES[self.lang].get(key, key)
        return text.format(**kwargs) if kwargs else text

    def show_menu(self):
        """Tilga mos menyuni ko'rsatish"""
        menu = f"""
        {self.get_text('main_menu')}
        1. {self.get_text('calculate_profit')}
        2. {self.get_text('change_language')}
        3. {self.get_text('exit')}
        """
        print(menu)

    def calculate_profit(self, entry_price, exit_price, quantity):
        """Foyda/zararni hisoblash"""
        profit = (exit_price - entry_price) * quantity
        if profit >= 0:
            return self.get_text('profit_message', amount=profit)
        return self.get_text('loss_message', amount=abs(profit))
