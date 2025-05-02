from config import LANGUAGES, DEFAULT_LANG, BOT_TOKEN, ADMIN_ID

class TradingBot:
    def init(self, lang=DEFAULT_LANG):
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

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import LANGUAGES, DEFAULT_LANG, ADMIN_ID

# User tillarini saqlash uchun oddiy xotira (hozircha)
user_languages = {}

def get_lang(user_id):
    return user_languages.get(user_id, DEFAULT_LANG)

def get_text(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = LANGUAGES.get(lang, LANGUAGES[DEFAULT_LANG]).get(key, "")
    return text.format(**kwargs)

def get_main_keyboard(user_id):
    lang = get_lang(user_id)
    texts = LANGUAGES[lang]
    keyboard = [
        [texts['calculate_profit']],
        [texts['change_language']],
        [texts['exit']]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_languages[user_id] = DEFAULT_LANG
    welcome = get_text(user_id, "welcome")
    menu = get_text(user_id, "main_menu")
    keyboard = get_main_keyboard(user_id)
    await update.message.reply_text(f"{welcome}\n\n{menu}", reply_markup=keyboard)

async def change_language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    buttons = [["uz", "en", "ru", "kz"]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    lang_text = get_text(user_id, "change_language")
    await update.message.reply_text(lang_text, reply_markup=keyboard)

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang_code = update.message.text.lower()
    if lang_code in LANGUAGES:
        user_languages[user_id] = lang_code
        msg = get_text(user_id, "language_changed")
    else:
        msg = get_text(user_id, "invalid_language")
    menu = get_text(user_id, "main_menu")
    keyboard = get_main_keyboard(user_id)
    await update.message.reply_text(f"{msg}\n\n{menu}", reply_markup=keyboard)

async def calculate_profit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prompt = get_text(user_id, "enter_prices")
    await update.message.reply_text(prompt)

async def handle_price_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        prices = list(map(float, update.message.text.split()))
        if len(prices) != 2:
            raise ValueError
        entry, exit = prices
        profit = round((exit - entry), 2)
        if profit >= 0:
            msg = get_text(user_id, "profit_message", amount=profit)
        else:
            msg = get_text(user_id, "loss_message", amount=abs(profit))
    except ValueError:
        msg = get_text(user_id, "enter_prices")
    await update.message.reply_text(msg)
