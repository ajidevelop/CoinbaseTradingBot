from flask import Flask
from take_profit import StopLossTakeProfit
app = Flask(__name__)


@app.get('/get_orders')
def get_orders():
    pass


@app.post('/new_order')
def new_order(coin, curr, sl, tp):
    pass


stop_loss = StopLossTakeProfit(sandbox=True)
stop_loss.start()
