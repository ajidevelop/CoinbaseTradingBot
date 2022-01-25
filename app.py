import json
from flask import Flask
from take_profit import StopLossTakeProfit
import asyncio

app = Flask(__name__)

sltp = StopLossTakeProfit()


@app.get('/get_orders')
def get_orders():
    return sltp.sltp


@app.post('/new_order')
def new_order(coin, curr, sl, tp):
    sltp.sltp[f'{coin}-{curr}'] = {
        'stop_loss': sl,
        'take_profit': tp
    }
    sltp.json_to_file()

    return json.load


print(sltp.sltp)
sltp.sltp = {}
print(sltp.sltp)
sltp.sltp['test'] = 'test'
print(sltp.sltp)
