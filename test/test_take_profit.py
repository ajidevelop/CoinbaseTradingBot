import unittest
import os
from take_profit import prices, CoinbaseAuth
from requests import request


class MyTestCase(unittest.TestCase):
    API_URI = 'https://api-public.sandbox.exchange.coinbase.com'

    def test_place_order(self):
        headers = CoinbaseAuth(os.getenv('sandbox_key'), os.getenv('sandbox_secret'), os.getenv('sandbox_passphrase'))
        prices['BTC-USD'] = 43000
        payload = {
            "type": "limit",
            "side": "sell",
            "stp": "dc",
        }
        SLTP = {}
        for key in prices.keys():
            if prices[key] >= SLTP[key]['take_profit']:
                payload['price'] = SLTP[key]['take_profit']
                payload['product_id'] = key
                payload['size'] = 10
                response = request('POST', MyTestCase.API_URI + '/orders', json=payload, auth=headers)
                print(response.text)
                self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
