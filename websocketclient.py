import websocket
import threading
from time import sleep

def on_message(ws, message):
    print(message)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

class WebSocketClient:
    """docstring for WebSocketClient"""
    def __init__(self):


        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://localhost:7777", on_message = on_message, on_close = on_close)
        wst = threading.Thread(target=ws.run_forever(dispatcher=rel, reconnect=0))

        wst.daemon = True
        wst.start()

        self.ws = ws

    def send_message(self, info):
        self.ws.send(info)

    def close(self):
        self.ws.close()













