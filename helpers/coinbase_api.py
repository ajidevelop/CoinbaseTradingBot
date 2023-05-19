import os
import json
from requests import request
from helpers.auth import CoinbaseAuth


class CoinbaseApi:
    def __init__(self):
        self.API_URL = 'https://api.exchange.coinbase.com'
        self.headers = CoinbaseAuth(os.getenv('key'), os.getenv('secret'), os.getenv('passphrase'))

    def get_price(self, product_id: str) -> float:
        url = f'{self.API_URL}/products/{product_id}/ticker'
        response = request('GET', url)
        return float(json.loads(response.content)['price'])

    def place_order(self, payload):
        url = f'{self.API_URL}/orders'
        response = request('POST', url, json=payload, auth=self.headers)
        return response
        print(1)
