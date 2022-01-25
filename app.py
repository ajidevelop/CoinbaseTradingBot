import json
from flask import Flask
from take_profit import StopLossTakeProfit
import asyncio

app = Flask(__name__)
loop = asyncio.get_event_loop()
SLTP = json.load(open('sltp.json', 'r'))


@app.get('/get_orders')
def get_orders():
    return SLTP


@app.post('/new_order')
def new_order(coin, curr, sl, tp):
    loop.create_task(StopLossTakeProfit.coin_ticker(coin, curr))
    SLTP[f'{coin}-{curr}'] = {
        'stop_loss': sl,
        'take_profit': tp
    }
    StopLossTakeProfit.json_to_file(SLTP)

    return json.load