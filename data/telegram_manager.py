# data/telegram_manager.py (신규 생성 파일)

import requests

class TelegramManager:
    def __init__(self, token, bot_id):
        """
        텔레그램 메시지를 관리하는 클래스
        :param token: 텔레그램 API 토큰
        :param bot_id: 텔레그램 봇 ID
        """
        self.token = token
        self.bot_id = bot_id

    def send_message(self, message):
        """
        텔레그램 메시지 전송 메서드
        :param message: 전송할 메시지
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            "chat_id": self.bot_id,
            "text": message
        }
        try:
            response = requests.post(url, params=params)
            if response.status_code == 200:
                print("✅ 텔레그램 메시지 전송 성공!")
            else:
                print(f"⚠️ 메시지 전송 실패! {response.json()}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

# ✅ 직접 실행 테스트 (수동으로 실행 가능)
if __name__ == "__main__":
    test_token = "YOUR_TELEGRAM_TOKEN_HERE"
    test_bot_id = "YOUR_TELEGRAM_BOT_ID_HERE"
    manager = TelegramManager(test_token, test_bot_id)
    manager.send_message("✅ 텔레그램 API 연결 테스트 메시지")
