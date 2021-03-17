import numpy
import config
from binance.client import Client

client = Client(config.api_key, config.api_secret)
#
#def historicalKline2():
#    candleDataClose_1H = []
#    klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "1 week ago UTC+3")
#    for entry in klines:
#        candleDataClose_1H.append(round(float(entry[4]),4))
#        x = numpy.asarray(candleDataClose_1H)
#        numpy.savetxt('BTCUSDT.csv',x,delimiter=",")
#
lens = client.get_historical_klines('BTCUSDT',Client.KLINE_INTERVAL_1DAY,'7 month ago UTC+3')
print(len(lens))
def goldenCrossfinder():
    SMAfast = numpy.random.random(50)
    SMAslow = numpy.random.random(200)

    for x in range(-3,0):
        print("---------")
        print(x)
        print("---------")
        for y in range(x-10,x):
            if 3 <= 1:    
                print("break")
                break
            else:
                print(y)

goldenCrossfinder()
#historicalKline2()