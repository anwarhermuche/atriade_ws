from typing import List
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from app.ai.prompts.system_prompt import SYSTEM_PROMPT
from app.ai.prompts.human_prompt import HUMAN_PROMPT
from app.services.finance import Finance
from app.services.news import News
from app.ai.structured_outputs.stocks_analyze_response import StocksAnalyzeResponse
from app.core.settings import settings

from langchain_openai import ChatOpenAI

class OpenAI:

    def __init__(self, ticker: str, model: str = "gpt-5.1", temperature: float = 0.2):
        self.ticker = ticker
        self.model = model
        self.temperature = temperature

    def __get_messages(self) -> List[AnyMessage]:
        finance = Finance(ticker=self.ticker)
        news = News(ticker=self.ticker)

        stocks_report = finance.get_report()
        news_report = news.get_report()

        new_system_prompt = SYSTEM_PROMPT.replace("{TICKER}", self.ticker)
        new_human_prompt = HUMAN_PROMPT.replace("{stocks_report}", stocks_report).replace("{news_report}", news_report)
        return [
            SystemMessage(content = new_system_prompt),
            HumanMessage(content = new_human_prompt)
        ]

    def get_reponse(self) -> StocksAnalyzeResponse:
        model = ChatOpenAI(model = self.model, temperature = self.temperature, api_key = settings.OPENAI_API_KEY)
        model_structured = model.with_structured_output(StocksAnalyzeResponse)

        return model_structured.invoke(self.__get_messages())