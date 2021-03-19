import time
import Database
import config
from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import talib
import numpy
from setup import bot
from setup import MACDEMA
from setup import RSI

SYMBOLS = []
TIME='1 month ago UTC+3'
connection = Database.create_connection("test.db")
def macdAndRsiKlineSell():
    SYMBOLS = Database.getOpenOrderSymbols(connection)
    for x in SYMBOLS:
        close=[]
        klines = client.get_historical_klines(x[1], Client.KLINE_INTERVAL_1HOUR, TIME)
        if len(klines) > 26:
            for entry in klines:
                close.append(float(entry[4]))

            rsiBuy, rsiSell, invRsi = RSI(close)
            macdBuy, macdSell, macd, signal = MACDEMA(close)
            print(x[1]," ",macd," ",signal, " ", invRsi)

            if macdSell:
                order = (klines[-1][4],klines[-1][0],x[0])
                Database.sellOrder(connection,order)
                msg = x[1]+ "\U0001F4C8 Satiş: " + str(round(klines[-1][4],2)).replace(".", ",")
                bot.send_message(-1001408874432, msg)
                print(msg)


if __name__ == '__main__':
    print("Seller is working...")
    client = Client(config.api_key, config.api_secret)
    while True:
        if Database.count_open_orders(connection) > 0:
            macdAndRsiKlineSell()
        else:
            time.sleep(20)

