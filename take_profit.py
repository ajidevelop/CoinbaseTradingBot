import asyncio
import os
import json
import datetime


from requests import request
from websockets import connect
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'cb-access-key': os.getenv('key'),
    'cb-access-passphrase': os.getenv('passphrase'),
    'cb-access-timestamp': str(datetime.datetime.now())
}

WS_URI = 'wss://ws-feed.exchange.coinbase.com'
# API_URI = 'https://api.exchange.coinbase.com/orders'
API_URI = 'https://api-public.sandbox.exchange.coinbase.com'

prices = dict()
SLTP = {
    'ADA-USD': {
        'stop_loss': 1.415,
        'take_profit': 1.51
    },
    'BTC-USD': {
        'stop_loss': 40415,
        'take_profit': 42551
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


async def stop_loss():
    payload = {
        "type": "limit",
        "side": "buy",
        "stp": "dc",
    }
    while True:
        for key in prices.keys():
            if prices[key] <= SLTP[key]['stop_loss']:
                payload['price'] = SLTP[key]['stop_loss']
                response = request('POST', API_URI, json=payload, headers=headers)
                print(response)


async def take_profit():
    payload = {
        "type": "limit",
        "side": "buy",
        "stp": "dc",
        "stop": "loss",
    }
    while True:
        for key in prices.keys():
            if prices[key] >= SLTP[key]['take_profit']:
                payload['price'] = SLTP[key]['take_profit']
                response = request('POST', API_URI, json=payload, headers=headers)
                print(response)


# loop = asyncio.get_event_loop()
#
# coin = 't'
# curr = ''
#
# while coin not in ['', 'n']:
#     coin = input('Coin 1: ')
#     if coin in ['', 'n']: break
#     curr = input('Coin 2/Fiat Currency: ')
#     loop.create_task(coin_ticker(coin, curr))
#
# loop.create_task(stop_loss())
# loop.create_task(take_profit())
# loop.run_forever()

def test_place_order():
    payload = {
        "type": "limit",
        "side": "buy",
        "stp": "dc",
        "stop": "loss",
    }
    for key in prices.keys():
        if prices[key] >= SLTP[key]['take_profit']:
            payload['price'] = SLTP[key]['take_profit']
            response = request('POST', API_URI, json=payload, headers=headers)
            print(response)

# test_place_order()
