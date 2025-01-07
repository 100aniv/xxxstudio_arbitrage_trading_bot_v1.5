# rsi_strategy.py (RSI 전략 완벽 구현)

import pandas as pd

class RSIStrategy:
    def __init__(self):
        pass

    def calculate_rsi(self, data, period=14):
        if 'close' not in data.columns:
            raise KeyError("데이터프레임에 'close' 열이 없습니다.")

        delta = data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        data['RSI'] = rsi
        return data

    def generate_signal(self, data):
        data = self.calculate_rsi(data)
        data['signal'] = 0
        data.loc[data['RSI'] > 70, 'signal'] = -1
        data.loc[data['RSI'] < 30, 'signal'] = 1
        return data
