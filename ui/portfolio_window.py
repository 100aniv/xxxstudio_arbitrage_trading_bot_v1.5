from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem
import pandas as pd

class PortfolioWindow(QMainWindow):
    def __init__(self, portfolio_data):
        super().__init__()
        self.setWindowTitle("포트폴리오 상세 정보")
        self.setGeometry(150, 150, 700, 500)

        self.layout = QVBoxLayout()

        # 포트폴리오 데이터 테이블
        self.portfolio_table = QTableWidget()
        self.portfolio_table.setRowCount(len(portfolio_data))
        self.portfolio_table.setColumnCount(3)
        self.portfolio_table.setHorizontalHeaderLabels(["코인", "보유량", "평가금액"])

        # 데이터 반영
        for row_index, (coin, details) in enumerate(portfolio_data.items()):
            self.portfolio_table.setItem(row_index, 0, QTableWidgetItem(coin))
            self.portfolio_table.setItem(row_index, 1, QTableWidgetItem(str(details['quantity'])))
            self.portfolio_table.setItem(row_index, 2, QTableWidgetItem(f"{details['value']} KRW"))

        self.layout.addWidget(self.portfolio_table)

        # 닫기 버튼
        self.close_button = QPushButton("닫기")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
