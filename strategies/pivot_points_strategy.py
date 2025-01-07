
# pivot_points_strategy.py
# Pivot Points (피봇 포인트) 기반 거래 전략

import pandas as pd

class PivotPointsStrategy:
    def __init__(self):
        """
        Pivot Points 전략 초기화
        """
        pass

    def calculate_pivot_points(self, data):
        """
        피봇 포인트와 저항/지지선 계산 메서드
        """
        data['PivotPoint'] = (data['High'].shift(1) + data['Low'].shift(1) + data['Close'].shift(1)) / 3
        data['Resistance1'] = (2 * data['PivotPoint']) - data['Low'].shift(1)
        data['Support1'] = (2 * data['PivotPoint']) - data['High'].shift(1)
        data['Resistance2'] = data['PivotPoint'] + (data['High'].shift(1) - data['Low'].shift(1))
        data['Support2'] = data['PivotPoint'] - (data['High'].shift(1) - data['Low'].shift(1))
        return data

    def generate_signal(self, data):
        """
        피봇 포인트 기반 거래 신호 생성 메서드
        """
        data = self.calculate_pivot_points(data.copy())
        data['signal'] = 0
        # Close가 Pivot Point를 상향 돌파하면 매수, 하향 돌파하면 매도
        data.loc[data['Close'] > data['PivotPoint'], 'signal'] = 1
        data.loc[data['Close'] < data['PivotPoint'], 'signal'] = -1
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = PivotPointsStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'PivotPoint', 'Resistance1', 'Support1', 'signal']].tail())
