# main.py
import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI(title="Carteira Cripto")

# Configuração do MongoDB Atlas com suas credenciais reais
MONGO_URI = (
    "mongodb+srv://grbWr4hMxImw2Q8j@crypto.huibgar.mongodb.net/?appName=crypto"
)
client = MongoClient(MONGO_URI)
db = client["carteira_cripto"]
transactions_collection = db["transactions"]

# Seu Access Token oficial gerado no painel do Mercado Pago
MP_ACCESS_TOKEN = "APP_USR-4af4c377-1955-41dd-bd59-187eb1640f87"
MP_API_URL = "https://api.mercadopago.com/v1/payments"


class DepositRequest(BaseModel):
  transaction_amount: float
  email: str


@app.post("/api/deposit/pix")
async def create_pix_deposit(data: DepositRequest):
  headers = {
      "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
      "Content-Type": "application/json",
  }

  payload = {
      "transaction_amount": data.transaction_amount,
      "description": "Deposito Carteira Cripto",
      "payment_method_id": "pix",
      "payer": {"email": data.email},
  }

  async with httpx.AsyncClient() as client_http:
    response = await client_http.post(
        MP_API_URL, json=payload, headers=headers
    )

    if response.status_code not in [200, 201]:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=(
              "Erro ao gerar pagamento PIX no Mercado Pago:"
              f" {response.text}"
          ),
      )

    payment_data = response.json()

    # Extraindo dados úteis para o pagamento via PIX
    point_of_interaction = payment_data.get("point_of_interaction", {})
    transaction_data = point_of_interaction.get("transaction_data", {})

    qr_code_base64 = transaction_data.get("qr_code_base64")
    qr_code = transaction_data.get("qr_code")
    ticket_url = transaction_data.get("ticket_url")

    # Salvando a transação no MongoDB
    transaction_doc = {
        "payment_id": payment_data.get("id"),
        "status": payment_data.get("status"),
        "transaction_amount": data.transaction_amount,
        "payer_email": data.email,
        "qr_code": qr_code,
    }
    transactions_collection.insert_one(transaction_doc)

    return {
        "status": "success",
        "payment_id": payment_data.get("id"),
        "payment_status": payment_data.get("status"),
        "qr_code_base64": qr_code_base64,
        "qr_code_copia_e_cola": qr_code,
        "ticket_url": ticket_url,
    }