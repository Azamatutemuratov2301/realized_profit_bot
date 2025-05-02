import MetaTrader5 as mt5
import time
import requests

BOT_TOKEN = "8158588417:AAEVoM7CdKJztk_eJHrHvipbUkRXYfHKowA"
CHAT_ID = "-100"  # Yoki sizning Telegram guruh ID (agar guruhga yuborilsa)
SYMBOL = "XAUUSD"  # Faqat GOLD

def get_last_trade():
    positions = mt5.positions_get(symbol=SYMBOL)
    if positions:
        pos = positions[0]
        order_type = "BUY" if pos.type == 0 else "SELL"
        price = pos.price_open
        volume = pos.volume
        return f"{order_type} opened on {SYMBOL} @ {price}, volume: {volume}"
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.ok

if not mt5.initialize():
    print("MetaTrader5 initialize error:", mt5.last_error())
    quit()

print("Monitoring trades... Press CTRL+C to stop.")

last_message = ""
try:
    while True:
        trade_info = get_last_trade()
        if trade_info and trade_info != last_message:
            send_telegram_message(f"📢 New Trade Signal:\n{trade_info}")
            last_message = trade_info
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopped monitoring.")
finally:
    mt5.shutdown()
