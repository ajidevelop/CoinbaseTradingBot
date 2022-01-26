import json
from flask import Flask
from take_profit import StopLossTakeProfit
import asyncio
import threading

app = Flask(__name__)

sltp = StopLossTakeProfit()
# t1 = threading.Thread(target=sltp., name='coin-ticker')
# t1.start()

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

print('works')
# t1.join()
sltp.stop_loss()
