import MetaTrader5 as mt5

LOGIN = 99026423
PASSWORD = "Azamat2301,"
SERVER = "XMGlobal-MT5 5"

def connect_mt5():
    if not mt5.initialize(login=LOGIN, password=PASSWORD, server=SERVER):
        raise Exception("MT5 ulanishda xatolik:", mt5.last_error())

def open_trade(symbol: str, lot: float, order_type: str):
    connect_mt5()
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return {"error": "Symbol not found"}

    mt5.symbol_select(symbol, True)

    order_type_code = mt5.ORDER_TYPE_BUY if order_type.lower() == "buy" else mt5.ORDER_TYPE_SELL

    price = symbol_info.ask if order_type.lower() == "buy" else symbol_info.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type_code,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Telegram Copy Trading",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result._asdict()
