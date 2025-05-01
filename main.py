from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Signal(BaseModel):
    symbol: str
    action: str  # BUY yoki SELL
    price: float
    sl: float
    tp: float

@app.get("/")
def root():
    return {"message": "Realized_Profit backend ishlamoqda"}

@app.post("/signal")
def receive_signal(signal: Signal):
    print(f"📡 Signal qabul qilindi: {signal}")
    return {"status": "success", "detail": f"{signal.action} signal qabul qilindi"}