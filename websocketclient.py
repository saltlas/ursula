import websocket
import threading
import rel

def on_message(ws, message):
    print(message)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_error(ws, error):
    print(error)

class WebSocketClient:
    """establishes non-blocking websocket client connection and
    sends messages down websocket when needed"""
    def __init__(self, port):


        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(port, on_message = on_message, on_close = on_close, on_error = on_error)

        # runs it on new thread to prevent blocking
        wst = threading.Thread(target=ws.run_forever)

        self.ws = ws

        rel.signal(2, self.interrupt)  # recognising keyboard interrupt even in daemon thread

        wst.daemon = True
        wst.start()


    def send_message(self, info):
        self.ws.send(info)

    def interrupt(self): #close the connection properly on keyboardinterrupt
        self.close()
        raise KeyboardInterrupt

    def close(self): # regular close logic to shut down websocket but also rel
        rel.abort()
        self.ws.close()













