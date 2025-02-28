from django.core.management.base import BaseCommand
from cryptoapp.models import NumberData , ProfitPrice2
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone



site = {'binance':'https://www.binance.com/ru/trade/0f3?type=spot', # BTC_USDT
        'huobi':'https://www.htx.com/ru-ru/trade/0f3?type=spot', # mbl_usdt
        'gateio':'https://www.gate.io/ru/trade/0f3', #MBL_USDT
        'kucoin': 'https://www.kucoin.com/ru/trade/0f3',} #MBL-USDT

class Command(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **options):
        # while True:
            round1()
            print('end 1')
            round2()
            print('end 2')
            round3()

            # time.sleep(10)  # Подождите 10 секунд

def round1():
    namecript = NumberData.objects.values_list('pair1').distinct()
    sites = NumberData.objects.values_list('Site').distinct()
    for par in namecript:     
            dataprai = NumberData.objects.filter(pair1 = par[0]).values_list('pair2', flat=True)
            set1 = set(dataprai)
            for sit in sites:
                    
                datasite = NumberData.objects.filter(Site = sit[0]).values_list('pair2', flat=True)
                set2 = set(datasite)
                list2 = list(set1.intersection(set2))
                
                for ss in list2:
                    
                    try:
                        data = NumberData.objects.filter(Site = sit[0], pair1 = par[0] , pair2 = ss).first()
                        if data is not None:
                            if data.pair1 != None and data.pair2 != None:
                                    parturllist = {
                                            'binance': data.pair2+'_'+data.pair1, # BTC_USDT
                                            'huobi': (data.pair2+'_'+data.pair1).lower(), # mbl_usdt
                                            'gateio': data.pair2+'_'+data.pair1, #MBL_USDT
                                            'kucoin': data.pair2+'-'+data.pair1, #MBL-USDT
                                    }
                                    if parturllist != None:
                    
                                        paur2url =  site[data.Site].replace('0f3',parturllist[data.Site])
                                    else:
                                        paur2url = site[data.Site]
                                    # print(data.id)
                                    dw_valute = how_dw_valute(data)
                                    sp_valute = how_sp_valute(data)
                                    obj, created = ProfitPrice2.objects.get_or_create(site = sit[0], paurstart = par[0] , paur2 = ss, defaults={
                                            'site': sit[0],
                                            'paurstart': data.pair1,
                                            'balance1': data.priсe,
                                            'paur2': data.pair2,
                                            'paur2url': paur2url,
                                            'buy1': data.askPrice,
                                            'buyask1': data.askSize,
                                            'sell1': data.bid,
                                            'sellask1': data.bidSize,
                                            'datetime_uploder':timezone.now(),
                                            'idpaur2':data.id,
                                            'dvizhenie_valut_2':dw_valute,
                                            'speed_valute_2': sp_valute


                                        })

                                        # Если запись существует, обновляем ее значения
                                    if not created:
                                        obj.site = sit[0]
                                        obj.paurstart = data.pair1
                                        obj.balance1 = data.askPrice
                                        obj.paur2 = data.pair2
                                        obj.paur2url = paur2url
                                        obj.buy1 = data.askPrice
                                        obj.buyask1 = data.askSize
                                        obj.sell1 = data.bid
                                        obj.sellask1 = data.bidSize
                                        obj.datetime_uploder = timezone.now()
                                        obj.idpaur2 = data.id
                                        obj.dvizhenie_valut_2 = dw_valute
                                        obj.speed_valute_2 = sp_valute
                                        obj.save()

                    except NumberData.DoesNotExist:
                        # Обработка случая, когда объект не найден
                        # print(ss.pair2 + " " + ss2.pair2)
                        pass



def round2():
    namecript = ProfitPrice2.objects.values_list('paur2').distinct()
    sites = ProfitPrice2.objects.values_list('site').distinct()
    for ss in sites:
         
         for sss in namecript:
            # print(sss)
            try: 
              data = NumberData.objects.filter(Site = ss[0], pair2=sss[0]).first()
              data2 = ProfitPrice2.objects.filter(site = ss[0], paur2=sss[0]).first()
            #   print(sss)
              if data is not None:
                 
                 if data.pair1 != data2.paurstart:
                    if data.pair1 != None and data.pair2 != None:
                                    parturllist = {
                                            'binance': data.pair2+'_'+data.pair1, # BTC_USDT
                                            'huobi': (data.pair2+'_'+data.pair1).lower(), # mbl_usdt
                                            'gateio': data.pair2+'_'+data.pair1, #MBL_USDT
                                            'kucoin': data.pair2+'-'+data.pair1, #MBL-USDT
                                    }
                                    if parturllist != None:
                    
                                        paur3url =  site[data.Site].replace('0f3',parturllist[data.Site])
                                    else:
                                        paur3url = site[data.Site]
                                    
                                    
                                    dw_valute = how_dw_valute(data)
                                    sp_valute = how_sp_valute(data)
                                    obj, created = ProfitPrice2.objects.get_or_create(site = ss[0], paurstart = data2.paurstart , paur2 = sss[0] , defaults={
                                            
                                            'balance2': data.priсe,
                                            'paur3': data.pair1,
                                            'paur3url': paur3url,
                                            'buy2': data.askPrice,
                                            'buyask2': data.askSize,
                                            'sell2': data.bid,
                                            'sellask2': data.bidSize,
                                            'idpaur3':data.id,
                                            'dvizhenie_valut_3':dw_valute,
                                            'speed_valute_3': sp_valute

                                        })

                                        # Если запись существует, обновляем ее значения
                                    if not created:
                                        
                                        obj.balance2 = data.askPrice
                                        obj.paur3 = data.pair1
                                        obj.paur3url = paur3url
                                        obj.buy2 = data.askPrice
                                        obj.buyask2 = data.askSize
                                        obj.sell2 = data.bid
                                        obj.sellask2 = data.bidSize
                                        obj.idpaur3 = data.id
                                        obj.dvizhenie_valut_3 = dw_valute
                                        obj.speed_valute_3 = sp_valute
                                        obj.save()
            except NumberData.DoesNotExist:
                        # Обработка случая, когда объект не найден
                        
                        pass


def round3(): 
    data = ProfitPrice2.objects.all()
    for ss in data:
        # if ss.paur3 == 'TRY':
            # print(ss.paur3)
        try: 
            if ss.paur3 == 'TRY':
                data2 = NumberData.objects.filter(Site = ss.site, pair2 = ss.paurstart, pair1 = ss.paur3).first()
            else:
                data2 = NumberData.objects.filter(Site = ss.site, pair1 = ss.paurstart, pair2 = ss.paur3).first() 
            if data2 is not None:
                # if ss.paur3 == 'TRY':
                    # print(data2.pair)
                if data2.pair1 != None and data2.pair2 != None:
                            # 
                            parturllist = {
                                    'binance': data2.pair2+'_'+data2.pair1, # BTC_USDT
                                    'huobi': (data2.pair2+'_'+data2.pair1).lower(), # mbl_usdt
                                    'gateio': data2.pair2+'_'+data2.pair1, #MBL_USDT
                                    'kucoin': data2.pair2+'-'+data2.pair1, #MBL-USDT
                            }
                            if ss.paur3 == 'TRY':
                                paurstart2 = data2.pair2
                            else:
                                paurstart2 = data2.pair1
                            # else:
                            #     print(data2.pair2 + ' ' + data2.pair1)
                            #     parturllist = {
                            #             'binance': data2.pair1+'_'+data2.pair2, # BTC_USDT
                            #             'huobi': (data2.pair1+'_'+data2.pair2).lower(), # mbl_usdt
                            #             'gateio': data2.pair1+'_'+data2.pair2, #MBL_USDT
                            #             'kucoin': data2.pair1+'-'+data2.pair2, #MBL-USDT
                            #     }
                            #     paurstart2 = data2.pair1 
                            # print(data2.Site)
                            if parturllist != None:
            
                                paurstart2url =  site[data2.Site].replace('0f3',parturllist[data2.Site])
                            else:
                                paurstart2url = site[data2.Site]
        
                            # print(paurstart2url)
                            dw_valute = how_dw_valute(data2)
                            sp_valute = how_sp_valute(data2)
                            obj, created = ProfitPrice2.objects.get_or_create(site = ss.site, paurstart = ss.paurstart , paur3 = ss.paur3 , paur2 = ss.paur2 , defaults={
                                            
                                            'balance3': data2.priсe,
                                            'paurstart2': paurstart2,
                                            'paurstart2url' : paurstart2url,
                                            'buy3': data2.askPrice,
                                            'buyask3': data2.askSize,
                                            'sell3': data2.bid,
                                            'sellask3': data2.bidSize,
                                            'idpaur4':data2.id,
                                            'dvizhenie_valut_4':dw_valute,
                                            'speed_valute_4': sp_valute


                                        })

                                        # Если запись существует, обновляем ее значения
                            if not created:
                                    obj.balance3 = data2.priсe
                                    obj.paurstart2 = paurstart2
                                    obj.paurstart2url = paurstart2url
                                    obj.buy3 = data2.askPrice
                                    obj.buyask3 = data2.askSize
                                    obj.sell3 = data2.bid
                                    obj.sellask3 = data2.bidSize
                                    obj.idpaur4 = data2.id
                                    obj.dvizhenie_valut_4 = dw_valute
                                    obj.speed_valute_4 = sp_valute
                                    obj.save()
        except NumberData.DoesNotExist:
                    # Обработка случая, когда объект не найден
                    
                    pass
    # print(i)
     


def how_dw_valute(data):
    chec = 0
     
    if type(data.priсe_1d) == float and type(data.priсe) == float:
        r = 100 - (data.priсe_1d / data.priсe) * 100
        if r* 100 > 0:
            if r * 100 > 10:
                 chec = chec + 2
            else:
                 chec = chec + 1
            # print(round(r*100,2))
        elif r*100 < 0:
            if r * 100 < -10:
                 chec = chec - 2
            else:
                 chec = chec - 1
            # print(round(r*100,2))

    if type(data.priсe_6h) == float and type(data.priсe) == float:
        c = 100 - (data.priсe_6h / data.priсe) * 100
        if c* 100 > 0:
            if c * 100 > 10:
                 chec = chec + 2
            else:
                 chec = chec + 1
        elif c*100 < 0:
            if c * 100 > -10:
                 chec = chec - 2
            else:
                 chec = chec - 1
    return(chec)

def how_sp_valute(data):
    pr1 = 15
    pr2 = 5
    pr3 = 1
    prc1 = 20
    prc2 = 2
    chec = 0
    list = []
     
    if type(data.priсe_1d) == float and type(data.priсe) == float:
        proc_priсe_1d = 100 - (data.priсe_1d / data.priсe) * 100
        list.append(proc_priсe_1d)   

    if type(data.priсe_6h) == float and type(data.priсe) == float:
        proc_priсe_6h = 100 - (data.priсe_6h / data.priсe) * 100
        list.append(proc_priсe_6h)
    
    if type(data.priсe_3h) == float and type(data.priсe) == float:
        proc_priсe_3h = 100 - (data.priсe_3h / data.priсe) * 100
        list.append(proc_priсe_3h)
    
    if type(data.priсe_1h) == float and type(data.priсe) == float:
        proc_priсe_1h = 100 - (data.priсe_1h / data.priсe) * 100
        list.append(proc_priсe_1h)

    if type(data.priсe_30m) == float and type(data.priсe) == float:
        proc_priсe_30m = 100 - (data.priсe_30m / data.priсe) * 100
        list.append(proc_priсe_30m)

    if type(data.priсe_15m) == float and type(data.priсe) == float:
        proc_priсe_15m = 100 - (data.priсe_15m / data.priсe) * 100 
        list.append(proc_priсe_15m)
    
    if type(data.priсe_5m) == float and type(data.priсe) == float:
        proc_priсe_5m = 100 - (data.priсe_5m / data.priсe) * 100 
        list.append(proc_priсe_5m)

    for index, item in enumerate(list):
        if index < len(list) - 1:
            re = (list[index] - list[index+1]*100)
            if re > 0:
                if re > prc1:
                     chec = chec + pr1 
                elif re > prc2 and re < prc1:
                     chec = chec + pr2
                elif re > 0 and re < prc2:
                     chec = chec + pr3
                # if chec != 0:
                #     print(chec)           
            elif re < 0:
                if re < -prc1:
                     chec = chec - pr1 
                elif re < -prc2 and re > -prc1:
                     chec = chec - pr2
                elif re > 0 and re < -prc2:
                     chec = chec - pr3
                # if chec != 0:
                #     print(chec)  

         

    # print(chec)
    return(chec)