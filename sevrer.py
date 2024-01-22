import asyncio

import websockets
import aio_pika
import datetime


async def handler(websocket):
    """function that runs upon websocket connection opening. 
    handles opening rabbitmq connection, recieving websocket 
    messages and sending them down rabbitmq"""

    # open and set up non-blocking rabbitmq connection
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost:5672/",
    )

    async with connection:
        routing_key = ""

        channel = await connection.channel()
        exchange = await channel.declare_exchange(name='myexchange', type=aio_pika.ExchangeType.TOPIC, durable = True)

        while True:
            # recieve messages via websocket and send them down rabbitmq
            message = await websocket.recv()
            print(datetime.datetime.now()) # debug
            await exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=routing_key,
            )
            print(message, datetime.datetime.now()) # debug

start_server = websockets.serve(handler, 'localhost', 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
