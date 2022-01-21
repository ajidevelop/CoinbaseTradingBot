from helpers.valid_input import ValidInput
from take_profit import StopLossTakeProfit
import asyncio
import json

file = open('sltp.json', 'r')
SLTP = json.load(file)

print('Welcome to Coinbase Trading Bot')
user_input = ValidInput('number', [1, 2]).input('Would you like to:\n1. Set SLTP orders:\n2. View SLTP orders ')

if user_input == 1:
    loop = asyncio.get_event_loop()

    coin = ValidInput('str', [])
    curr = ValidInput('str', [])

    while coin not in ['', 'n']:
        coin = ValidInput('str', []).input('Coin 1: ')
        curr = ValidInput('str', []).input('Coin 2/Fiat Currency: ')

        if coin in ['', 'n']: break
        loop.create_task(StopLossTakeProfit.coin_ticker(coin, curr))

        SL = ValidInput('number', []).input('Stop Loss: ')
        TP = ValidInput('number', []).input('Take Profit: ')

        SLTP[f'{coin}-{curr}'] = {
            'stop_loss': SL,
            'take_profit': TP
        }
        StopLossTakeProfit.json_to_file(SLTP)

    loop.create_task(StopLossTakeProfit.stop_loss(SLTP))
    loop.create_task(StopLossTakeProfit.take_profit(SLTP))
    loop.run_forever()

