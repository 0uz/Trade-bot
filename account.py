from binance.enums import ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET
from test import SYMBOL
import config
from binance.client import Client
import talib
from binance.exceptions import BinanceAPIException, BinanceOrderException

client = Client(config.api_key, config.api_secret)
client.API_URL = 'https://testnet.binance.vision/api'
account = client.get_account()

def printAccountWallet(account):
    for data in account['balances']:
        print(data['asset'], " ", data['free'])




def marketOrder(symbol,quantitiy):
    try:
        buy_market = client.order_market_buy(
            symbol=symbol,
            quantity=quantitiy)

        return buy_market
    except BinanceAPIException as e:
        print(e)
    except BinanceOrderException as e:
        print(e)

def limitOrder(symbol,quantitiy,price):
    try:
        buy_limit = client.order_limit_buy(
            symbol=symbol,
            quantitiy=quantitiy,
            price=price)
        return buy_limit
    except BinanceAPIException as e:
        print(e)
    except BinanceOrderException as e:
        print(e)



def printOrder():
    return client.get_my_trades(symbol ='BNBUSDT')



#print(marketOrder('BNBUSDT','1'))
print(printOrder())
#printAccountWallet(account)
#print(client.get_all_tickers())