# data/data_collector.py - 업비트 & 바이낸스 동시 웹소켓 수집 (멀티스레딩 적용)
import websocket
import json
import threading

class DataCollector:
    def __init__(self):
        self.upbit_data = None
        self.binance_data = None

    def on_message_upbit(self, ws, message):
        try:
            self.upbit_data = json.loads(message)
            print("업비트 데이터 수집 성공:", self.upbit_data)
        except Exception as e:
            print(f"업비트 데이터 오류: {e}")

    def on_message_binance(self, ws, message):
        try:
            self.binance_data = json.loads(message)
            print("바이낸스 데이터 수집 성공:", self.binance_data)
        except Exception as e:
            print(f"바이낸스 데이터 오류: {e}")

    def start_upbit_stream(self):
        ws = websocket.WebSocketApp(
            "wss://api.upbit.com/websocket/v1",
            on_message=self.on_message_upbit
        )
        ws.run_forever()

    def start_binance_stream(self):
        ws = websocket.WebSocketApp(
            "wss://stream.binance.com:9443/ws/btcusdt@trade",
            on_message=self.on_message_binance
        )
        ws.run_forever()

    def start_streaming(self):
        upbit_thread = threading.Thread(target=self.start_upbit_stream)
        binance_thread = threading.Thread(target=self.start_binance_stream)

        upbit_thread.start()
        binance_thread.start()
