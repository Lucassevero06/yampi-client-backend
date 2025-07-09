from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

YAMPI_API_KEY = os.getenv("sk_ZjJRwhWxoUR3MVgThcapXI9WAXJNrIIl2Mlbf")  # Chave secreta da sua API
YAMPI_PRODUCT_ID = os.getenv("41410195")  # ID do produto oculto (pode ser de R$0)

@app.post("/criar-cliente")
async def criar_cliente(req: Request):
    data = await req.json()
    nome = data.get("nome")
    email = data.get("email")
    cpf = data.get("cpf")
    telefone = data.get("telefone")

    if not nome or not email or not cpf or not telefone:
        return JSONResponse({"success": False, "error": "Dados incompletos"}, status_code=400)

    headers = {
        "Authorization": f"Bearer {YAMPI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "customer": {
            "name": nome,
            "email": email,
            "cpf": cpf,
            "phone": telefone
        },
        "items": [
            {
                "product_id": int(YAMPI_PRODUCT_ID),
                "quantity": 1
            }
        ],
        "payment_method": "free"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.yampi.com.br/v1/orders", json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
    except httpx.HTTPStatusError as e:
        return JSONResponse({"success": False, "error": str(e.response.text)}, status_code=500)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)