import asyncio

import websockets



async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)

start_server = websockets.serve(handler, 'localhost', 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
