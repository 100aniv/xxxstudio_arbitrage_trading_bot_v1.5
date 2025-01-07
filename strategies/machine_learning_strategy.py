
# machine_learning_strategy.py
# XGBoost & LightGBM 기반 머신러닝 전략

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

class MachineLearningStrategy:
    def __init__(self):
        self.model_xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.model_lgbm = LGBMClassifier()
        self.scaler = StandardScaler()

    def prepare_data(self, data):
        """
        데이터를 전처리하여 학습에 사용 가능한 형식으로 변환
        """
        data['returns'] = data['Close'].pct_change()
        data['volatility'] = data['Close'].rolling(window=5).std()
        data['RSI'] = self.calculate_rsi(data)
        data.dropna(inplace=True)
        
        # X, y 분리
        X = data[['returns', 'volatility', 'RSI']]
        y = np.where(data['returns'] > 0, 1, 0)  # 상승 = 1, 하락 = 0
        X_scaled = self.scaler.fit_transform(X)
        return train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    def calculate_rsi(self, data, period=14):
        """
        RSI 계산
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def train_models(self, data):
        """
        XGBoost 및 LightGBM 모델 학습
        """
        X_train, X_test, y_train, y_test = self.prepare_data(data)
        
        # XGBoost 학습
        self.model_xgb.fit(X_train, y_train)
        xgb_pred = self.model_xgb.predict(X_test)
        xgb_accuracy = accuracy_score(y_test, xgb_pred)

        # LightGBM 학습
        self.model_lgbm.fit(X_train, y_train)
        lgbm_pred = self.model_lgbm.predict(X_test)
        lgbm_accuracy = accuracy_score(y_test, lgbm_pred)

        return {"XGBoost Accuracy": xgb_accuracy, "LightGBM Accuracy": lgbm_accuracy}

    def generate_signals(self, data):
        """
        XGBoost와 LightGBM 예측 신호 생성
        """
        X_scaled = self.scaler.transform(data[['returns', 'volatility', 'RSI']])
        data['XGB_Signal'] = self.model_xgb.predict(X_scaled)
        data['LGBM_Signal'] = self.model_lgbm.predict(X_scaled)
        return data

# 테스트 실행
if __name__ == "__main__":
    import yfinance as yf
    btc_data = yf.download('BTC-USD', period='6mo', interval='1d')

    strategy = MachineLearningStrategy()
    results = strategy.train_models(btc_data)
    print(f"XGBoost 정확도: {results['XGBoost Accuracy']:.2f}")
    print(f"LightGBM 정확도: {results['LightGBM Accuracy']:.2f}")

    signal_data = strategy.generate_signals(btc_data)
    print(signal_data[['Close', 'XGB_Signal', 'LGBM_Signal']].tail())
