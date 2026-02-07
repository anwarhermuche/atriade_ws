from fastapi import FastAPI


app = FastAPI()

@app.get("/ola")
def retorna_ola():
    return {"mensagem": "olá!"}