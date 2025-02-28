from datetime import  timedelta
from django.utils import timezone
import requests
from django.core.management.base import BaseCommand
from cryptoapp.models import NumberData  
import concurrent.futures
import re
import time

namecript = ['ETH','TRY','BTC','USDT','USDC','SGD','CNYX','SNET','FDUSD','BNB','TUSD','BRL','TRY','BIDR','DAI','EUR','NGN','RUB','UAH','PLN','RON','ARS','AEUR']


class Command(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **options):
        while True:
            try:
                # Здесь вызывайте вашу функцию или выполняйте нужные действия
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Запускаем функции в отдельных потоках
                    # huobi = executor.submit(gifhuobi())
                    # binance = executor.submit(gifbinance())
                    # gateio = executor.submit(gifgateio())
                    kucoin = executor.submit(gifkucoin())
                    # Дожидаемся завершения выполнения обеих функций
                    # concurrent.futures.wait([huobi, binance, gateio])
                time.sleep(10)  # Подождите 10 секунд
            except Exception as e:
                print(e)
                time.sleep(10)

def gifhuobi():
    print('start huobi')
    data = requests.get("https://api.huobi.pro/market/tickers").json()
    objdata = {}
    for ss in data['data']:
        objdata['site'] = 'huobi'
        objdata['pair'] = ss['symbol'].upper()
        objdata['askPrice'] = ss['ask']
        objdata['askSize'] = ss['askSize']
        objdata['priсe'] = ss['close']
        objdata['bidSize'] = ss['bidSize']
        objdata['bid'] = ss['bid']
        createUpData(objdata)
        # NumberData.objects.create(Site=site,pair=pair,askPrice=askPrice,askSize=askSize,priсe=priсe,bidSize=bidSize,bid=bid)
        # Пытаемся найти запись с соответствующими значениями Site и pair
    print('Stop huobi')

def gifbinance():
    print('start binance')
    data = requests.get("https://api.binance.com/api/v3/ticker/24hr").json()
    objdata = {}
    for ss in data:
        objdata['site'] = 'binance'
        objdata['pair'] = ss['symbol']
        objdata['askPrice'] = ss['askPrice']
        objdata['askSize'] = ss['askQty']
        objdata['priсe'] = ss['lastPrice']
        objdata['bidSize'] = ss['bidQty']
        objdata['bid'] = ss['bidPrice']

        createUpData(objdata)
    print('Stop binance')

def gifgateio():
    print('start gateio')
    data = requests.get("https://api.gateio.ws/api/v4/spot/tickers/").json()
    objdata = {}
    for ss in data:
        if not ss['lowest_ask']:
            lowest_ask = 0
        else:
            lowest_ask = ss['lowest_ask']
        
        if not ss['highest_bid']:
            highest_bid = 0
        else:
            highest_bid = ss['highest_bid']
        objdata['site'] = 'gateio'
        objdata['pair'] = ss['currency_pair'].replace('_', '')
        objdata['askPrice'] = lowest_ask
        objdata['askSize'] = 0
        objdata['priсe'] = ss['last']
        objdata['bidSize'] = 0
        objdata['bid'] = highest_bid

        createUpData(objdata)
    print('Stop gateio')


def gifkucoin():
    print('start kucoin')
    data = requests.get("https://api.kucoin.com/api/v1/market/allTickers").json()
    objdata = {}
    for ss in data['data']['ticker']:
        objdata['site'] = 'kucoin'
        objdata['pair'] = ss['symbolName'].replace('-', '')
        objdata['askPrice'] = ss['sell']
        objdata['askSize'] = ss['bestBidSize']
        objdata['priсe'] = ss['last']
        objdata['bidSize'] = ss['bestAskSize']
        objdata['bid'] = ss['buy']

        createUpData(objdata)
    print('Stop kucoin')
        
def createUpData(objdata):  
        pair1 = ''
        pair2 = ''
        if re.findall(r'\b\w+USD\b', objdata['pair']):
            pair1 = 'USD'
            pair2 = objdata['pair'].replace(pair1,'')
        else:
            for NAME in namecript:
                # print(NAME)
                if re.search(NAME, objdata['pair']):
                    pair1 = NAME
                    pair2 = objdata['pair'].replace(NAME,'')
                    # print(pair1)

        obj, created = NumberData.objects.get_or_create(Site=objdata['site'], pair=objdata['pair'], defaults={
            'pair1': pair1,
            'pair2': pair2,
            'askPrice': objdata['askPrice'],
            'askSize': objdata['askSize'],
            'priсe': objdata['priсe'],
            'bidSize': objdata['bidSize'],
            'bid': objdata['bid'],
            'priсe_1m': objdata['priсe'],
            'datetime_1m': timezone.now(),
            'priсe_5m': objdata['priсe'],
            'datetime_5m': timezone.now(),
            'priсe_15m': objdata['priсe'],
            'datetime_15m': timezone.now(),
            'priсe_30m': objdata['priсe'],
            'datetime_30m': timezone.now(),


        })

        # Если запись существует, обновляем ее значения
        if not created:
            obj.pair1 = pair1
            obj.pair2 = pair2
            obj.askPrice = objdata['askPrice']
            obj.askSize = objdata['askSize']
            obj.priсe = objdata['priсe']
            obj.bidSize = objdata['bidSize']
            obj.bid = objdata['bid']
            time1m(obj)
            time5m(obj)
            time15m(obj)
            time30m(obj)
            time1h(obj)
            time3h(obj)
            time6h(obj)
            time12h(obj)
            time1d(obj)
            obj.save()

   
    # Проверить разницу времени



def time1m(obj):
    current_time = timezone.now()
    if obj.datetime_1m is not None:
        time_difference = current_time - obj.datetime_1m
        if time_difference > timedelta(minutes=1):
            obj.priсe_1m = obj.priсe
            obj.datetime_1m = current_time
            
    else:
        obj.priсe_1m = obj.priсe
        obj.datetime_1m = current_time


def time5m(obj):
    current_time = timezone.now()
    if obj.datetime_5m is not None:
        time_difference = current_time - obj.datetime_5m
        if time_difference > timedelta(minutes=5):
            obj.priсe_5m = obj.priсe
            obj.datetime_5m = current_time
            
    else:
        obj.priсe_5m = obj.priсe
        obj.datetime_5m = current_time      

def time15m(obj):
    current_time = timezone.now()
    if obj.datetime_15m is not None:
        time_difference = current_time - obj.datetime_15m
        if time_difference > timedelta(minutes=15):
            obj.priсe_15m = obj.priсe
            obj.datetime_15m = current_time
            
    else:
        obj.priсe_15m = obj.priсe
        obj.datetime_15m = current_time


def time30m(obj):
    current_time = timezone.now()
    if obj.datetime_30m is not None:
        time_difference = current_time - obj.datetime_30m
        if time_difference > timedelta(minutes=30):
            obj.priсe_30m = obj.priсe
            obj.datetime_30m = current_time
            
    else:
        obj.priсe_30m = obj.priсe
        obj.datetime_30m = current_time

def time1h(obj):
    current_time = timezone.now()
    if obj.datetime_1h is not None:
        time_difference = current_time - obj.datetime_1h
        if time_difference > timedelta(minutes=60):
            obj.priсe_1h = obj.priсe
            obj.datetime_1h = current_time
            
    else:
        obj.priсe_1h = obj.priсe
        obj.datetime_1h = current_time

def time3h(obj):
    current_time = timezone.now()
    if obj.datetime_3h is not None:
        time_difference = current_time - obj.datetime_3h
        if time_difference > timedelta(minutes=180):
            obj.priсe_3h = obj.priсe
            obj.datetime_3h = current_time
            
    else:
        obj.priсe_3h = obj.priсe
        obj.datetime_3h = current_time

def time6h(obj):
    current_time = timezone.now()
    if obj.datetime_6h is not None:
        time_difference = current_time - obj.datetime_6h
        if time_difference > timedelta(minutes=360):
            obj.priсe_6h = obj.priсe
            obj.datetime_6h = current_time
            
    else:
        obj.priсe_6h = obj.priсe
        obj.datetime_6h = current_time

def time12h(obj):
    current_time = timezone.now()
    if obj.datetime_12h is not None:
        time_difference = current_time - obj.datetime_12h
        if time_difference > timedelta(minutes=720):
            obj.priсe_12h = obj.priсe
            obj.datetime_12h = current_time
            
    else:
        obj.priсe_12h = obj.priсe
        obj.datetime_12h = current_time

def time1d(obj):
    current_time = timezone.now()
    if obj.datetime_1d is not None:
        time_difference = current_time - obj.datetime_1d
        if time_difference > timedelta(minutes=1440):
            obj.priсe_1d = obj.priсe
            obj.datetime_1d = current_time
            
    else:
        obj.priсe_1d = obj.priсe
        obj.datetime_1d = current_time