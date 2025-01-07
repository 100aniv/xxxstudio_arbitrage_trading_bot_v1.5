
# vwap_strategy.py
# VWAP (Volume Weighted Average Price) 기반 거래 전략

import pandas as pd

class VWAPStrategy:
    def __init__(self):
        """
        VWAP 전략 초기화
        """
        pass

    def calculate_vwap(self, data):
        """
        VWAP 계산 메서드
        """
        data['Cumulative Volume'] = data['Volume'].cumsum()
        data['Cumulative Price Volume'] = (data['Close'] * data['Volume']).cumsum()
        data['VWAP'] = data['Cumulative Price Volume'] / data['Cumulative Volume']
        return data

    def generate_signal(self, data):
        """
        VWAP 기반 거래 신호 생성 메서드
        """
        data = self.calculate_vwap(data.copy())
        data['signal'] = 0
        # 가격이 VWAP을 상향 돌파하면 매수, 하향 돌파하면 매도
        data.loc[data['Close'] > data['VWAP'], 'signal'] = 1
        data.loc[data['Close'] < data['VWAP'], 'signal'] = -1
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = VWAPStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'VWAP', 'signal']].tail())
