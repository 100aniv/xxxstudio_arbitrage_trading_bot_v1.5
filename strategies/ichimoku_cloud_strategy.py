
# ichimoku_cloud_strategy.py
# Ichimoku Cloud (일목균형표) 기반 거래 전략

import pandas as pd

class IchimokuCloudStrategy:
    def __init__(self):
        """
        Ichimoku Cloud 전략 초기화
        """
        self.conversion_line_period = 9
        self.base_line_period = 26
        self.leading_span_b_period = 52

    def calculate_ichimoku_cloud(self, data):
        """
        일목균형표 계산 메서드
        """
        data['ConversionLine'] = (data['High'].rolling(window=self.conversion_line_period).max() +
                                  data['Low'].rolling(window=self.conversion_line_period).min()) / 2

        data['BaseLine'] = (data['High'].rolling(window=self.base_line_period).max() +
                            data['Low'].rolling(window=self.base_line_period).min()) / 2

        data['LeadingSpanA'] = ((data['ConversionLine'] + data['BaseLine']) / 2).shift(self.base_line_period)
        data['LeadingSpanB'] = ((data['High'].rolling(window=self.leading_span_b_period).max() +
                                 data['Low'].rolling(window=self.leading_span_b_period).min()) / 2).shift(self.base_line_period)
        return data

    def generate_signal(self, data):
        """
        일목균형표 기반 거래 신호 생성 메서드
        """
        data = self.calculate_ichimoku_cloud(data.copy())
        data['signal'] = 0
        # Conversion Line이 Base Line을 상향 돌파할 경우 매수 신호
        data.loc[data['ConversionLine'] > data['BaseLine'], 'signal'] = 1
        # Conversion Line이 Base Line을 하향 돌파할 경우 매도 신호
        data.loc[data['ConversionLine'] < data['BaseLine'], 'signal'] = -1
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = IchimokuCloudStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'ConversionLine', 'BaseLine', 'LeadingSpanA', 'LeadingSpanB', 'signal']].tail())
