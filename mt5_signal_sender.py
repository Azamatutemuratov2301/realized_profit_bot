import MetaTrader5 as mt5
import requests
import time

API_URL = "https://realized-profit-bot.onrender.com/signal"
SYMBOL = "XAUUSD"
TIMEFRAME = mt5.TIMEFRAME_M1

if not mt5.initialize():
    print("MT5 ulanmadi:", mt5.last_error())
    quit()

def send_signal(action, price, sl, tp):
    data = {
        "symbol": SYMBOL,
        "action": action,
        "price": price,
        "sl": sl,
        "tp": tp
    }
    try:
        response = requests.post(API_URL, json=data)
        print("✅ Signal yuborildi:", response.status_code, response.text)
    except Exception as e:
        print("❌ Yuborishda xatolik:", e)

def check_for_signal():
    rates = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, 3)
    if rates is None or len(rates) < 3:
        print("Tarix olinmadi.")
        return

    open1 = rates[1]['open']
    close1 = rates[1]['close']

    open2 = rates[2]['open']
    close2 = rates[2]['close']

    if close1 > open1 and close2 > open2:
        price = mt5.symbol_info_tick(SYMBOL).ask
        send_signal("BUY", price, price - 2.0, price + 2.0)

    elif close1 < open1 and close2 < open2:
        price = mt5.symbol_info_tick(SYMBOL).bid
        send_signal("SELL", price, price + 2.0, price - 2.0)

while True:
    check_for_signal()
    time.sleep(60)