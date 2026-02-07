from pydantic import BaseModel, Field
from typing import Literal, List


# Criando uma classe Ticker que representa uma ação
class Ticker(BaseModel):
    ticker: str = Field(description="Ticker da ação analizada (por exemplo: AAPL)")

class AnalyzeSchema(BaseModel):
    ticker: str
    action: Literal['HOLD', 'BUY', 'SELL'] = Field(description="Ação a ser tomada: HOLD, BUY ou SELL")
    confidence: float = Field(ge = 0, le = 1, description = "Float entre 0 e 1 com a confiança da recomendação da ação a ser tomada")
    reasoning: str = Field(description = "sua explicação técnica para o contratante do porquê sugeriu aquela ação")
    risks: List[str] = Field(description = "lista de strings com os riscos associados a ação a ser tomada com links de notícias que fortalecem o argumento")
    opportunities: List[str] = Field(description = "lista de strings com as oportunidades associadas a ação a ser tomada com links de notícias que fortalecem o argumento")