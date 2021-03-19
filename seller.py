import time
import Database
import config
from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import talib
import telebot
import numpy

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
            macdBuy, signalSell, macd, signal = MACDEMA(close)
            print(x[1]," ",macd," ",signal, " ", invRsi)

            if signalSell:
                order = (klines[-1][4],klines[-1][0],x[0])
                Database.sellOrder(connection,order)
                msg = x[1]+ "\U0001F4C8 Satiş:" + str(klines[-1][4]).replace(".", ",")
                bot.send_message(-1001408874432, msg)
                print(msg)

def RSI(close):
    rsi = talib.RSI(numpy.asarray(close), timeperiod=21)
    v1 = 0.1 * (rsi - 50)
    v2 = talib.WMA(numpy.asarray(v1), timeperiod=9)
    inv = []
    for entry in v2:
        inv.append((math.exp(2 * entry) - 1) / (math.exp(2 * entry) + 1))

    rsiSell = (inv[-2] > 0.5) and (inv[-1] <= 0.5)
    rsiBuy = (inv[-2] < -0.5) and (inv[-1] >= -0.5)

    return rsiBuy, rsiSell, round(inv[-1], 2)

def MACDEMA(close):
    MMEslowa = talib.EMA(numpy.asarray(close),timeperiod=26)
    MMEslowb = talib.EMA(MMEslowa, timeperiod=26)
    DEMAslow = ((2 * MMEslowa) - MMEslowb)

    MMEfasta = talib.EMA(numpy.asarray(close), timeperiod=12)
    MMEfastb = talib.EMA(MMEfasta, timeperiod=12)
    DEMAfast = ((2 * MMEfasta) - MMEfastb)

    LigneMACD = DEMAfast - DEMAslow

    MMEsignala = talib.EMA(LigneMACD, timeperiod=9)
    MMEsignalb = talib.EMA(MMEsignala, timeperiod=9)
    Lignesignal = ((2 * MMEsignala) - MMEsignalb)

    macdBuy = LigneMACD[-2] < Lignesignal[-2] and LigneMACD[-3] < Lignesignal[-3] and LigneMACD[-1] >= Lignesignal[-1]
    macdSell = LigneMACD[-2] > Lignesignal[-2] and LigneMACD[-3] > Lignesignal[-3] and LigneMACD[-1] <= Lignesignal[-1]
    return macdBuy,macdSell, round(LigneMACD[-1],2), round(Lignesignal[-1],2)

if __name__ == '__main__':
    print("Seller is working...")
    client = Client(config.api_key, config.api_secret)
    bot = telebot.TeleBot("1628197070:AAFLvfUgbwO8qnY4YkQJ8yLHLoube-51GKc", parse_mode="MarkdownV2")
    while True:
        if Database.count_open_orders(connection) > 0:
            macdAndRsiKlineSell()
        else:
            time.sleep(20)

