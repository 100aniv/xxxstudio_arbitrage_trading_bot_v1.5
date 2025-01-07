
# adx_strategy.py
# ADX (Average Directional Index) 기반 거래 전략

import pandas as pd

class ADXStrategy:
    def __init__(self, period=14):
        """
        ADX 전략 초기화
        period: ADX 계산 시 사용할 기간 (기본값: 14)
        """
        self.period = period

    def calculate_adx(self, data):
        """
        ADX 계산 메서드
        """
        data['TR'] = pd.concat([
            data['High'] - data['Low'],
            abs(data['High'] - data['Close'].shift(1)),
            abs(data['Low'] - data['Close'].shift(1))
        ], axis=1).max(axis=1)

        data['ATR'] = data['TR'].rolling(window=self.period).mean()

        data['+DM'] = data['High'].diff()
        data['-DM'] = -data['Low'].diff()

        data['+DM'] = data['+DM'].where((data['+DM'] > data['-DM']) & (data['+DM'] > 0), 0)
        data['-DM'] = data['-DM'].where((data['-DM'] > data['+DM']) & (data['-DM'] > 0), 0)

        data['+DI'] = (data['+DM'].rolling(window=self.period).mean() / data['ATR']) * 100
        data['-DI'] = (data['-DM'].rolling(window=self.period).mean() / data['ATR']) * 100

        data['DX'] = abs(data['+DI'] - data['-DI']) / (data['+DI'] + data['-DI']) * 100
        data['ADX'] = data['DX'].rolling(window=self.period).mean()
        return data

    def generate_signal(self, data):
        """
        ADX 기반 매매 신호 생성 메서드
        """
        data = self.calculate_adx(data.copy())
        data['signal'] = 0
        data.loc[(data['ADX'] > 25) & (data['+DI'] > data['-DI']), 'signal'] = 1  # 매수 신호
        data.loc[(data['ADX'] > 25) & (data['+DI'] < data['-DI']), 'signal'] = -1  # 매도 신호
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')

    strategy = ADXStrategy()
    result = strategy.generate_signal(btc_data)
    print(result[['Close', 'ADX', 'signal']].tail())
