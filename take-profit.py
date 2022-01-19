import asyncio

from websockets import connect
from dotenv import load_dotenv
import json

load_dotenv('.env')

WS_URI = 'wss://ws-feed.exchange.coinbase.com'
API_URI = 'https://api.exchange.coinbase.com/orders'

prices = {}
SLTP = {
    'ADA-USD': {
        'stop_loss': 1.415,
        'take_profit': 1.51
    }
}


async def coin_ticker(coin: str, curr: str):
    async with connect(WS_URI, ping_interval=None) as ws:
        data = {
            'type': 'subscribe',
            'channels': ['ticker'],
            'product_ids': [f'{coin.upper()}-{curr.upper()}'],
        }
        await ws.send(json.dumps(data))
        await ws.recv()
        while True:
            await asyncio.sleep(1)
            ticker = json.loads(await ws.recv())
            prices[ticker['product_id']] = float(ticker['price'])
            print(prices)


async def unsubscribe():
    async with connect(WS_URI) as ws:
        data = {
            'type': 'unsubscribe',
            'channels': ['heartbeat']
        }
        await ws.send(json.dumps(data))


async def take_profit():
    payload = {
        "type": "limit",
        "side": "buy",
        "stp": "dc",
        "stop": "loss",
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    while True:
        for key in prices.keys():
            if prices[key] <= SLTP[key]['stop_loss']:
                pass


loop = asyncio.get_event_loop()

coin = 't'
curr = ''

while coin not in ['', 'n']:
    coin = input('Coin 1: ')
    if coin in ['', 'n']: break
    curr = input('Coin 2/Fiat Currency: ')
    loop.create_task(coin_ticker(coin, curr))

loop.run_forever()
