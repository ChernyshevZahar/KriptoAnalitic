from django.core.management.base import BaseCommand
from cryptoapp.models import ProfitPrice2, settingAll
from django.utils import timezone

class Command(BaseCommand):
    help = 'My custom command'


    def handle(self, *args, **options):
        pairlist = {}
        data = ProfitPrice2.objects.all()
        balance = settingAll.objects.get(name = 'balance')
        # print(balance.balance)

        for ss in data:

            if ss.balance1 != None  and ss.balance2 != None and ss.balance3 != None:
                try:
                    if ss.paurstart not in pairlist:
                         
                        pair = settingAll.objects.get(name = ss.paurstart)
                    
                    
                    

                    if ss.paur3 == 'TRY':  

                        pairstart = balance.balance / pair.balance

                        result_tyda_pair1 = pairstart/ss.buy1
                        result_tyda_pair2 = ss.sell2 * result_tyda_pair1
                        result_tyda_pair3 = ss.sell3 * result_tyda_pair2
                        result_tyda_pair4 = result_tyda_pair3 - pairstart

                        print(ss.paur2)

                        result_back_pair1 = pairstart/ss.buy3
                        print(result_back_pair1)
                        result_back_pair2 = ss.buy2 * result_back_pair1
                        print(result_back_pair2)
                        result_back_pair3 = ss.buy1 / result_back_pair2
                        print(result_back_pair3)
                        result_back_pair4 = result_back_pair3 - pairstart
                        print(result_back_pair4)
                                            


                        rastdohodcent = pairstart / ss.balance1 * ss.balance2 / ss.balance3
                        dohod3 = (rastdohodcent - pairstart)
                        # print(dohod2)
                        dohodend1 = result_tyda_pair4 * pair.balance
                        dohodend2 = result_back_pair4 * pair.balance
                        dohodend3 = dohod3 * pair.balance
                    

                    else:
                        pairstart = balance.balance / pair.balance

                        result_tyda_pair1 = pairstart/ss.buy1
                        result_tyda_pair2 = ss.sell2 * result_tyda_pair1
                        result_tyda_pair3 = ss.sell3 * result_tyda_pair2
                        result_tyda_pair4 = result_tyda_pair3 - pairstart

                       

                        result_back_pair1 = pairstart/ss.buy3
                        
                        result_back_pair2 = ss.buy2 / result_back_pair1
                        
                        result_back_pair3 = ss.sell1 / result_back_pair2
                        
                        result_back_pair4 = result_back_pair3 - pairstart
                        

                        if ss.paur2 == "SOUL":
                            print(result_back_pair1)
                            print(result_back_pair2)              
                            print(result_back_pair3)
                            print(result_back_pair4)

                        rastdohodcent = pairstart / ss.balance1 * ss.balance2 / ss.balance3
                        dohod3 = (rastdohodcent - pairstart)
                        # print(dohod2)
                        dohodend1 = result_tyda_pair4 * pair.balance
                        dohodend2 = result_back_pair4 * pair.balance
                        dohodend3 = dohod3 * pair.balance

                    

                    
                    # if type(dohod2) == float:

                        obj, created = ProfitPrice2.objects.get_or_create(site = ss.site, paurstart = ss.paurstart , paur2 = ss.paur2, paur3 = ss.paur3, defaults={
                                        'dohod': round(dohodend3,2),
                                        'dohodtyda' : round(dohodend1,2),
                                        'dohodsyda' : round(dohodend2,2),
                                        'datadohod' : timezone.now(),

                                    })

                                    # Если запись существует, обновляем ее значения
                        if not created:
                            obj.dohod = round(dohodend3,2)
                            obj.dohodtyda = round(dohodend1,2)
                            obj.dohodsyda = round(dohodend2,2)
                            obj.datadohod = timezone.now()
                            obj.save()
                except Exception as e:
                    print(e)

    
                   

                