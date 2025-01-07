
# notify.py
# 텔레그램 및 이메일 알림을 제공하는 모듈입니다.

import requests
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class Notifier:
    def __init__(self):
        """
        텔레그램 및 이메일 알림 설정 초기화
        """
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')

    def send_telegram_message(self, message):
        """
        텔레그램 메시지 전송 메서드
        """
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {"chat_id": self.telegram_chat_id, "text": message}
        requests.post(url, data=data)

    def send_email(self, subject, message):
        """
        이메일 전송 메서드
        """
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.email_user
        msg["To"] = self.email_user

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.email_user, self.email_pass)
            server.sendmail(self.email_user, self.email_user, msg.as_string())

if __name__ == "__main__":
    notifier = Notifier()
    notifier.send_telegram_message("Testing Telegram Alert!")
    notifier.send_email("Test Email", "This is a test email from the bot.")
