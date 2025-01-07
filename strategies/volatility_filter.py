
# volatility_filter.py
# 변동성 기반 데이터 필터링 전략

import pandas as pd
import numpy as np

class VolatilityFilter:
    def __init__(self, threshold=0.02):
        """
        변동성 기반 필터 초기화
        :param threshold: 필터링 기준 변동성 임계값 (기본값: 2%)
        """
        self.threshold = threshold

    def calculate_volatility(self, data):
        """
        변동성을 계산하는 메서드 (표준 편차 기반)
        """
        data['returns'] = data['Close'].pct_change()
        data['volatility'] = data['returns'].rolling(window=10).std()
        return data

    def filter_data(self, data):
        """
        변동성이 기준 임계값 이상인 데이터만 유지
        """
        data = self.calculate_volatility(data)
        filtered_data = data[data['volatility'] > self.threshold]
        return filtered_data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='6mo', interval='1d')

    filter_strategy = VolatilityFilter(threshold=0.02)
    filtered_data = filter_strategy.filter_data(btc_data)
    print(f"Filtered {len(filtered_data)} rows from {len(btc_data)} total rows.")
    print(filtered_data[['Close', 'volatility']].tail())
