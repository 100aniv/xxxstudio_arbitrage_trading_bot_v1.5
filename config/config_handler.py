
# config_handler.py
# 이 모듈은 API 키를 안전하게 암호화하고, 보관 및 복호화하는 기능을 포함합니다.

from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()

class ConfigHandler:
    def __init__(self):
        """
        ConfigHandler 클래스 초기화
        """
        # 환경 변수에서 AES-256 키 로드
        self.key = os.getenv('ENCRYPTION_KEY')
        if not self.key:
            # 키가 없는 경우 새 키를 생성하고 .env에 저장
            self.key = Fernet.generate_key().decode()
            with open(".env", "a") as env_file:
                env_file.write(f"\nENCRYPTION_KEY={self.key}")

        self.cipher = Fernet(self.key.encode())

    def encrypt(self, data):
        """
        데이터 암호화 메서드
        """
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """
        데이터 복호화 메서드
        """
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def load_api_keys(self):
        """
        API 키 로딩 메서드
        """
        upbit_key = os.getenv('UPBIT_API_KEY')
        binance_key = os.getenv('BINANCE_API_KEY')
        return upbit_key, binance_key

# 테스트 코드
if __name__ == "__main__":
    config = ConfigHandler()
    test_key = "test_api_key"
    encrypted = config.encrypt(test_key)
    print("Encrypted:", encrypted)
    print("Decrypted:", config.decrypt(encrypted))
