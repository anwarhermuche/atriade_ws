from fastapi import APIRouter
from app.services.openai import OpenAI
from app.schemas.stocks import Ticker, AnalyzeSchema

router = APIRouter(prefix = "/api/v1/stocks", tags = ["stocks"])

@router.post("/analyze", response_model = AnalyzeSchema)
def analyze(ticker: Ticker):
    openai = OpenAI(ticker=ticker.ticker)
    return AnalyzeSchema(**openai.get_reponse().model_dump())