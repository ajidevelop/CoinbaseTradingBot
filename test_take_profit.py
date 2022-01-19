import unittest
from take_profit import headers, prices, SLTP
from requests import request


class MyTestCase(unittest.TestCase):
    API_URI = 'https://api-public.sandbox.exchange.coinbase.com'

    def test_place_order(self):
        prices['BTC-USD'] = 43000
        payload = {
            "type": "limit",
            "side": "buy",
            "stp": "dc",
            "stop": "loss",
        }
        for key in prices.keys():
            if prices[key] >= SLTP[key]['take_profit']:
                payload['price'] = SLTP[key]['take_profit']
                response = request('POST', MyTestCase.API_URI, json=payload, headers=headers)
                print(response.text)
                self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
