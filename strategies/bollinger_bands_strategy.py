
# bollinger_bands_strategy.py
# Bollinger Bands (볼린저 밴드) 기반 거래 전략

import pandas as pd

class BollingerBandsStrategy:
    def __init__(self, period=20, std_dev=2):
        """
        Bollinger Bands 전략 초기화
        period: 이동 평균 계산에 사용할 기간 (기본값: 20)
        std_dev: 표준 편차 기준선 (기본값: 2)
        """
        self.period = period
        self.std_dev = std_dev

    def calculate_bollinger_bands(self, data):
        """
        Bollinger Bands 계산 메서드
        """
        data['SMA'] = data['Close'].rolling(window=self.period).mean()
        data['STD'] = data['Close'].rolling(window=self.period).std()
        data['UpperBand'] = data['SMA'] + (data['STD'] * self.std_dev)
        data['LowerBand'] = data['SMA'] - (data['STD'] * self.std_dev)
        return data

    def generate_signal(self, data):
        """
        Bollinger Bands 기반 거래 신호 생성 메서드
        """
        data = self.calculate_bollinger_bands(data.copy())
        data['signal'] = 0
        # Close가 UpperBand를 초과하면 매도 신호, LowerBand를 하향 돌파하면 매수 신호
        data.loc[data['Close'] > data['UpperBand'], 'signal'] = -1
        data.loc[data['Close'] < data['LowerBand'], 'signal'] = 1
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = BollingerBandsStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'SMA', 'UpperBand', 'LowerBand', 'signal']].tail())
