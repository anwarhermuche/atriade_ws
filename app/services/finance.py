import pandas as pd
import yfinance as yf

class Finance:

    def __init__(self, ticker: str, period: str = "1y", interval: str = "1d"):
        self.ticker = ticker
        self.period = period
        self.interval = interval

    def __get_history(self) -> pd.DataFrame:
        return yf.Ticker(ticker = self.ticker).history(period=self.period, interval=self.interval)

    def __calc_statistics(self) -> dict:
        df = self.__get_history()

        # Estatísticas padrão
        df['Return'] = df['Close'].pct_change()
        df['Diff'] = df['Close'].diff()
        avg_return = df['Return'].mean()
        median_return = df['Return'].median()
        volatility = df['Return'].std()
        max_price = df['Close'].max()
        min_price = df['Close'].min()
        cumulative_returns_series = (1 + df['Return'].dropna()).cumprod()
        total_cumulative_return = (cumulative_returns_series.iloc[-1] - 1) if not cumulative_returns_series.empty else 0

        # RSI
        df['Gain'] = df['Diff'].apply(lambda x: x if x > 0 else 0)
        df['Loss'] = df['Diff'].apply(lambda x: abs(x) if x < 0 else 0)
        rsi_period = 14
        avg_gain = df['Gain'].ewm(span=rsi_period, adjust=False).mean()
        avg_loss = df['Loss'].ewm(span=rsi_period, adjust=False).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        last_rsi = df['RSI'].iloc[-1]

        return {
            "avg_return": avg_return,
            "median_return": median_return,
            "volatility": volatility,
            "max_price": max_price,
            "min_price": min_price,
            "total_cumulative_return": total_cumulative_return,
            "last_rsi": last_rsi
        }

    def get_report(self) -> str:
        stock_statistcs = self.__calc_statistics()
        return f"""
        # Estatísticas da Ação {self.ticker} (Período analisado: {self.period} | Granularidade dos dados: {self.interval})
        Retorno médio diário: {stock_statistcs.get('avg_return'):.4f}
        Mediana do retorno diário: {stock_statistcs.get('median_return'):.4f}
        Volatilidade diária (desvio padrão dos retornos): {stock_statistcs.get('volatility'):.4f}
        Preço Máximo de Fechamento: {stock_statistcs.get('max_price'):.2f}
        Preço Mínimo de Fechamento: {stock_statistcs.get('min_price'):.2f}
        Retorno Cumulativo Total (período): {stock_statistcs.get('total_cumulative_return'):.4f}
        Último RSI: {stock_statistcs.get('last_rsi'):.4f}
        """