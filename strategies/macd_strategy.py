# macd_strategy.py (MACD 전략 완벽 구현)

import pandas as pd


class MACDStrategy:
    def __init__(self):
        pass

    def calculate_macd(self, data, short_window=12, long_window=26, signal_window=9):
        if 'close' not in data.columns:
            raise KeyError("데이터프레임에 'close' 열이 없습니다.")

        short_ema = data['close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['close'].ewm(span=long_window, adjust=False).mean()
        data['MACD'] = short_ema - long_ema
        data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
        return data

    def generate_signal(self, data):
        data = self.calculate_macd(data)
        data['signal'] = 0
        data.loc[data['MACD'] > data['Signal_Line'], 'signal'] = 1
        data.loc[data['MACD'] < data['Signal_Line'], 'signal'] = -1
        return data
