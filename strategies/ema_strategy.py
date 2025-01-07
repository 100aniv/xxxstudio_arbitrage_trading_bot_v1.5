# ema_strategy.py (EMA 전략 완벽 구현)

import pandas as pd

class EMAStrategy:
    def __init__(self):
        pass

    def calculate_ema(self, data, period=14):
        if 'close' not in data.columns:
            raise KeyError("데이터프레임에 'close' 열이 없습니다.")

        data['EMA'] = data['close'].ewm(span=period, adjust=False).mean()
        return data

    def generate_signal(self, data):
        data = self.calculate_ema(data)
        data['signal'] = 0
        data.loc[data['close'] > data['EMA'], 'signal'] = 1
        data.loc[data['close'] < data['EMA'], 'signal'] = -1
        return data
