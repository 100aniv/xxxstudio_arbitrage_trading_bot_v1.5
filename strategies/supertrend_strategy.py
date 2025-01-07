
# supertrend_strategy.py
# SuperTrend 지표를 기반으로 거래 신호를 생성하는 전략입니다.

import pandas as pd

class SuperTrendStrategy:
    def __init__(self, atr_period=10, multiplier=3):
        """
        SuperTrend 전략 초기화
        atr_period: ATR 계산에 사용할 기간 (기본: 10)
        multiplier: ATR에 곱할 배수 (기본: 3)
        """
        self.atr_period = atr_period
        self.multiplier = multiplier

    def calculate_atr(self, data):
        """
        ATR (Average True Range) 계산 메서드
        """
        high_low = data['High'] - data['Low']
        high_close = abs(data['High'] - data['Close'].shift(1))
        low_close = abs(data['Low'] - data['Close'].shift(1))

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(self.atr_period).mean()
        return atr

    def generate_signal(self, data):
        """
        SuperTrend 기반의 거래 신호 생성 메서드
        """
        data = data.copy()
        data['ATR'] = self.calculate_atr(data)

        # 기본 SuperTrend 계산
        data['UpperBand'] = (data['High'] + data['Low']) / 2 + (self.multiplier * data['ATR'])
        data['LowerBand'] = (data['High'] + data['Low']) / 2 - (self.multiplier * data['ATR'])

        # SuperTrend 라인 계산
        data['SuperTrend'] = data['LowerBand']
        for i in range(1, len(data)):
            if data['Close'].iloc[i] > data['SuperTrend'].iloc[i-1]:
                data['SuperTrend'].iloc[i] = max(data['LowerBand'].iloc[i], data['SuperTrend'].iloc[i-1])
            else:
                data['SuperTrend'].iloc[i] = min(data['UpperBand'].iloc[i], data['SuperTrend'].iloc[i-1])

        # 매매 신호 생성
        data['signal'] = 0
        data.loc[data['Close'] > data['SuperTrend'], 'signal'] = 1  # 매수 신호
        data.loc[data['Close'] < data['SuperTrend'], 'signal'] = -1  # 매도 신호

        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = SuperTrendStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'SuperTrend', 'signal']].tail())
