import MetaTrader5 as mt5
from config import MASTER_LOGIN, MASTER_PASSWORD, MASTER_SERVER

def connect_master():
    if not mt5.initialize(login=MASTER_LOGIN, password=MASTER_PASSWORD, server=MASTER_SERVER):
        raise Exception(f"Failed to connect to master account: {mt5.last_error()}")
    print("Master account connected.")
