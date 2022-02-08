import os
import json
import time

from threading import Thread
from helpers.auth import CoinbaseAuth
from requests import request
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv('.env')


WS_URI = 'wss://ws-feed.exchange.coinbase.com'
# API_URI =


class WebsocketClient(object):
    def __init__(self):
        self.WS_URL = 'wss://ws-feed.exchange.coinbase.com'
        self.API_URL = 'https://api.exchange.coinbase.com'
        self._products = json.load(open('sltp.json', 'r'))
        self.channels = None
        self.stop = True
        self.ws = None
        self.thread = None
        self.keep_alive = None
        self.error = None
        self._prices = dict()

    def get_orders(self) -> dict:
        return self._products

    def add_pair(self, pair: dict):  # TODO: Add support for multi-add (take a list and loop through to add into a temp dict then subscribe after)
        self._products[pair['product_id'].upper()] = pair['sltp']
        json.dump(self._products, open('sltp.json', 'r'))
        self.ws.send(json.dumps({
            'type': 'subscribe',
            'product_ids': pair['product_id'].upper(),
            'channels': self.channels
        }))

    def remove_pair(self, pair: str):
        del self._products[pair.upper()]
        del self._prices[pair.upper()]
        json.dump(self._products, open('sltp.json', 'w'))
        self.ws.send(json.dumps({
            'type': 'unsubscribe',
            'product_id': pair.upper()
        }))

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stop = False
        self.keep_alive = Thread(target=self._keep_alive)
        self.thread = Thread(target=_go)
        self.thread.start()

    def _connect(self):
        products = [f'{coin_pair}' for coin_pair in self._products.keys()]

        if self.channels is None:
            self.channels = ['ticker']

        params = {'type': 'subscribe', 'product_ids': products, 'channels': self.channels}

        self.ws = create_connection(self.WS_URL)
        self.ws.send(json.dumps(params))
        self.on_open()

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

    def on_message(self, msg):
        try:
            self._prices[msg['product_id']] = float(msg['price'])
        except KeyError:
            pass

    def on_error(self, e, data=None):
        self.error = e
        self.stop = True
        print(f'{e} - data: {data}')


class StopLossTakeProfit(WebsocketClient):

    def __init__(self, sandbox=False):
        super().__init__()
        self.take_profit = None
        self.stop_loss = None
        self.sandbox = sandbox

        if self.sandbox:
            self.headers = CoinbaseAuth(os.getenv('sandbox_key'), os.getenv('sandbox_secret'),
                                        os.getenv('sandbox_passphrase'))
            self.WS_URL = 'wss://ws-feed-public.sandbox.exchange.coinbase.com'
            self.API_URL = 'https://api-public.sandbox.exchange.coinbase.com'
        else:
            self.headers = CoinbaseAuth(os.getenv('key'), os.getenv('secret'), os.getenv('passphrase'))

    def start(self):
        super().start()
        self.stop_loss = Thread(target=self._stop_loss)
        self.stop_loss.start()
        # self.take_profit = Thread(target=self._take_profit)
        # self.take_profit.start()

    def close(self):
        super().close()
        self.stop_loss.join()
        # self.take_profit.join()

    def _stop_loss(self):
        payload = {
            "type": "market",
            "side": "sell",
            "stp": "dc",
        }
        url = f'{self.API_URL}/orders'
        while not self.stop:
            for key in list(self._prices.keys()):
                if key not in self._products.keys():
                    del self._prices[key]
                    continue

                if self._prices[key] <= self._products[key]['stop_loss']:
                    # payload['price'] = self._products[key]['stop_loss'] # TODO add support for limit sell
                    payload['product_id'] = key
                    payload['size'] = 1
                    response = request('POST', url, json=payload, auth=self.headers)
                    print(response.content)
                    print('-- Stop Loss --')

                    if response.status_code == 401:
                        self.on_error(response.status_code, response.content)

                    self.remove_pair(key)
                elif self._prices[key] >= float(list(self._products[key]['take_profit'].items())[0]):
                    # payload['price'] = self._products[key]['take_profit'] # TODO add support for limit sell
                    payload['product_id'] = key
                    payload['size'] = float(list(self._products[key]['take_profit'].keys())[0])
                    response = request('POST', url, json=payload, auth=self.headers)
                    print(response.content)
                    print('-- Take Profit --')

                    if response.status_code == 401:
                        self.on_error(response.status_code, response.content)


    # def _take_profit(self):
    #     """
    #     _products['BTC-USD']['take_profit'] = { 1: 43000, 1.5: 43500, .4: 44500 }
    #     :return:
    #     """
    #     payload = {
    #         "type": "market",
    #         "side": "sell",
    #         "stp": "dc",
    #     }
    #     url = f'{self.API_URL}/orders'
    #     while not self.stop:
    #         for key in list(self._prices.keys()):
    #             if key not in self._products.keys():
    #                 del self._prices[key]
    #                 continue
    #
    #             if self._prices[key] >= self._products[key]['take_profit'].items()[0]:
    #                 # payload['price'] = self._products[key]['take_profit'] # TODO add support for limit sell
    #                 payload['product_id'] = key
    #                 payload['size'] = self._products[key]['take_profit'].keys()[0]
    #                 response = request('POST', url, json=payload, auth=self.headers)
    #                 print(response.content)
    #
    #                 if response.status_code == 401:
    #                     self.on_error(response.status_code, response.content)
