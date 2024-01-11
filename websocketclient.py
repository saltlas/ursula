import websocket
import threading
from time import sleep
import rel

def on_message(ws, message):
    print(message)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_error(ws, error):
    print(error)

class WebSocketClient:
    """docstring for WebSocketClient"""
    def __init__(self):


        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://localhost:8001", on_message = on_message, on_close = on_close, on_error = on_error)
        #wst = threading.Thread(target=ws.run_forever(dispatcher=rel))

        ws.run_forever(dispatcher=rel)
        self.ws = ws

        rel.signal(2, self.close)  # Keyboard Interrupt  
        #rel.dispatch()  # WHAT ARE THE DOWNSIDES OF COMMENTING THIS OUT??

        #wst.daemon = True
        #wst.start()


    def send_message(self, info):
        self.ws.send(info)

    def close(self): #close the connection properly on keyboardinterrupt
        rel.abort()
        self.ws.close()
        raise KeyboardInterrupt













