import websocket
import json
import pprint
import talib
import numpy as np
import configparser
from binance.client import Client
from binance.enums import *

SYMBOL = 'ETHUSDT'
INTERVAL = '1s'
SOCKET = f'wss://stream.binance.com:9443/ws/ethusdt@kline_{INTERVAL}'

SIGNAL = 12
FILTER = 20

TRADE_QTY = 0.002

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['API_KEY']
API_SECRET = config['binance']['API_SECRET']

client = Client(API_KEY, API_SECRET)
status = client.get_account_status()
balance = client.get_asset_balance(asset = 'USDT')
print(status)
print(balance)

closes = []

position = 0

def order(side, quantity, symbol, order_type = ORDER_TYPE_MARKET):
    #try:
    print("Sending order...")
    order = client.create_test_order(symbol = symbol,
                                side = side,
                                type = order_type,
                                quantity = quantity)
    print(order)
    return True
    #except:
        #return False

def on_open(ws):
    print('Connection is opened.')

def on_close(ws):
    print('Connection is closed.')

def on_message(ws, message):
    global position
    json_message = json.loads(message)
    #pprint.pprint(json_message)
    candle = json_message['k']
    candle_closed = candle['x']
    close = candle['c']

    if candle_closed:
        print(f'Candle closed at {close}')
        closes.append(float(close))
        #print(closes)

        if len(closes) > max(SIGNAL, FILTER):
            np_closes = np.array(closes)
            rsi_signal = talib.RSI(np_closes, SIGNAL)
            rsi_filter = talib.RSI(np_closes, FILTER)
            print(rsi_signal[-1])

            if rsi_signal[-1] > 70:
                if position == 0:
                    print("BUY!!")
                    order_succeeded = order(SIDE_BUY, TRADE_QTY, SYMBOL)
                    if order_succeeded:
                        position = 1


            if rsi_signal[-1] < 30:
                if position == 1:
                    print("SELL!!")
                    order_succeeded = order(SIDE_SELL, TRADE_QTY, SYMBOL)
                    if order_succeeded:
                        position = 0


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()