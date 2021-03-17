import config
from binance.client import Client
import numpy
import talib
import math
from binance.enums import *
from binance.websockets import BinanceSocketManager
import telebot


SYMBOL = 'BTCUSDT'
SYMBOLS = []
TIME = "1 month ago UTC+3"

candleDataClose_4H = []
candleDataClose_1H = []

EMA_1H = []
EMA_15M = []
MACD = []

counter = 0

def fillSymbols():
    SYMBOLS.clear()
    data = client.get_all_tickers()
    for x in data:
        if x['symbol'][-4:] == 'USDT' and x['symbol'].find('UP')==-1 and x['symbol'].find('DOWN')==-1:
            SYMBOLS.append(x['symbol'])

def process_message_4HOUR(msg):
    global hour4_first
    global EMA_1H
    global counter
    if msg['k']['x']:
        candleDataClose_4H.append(round(float(msg['k']['c']), 2))
    else:
        candleDataClose_4H[-1] = round(float(msg['k']['c']), 2)

    print(SYMBOL," inverse rsi: ", RSI(candleDataClose_4H))
    print('-------------------------')
    counter+=1
    print(counter)

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

def goldenCrossCalc(close):
    MAfast = talib.MA(numpy.asarray(close), timeperiod=50)
    MAslow = talib.MA(numpy.asarray(close), timeperiod=200)
    goldenCross = []
    deathCross = []
    for x in range(-3,0):
        fastUnder = True
        slowUnder = True
        for y in range(x-8,x):
            if MAfast[y] > MAslow[y]:
                fastUnder = False
                break
            if MAfast[y] < MAslow[y]:
                slowUnder = False
                break
        goldenCross.append(fastUnder and MAfast[x] >= MAslow[x])
        deathCross.append(slowUnder and MAfast[x] <= MAslow[x])

    return goldenCross,deathCross

def macdAndRsiKline():
    dataBuy = []
    for x in SYMBOLS:
        close=[]
        klines = client.get_historical_klines(x, Client.KLINE_INTERVAL_1HOUR, TIME)
        if len(klines) > 26:
            for entry in klines:
                close.append(float(entry[4]))

            rsiBuy, rsiSell, invRsi = RSI(close)
            macdBuy, signalSell, macd, signal = MACDEMA(close)
            print(x," ",macd," ",signal, " ", invRsi)

            if macdBuy and rsiBuy:
                data = {
                    "symbol": x,
                    "openPrice": klines[-1][4],
                    "time": klines[-1][0],
                    "rsi" : invRsi,
                    "macd" : macd,
                    "macdSignal" : signal
                }
                dataBuy.append(data)
                msg = data["symbol"]+ " Alış:" + str(data["openPrice"]).replace(".", ",")
                bot.send_message(-1001408874432, msg)
                print(msg)
    if len(dataBuy)>0:
        return dataBuy

def rsiKline():
    RSIDATA = []
    for x in SYMBOLS:
        close=[]
        klines = client.get_historical_klines(x, Client.KLINE_INTERVAL_1HOUR, TIME)

        if len(close) > 21:
            for entry in klines:
                close.append(float(entry[4]))

            sell,  buy, invRsi = RSI(close)

            print(x," ",sell," ", buy, " ", invRsi)
            if buy:
                data = {
                    "symbol": x,
                    "openPrice": klines[-1][4],
                    "time": klines[-1][0],
                    "rsi": invRsi
                }
                RSIDATA.append(data)
                msg = data["symbol"]+ " Alış:" + str(data["openPrice"]).replace(".", ",")
                #bot.send_message(-1001408874432, msg)
    return RSIDATA



def historicalKline2():
        klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, TIME)
        for entry in klines:
            candleDataClose_1H.append(float(entry[4]))

def goldenCrossKline():
    for x in SYMBOLS:
        close=[]
        klines = client.get_historical_klines(x, Client.KLINE_INTERVAL_1DAY, TIME)
        if len(klines) > 200:
            for entry in klines:
                close.append(float(entry[4]))

            goldenCross,deathcross = goldenCrossCalc(close)

            print(x," ",goldenCross)
            if goldenCross[0] or goldenCross[1] or goldenCross[2]:
                msg1 = "Golden Cross: " + x
                bot.send_message(-1001408874432, msg1)
                print(msg1)
            if deathcross[0] or deathcross[1] or deathcross[2]:
                msg2 = "Death Cross: " + x
                print(msg2)
                bot.send_message(-1001408874432, msg2)
            
                

def process_message_1HOUR(msg):
    global hour4_first
    if msg['k']['x'] :
        candleDataClose_1H.append(float(msg['k']['c']))
    else:
        candleDataClose_1H[-1] = float(msg['k']['c'])
    
    ligneMACD,signal = MACDEMA(candleDataClose_1H)
    print("MACD DEMA: ",ligneMACD,signal)


def websocket():
    bm = BinanceSocketManager(client)
    bm.start()
    bm.start_kline_socket(SYMBOL, process_message_1HOUR, interval=KLINE_INTERVAL_1HOUR)


Scounter=0
if __name__ == '__main__':

    client = Client(config.api_key, config.api_secret)
    bot = telebot.TeleBot("1628197070:AAFLvfUgbwO8qnY4YkQJ8yLHLoube-51GKc", parse_mode="MarkdownV2")
    fillSymbols()
    macdAndRsiKline()
    bot.polling()
    #websocket()
    


    # -1001408874432 GRUP
    # 1487856885 EMRE



  
    #
    #isOpen = False
    #while True:
    #    if not isOpen:
    #        historcialKline()
    #        
    #        isOpen=True
    #        Scounter +=1
    #        if Scounter >= len(SYMBOL): Scounter = 0
    #    else:
    #        if counter == 3:
    #            bm.stop_socket(key)
    #            counter=0
    #            isOpen=False
    #            candleDataClose_4H.clear()
    #            SYMBOL = SYMBOLS[Scounter]
#