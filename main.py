from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

class WalletTransaction(BaseModel):
    name: str = Field(..., description="Nome do usuário ou identificação")
    amount: float = Field(..., gt=0, description="Valor da transação")
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('O valor deve ser maior que zero')
        return v

class CurrencyExchange(BaseModel):
    user_id: str = Field(..., description="Identificação do usuário")
    from_currency: str = Field(..., description="Moeda de origem (ex: BRL, BTC, ETH)")
    to_currency: str = Field(..., description="Moeda de destino (ex: BRL, BTC, ETH)")
    amount: float = Field(..., gt=0, description="Quantidade a ser negociada")

@app.post("/transaction")
def create_transaction(transaction: WalletTransaction):
    return {
        "status": "success", 
        "message": f"Transação de {transaction.amount} para {transaction.name} processada com sucesso."
    }

@app.post("/exchange")
def exchange_currency(exchange: CurrencyExchange):
    # Simulação de taxa de câmbio para teste na API
    mock_rates = {
        "BTC_BRL": 350000.0,
        "ETH_BRL": 18000.0,
        "BRL_BTC": 1 / 350000.0,
        "BRL_ETH": 1 / 18000.0
    }
    
    pair = f"{exchange.from_currency}_{exchange.to_currency}"
    
    if exchange.from_currency == exchange.to_currency:
        raise HTTPException(status_code=400, detail="A moeda de origem e destino não podem ser iguais.")
    
    # Se for conversão direta simulada
    rate = mock_rates.get(pair, 1.0)
    converted_amount = exchange.amount * rate
    
    return {
        "status": "success",
        "user_id": exchange.user_id,
        "from": {
            "currency": exchange.from_currency,
            "amount": exchange.amount
        },
        "to": {
            "currency": exchange.to_currency,
            "amount": converted_amount
        },
        "rate_applied": rate,
        "message": f"Negociação de {exchange.amount} {exchange.from_currency} para {exchange.to_currency} realizada com sucesso."
    }

@app.get("/")
def read_root():
    return {"status": "online", "service": "Crypto Wallet & Mercado Pago API"}
