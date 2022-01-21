import asyncio
import os
import json
from helpers.auth import CoinbaseAuth
from requests import request
from websockets import connect
from dotenv import load_dotenv

load_dotenv('.env')

SANDBOX = False
headers = CoinbaseAuth(os.getenv('key'), os.getenv('secret'), os.getenv('passphrase'))


WS_URI = 'wss://ws-feed.exchange.coinbase.com'
# API_URI = 'https://api.exchange.coinbase.com/orders'
API_URI = 'https://api-public.sandbox.exchange.coinbase.com'

prices = dict()


class StopLossTakeProfit:
    @staticmethod
    def json_to_file(sltp):
        with open('sltp.json', 'w+') as file:
            json.dump(sltp, file)

    @staticmethod
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

    @staticmethod
    async def unsubscribe():
        async with connect(WS_URI) as ws:
            data = {
                'type': 'unsubscribe',
                'channels': ['heartbeat']
            }
            await ws.send(json.dumps(data))

    @staticmethod
    async def stop_loss(sltp: dict):
        payload = {
            "type": "limit",
            "side": "buy",
            "stp": "dc",
        }
        while True:
            for key in prices.keys():
                if prices[key] <= sltp[key]['stop_loss']:
                    payload['price'] = sltp[key]['stop_loss']
                    response = request('POST', API_URI, json=payload, headers=headers)
                    print(response)

    @staticmethod
    async def take_profit(sltp: dict):
        payload = {
            "type": "limit",
            "side": "buy",
            "stp": "dc",
            "stop": "loss",
        }
        while True:
            for key in prices.keys():
                if prices[key] >= sltp[key]['take_profit']:
                    payload['price'] = sltp[key]['take_profit']
                    response = request('POST', API_URI, json=payload, headers=headers)
                    print(response)
