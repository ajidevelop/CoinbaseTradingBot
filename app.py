from flask import Flask
from take_profit import StopLossTakeProfit
app = Flask(__name__)

stop_loss = StopLossTakeProfit(sandbox=True)
stop_loss.start()


@app.get('/get_orders')
def get_orders():
    return stop_loss.get_orders()


@app.post('/new_order')
def new_order(coin_pair, sl, tp):
    pass


