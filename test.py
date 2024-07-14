import websocket
import json
import pprint
import talib
import numpy as np
from binance.client import Client
from binance.enums import *

SYMBOL = 'ETHUSDT'

#api key for stuartlu
API_KEY = '1AgjhkkZGBO0gVFmcRsAeJRZFO5nwS3eWdLhjR4NFOsMzncAqsc5lEbsWGis3JKn'
API_SECRET = 'XCMN5C4QoM0GzcHo9cAfX37HGSiS2x3SlAD0mBa8Z82MEv6JvabdlHJCqV1h4lCo'

TRADE_QTY = 10

client = Client(API_KEY, API_SECRET)
status = client.get_account_status()
balance = client.get_asset_balance(asset = 'USDT')
print(status)
print(balance)

print('sending order')
order = client.create_order(symbol = SYMBOL,
                                side = SIDE_BUY,
                                type = ORDER_TYPE_MARKET,
                                quantity = 0.002)
print(order)
print('order sent successfully')