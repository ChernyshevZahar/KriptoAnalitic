from django.core.management.base import BaseCommand
from cryptoapp.models import NumberData , settingAll , ProfitPrice
import re


site = {'binance':'https://www.binance.com/ru/trade/0f3?type=spot', # BTC_USDT
        'huobi':'https://www.htx.com/ru-ru/trade/0f3?type=spot', # mbl_usdt
        'gateio':'https://www.gate.io/ru/trade/0f3', #MBL_USDT
        'kucoin': 'https://www.kucoin.com/ru/trade/0f3',} #MBL-USDT


class Command(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **options):
        # while True:
            data = ProfitPrice.objects.all()
            for ss in data: 
                if ss.pair1 != None and ss.pair2 != None:
                    parturllist = {
                            'binance': ss.pair2+'_'+ss.pair1, # BTC_USDT
                            'huobi': (ss.pair2+'_'+ss.pair1).lower(), # mbl_usdt
                            'gateio': ss.pair2+'_'+ss.pair1, #MBL_USDT
                            'kucoin': ss.pair2+'-'+ss.pair1, #MBL-USDT
                    }


                list = {}
                if ss.binance:
                      list['binance'] = ss.binance
                if ss.huobi:
                      list['huobi'] = ss.huobi
                if ss.gateio:
                      list['gateio'] = ss.gateio
                if ss.kucoin:
                      list['kucoin'] = ss.kucoin
                      

                if list:
                    profit = list[max(list, key=list.get)] / list[min(list, key=list.get)]
                    buy = min(list, key=list.get)
                    sell = max(list, key=list.get)

                    if parturllist != None:
                    
                        urlbuy =  site[buy].replace('0f3',parturllist[buy])
                        urlsell =  site[sell].replace('0f3',parturllist[sell])
                    else:
                        urlbuy = site[buy]
                        urlsell = site[sell] 
                    
                    createUpData(ss.pair,profit,buy,sell,list,urlsell,urlbuy)
                   
            
                # time.sleep(10)  # Подождите 10 секунд
                  

def createUpData(name, profit,buy,sell,list,urlsell,urlbuy):

        data = settingAll.objects.get(name='balance')
        howbuy = data.balance/list[buy]
        profit = howbuy*profit
        howsell = round(profit*list[sell]-data.balance,4)
        spred = round(list[sell]/list[buy]*100-100,4)


        try: 
            obj, created = ProfitPrice.objects.get_or_create(pair=name,defaults={
                'profit': profit,
                'buy': buy,
                'sell': sell,
                'round': howsell,
                'spred': spred,
                'sellurl': urlsell,
                'buyurl': urlbuy,

            })

            if not created:
                obj.profit = profit
                obj.buy = buy
                obj.sell = sell
                obj.round = howsell
                obj.spred = spred
                obj.sellurl = urlsell
                obj.buyurl = urlbuy
                obj.save()
        except Exception as e:
             pass


