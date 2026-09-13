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

@app.post("/transaction")
def create_transaction(transaction: WalletTransaction):
    return {
        "status": "success", 
        "message": f"Transação de {transaction.amount} para {transaction.name} processada com sucesso."
    }

@app.get("/")
def read_root():
    return {"status": "online", "service": "Crypto Wallet & Mercado Pago API"}
