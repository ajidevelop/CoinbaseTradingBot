import asyncio
import time

from websockets import connect, serve
from threading import Thread
from dotenv import load_dotenv
import os
import json

load_dotenv('.env')

URI = 'ws-feed.exchange.coinbase.com'


async def test_websocket():
    async with connect(URI) as ws:
        data = {
            'type': 'subscribe',
            'channels': ['ticker'],
            'product_ids': ['BTC-USD'],
        }
        await ws.send(json.dumps(data))

        print(await ws.recv())


async def unsubscribe():
    async with connect(f'wss://{URI}') as ws:
        data = {
            'type': 'unsubscribe',
            'channels': ['heartbeat']
        }
        await ws.send(json.dumps(data))


def start_loop(loop, server):
    loop.run_until_complete(server)
    loop.run_forever()


new_loop = asyncio.new_event_loop()
start_server = serve(test_websocket, URI, loop=new_loop)
t = Thread(target=start_loop, args=(new_loop, start_server))
t.start()
asyncio.get_event_loop().run_until_complete(test_websocket())
