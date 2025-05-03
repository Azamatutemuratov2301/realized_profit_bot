# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from mt5_utils import connect_to_mt5, disconnect_mt5, get_account_info, get_open_orders, send_order

app = FastAPI()

class MT5LoginData(BaseModel):
    login: int
    password: str
    server: str

class OrderData(BaseModel):
    symbol: str
    lot: float
    order_type: str  # "buy" or "sell"
    sl: float | None = None
    tp: float | None = None

@app.post("/login")
def login(data: MT5LoginData):
    if connect_to_mt5(data.login, data.password, data.server):
        return {"status": "success"}
    return {"status": "error"}

@app.get("/account")
def account_info():
    return get_account_info()

@app.get("/orders")
def orders():
    return get_open_orders()

@app.post("/trade")
def trade(data: OrderData):
    return send_order(data.symbol, data.lot, data.order_type, data.sl, data.tp)

@app.get("/logout")
def logout():
    disconnect_mt5()
    return {"status": "disconnected"}
