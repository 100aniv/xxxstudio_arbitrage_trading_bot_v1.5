# ui/gui.py (클래스 이름 확인 및 수정)
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QMessageBox
import json

class TradingBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot - Login")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("이메일 입력")
        self.layout.addWidget(self.email_input)

        self.upbit_api_key_input = QLineEdit(self)
        self.upbit_api_key_input.setPlaceholderText("업비트 API Key")
        self.layout.addWidget(self.upbit_api_key_input)

        self.upbit_api_secret_input = QLineEdit(self)
        self.upbit_api_secret_input.setPlaceholderText("업비트 API Secret Key")
        self.layout.addWidget(self.upbit_api_secret_input)

        self.binance_api_key_input = QLineEdit(self)
        self.binance_api_key_input.setPlaceholderText("바이낸스 API Key")
        self.layout.addWidget(self.binance_api_key_input)

        self.binance_api_secret_input = QLineEdit(self)
        self.binance_api_secret_input.setPlaceholderText("바이낸스 API Secret Key")
        self.layout.addWidget(self.binance_api_secret_input)

        self.telegram_api_key_input = QLineEdit(self)
        self.telegram_api_key_input.setPlaceholderText("텔레그램 API Key")
        self.layout.addWidget(self.telegram_api_key_input)

        self.telegram_bot_id_input = QLineEdit(self)
        self.telegram_bot_id_input.setPlaceholderText("텔레그램 Bot ID")
        self.layout.addWidget(self.telegram_bot_id_input)

        self.remember_me_checkbox = QCheckBox("로그인 유지", self)
        self.layout.addWidget(self.remember_me_checkbox)

        # 저장 및 로그인 버튼
        self.login_button = QPushButton("저장 및 로그인", self)
        self.login_button.clicked.connect(self.save_credentials)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def save_credentials(self):
        credentials = {
            "email": self.email_input.text(),
            "upbit_api_key": self.upbit_api_key_input.text(),
            "upbit_api_secret": self.upbit_api_secret_input.text(),
            "binance_api_key": self.binance_api_key_input.text(),
            "binance_api_secret": self.binance_api_secret_input.text(),
            "telegram_api_key": self.telegram_api_key_input.text(),
            "telegram_bot_id": self.telegram_bot_id_input.text(),
            "remember_me": self.remember_me_checkbox.isChecked()
        }
        try:
            with open("ui/credentials.json", "w") as file:
                json.dump(credentials, file)
            QMessageBox.information(self, "로그인 성공", "자격 증명이 저장되었습니다!")
            from ui.main_window import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"자격 증명 저장 실패: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    window = TradingBotGUI()
    window.show()
    app.exec()
