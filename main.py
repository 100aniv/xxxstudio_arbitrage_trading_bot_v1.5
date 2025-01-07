# main.py (업데이트 완료)
from PyQt6.QtWidgets import QApplication
from ui.gui import TradingBotGUI

def main():
    # PyQt 애플리케이션 생성
    app = QApplication([])

    # 로그인 화면 실행
    window = TradingBotGUI()
    window.show()

    # PyQt 이벤트 루프 시작
    app.exec()

if __name__ == "__main__":
    main()
