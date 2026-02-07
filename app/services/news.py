import requests
import json

class News:

    def __init__(self, ticker: str, engine: str = "google", time_period: str = "last_week"):
        self.ticker = ticker
        self.engine = engine
        self.time_period = time_period
        self.base_url = "https://www.searchapi.io/api/v1/search"

    def __get_query(self) -> str:
        return f"opinions about {self.ticker} in the market"

    def __get_organic_results(self) -> list:
        params = {
        "engine": self.engine,
        "q": self.__get_query(),
        "api_key": SEARCH_API_KEY,
        "time_period": self.time_period
        }

        response = requests.get(self.base_url, params=params)
        news = json.loads(response.text)
        organic_results = news.get("organic_results", [])
        return organic_results

    def get_report(self) -> str:
        organic_results = self.__get_organic_results()
        news_report = f"# Opiniões da Internet sobre {self.ticker} na semana\n"
        for result in organic_results:
            position = result.get("position", "Não encontrado")
            title = result.get("title", "Não encontrado")
            source = result.get("source", "Não encontrado")
            snippet = result.get("snippet", "Não encontrado")
            news_report += f"## {title} - posição {position}\n- Fonte: {source}\n- Snippet: {snippet}\n"

        news_report += "\n'posição' significa a posição nos resultados de busca"
        return news_report