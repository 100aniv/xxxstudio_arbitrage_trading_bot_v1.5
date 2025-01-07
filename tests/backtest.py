
# backtest.py
# 이 모듈은 RSI 기반의 백테스팅을 수행하는 데 사용됩니다.

import pandas as pd
from strategies.rsi_strategy import RSIStrategy

class Backtest:
    def __init__(self, data):
        """
        백테스팅 클래스 초기화
        data: pandas DataFrame, 과거 데이터 포함
        """
        self.data = data
        self.strategy = RSIStrategy()

    def run_backtest(self):
        """
        RSI 전략을 기반으로 백테스팅을 수행하는 메서드
        """
        self.data = self.strategy.generate_signal(self.data)
        
        initial_balance = 10000  # 초기 투자금
        balance = initial_balance
        position = 0

        # 백테스팅 실행 루프
        for index, row in self.data.iterrows():
            if row['signal'] == 1 and balance > 0:
                # 매수
                position = balance / row['close']
                balance = 0
            elif row['signal'] == -1 and position > 0:
                # 매도
                balance = position * row['close']
                position = 0

        final_balance = balance + (position * self.data.iloc[-1]['close'])
        profit = final_balance - initial_balance
        print(f"최종 자산: {final_balance:.2f} | 수익: {profit:.2f}")

if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='1mo', interval='1d')
    backtest = Backtest(btc_data)
    backtest.run_backtest()
