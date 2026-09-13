from pydantic import BaseModel, Field
from typing import Dict

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class WalletBalance(BaseModel):
    user_id: str
    balances: Dict[str, float] = Field(default_factory=lambda: {"BRL": 0.0, "USDT": 0.0, "BTC": 0.0})

class PixTransaction(BaseModel):
    user_id: str
    amount_brl: float
    pix_key: str
    pix_key_type: str

class CryptoSwap(BaseModel):
    user_id: str
    from_currency: str
    to_currency: str
    amount: float