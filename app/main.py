from fastapi import FastAPI
from app.api.v1.stocks import router as stocks_router


app = FastAPI(title = "API de Análise de Ações",
              description="Faz ETL das ações e análise com IA")

app.include_router(stocks_router)

@app.get("/ola")
def retorna_ola():
    return {"mensagem": "olá!"}