
# atr_strategy.py
# ATR (Average True Range) 기반 거래 전략

import pandas as pd

class ATRStrategy:
    def __init__(self, period=14):
        """
        ATR 전략 초기화
        period: ATR 계산 시 사용할 기간 (기본값: 14)
        """
        self.period = period

    def calculate_atr(self, data):
        """
        ATR 계산 메서드
        """
        high_low = data['High'] - data['Low']
        high_close = abs(data['High'] - data['Close'].shift(1))
        low_close = abs(data['Low'] - data['Close'].shift(1))

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(self.period).mean()
        return atr

    def generate_signal(self, data):
        """
        ATR 기반 거래 신호 생성 메서드
        """
        data['ATR'] = self.calculate_atr(data.copy())
        data['signal'] = 0
        # ATR을 기준으로 거래량이 높은 변동성을 거래 신호로 활용
        data.loc[data['ATR'] > data['ATR'].mean(), 'signal'] = 1  # 매수 신호
        data.loc[data['ATR'] < data['ATR'].mean(), 'signal'] = -1  # 매도 신호
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = ATRStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'ATR', 'signal']].tail())
