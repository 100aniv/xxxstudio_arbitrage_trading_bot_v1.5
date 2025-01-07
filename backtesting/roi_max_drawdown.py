
# roi_max_drawdown.py
# ROI 및 Max Drawdown 백테스팅 기능

import pandas as pd
import numpy as np

class BacktestingMetrics:
    def __init__(self):
        pass

    def calculate_roi(self, data):
        """
        ROI (Return on Investment) 계산
        """
        initial_value = data['Close'].iloc[0]
        final_value = data['Close'].iloc[-1]
        roi = (final_value - initial_value) / initial_value * 100
        return roi

    def calculate_max_drawdown(self, data):
        """
        Max Drawdown (최대 손실) 계산
        """
        data['CumulativeReturn'] = data['Close'].cummax()
        data['Drawdown'] = data['Close'] / data['CumulativeReturn'] - 1
        max_drawdown = data['Drawdown'].min()
        return max_drawdown

    def backtest_summary(self, data):
        """
        ROI 및 Max Drawdown을 종합적으로 계산하고 요약
        """
        roi = self.calculate_roi(data)
        max_drawdown = self.calculate_max_drawdown(data)
        return {
            "ROI": f"{roi:.2f}%",
            "Max Drawdown": f"{max_drawdown:.2f}%"
        }

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='6mo', interval='1d')

    backtester = BacktestingMetrics()
    results = backtester.backtest_summary(btc_data)
    print(f"ROI: {results['ROI']}, Max Drawdown: {results['Max Drawdown']}")
