
# trade_logger.py
# 거래 내역을 CSV 파일로 기록하고, 로그를 관리하는 모듈입니다.

import csv
import os

class TradeLogger:
    def __init__(self, log_file="logs/trade_log.csv"):
        """
        로그 파일 초기화 메서드
        """
        self.log_file = log_file
        if not os.path.exists(log_file):
            with open(log_file, mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "action", "amount", "price", "balance"])

    def log_trade(self, timestamp, action, amount, price, balance):
        """
        거래 내역을 CSV 파일에 기록하는 메서드
        """
        with open(self.log_file, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, action, amount, price, balance])
        print(f"{timestamp} - {action} | Amount: {amount}, Price: {price}, Balance: {balance}")

if __name__ == "__main__":
    logger = TradeLogger()
    logger.log_trade("2024-01-01 12:00:00", "BUY", 0.01, 50000, 10000)
