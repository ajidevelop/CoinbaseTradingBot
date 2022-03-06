from app_config import app

from flask import request
from take_profit import StopLossTakeProfit

stop_loss = StopLossTakeProfit(sandbox=True)
stop_loss.start()


@app.get('/get_orders')
def get_orders():
    return stop_loss.get_orders()


@app.post('/new_order')
def new_order():
    stop_loss.add_pair(request.json)
    return {'200': '200'}


if __name__ == '__main__':
    app.run(debug=True)
