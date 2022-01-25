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


class StopLossTakeProfit:

    def __init__(self):
        self._sltp = json.load(open('sltp.json', 'r'))
        self.prices = dict()

        loop = asyncio.get_event_loop()
        loop.create_task(self.coin_ticker())
        loop.create_task(self.stop_loss())
        loop.create_task(self.take_profit())
        loop.run_forever()

    @property
    def sltp(self):
        return self._sltp

    @sltp.setter
    def sltp(self, val):
        print('hello')
        self._sltp = val

    def json_to_file(self):
        with open('sltp.json', 'w+') as file:
            json.dump(self.sltp, file)

    async def coin_ticker(self):
        async with connect(WS_URI, ping_interval=None) as ws:
            data = {
                'type': 'subscribe',
                'channels': ['ticker'],
                'product_ids': [f'{coin.upper()}-{curr.upper()}' for coin, curr in self.sltp.items()],
            }
            await ws.send(json.dumps(data))
            await ws.recv()
            while True:
                await asyncio.sleep(1)
                ticker = json.loads(await ws.recv())
                self.prices[ticker['product_id']] = float(ticker['price'])

    @staticmethod
    async def unsubscribe():
        async with connect(WS_URI) as ws:
            data = {
                'type': 'unsubscribe',
                'channels': ['heartbeat']
            }
            await ws.send(json.dumps(data))

    async def stop_loss(self):
        payload = {
            "type": "limit",
            "side": "buy",
            "stp": "dc",
        }
        while True:
            for key in self.prices.keys():
                if self.prices[key] <= self.sltp[key]['stop_loss']:
                    payload['price'] = self.sltp[key]['stop_loss']
                    response = request('POST', API_URI, json=payload, headers=headers)
                    print(response)

    async def take_profit(self):
        payload = {
            "type": "limit",
            "side": "buy",
            "stp": "dc",
            "stop": "loss",
        }
        while True:
            for key in self.prices.keys():
                if self.prices[key] >= self.sltp[key]['take_profit']:
                    payload['price'] = self.sltp[key]['take_profit']
                    response = request('POST', API_URI, json=payload, headers=headers)
                    print(response)
