import MetaTrader5 as mt5
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# MT5 login ma'lumotlari
LOGIN = 313652330
PASSWORD = "Azamat2301,"
SERVER = "XMGlobal-MT5 7"

# Telegram bot token
BOT_TOKEN = "8158588417:AAEVoM7CdKJztk_eJHrHvipbUkRXYfHKowA"
ADMIN_ID = 731008470  # Sizning Telegram ID

# MT5 ga ulanish
def mt5_connect():
    mt5.initialize()
    mt5.login(LOGIN, PASSWORD, SERVER)

# Savdo ochish funksiyasi
def open_trade(action: str):
    symbol = "XAUUSD"
    volume = 0.1

    mt5.symbol_select(symbol, True)
    price = mt5.symbol_info_tick(symbol).ask if action == "buy" else mt5.symbol_info_tick(symbol).bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "TelegramBotTrade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result

# Telegram komandalar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Xush kelibsiz! BUY yoki SELL yozing.")

async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Sizda ruxsat yo‘q.")
        return

    command = update.message.text.lower()
    if command == "/buy":
        mt5_connect()
        result = open_trade("buy")
        mt5.shutdown()
        await update.message.reply_text(f"✅ BUY buyruq yuborildi\nNatija: {result}")
    elif command == "/sell":
        mt5_connect()
        result = open_trade("sell")
        mt5.shutdown()
        await update.message.reply_text(f"✅ SELL buyruq yuborildi\nNatija: {result}")
    else:
        await update.message.reply_text("⚠️ Notanish buyruq.")

# Bot ishga tushurish
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", trade_command))
    app.add_handler(CommandHandler("sell", trade_command))
    app.run_polling()

if __name__ == "__main__":
    main()
