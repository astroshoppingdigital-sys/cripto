from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mercadopago
import os

app = FastAPI()

# Inicialize o SDK do Mercado Pago com seu token de acesso
# (Você pode configurar a variável de ambiente MERCADOPAGO_ACCESS_TOKEN no Render)
access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "SEU_ACCESS_TOKEN_AQUI")
sdk = mercadopago.SDK(access_token)

class PixPaymentRequest(BaseModel):
    transaction_amount: float
    description: str
    payer_email: str

@app.get("/")
def read_root():
    return {"status": "API Crypto Wallet & PIX online!"}

@app.post("/criar-pagamento-pix")
def criar_pagamento_pix(payment: PixPaymentRequest):
    try:
        payment_data = {
            "transaction_amount": payment.transaction_amount,
            "description": payment.description,
            "payment_method_id": "pix",
            "payer": {
                "email": payment.payer_email
            }
        }

        result = sdk.payment().create(payment_data)
        payment_response = result["response"]
        
        # Retorna os dados essenciais para o cliente pagar via PIX (QR Code e Copia e Cola)
        point_of_interaction = payment_response.get("point_of_interaction", {})
        qr_data = point_of_interaction.get("transaction_data", {})

        return {
            "status": payment_response.get("status"),
            "payment_id": payment_response.get("id"),
            "qr_code": qr_data.get("qr_code"),
            "qr_code_base64": qr_data.get("qr_code_base64"),
            "ticket_url": qr_data.get("ticket_url")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
