import MetaTrader5 as mt5

def get_master_positions():
    positions = mt5.positions_get()
    return positions if positions else []

def copy_positions_to_slave(slave_login, slave_password, slave_server):
    if not mt5.initialize(login=slave_login, password=slave_password, server=slave_server):
        print("Failed to connect to slave.")
        return

    for pos in get_master_positions():
        symbol = pos.symbol
        volume = pos.volume
        order_type = mt5.ORDER_TYPE_BUY if pos.type == 0 else mt5.ORDER_TYPE_SELL

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid,
            "deviation": 20,
            "magic": 234000,
            "comment": "Copy trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        mt5.order_send(request)

    mt5.shutdown()
