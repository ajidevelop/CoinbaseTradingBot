import base64, hmac, hashlib, time
from requests.auth import AuthBase


class CoinbaseAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())

        message = timestamp + request.method + request.path_url
        message = message.encode('utf-8')
        if request.body:
            message = message + request.body

        signature = hmac.new(base64.b64decode(self.secret_key), message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase
        })
        return request
