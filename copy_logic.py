import time
import logging
import MetaTrader5 as mt5

class CopyLogic:
    def __init__(self, connector):
        self.connector = connector
        self.prev_tickets = set()
        self.prev_positions = []

    def run(self):
        while True:
            # Master akkauntga ulang va pozitsiyalarni oling
            self.connector.master.connect()
            positions = mt5.positions_get()

            # Agar positions None qaytarsa, qaytadan urinib ko'rish
            if positions is None:
                logging.error("MT5.positions_get() returned None, retrying in 1s...")
                time.sleep(1)
                continue

            current_tickets = set(pos.ticket for pos in positions)

            # Yangi ochilgan pozitsiyalarni aniqlash
            new_tickets = current_tickets - self.prev_tickets
            for pos in positions:
                if pos.ticket in new_tickets:
                    self.open_for_slaves(pos)

            # Yopilgan pozitsiyalarni aniqlash
            closed_tickets = self.prev_tickets - current_tickets
            for ticket in closed_tickets:
                closed_pos = next((p for p in self.prev_positions if p.ticket == ticket), None)
                if closed_pos:
                    self.close_for_slaves(closed_pos)

            # Holatni yangilash
            self.prev_tickets = current_tickets
            self.prev_positions = positions

            time.sleep(1)

    def open_for_slaves(self, pos):
        for slave in self.connector.slaves:
            # Slave akkauntga ulanib, buyurtma jo'natish
            mt5.initialize(slave.path, login=slave.login, password=slave.password, server=slave.server)
            order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": pos.type,
                "price": pos.price_open,
                "deviation": 10,
                "magic": 123456,
                "comment": f"Copy open {pos.ticket}",
                "type_filling": mt5.ORDER_FILLING_IOC,
                "type_time": mt5.ORDER_TIME_GTC,
            }
            result = mt5.order_send(order)
            logging.info(f"Opened for slave {slave.login}: ticket {pos.ticket}, result {result}")

    def close_for_slaves(self, pos):
        for slave in self.connector.slaves:
            # Slave akkauntga ulanib, yopish buyurtmasi jo'natish
            mt5.initialize(slave.path, login=slave.login, password=slave.password, server=slave.server)
            order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = (
                mt5.symbol_info_tick(pos.symbol).bid
                if order_type == mt5.ORDER_TYPE_SELL
                else mt5.symbol_info_tick(pos.symbol).ask
            )
            order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 10,
                "magic": 123456,
                "comment": f"Copy close {pos.ticket}",
                "type_filling": mt5.ORDER_FILLING_IOC,
                "type_time": mt5.ORDER_TIME_GTC,
            }
            result = mt5.order_send(order)
            logging.info(f"Closed for slave {slave.login}: ticket {pos.ticket}, result {result}")
