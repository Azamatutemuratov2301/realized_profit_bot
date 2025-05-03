# mt5_utils.py
import MetaTrader5 as mt5

def connect_to_mt5(login: int, password: str, server: str) -> bool:
    if not mt5.initialize(login=login, password=password, server=server):
        print("MT5 ulanishda xatolik:", mt5.last_error())
        return False
    return True

def disconnect_mt5():
    mt5.shutdown()

def get_account_info():
    return mt5.account_info()._asdict() if mt5.account_info() else None

def get_open_orders():
    orders = mt5.positions_get()
    return [order._asdict() for order in orders] if orders else []

def send_order(symbol: str, lot: float, order_type: str, sl: float = None, tp: float = None) -> dict:
    price = mt5.symbol_info_tick(symbol).ask if order_type == "buy" else mt5.symbol_info_tick(symbol).bid
    order_type_map = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type_map[order_type],
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Realized Profit Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    if sl:
        request["sl"] = sl
    if tp:
        request["tp"] = tp

    result = mt5.order_send(request)
    return result._asdict()
