from helpers.valid_input import ValidInput
from take_profit import stop_loss, take_profit, coin_ticker, SLTP, json_to_file
import asyncio
import atexit

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
        loop.create_task(coin_ticker(coin, curr))

        SL = ValidInput('number', []).input('Stop Loss: ')
        TP = ValidInput('number', []).input('Take Profit: ')

        SLTP[f'{coin}-{curr}'] = {
            'stop_loss': SL,
            'take_profit': TP
        }

    loop.create_task(stop_loss())
    loop.create_task(take_profit())
    loop.run_forever()

atexit.register(json_to_file)
