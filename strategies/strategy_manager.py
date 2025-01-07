# strategies/strategy_manager.py (전략 관리)
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy

class StrategyManager:
    def __init__(self):
        self.strategies = {
            "RSI": RSIStrategy(),
            "MACD": MACDStrategy()
        }
        self.results = {}

    def apply_strategies(self, data):
        for name, strategy in self.strategies.items():
            try:
                self.results[name] = strategy.generate_signal(data.copy())
            except KeyError:
                print(f"{name} 전략 데이터 없음.")

    def get_performance(self):
        return self.results
