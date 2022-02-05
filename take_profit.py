import asyncio
import os
import json
import time

from threading import Thread
from helpers.auth import CoinbaseAuth
from requests import request
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv('.env')

SANDBOX = False
headers = CoinbaseAuth(os.getenv('key'), os.getenv('secret'), os.getenv('passphrase'))


WS_URI = 'wss://ws-feed.exchange.coinbase.com'
# API_URI = 'https://api.exchange.coinbase.com/orders'
API_URI = 'https://api-public.sandbox.exchange.coinbase.com'


class WebsocketClient(object):
    def __init__(self):
        self.url = 'wss://ws-feed.exchange.coinbase.com'
        self.products = json.load(open('sltp.json', 'r'))
        self.channels = None
        self.stop = True
        self.ws = None
        self.thread = None
        self.keep_alive = None
        self.error = None
        self.prices = dict()

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stop = False
        self.keep_alive = Thread(target=self._keep_alive)
        self.thread = Thread(target=_go())
        self.thread.start()

    def _connect(self):
        self.products = [f'{coin_pair}' for coin_pair in self.products.keys()]

        if self.channels is None:
            self.channels = ['ticker']

        params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}

        self.ws = create_connection(self.url)
        self.ws.send(json.dumps(params))

    def _keep_alive(self, interval=30):
        while self.ws.connected:
            self.ws.ping('keepalive')
            time.sleep(interval)

    def _listen(self):
        self.keep_alive.start()
        while not self.stop:
            try:
                data = self.ws.recv()
                msg = json.loads(data)
            except ValueError as e:
                self.on_error(e)
            else:
                self.on_message(msg)

    def _disconnect(self):
        try:
            if self.ws:
                self.ws.close()
        except Exception as e:
            self.on_error(e)
        finally:
            self.keep_alive.join()

        self.on_close()

    def close(self):
        self.stop = True
        self._disconnect()
        self.thread.join()

    @staticmethod
    def on_open():
        print("-- Subscribed! --\n")

    @staticmethod
    def on_close():
        print("\n-- Socket Closed --")

    @staticmethod
    def on_message(msg):
        print(msg)

    def on_error(self, e, data=None):
        self.error = e
        self.stop = True
        print('{} - data: {}'.format(e, data))


class StopLossTakeProfit:

    def __init__(self):
        self.sltp = json.load(open('sltp.json', 'r'))
        self.prices = dict()

        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.coin_ticker())
        self.loop.create_task(self.stop_loss())
        self.loop.create_task(self.take_profit())
        self.loop.run_forever()

    def json_to_file(self):
        with open('sltp.json', 'w+') as file:
            json.dump(self.sltp, file)

    async def coin_ticker(self):
        async with connect(WS_URI, ping_interval=None) as ws:
            print('t')
            data = {
                'type': 'subscribe',
                'channels': ['ticker'],
                'product_ids': [f'{coin.upper()}-{curr.upper()}' for coin, curr in self.sltp.items()],
            }
            await ws.send(json.dumps(data))
            await ws.recv()
            while True:
                print('t')
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
