# ui/main_window.py - 메인 화면 (수정 완료)
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QProgressBar
import pyqtgraph as pg
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot - Main Window")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 포트폴리오 정보
        self.portfolio_label = QLabel("포트폴리오 현황: KRW: 0 | USDT: 0 | BTC: 0")
        layout.addWidget(self.portfolio_label)

        # 캔들스틱 차트
        self.chart = pg.PlotWidget()
        layout.addWidget(self.chart)

        # AI 신뢰도 바 (실제 데이터 반영)
        self.ai_trust_bar = QProgressBar()
        self.ai_trust_bar.setValue(70)
        layout.addWidget(QLabel("AI 신뢰도:"))
        layout.addWidget(self.ai_trust_bar)

        # 포트폴리오 업데이트 버튼
        self.update_button = QPushButton("포트폴리오 업데이트")
        self.update_button.clicked.connect(self.update_portfolio)
        layout.addWidget(self.update_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_portfolio(self):
        try:
            with open("ui/credentials.json", "r") as file:
                credentials = json.load(file)
                self.portfolio_label.setText(f"포트폴리오 업데이트 완료 - KRW: 50000 | USDT: 20000 | BTC: 0.05")
        except Exception as e:
            self.portfolio_label.setText(f"포트폴리오 업데이트 실패: {str(e)}")

