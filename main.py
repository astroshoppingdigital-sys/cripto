import json
import urllib.request
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Crypto Wallet & Real Trading API",
    description="API de carteira de criptomoedas com cotações reais de mercado.",
    version="1.2.1"
)

# Modelos de Dados (Pydantic v2)
class WalletTransaction(BaseModel):
    name: str = Field(..., description="Nome do usuário ou identificação")
    amount: float = Field(..., gt=0, description="Valor da transação")
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('O valor deve ser maior que zero')
        return v

class TradeOrder(BaseModel):
    user_id: str
    crypto_id: str = Field(..., description="ID da criptomoeda, ex: 'bitcoin', 'ethereum'")
    fiat_currency: str = Field(default="brl", description="Moeda fiduciária, ex: 'brl', 'usd'")
    side: str = Field(..., description="Tipo de ordem: 'buy' ou 'sell'")
    amount_fiat: float = Field(..., gt=0, description="Valor em dinheiro (ex: R$ 5,00)")

# Rotas da API
@app.get("/")
def read_root():
    return {
        "status": "online", 
        "service": "Crypto Wallet Real Engine",
        "ready_for": "Integração de cotações reais e Pix."
    }

@app.get("/market/price/{crypto_id}")
def get_real_market_price(crypto_id: str, fiat: str = "brl"):
    """
    Busca o preço real e atualizado usando bibliotecas nativas do Python.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={fiat}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if crypto_id not in data:
                raise HTTPException(status_code=404, detail="Criptomoeda não encontrada na base de dados global.")
                
            current_price = data[crypto_id][fiat.lower()]
            return {
                "status": "success",
                "crypto": crypto_id,
                "currency": fiat.upper(),
                "market_price": current_price
            }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao conectar com a fonte de dados: {str(e)}")

@app.post("/trade/real-execute")
def execute_real_trade(order: TradeOrder):
    """
    Executa a simulação real com cotação obtida via API pública.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={order.crypto_id}&vs_currencies={order.fiat_currency}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if order.crypto_id not in data:
                raise HTTPException(status_code=404, detail="Ativo digital não localizado.")
                
            price = data[order.crypto_id][order.fiat_currency.lower()]
            crypto_amount = order.amount_fiat / price if order.side.lower() == 'buy' else 0.0
            
            return {
                "status": "success_prepared",
                "user_id": order.user_id,
                "operation": order.side.upper(),
                "fiat_invested": order.amount_fiat,
                "currency": order.fiat_currency.upper(),
                "asset": order.crypto_id,
                "execution_price_real": price,
                "crypto_acquired": crypto_amount,
                "message": f"Ordem real processada com preço de mercado de R$ {price:.2f}."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transaction")
def create_transaction(transaction: WalletTransaction):
    return {
        "status": "success", 
        "message": f"Transação de {transaction.amount} processada."
    }
