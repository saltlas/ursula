import asyncio

import websockets
import aio_pika
import logging
import datetime


async def handler(websocket):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost:5672/",
    )

    async with connection:
        routing_key = ""

        channel = await connection.channel()
        exchange = await channel.declare_exchange(name='myexchange', type=aio_pika.ExchangeType.TOPIC, durable = True)

        while True:
            message = await websocket.recv()
            print(datetime.datetime.now())
            await exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=routing_key,
            )
            print(message, datetime.datetime.now())

start_server = websockets.serve(handler, 'localhost', 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
