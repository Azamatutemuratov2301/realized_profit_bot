from fastapi import FastAPI
from pydantic import BaseModel
from mt5_utils import open_trade

app = FastAPI()

class TradeRequest(BaseModel):
    symbol: str
    lot: float
    order_type: str

@app.post("/trade")
def trade(request: TradeRequest):
    result = open_trade(request.symbol, request.lot, request.order_type)
    return result
